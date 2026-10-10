"""Batch independent calls to the existing frozen-model decoder."""
from __future__ import annotations

from concurrent.futures import Future
from dataclasses import dataclass
import inspect
from queue import Empty, Queue
from threading import Thread
import time

import torch

from reasoning_diff.models.adapters import model_device
from reasoning_diff.models.generate import sample_next


@dataclass
class DecodeRequest:
    model: object
    prompt_ids: object
    generator: object
    max_new: int
    eos_id: int | None = None
    temperature: float = 1.0
    top_k: int = 0
    top_p: float = 1.0
    stop_condition: object = None


def decode_batch(requests: list[DecodeRequest]) -> list[dict]:
    model = requests[0].model
    if any(request.model is not model for request in requests):
        raise ValueError("decode batch must share one model")
    device = model_device(model)
    prompts = [request.prompt_ids.reshape(-1).tolist() if hasattr(request.prompt_ids, "reshape")
               else list(request.prompt_ids) for request in requests]
    width = max(map(len, prompts))
    pad = getattr(model.config, "pad_token_id", None)
    pad = 0 if pad is None else pad
    tokens = torch.tensor([[pad] * (width - len(prompt)) + prompt for prompt in prompts], device=device)
    attention = torch.tensor([[0] * (width - len(prompt)) + [1] * len(prompt) for prompt in prompts], device=device)
    position_ids = (attention.cumsum(-1) - 1).clamp_min(0)
    generated = [[] for _ in requests]
    reasons = ["max_new" for _ in requests]
    active = [request.max_new > 0 for request in requests]
    past = None
    # HF Qwen supports retaining only the final logits during prefill.
    logits_options = {"logits_to_keep": 1} if "logits_to_keep" in inspect.signature(model.forward).parameters else {}
    started = time.perf_counter()
    with torch.inference_mode():
        for _ in range(max(request.max_new for request in requests)):
            out = model(input_ids=tokens, attention_mask=attention, position_ids=position_ids,
                        past_key_values=past, use_cache=True, **logits_options)
            past = out.past_key_values
            next_tokens = []
            for index, request in enumerate(requests):
                if not active[index]:
                    next_tokens.append(torch.tensor([[pad]], device=device))
                    continue
                nxt = sample_next(out.logits[index:index + 1, -1, :], request.generator,
                                  temperature=request.temperature, top_k=request.top_k, top_p=request.top_p)
                token = int(nxt.item())
                generated[index].append(token)
                next_tokens.append(nxt)
                if request.eos_id is not None and token == request.eos_id:
                    reasons[index], active[index] = "eos", False
                elif request.stop_condition is not None and request.stop_condition(generated[index]):
                    reasons[index], active[index] = "stop_condition", False
                elif len(generated[index]) >= request.max_new:
                    active[index] = False
            if not any(active):
                break
            tokens = torch.cat(next_tokens, dim=0)
            attention = torch.cat([attention, torch.tensor(active, device=device, dtype=attention.dtype).unsqueeze(1)], dim=1)
            position_ids = (attention.sum(-1) - 1).clamp_min(0).unsqueeze(1)
    torch.cuda.synchronize(device) if device.type == "cuda" else None
    execution = {
        "backend": "shared_model_batched_decode", "batch_size": len(requests),
        "batch_prompt_lengths": list(map(len, prompts)), "batch_seeds": [request.generator.initial_seed() for request in requests],
        "batch_elapsed_seconds": time.perf_counter() - started,
    }
    return [{
        "prompt_ids": prompt, "generated_ids": produced, "token_ids": prompt + produced,
        "stop_reason": reason,
        "sampling": {"temperature": request.temperature, "top_k": request.top_k, "top_p": request.top_p},
        "device": str(device), "device_transfer_seconds": 0.0,
        "batch_execution": {**execution, "batch_index": index},
    } for index, (prompt, produced, reason, request) in enumerate(zip(prompts, generated, reasons, requests, strict=True))]


class BatchDecoder:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.queue = Queue()
        self.thread = Thread(target=self._serve, daemon=True)
        self.thread.start()

    def __call__(self, *args, **kwargs):
        request = DecodeRequest(*args, **kwargs)
        future = Future()
        self.queue.put((request, future))
        return future.result()

    def _serve(self):
        while True:
            first = self.queue.get()
            if first is None:
                return
            pending = [first]
            deadline = time.monotonic() + 0.05
            while len(pending) < self.batch_size:
                try:
                    pending.append(self.queue.get(timeout=max(0, deadline - time.monotonic())))
                except Empty:
                    break
            try:
                decoded = decode_batch([request for request, _future in pending])
            except BaseException as exc:
                for _request, future in pending:
                    future.set_exception(exc)
            else:
                for result, (_request, future) in zip(decoded, pending, strict=True):
                    future.set_result(result)

    def close(self):
        self.queue.put(None)
        self.thread.join()
