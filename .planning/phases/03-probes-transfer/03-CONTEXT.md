# Phase 3: 探针、公平基线与跨模型迁移 - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
双头低秩探针、边界 MLP、保形校准、文本/注意力/verbalizer、直接/配对/监督迁移。
</domain>
<decisions>
## Implementation Decisions
### D-07
- score = σ(h^T U V^T e + b), λ_FN=10, unknown masked.
- conformal k=ceil((N+1)(1-α)); k>N → +∞.
- verbalizer reflection is retrospective.
- Mapping fit only on transfer_pairs.
</decisions>
<code_context>
src/reasoning_diff/probes, baselines.py, transfer.py
</code_context>
<specifics>
None
</specifics>
<deferred>
Real-model F1 / expected numbers.
</deferred>
