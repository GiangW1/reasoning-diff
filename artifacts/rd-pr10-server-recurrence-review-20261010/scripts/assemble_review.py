"""Package contextual assistant review of existing texts; never calls a model."""
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re

OUT = Path('/mnt/mydata/wja/reasoning-diff/reports/pr10-server-recurrence-review-20261010')
REPO = Path('/home/wja/reasoning-diff-pr10')
AUDIT = REPO / 'experiments/natural-recurrence-audit-20261010'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def phase(nums, kind, note):
    return {'paragraph_numbers':nums, 'speech_act':kind, 'note':note}


def case(code, category, judgment, uncertainty, **phases):
    return {'code':code, 'category':category, 'judgment':judgment,
            'uncertainty':uncertainty, 'phases':phases}


CASES = [
    case('P05', 'persistent_wrong_source_interpretation',
         '目标的前向算式一直能得到2，但标签17仍被称作目标given；未确认来源纠正或纠正后实际误用。',
         '首次实际以标签17改变下游计算没有充分证据。第一乘积合法等于17，不能仅按数字认定污染。',
         initial_wrong_restatement=phase([4,9,12], 'assertion', '标签被命名为MZ_P=17。'),
         correct_forward_value=phase([5,6,7,8], 'actual_computation', '7×9的17有独立合法来源；三个乘积之和为2。'),
         later_reappearance=phase([166,178,204,205], 'persistent_assertion_and_correct_answer', '结尾仍写17 given，框内选2；没有明确来源分离。')),
    case('P22', 'initial_wrong_use_then_rejected_hypothesis',
         '初期以错绑T_H=17实际逆推R_T=12；随后前向得到19和1，后期12位于被拒绝的If分支。',
         'P022已提出另一数量，但含maybe/perhaps及反复疑问，来源纠正的稳定程度有限。',
         initial_wrong_restatement=phase([4], 'assertion', '纪念标签17被绑定为T_H。'),
         first_actual_error_adoption=phase([9,17], 'asserted_inverse_computation', '17=5+R_T，断言R_T must be12；原图R_T=19。'),
         source_interpretation_correction=phase([22], 'explicit_separation_with_hedging', '指出标签与T_H不是同一数量；保留语气的不确定性。'),
         numeric_correction=phase([43,44], 'actual_computation', 'R_T=19，T_H=1。'),
         later_reappearance=phase([74,75], 'hypothesis_explicitly_rejected', '先声明另一个解释，再If假定T_H17并以R_T19矛盾拒绝。')),
    case('V24', 'wrong_restatement_before_source_correction',
         '数值4出现后，条件表仍重述目标17；该重述先于明确来源分离，且未用于实际错误计算。',
         'P020属于解释候选；P023同时保留目标17和前向结果4，不能将表中重述直接升级为采用。',
         initial_wrong_restatement=phase([4], 'assertion', '将标签17写成目标Haddock17。'),
         correct_forward_value=phase([11,12,13], 'actual_computation', '前向链得到目标4。'),
         later_reappearance=phase([20,23], 'interpretation_hypothesis_and_inconsistent_table', '来源解释仍含混；同一表实际前向链仍得到4。'),
         source_interpretation_correction=phase([32], 'explicit_separation', '明确标签17并非目标数量。'),
         subsequent_correct_use=phase([37,40], 'actual_computation', '明确分离后仍按正确链得到4。')),
    case('V17', 'real_arithmetic_error_propagation_then_recovery',
         '真实算术错误19传播到8个后续非目标量；自行改成13并重算，未确认同一错误再次被采用。',
         '这是加法错误，不是纪念标签绑定。不同实体后来等于19不能算同源复发；最终7由原图抵消。',
         first_actual_error_adoption=phase([13,14,15,16,17,18,19,20,21,22,33], 'actual_erroneous_computation', '(18+12)+6被误算为42，再用A_Frilled19传播。'),
         numeric_correction=phase([71,72,73,74,75], 'explicit_self_correction', '明确30+6=36，A_Frilled=13而非19。'),
         subsequent_correct_use=phase(list(range(78,88))+[100,109,110], 'actual_corrected_computation', '重算八个后续量，终点仍7；实际使用正确13。')),
    case('P47', 'persistent_binding_with_ambiguous_inverse_constraints',
         '前向18后又逆推KH22，但一直未稳定纠正标签来源；约束检验的执行性质不确定，不确认为数值纠正后实际复发。',
         'P030/P037虽用断言语气解约束，却同时强调与KH0矛盾；没有足够证据将KH22视为取代当前前向值的工作状态。',
         initial_wrong_restatement=phase([5,6,7], 'assertion_with_questions', '标签17反复被命名为ZG。'),
         correct_forward_value=phase([16], 'actual_computation', '正常KH0、ZG18，但仍认为冲突。'),
         ambiguous_inverse_constraint=phase([30,31,37], 'inverse_constraint_with_unresolved_conflict', '由错绑ZG17推出KH22；同时保留前向KH0。'),
         later_reappearance=phase([49,50,51,52,53], 'hypothesis_with_inconsistency_check', '明确Suppose KH22并推出矛盾。'),
         final_source_state=phase([152], 'unresolved_source_conflict', '结尾仍认为17可能是不一致或干扰，未明确区分标签数量。')),
    case('P48', 'late_source_correction_without_actual_recurrence',
         '起初持续错绑17，前向总和2；后段明确两种数量不同，此后未确认实际误用。',
         '目标17的表述不是已经观测到的下游传播；乘积17有合法来源。',
         initial_wrong_restatement=phase([6,24,25], 'assertion', '目标被写作17 given。'),
         correct_forward_value=phase([51,52,53,54,55,56], 'actual_computation', '三个合法乘积17、19、12相加得到2。'),
         source_interpretation_correction=phase([142,143,144,145], 'explicit_separation', '明确标签数17与Monument Zone Product不同。'),
         subsequent_correct_use=phase([146,147,149,150,151,152], 'actual_computation_or_correct_commitment', '确认2并开始正确重算，没有将标签17用作计算目标。')),
    case('P69', 'post_source_correction_rejected_inverse_hypothesis',
         '来源分离后逆推TigerAlula13发生在明确假设分支，并以正确0矛盾拒绝；不是实际复发。',
         '语义分离早期仍反复犹豫，但P062/P133已明确区别；P145计算量很长也不改变其假设地位。',
         initial_wrong_restatement=phase([8], 'assertion', '标签17被称为TigerUlna。'),
         tentative_source_separation=phase([25], 'separate_variable_assignment', '给标签独立名称。'),
         correct_forward_value=phase([48,49,50,51,52], 'actual_computation', 'MonkeyUlna17来自22×6；TigerAlula0、TigerUlna0。'),
         source_interpretation_correction=phase([62,133], 'explicit_separation', '指出另一个数量且无关，可以忽略。'),
         later_reappearance=phase(list(range(94,116))+[145], 'hypothesis_explicitly_rejected', 'Alternatively引出17，逆元算13后以正常0矛盾排除；另一分支同样被拒绝。'),
         subsequent_correct_use=phase(list(range(159,185)), 'correct_commitment_and_explanation', '最终解释保持正确前向0。')),
    case('V58', 'persistent_source_conflict_with_inverse_hypotheses',
         '多次错称WJ17；实际得到0后仍认为冲突。没有稳定来源纠正，后期逆元约束是另一解释的假设。',
         '由差值13推得WL12只是离线诊断候选；原文未把WalrusLiver12确认为工作值，不能伪造传播。',
         initial_wrong_restatement=phase([6,7,15,21], 'assertion_with_questions', '标签反复被绑定WJ17。'),
         correct_forward_value=phase([45], 'actual_computation', 'WL22-BWG22得到WJ0，仍认为冲突。'),
         ambiguous_inverse_constraint=phase([63], 'asserted_constraint_with_unresolved_conflict', '仍认为两个WJ表达式相同，但未实际设置错误WL工作值。'),
         later_reappearance=phase(list(range(127,151))+[159], 'alternative_hypothesis', 'Alternatively及Suppose/assume引出差值13约束。'),
         final_source_state=phase([190,199,200,201], 'persistent_source_conflict', '条件表仍列WJ17，结尾冲突解释未稳定修复。')),
    case('V50', 'explicit_source_recovery_control',
         '先错绑17，后明确承认误把标签当目标；后续保持S_labels17与S_Haddock4分离。',
         '错误重述未被确认为实际下游误用，数值4与来源纠正需分开记录。',
         initial_wrong_restatement=phase([6,7], 'assertion', '标签17误命名为Haddock。'),
         correct_forward_value=phase([26], 'actual_computation', '按方程得到4。'),
         source_interpretation_correction=phase([45,46,47,48,49,51], 'explicit_self_correction_of_source', '明确初始17只属于标签，承认先前假设错误。'),
         subsequent_correct_use=phase([55,69,78,85], 'separated_variables_and_correct_value', '保持来源分离与目标4。')),
    case('P32', 'early_separation_with_rejected_alternatives',
         '瞬时错命名后立即给标签独立变量；前向0，后来的17为被区分的另一解释。',
         'P003含错误命名但同段立即质疑；未确认17进入实际错误计算。',
         initial_wrong_restatement=phase([3], 'short_lived_assertion_then_question', '暂写TigerUlna17。'),
         source_interpretation_correction=phase([4], 'explicit_separation', 'TigerUlnaLabels17作为另一量。'),
         correct_forward_value=phase([7,9], 'actual_computation', 'TigerAlula0、TigerUlna0。'),
         later_reappearance=phase([28,50], 'alternative_explicitly_separated', '讨论标签等同目标的可能，但明确与原文分离。')),
    case('P66', 'conditional_inverse_constraint_before_stable_separation',
         'KH22在If条件分支，发生于稳定来源分离前；正常前向18，后段明确标签无关。',
         'P015/P016语言来回切换，不能仅把其中等式视作实际工作状态。',
         initial_wrong_restatement=phase([4], 'assertion_then_question', '暂写ZG17并马上质疑。'),
         ambiguous_inverse_constraint=phase([15,16], 'conditional_identity_hypothesis', 'If两种身份相同才得到KH22。'),
         correct_forward_value=phase([34], 'correct_forward_result', '实际选择ZG18。'),
         source_interpretation_correction=phase([62], 'explicit_separation', '标签无关，目标18。')),
    case('V69', 'early_source_separation_control',
         '短暂误述17后区分标签与Crab，登记独立变量；后续7与分离均保持。',
         '没有观察到首次实际错误采用；合法常量17不可按同数字升级为同源。',
         initial_wrong_restatement=phase([5], 'questioned_restatement', '短暂说目标given17并马上检查。'),
         source_interpretation_correction=phase([6,10,13,14], 'explicit_separation', 'TDCrabLabels17与TDCrab分开。'),
         subsequent_correct_use=phase([40,50,95], 'correct_value_with_separated_source', '目标7且末尾仍明确标签未用于计算。')),
    case('P24', 'source_separation_with_rejected_identity_hypotheses',
         '标签另名后实际目标21；后续If/Suppose分支用21不等17排除，未确认实际复发。',
         '早期N_A17是否实际改变计算没有证据；P026的标签另名可与正确前向链同时核对。',
         initial_wrong_restatement=phase([4,5], 'assertion_then_identity_question', '初列N_A17但疑问身份。'),
         source_interpretation_correction=phase([26], 'separate_variable_assignment', '标签另名，目标用公式求21。'),
         correct_forward_value=phase([26], 'actual_computation', '3×7=21。'),
         later_reappearance=phase([36,44,45,46,47], 'hypotheses_explicitly_rejected', 'If/Suppose再假设17身份，随即以矛盾否定。')),
    case('V13', 'ambiguous_source_interpretation_with_rejected_constraint',
         '初列SBS17而前向得到11；后段17约束由If引出并用11矛盾拒绝，不确认为实际复发。',
         'P004的SBS/SBST简称混淆后立即核对原文，未确认错值17进入实际算式；P058来源分离仍用maybe。',
         initial_wrong_restatement=phase([4], 'assertion_and_immediate_formula_check', '目标17且简称混淆，但马上检查原式。'),
         correct_forward_value=phase([13], 'actual_computation', '21+13模23为11。'),
         tentative_source_separation=phase([58], 'hedged_source_separation', '可能是另一个数量。'),
         later_reappearance=phase([59,60,61], 'hypothesis_explicitly_rejected', 'If第一句是SBS17才有该约束，后用11拒绝。')),
    case('E24', 'rejected_operand_reversal_control',
         '实际Sr20-Ba13=7；反向16由If明确引出且立即以原题减法顺序拒绝。',
         '没有初始真实反向误用、纠正、再误用四阶段链，不能将候选提及当状态变化。',
         correct_forward_value=phase([93,94], 'actual_computation', 'SwimmingPoolRucksack20减AerobicsStudioBackpack13。'),
         later_reappearance=phase([95,96], 'hypothesis_explicitly_rejected', 'If反向为16，但题目是Sr-Ba，仍选7。')),
    case('V70', 'early_source_separation_paired_control',
         '与V58同题另seed，早期给标签另名，前向0；没有纠正后实际误用。',
         '同题配对只说明本轮文本行为不同，不能估计随机种子效应或内部机制。',
         initial_wrong_restatement=phase([5], 'assertion_then_question', '瞬时WJ17。'),
         source_interpretation_correction=phase([6,9,12], 'explicit_separation', '另记WJ_souvenir17。'),
         correct_forward_value=phase([22,23], 'actual_computation', 'WalrusLiver22-BWG22得到WJ0。'),
         subsequent_correct_use=phase([55], 'maintained_source_separation', '标签仍被视为另量。')),
    case('V59', 'early_source_separation_control',
         '初期ADC17含混；明确标签另量后计算目标10，后续保持分离。',
         '初期误命名没有确认为实际错误采用；后面正确值不足以反证先前语义含混。',
         initial_wrong_restatement=phase([5,16], 'ambiguous_restatement', '将标签数与ADC混称。'),
         source_interpretation_correction=phase([22,24,25,29,31], 'explicit_separation', 'SADC17与ADC分开。'),
         correct_forward_value=phase([36], 'actual_computation', '完整模23计算得到目标10。'),
         subsequent_correct_use=phase([37,41,60], 'maintained_separation_and_correct_value', '仍区分标签17和目标10。')),
    case('V43', 'separation_without_confirmed_initial_error_control',
         '从早段已给标签另名，正常前向目标11；没有确认初始错绑或实际复发。',
         '公式常量17有题目中的合法来源；关键词检索命中不表示污染。',
         source_interpretation_correction=phase([5,7], 'separated_from_outset_not_correction', '早段将标签视为另一数量。'),
         correct_forward_value=phase([17,32], 'actual_computation', '保留合法常量17，目标11。')),
    case('P26', 'early_source_recovery_paired_control',
         '与P22同图另seed，初期误述后区分标签，实际前向1并维持；没有R_T12工作值。',
         '原文没有P22式的实际逆推误用；本例仅做target17覆盖诊断，不伪造R_T12观测。',
         initial_wrong_restatement=phase([5,6,7,10], 'alternating_restatement_and_question', '来回确认第一句究竟是标签还是鱼数。'),
         source_interpretation_correction=phase([25], 'explicit_separation', '标签独立，按方程先计算RPT。'),
         correct_forward_value=phase([32], 'correct_forward_result', '目标1。'),
         subsequent_correct_use=phase([56], 'maintained_source_separation', '仍区分鱼数与标签。')),
    case('P27', 'ambiguous_restatement_after_source_separation',
         '明确标签另量后又问第一句是否目标17，但没有实际以17替代正确11计算。',
         'P060为疑问且同时记得标签独立，只支持表述不稳；不确认为数值复发或内部绑定残留。',
         initial_wrong_restatement=phase([31,37,38], 'wrong_restatement_with_conflict_check', '多次把标签称作Millet17。'),
         source_interpretation_correction=phase([45], 'explicit_separation', '标签不是Millet。'),
         later_reappearance=phase([60], 'ambiguous_question_after_separation', '再次问目标17还是不同数量，但仍承认计算11。'),
         subsequent_correct_use=phase([80,86,87,103], 'actual_computation_and_separated_source', '12-1=11，仍区分标签。')),
    case('P31', 'wrong_restatement_after_explicit_source_separation',
         'P057/P059分离来源后P060确有错误重述再现，随后多次含混；没有17再次进入实际错误计算的证据。',
         '明确分离的陈述并不稳定；只支持来源解释/表述来回摇摆，不支持潜伏内部绑定机制。',
         initial_wrong_restatement=phase([4], 'assertion', 'C_S被称为SquashCourt17 given。'),
         correct_forward_value=phase([25], 'actual_computation', '19+(0+18)模23为14。'),
         source_interpretation_correction=phase([57,59], 'explicit_separation_but_not_stable', '说明标签17与计算目标不同。'),
         later_reappearance=phase([60,63,66,69,70], 'wrong_restatement_and_unresolved_identity_questions', '又说第一句是SquashCourt17，出现矛盾检验；没有替代前向值。'),
         subsequent_correct_use=phase([84,117,126], 'explicit_separation_and_rejected_identity_hypothesis', '再次确认目标14，结尾C_S17明确是标签。')),
    case('P40', 'modular_equivalence_false_correction_control',
         '自称earlier wrong，但54与31模23均为8，实际数值没有改变。',
         '模型自报错误不能作为数值纠正真值；本例只复核该检索候选，不对其它来源歧义作穷尽标注。',
         equivalence_control=phase([54,55,56], 'self_reported_error_with_equivalent_computation', '12+42与12+19同余，后续答案20不变。')),
    case('P71', 'modular_equivalence_recheck_control',
         '先自称mistake，随后明确54与31模23都8，原步正确。',
         'neutral_noop对照；没有可确认的数值纠正阶段或同源错误。',
         equivalence_control=phase(list(range(59,70)), 'self_reported_error_then_explicit_equivalence', '保留完整原步、两种求余和后续20。')),
    case('E18', 'modular_equivalence_recheck_control',
         '21+38=59与21+15=36模23都13，模型复核后也确认原步正确。',
         'Th为CannedVegetablesThyme简称，不能因简称或自报mistake认定错误。',
         equivalence_control=phase([31,32], 'self_reported_error_then_correct_recheck', '两种合法约减均得到13。')),
]


