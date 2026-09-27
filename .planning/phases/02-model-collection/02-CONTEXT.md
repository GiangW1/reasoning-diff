# Phase 2: 冻结模型采集与边界接口 - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary
冻结 HF 采集、三时机特征、独立随机流、hook/缓存与成本。本机用微型随机模型验证。
</domain>
<decisions>
## Implementation Decisions
### D-06
- resid_post hook on decoder layer output; try/finally cleanup.
- Explicit multinomial loop with torch.Generator; do not use generate(generator=).
- Direct transfer 4096→3584 is N/A.
- CPU tiny Qwen2/Qwen3 tests only; real revisions pending_server.
</decisions>
<code_context>
Implemented in src/reasoning_diff/models/.
</code_context>
<specifics>
Qwen3 thinking template vs R1 pre-inserted think tag.
</specifics>
<deferred>
Real weights, CUDA, long-context.
</deferred>
