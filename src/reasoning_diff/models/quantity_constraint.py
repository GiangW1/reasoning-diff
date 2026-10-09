"""Single-stream structural decoding; no answers or dependency values supplied."""
from collections import deque
from functools import lru_cache
import re

import torch

PROTOCOL = 'registered_quantity_constrained_v1'


@lru_cache(maxsize=4)
def vocabulary(tokenizer):
    pieces = {i: tokenizer.decode([i], skip_special_tokens=False) for i in range(len(tokenizer))}
    blocked = {i for i, text in pieces.items() if '<' in text} | set(tokenizer.all_special_ids)
    digits = {i: text for i, text in pieces.items() if re.fullmatch(r'[0-9]+', text)}
    minus = {i for i, text in pieces.items() if text == '-'}
    return blocked, digits, minus


class QuantityConstraint:
    """Emit registered tags, sample prose and integers, never retry a trace.

    Reasoning is bounded per node. At that bound the decoder requests a
    model-sampled integer commitment, and records that the bound was reached.
    The outer generation budget can still truncate any structural phase.
    """
    def __init__(self, tokenizer, node_ids, reasoning_limit=512):
        if not node_ids or len(set(node_ids)) != len(node_ids) or reasoning_limit < 1:
            raise ValueError('invalid registered quantity schedule')
        self.tokenizer, self.nodes, self.limit = tokenizer, list(node_ids), reasoning_limit
        self.blocked, self.digits, self.minus = vocabulary(tokenizer)
        self.commit = tokenizer.encode('<commit>', add_special_tokens=False)
        self.close = tokenizer.encode('</commit></step>\n', add_special_tokens=False)
        self.final_close = tokenizer.encode('}', add_special_tokens=False)
        self.index, self.reasoning_tokens, self.number = 0, 0, ''
        self.position, self.forced, self.numeric, self.capped = 0, [], 0, 0
        self.queue, self.phase, self.after = deque(), '', ''
        self._force('<think>\n' + self._header(), 'reasoning')

    def _header(self):
        return f'<step node="{self.nodes[self.index]}">'

    def _force(self, text, after):
        self.queue = deque(self.tokenizer.encode(text, add_special_tokens=False))
        self.phase, self.after = 'forced', after

    def _prepare(self):
        if self.phase == 'reasoning' and self.reasoning_tokens >= self.limit:
            self.capped += 1
            self._force('<commit>', 'integer')
        elif self.phase in {'integer', 'answer'} and len(self.number.lstrip('-')) >= 12:
            self._close_number()

    def _close_number(self, first_consumed=False):
        if self.phase == 'answer':
            self._force('}', 'eos')
        else:
            self._force('</commit></step>\n', 'next_node')
        if first_consumed:
            self.queue.popleft()
            self._advance_forced()

    def _advance_forced(self):
        if self.queue:
            return
        self.phase = self.after
        if self.phase == 'next_node':
            self.index += 1
            if self.index < len(self.nodes):
                self.reasoning_tokens = 0
                self._force(self._header(), 'reasoning')
            else:
                self._force('</think>\n\\boxed{', 'answer')
        elif self.phase in {'integer', 'answer'}:
            self.number = ''
        elif self.phase == 'eos':
            self.queue = deque([self.tokenizer.eos_token_id])
            self.phase, self.after = 'forced', 'complete'

    def _numeric_allowed(self):
        allowed = [i for i, s in self.digits.items() if len(self.number.lstrip('-')) + len(s) <= 12]
        if not self.number:
            allowed.extend(self.minus)
        elif self.number != '-':
            allowed.append((self.final_close if self.phase == 'answer' else self.close)[0])
        return allowed

    def mask(self, logits):
        self._prepare()
        out = torch.full_like(logits, -float('inf'))
        if self.phase == 'forced':
            out[..., self.queue[0]] = 0
        elif self.phase == 'reasoning':
            out[..., :len(self.tokenizer)] = logits[..., :len(self.tokenizer)]
            out[..., list(self.blocked)] = -float('inf')
            out[..., self.commit[0]] = logits[..., self.commit[0]]
        elif self.phase in {'integer', 'answer'}:
            allowed = self._numeric_allowed()
            out[..., allowed] = logits[..., allowed]
        else:
            raise ValueError('cannot decode past complete quantity sequence')
        return out

    def accept(self, token):
        self._prepare()
        if self.phase == 'forced':
            if token != self.queue[0]:
                raise ValueError('prefix violates registered structural tokens')
            self.forced.append(self.position)
            self.queue.popleft()
            self._advance_forced()
        elif self.phase == 'reasoning':
            if token == self.commit[0]:
                self.forced.append(self.position)
                self._force('<commit>', 'integer')
                self.queue.popleft()
                self._advance_forced()
            elif token in self.blocked or token >= len(self.tokenizer):
                raise ValueError('prefix violates reasoning region constraint')
            else:
                self.reasoning_tokens += 1
        elif self.phase in {'integer', 'answer'}:
            if token not in self._numeric_allowed():
                raise ValueError('prefix violates integer constraint')
            if token in self.digits:
                self.number += self.digits[token]
                self.numeric += 1
            elif token in self.minus:
                self.number += '-'
                self.numeric += 1
            else:
                self.forced.append(self.position)
                self._close_number(first_consumed=True)
        else:
            raise ValueError('prefix continues after completion')
        self.position += 1

    def report(self):
        return {'protocol': PROTOCOL, 'complete': self.phase == 'complete',
                'structural_token_positions': list(self.forced), 'sampled_numeric_tokens': self.numeric,
                'reasoning_budget_per_node': self.limit, 'integer_max_digits': 12,
                'reasoning_budget_forced_commits': self.capped,
                'generation_retries': 0, 'format_coverage_is_by_construction': True}

    def fork(self):
        import copy
        result = copy.copy(self)
        result.queue, result.forced = self.queue.copy(), self.forced.copy()
        return result


def for_task(task, tokenizer, prefix=()):
    if task.metadata.get('quantity_decoding_protocol') != PROTOCOL:
        return None
    result = QuantityConstraint(tokenizer, [s['node_id'] for s in task.metadata['quantity_step_plan']])
    for token in prefix:
        result.accept(int(token))
    return result
