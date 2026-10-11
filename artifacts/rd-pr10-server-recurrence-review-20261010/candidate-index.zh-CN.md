# 24条重点上下文复核

非穷尽标注，不估计总体复发率。每例附完整相关段落与字符区间。

| 编号 | run/role/seed | 条件 | 判定 |
|---|---|---|---|
| [P05](evidence/P05.md) | pr9-pilot-20261009/reference/0 | related_noop | 目标的前向算式一直能得到2，但标签17仍被称作目标given；未确认来源纠正或纠正后实际误用。 |
| [P22](evidence/P22.md) | pr9-pilot-20261009/reference/0 | related_noop | 初期以错绑T_H=17实际逆推R_T=12；随后前向得到19和1，后期12位于被拒绝的If分支。 |
| [V24](evidence/V24.md) | pr9-validation-natural-20261010/reference/0 | related_noop | 数值4出现后，条件表仍重述目标17；该重述先于明确来源分离，且未用于实际错误计算。 |
| [V17](evidence/V17.md) | pr9-validation-natural-20261010/reference/0 | base | 真实算术错误19传播到8个后续非目标量；自行改成13并重算，未确认同一错误再次被采用。 |
| [P47](evidence/P47.md) | pr9-pilot-20261009/noise/3 | related_noop | 前向18后又逆推KH22，但一直未稳定纠正标签来源；约束检验的执行性质不确定，不确认为数值纠正后实际复发。 |
| [P48](evidence/P48.md) | pr9-pilot-20261009/noise/3 | related_noop | 起初持续错绑17，前向总和2；后段明确两种数量不同，此后未确认实际误用。 |
| [P69](evidence/P69.md) | pr9-pilot-20261009/reference/0 | related_noop | 来源分离后逆推TigerAlula13发生在明确假设分支，并以正确0矛盾拒绝；不是实际复发。 |
| [V58](evidence/V58.md) | pr9-validation-natural-20261010/noise/3 | related_noop | 多次错称WJ17；实际得到0后仍认为冲突。没有稳定来源纠正，后期逆元约束是另一解释的假设。 |
| [V50](evidence/V50.md) | pr9-validation-natural-20261010/noise/3 | related_noop | 先错绑17，后明确承认误把标签当目标；后续保持S_labels17与S_Haddock4分离。 |
| [P32](evidence/P32.md) | pr9-pilot-20261009/noise/3 | related_noop | 瞬时错命名后立即给标签独立变量；前向0，后来的17为被区分的另一解释。 |
| [P66](evidence/P66.md) | pr9-pilot-20261009/reference/0 | related_noop | KH22在If条件分支，发生于稳定来源分离前；正常前向18，后段明确标签无关。 |
| [V69](evidence/V69.md) | pr9-validation-natural-20261010/reference/0 | related_noop | 短暂误述17后区分标签与Crab，登记独立变量；后续7与分离均保持。 |
| [P24](evidence/P24.md) | pr9-pilot-20261009/reference/0 | related_noop | 标签另名后实际目标21；后续If/Suppose分支用21不等17排除，未确认实际复发。 |
| [V13](evidence/V13.md) | pr9-validation-natural-20261010/reference/0 | related_noop | 初列SBS17而前向得到11；后段17约束由If引出并用11矛盾拒绝，不确认为实际复发。 |
| [E24](evidence/E24.md) | pr8-natural-pilot-20261007-d02a40c/unedited_original/2 | base | 实际Sr20-Ba13=7；反向16由If明确引出且立即以原题减法顺序拒绝。 |
| [V70](evidence/V70.md) | pr9-validation-natural-20261010/reference/0 | related_noop | 与V58同题另seed，早期给标签另名，前向0；没有纠正后实际误用。 |
| [V59](evidence/V59.md) | pr9-validation-natural-20261010/noise/3 | related_noop | 初期ADC17含混；明确标签另量后计算目标10，后续保持分离。 |
| [V43](evidence/V43.md) | pr9-validation-natural-20261010/noise/3 | related_noop | 从早段已给标签另名，正常前向目标11；没有确认初始错绑或实际复发。 |
| [P26](evidence/P26.md) | pr9-pilot-20261009/noise/3 | related_noop | 与P22同图另seed，初期误述后区分标签，实际前向1并维持；没有R_T12工作值。 |
| [P27](evidence/P27.md) | pr9-pilot-20261009/noise/3 | related_noop | 明确标签另量后又问第一句是否目标17，但没有实际以17替代正确11计算。 |
| [P31](evidence/P31.md) | pr9-pilot-20261009/noise/3 | related_noop | P057/P059分离来源后P060确有错误重述再现，随后多次含混；没有17再次进入实际错误计算的证据。 |
| [P40](evidence/P40.md) | pr9-pilot-20261009/noise/3 | related_noop | 自称earlier wrong，但54与31模23均为8，实际数值没有改变。 |
| [P71](evidence/P71.md) | pr9-pilot-20261009/reference/0 | neutral_noop | 先自称mistake，随后明确54与31模23都8，原步正确。 |
| [E18](evidence/E18.md) | pr8-natural-pilot-20261007-d02a40c/unedited_original/2 | base | 21+38=59与21+15=36模23都13，模型复核后也确认原步正确。 |