def main():
    records = [json.loads(s) for s in (OUT/'records.jsonl').read_text().splitlines()]
    lookup = {r['code']:r for r in records}
    coverage = json.loads((OUT/'coverage-records.json').read_text())
    old = json.loads((AUDIT/'natural-recurrence-evidence.json').read_text())
    old_lookup = {r['code']:r for r in old['inventory']}
    summary = json.loads((OUT/'coverage-summary.json').read_text())
    sensitivity = json.loads((OUT/'task-sensitivity.json').read_text())
    assert len(CASES)==24 and len({c['code'] for c in CASES})==24
    assert set(c['code'] for c in CASES)==set(sensitivity['cases'])
    evidence_dir = OUT/'evidence'
    evidence_dir.mkdir(exist_ok=True)
    candidates=[]
    for c in CASES:
        r=lookup[c['code']]
        text=(OUT/r['fulltext_path']).read_text()
        paragraphs=list(re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*',text))
        m=r['meta']
        target=next(n for n in r['task']['nodes'] if n['id']==r['task']['target'])
        source_premise=next((p for p in r['task']['premises'] if p['premise_id']=='noop'), None)
        source={'identity_kind':'related_distractor_binding' if r['condition']=='related_noop' else 'arithmetic_or_operand_control',
                'target_node_id':target['id'],'target_aliases':target['aliases'],
                'target_canonical_value':target['value'],'distractor_premise':source_premise,
                'identity_rule':'Compare the named entity, premise and operation. Equal digits alone do not establish a shared source.'}
        diagnosis=sensitivity['cases'][c['code']]
        source.update(diagnostic_node_id=diagnosis['node_id'],diagnostic_node_aliases=diagnosis['aliases'],
                      diagnostic_value_interpretation=diagnosis['candidate_value_interpretation'])
        if c['code']=='V17':
            source.update(error_entity="Aquarium's Frilled Lizard", error='18+12 miscomputed as36; sum42 instead of36', wrong_residue=19, correct_residue=13)
        item={k:v for k,v in c.items() if k!='phases'}
        item.update(run=r['run'],original_id=m['id'],request_id=m.get('request_id'),
                    task_id=m['task_id'],base_group_id=m['base_group_id'],seed=m['seed'],role=m['role'],condition=r['condition'],
                    original_source_path=r['source_path'],fulltext_path=r['fulltext_path'],text_sha256=r['text_sha256'],
                    source_identity=source,review_depth='selected_contextual_assistant_review',
                    strict_post_numeric_correction_actual_same_source_recurrence='not_confirmed',
                    strict_post_source_correction_actual_same_source_recurrence='not_confirmed',
                    position_convention='zero-based Python Unicode code point intervals [start,end) in complete original text, including prompt',
                    evidence_file=f'evidence/{c["code"]}.md',phases={})
        numbers=sorted({n for stage in c['phases'].values() for n in stage['paragraph_numbers']})
        excerpts=[]
        for n in numbers:
            p=paragraphs[n-1]
            excerpt={'paragraph':n,'start':p.start(),'end':p.end(),'text':p.group()}
            assert text[excerpt['start']:excerpt['end']]==excerpt['text']
            excerpts.append(excerpt)
        for key,stage in c['phases'].items():
            item['phases'][key]={**stage,'positions':[{'paragraph':n,'start':paragraphs[n-1].start(),'end':paragraphs[n-1].end()} for n in stage['paragraph_numbers']]}
        for key,reason in {
                'first_actual_error_adoption':'未确认首次错误实际采用；相关重述、疑问或约束候选另列。',
                'numeric_correction':'未确认真实错误工作值被自行改正；正确前向值或模等价另列。',
                'source_interpretation_correction':'未确认稳定的明确来源纠正；若有试探分离，另列。',
                'post_correction_actual_error_use':'重点上下文复核没有确认纠正后同一错误来源再次进入实际执行的计算。'}.items():
            if key not in item['phases']:
                item['phases'][key]={'positions':None,'paragraph_numbers':[], 'speech_act':'not_confirmed','note':reason}
        item['excerpts']=excerpts
        item['task_sensitivity']=sensitivity['cases'][c['code']]
        candidates.append(item)
        body=[f'# {c["code"]}：{c["category"]}', '', c['judgment'], '',
              f'原始ID：`{m["id"]}`；run：`{r["run"]}`；task：`{m["task_id"]}`；seed：{m["seed"]}；role：`{m["role"]}`。', '',
              f'原文件：`{r["source_path"]}`', '', f'全文SHA256：`{r["text_sha256"]}`', '',
              f'[逐字全文](../{r["fulltext_path"]})；[候选表](../candidates.json)。', '',
              '本文件的P编号对应完整原文段落。字符位置是Python Unicode字符区间，包含原始prompt，起点含、终点不含。', '',
              f'不确定性：{c["uncertainty"]}', '', '## 分阶段判定', '']
        for key,stage in item['phases'].items():
            locations=', '.join(f'[P{p["paragraph"]:03}]'+f'(#p{p["paragraph"]:03})' for p in (stage['positions'] or [])) or '未确认，位置为null'
            body.extend([f'- **{key}**（{stage["speech_act"]}）：{stage["note"]} 证据：{locations}。',''])
        s=item['task_sensitivity']
        body.extend(['## 保存题目图的算术诊断', '',
                     f'解释：`{s["candidate_value_interpretation"]}`。此处是离线算术替换，不是新增模型干预或观测。', '',
                     f'节点：`{s["node_id"]}`；正确值{s["canonical_value"]}；直接消费者数{len(s["children"])}；图上后代数{len(s["descendants"])}。', '',
                     f'全部23个余数产生{s["distinct_final_values"]}种最终值；标准答案{s["canonical_final"]}。', ''])
        if 'wrong_value' in s:
            body.extend([f'候选值{s["wrong_value"]}对应最终值{s["wrong_final"]}；数值发生变化的后续节点数{len(s["changed_downstream_nodes"])}。候选是否实际采用以本例文本判定为准。',''])
        else:
            body.extend([f'两种整数表示{s["representative_a"]}和{s["representative_b"]}的余数均为{s["both_residues"]}，没有制造错误节点。',''])
        body.extend(['## 完整相关段落', ''])
        for e in excerpts:
            body.extend([f'### P{e["paragraph"]:03}', '', f'字符区间 `{e["start"]}:{e["end"]}`', '',
                         '```text', e['text'], '```', ''])
        (evidence_dir/(c['code']+'.md')).write_text('\n'.join(body))
    write_json('candidates.json',{'reviewer':'current Codex assistant; independent reading from original audit, not a second human annotator or gold standard',
                                 'selection':'purposive handoff candidates, source-conflict/separation cases in recovered texts, and arithmetic/operand controls; not exhaustive semantic labeling',
                                 'n_reviewed':24,'related_noop_reviewed':sum(c['condition']=='related_noop' for c in candidates),
                                 'confirmed_strict_post_numeric_correction_same_source_actual_recurrence':0,
                                 'confirmed_strict_post_source_correction_same_source_actual_recurrence':0,
                                 'no_prevalence_estimate':True,'records':candidates})
    fields=['code','run','original_id','request_id','task_id','base_group_id','seed','role','condition','category','judgment','uncertainty','original_source_path','text_sha256','evidence_file',
            'first_actual_error_adoption','numeric_correction','source_interpretation_correction','later_reappearance','post_correction_actual_error_use',
            'strict_post_numeric_correction_actual_same_source_recurrence','strict_post_source_correction_actual_same_source_recurrence']
    with (OUT/'candidates.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for c in candidates:
            row={k:c.get(k) for k in fields}
            for key in fields:
                if key in c['phases']:row[key]=json.dumps(c['phases'][key],ensure_ascii=False)
            writer.writerow(row)
    all_coverage=[]
    coverage_lookup={r['code']:r for r in coverage}
    for r in records:
        m=r['meta']
        if r['code'] in coverage_lookup:
            row={**coverage_lookup[r['code']], 'record_kind':'original_pr9_response',
                 'source_path':r['source_path'],'fulltext_path':r['fulltext_path'],
                 'archive_sha256':None,'archive_member':None,'source_line':None}
        else:
            archive_path, member, line = r['source_path'].split('::')
            row={'code':r['code'],'run':r['run'],'id':m['id'],'request_id':None,'task_id':m['task_id'],
                 'base_group_id':m['base_group_id'],'seed':m['seed'],'role':m['role'],'condition':r['condition'],
                 'record_kind':'original_pr8_unedited_archive_member','source_path':r['source_path'],'fulltext_path':r['fulltext_path'],
                 'previously_missing':False,'found':True,'archive_sha256':summary['pr8_archive_sha256'],
                 'archive_member':member,'source_line':int(line.removeprefix('line=')),
                 'text_sha256':r['text_sha256'],'expected_text_sha256':old_lookup[r['code']]['text_sha256'],
                 'text_hash_match':True,'original_audit_text_match':True,'archive_hash_match':True,
                 'file_hash_match':None,'metadata_match':True,'protocol_and_request_digest_match':None,
                 'protocol_note':'PR8 archive does not supply PR9-style response/request digests; not applicable, not reported as matched.',
                 'verified':True,'identity_note':summary['identity_note']}
        row['identity_key']=[r['run'],m['task_id'],m['seed'],m['role']]
        all_coverage.append(row)
    write_json('coverage-all-records.json',all_coverage)
    all_fields=list(dict.fromkeys(k for r in all_coverage for k in r))
    with (OUT/'coverage-all-records.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=all_fields);writer.writeheader()
        for r in all_coverage:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
    groups=defaultdict(Counter)
    for r in all_coverage:
        group=groups[(r['run'],r['role'],r['seed'],r['condition'])]
        group.update(expected=1,found=int(r['found']),verified=int(r['verified']),
                     file_hash_match=int(bool(r['file_hash_match'])),file_hash_not_applicable=int(r['file_hash_match'] is None),
                     text_hash_match=int(r['text_hash_match']),archive_hash_match=int(bool(r.get('archive_hash_match'))),
                     content_mismatch=int(not r['text_hash_match']),missing=int(not r['found']))
    grouped=[dict(run=k[0],role=k[1],seed=k[2],condition=k[3],**v) for k,v in sorted(groups.items())]
    with (OUT/'coverage-all-groups.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(grouped[0]));writer.writeheader();writer.writerows(grouped)
    write_json('review-summary.json',{'pr10_commit':summary['pr10_commit'],'unique_records_recovered':168,
                                     'previously_missing_recovered_and_verified':96,'pr9_verified':144,'pr8_original_verified':24,
                                     'semantic_context_reviewed':24,'related_context_reviewed':sum(c['condition']=='related_noop' for c in candidates),
                                     'strict_recurrence_confirmed_in_reviewed_candidates':0,
                                     'not_a_population_rate':True,'not_independent_human_gold':True,
                                     'arithmetic':sensitivity['summary'],'coverage_groups':grouped,
                                     'categories':dict(Counter(c['category'] for c in candidates))})
    table=['| 编号 | run/role/seed | 条件 | 判定 |', '|---|---|---|---|']
    for c in candidates:
        table.append(f'| [{c["code"]}]({c["evidence_file"]}) | {c["run"]}/{c["role"]}/{c["seed"]} | {c["condition"]} | {c["judgment"]} |')
    (OUT/'candidate-index.zh-CN.md').write_text('# 24条重点上下文复核\n\n非穷尽标注，不估计总体复发率。每例附完整相关段落与字符区间。\n\n'+'\n'.join(table)+'\n')
    print(json.dumps({'candidates':len(candidates),'excerpt_paragraphs':sum(len(c['excerpts']) for c in candidates),'coverage_all':len(all_coverage),'groups':len(grouped)},ensure_ascii=False))


if __name__=='__main__':main()
