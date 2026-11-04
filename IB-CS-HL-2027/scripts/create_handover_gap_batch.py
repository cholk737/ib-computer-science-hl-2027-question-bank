"""One bounded, coordinator-authored original batch. Refuses overwriting IDs.

Created after repository-first commit for user-requested Phase 1. No test,
examination or PDF is assembled. Answers stay out of student question files.
"""
from pathlib import Path
import csv
import hashlib
import io
import itertools
import json
import os
import tempfile
from datetime import datetime, timezone

P = Path(__file__).resolve().parents[1]


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    os.replace(temp, path)


def main():
    scope = {s['code']: s for s in json.loads((P / 'syllabus/SYLLABUS_MASTER.json').read_text())}
    with (P / 'question-bank/QUESTION_BANK.csv').open() as f:
        reader = csv.DictReader(f); fields = list(reader.fieldnames); rows = list(reader)
    existing = {r['question_id'] for r in rows}
    definitions = [
        {
            'question_id': 'O-C3-B-001', 'code_id': 'B2.5.1', 'level': 'SL/HL common',
            'prompt': 'A laboratory stores one integer measurement on each line of a text file. There are no blank lines, but the file may contain no measurements. Construct load_totals(input_path, output_path) in Python. Read all the measurements, then overwrite output_path with exactly two lines: the number of measurements, followed by their total. End each output line with a newline. Return (number_of_measurements, total). Both paths refer to different files; the input is readable and the output is writable. Close all files after use. You may use Python built-ins and either explicit closing or a context manager.',
            'reference': 'def load_totals(input_path, output_path):\n    count = 0\n    total = 0\n    with open(input_path, "r", encoding="utf-8") as source:\n        for line in source:\n            total += int(line.strip())\n            count += 1\n    with open(output_path, "w", encoding="utf-8") as report:\n        report.write(str(count) + "\\n")\n        report.write(str(total) + "\\n")\n    return count, total',
            'criteria': ['Opens and reads the input text file in read mode.', 'Converts and processes every integer measurement, including negative values.', 'Determines both count and total correctly, including an empty input.', 'Opens the output in write/overwrite mode and writes the two requested newline-terminated lines in order.', 'Closes both files, including correct use of context managers.', 'Returns the correct count/total tuple after completing file processing.'],
            'skills': [(1, 'Construct text-file input and a numeric summary report.', 'direct'), (2, 'Select read and overwrite/write modes for different text files.', 'partial'), (3, 'Read and write sequential text, then close both files.', 'partial'), (5, 'Apply appropriate Python file operations; context-manager closing is acceptable.', 'partial')],
            'limits': 'Append mode remains untested. Python helper examples are may-include, not a mandatory call checklist. No Java requirement is introduced.'
        },
        {
            'question_id': 'O-C3-B-002', 'code_id': 'B4.1.5', 'level': 'HL-only',
            'prompt': 'Two clubs supply lists of member IDs, club_a and club_b. An ID can occur more than once in either list. Construct compare_members(club_a, club_b) in Python. Return a tuple containing three sets in this order: IDs in both clubs; IDs in club_a but not club_b; IDs in at least one club. Each ID must occur only once in a returned set. Set order is irrelevant. Do not modify the input lists. You may use Python set operations.',
            'reference': 'def compare_members(club_a, club_b):\n    a = set(club_a)\n    b = set(club_b)\n    both = a & b\n    only_a = a - b\n    either = a | b\n    return both, only_a, either',
            'criteria': ['Represents club_a membership uniquely as a set or equivalent set-based construction.', 'Represents club_b membership uniquely as a set or equivalent set-based construction.', 'Computes the intersection for IDs in both clubs.', 'Computes the directional difference A minus B.', 'Computes the union for IDs in either club.', 'Returns the three sets in the requested order without modifying either input list.'],
            'skills': [(1, 'Apply unique, unordered set membership to duplicate-bearing lists.', 'direct'), (2, 'Construct union, intersection and directional difference.', 'direct')],
            'limits': 'Does not test membership/add/remove/subset operations or hash-table mechanics. Order of set iteration must not be marked.'
        },
        {
            'question_id': 'O-C3-B-003', 'code_id': 'B4.1.5', 'level': 'HL-only',
            'prompt': 'A visitor system uses a mutable set active and a separate set permitted. Construct update_access(active, new_id, leaving_id, permitted) in Python. First add new_id to active. Then remove leaving_id if it is present; an absent leaving_id must not cause an error. Finally return a tuple (new_still_active, all_permitted): whether new_id is in the final active set, and whether every final active ID belongs to permitted. The two IDs may be equal, so the stated operation order matters. Modify active itself and leave permitted unchanged. You may use Python set operations.',
            'reference': 'def update_access(active, new_id, leaving_id, permitted):\n    active.add(new_id)\n    if leaving_id in active:\n        active.remove(leaving_id)\n    return new_id in active, active <= permitted',
            'criteria': ['Adds new_id to the original active set.', 'Removes leaving_id when present after the addition.', 'Handles an absent leaving_id safely without an exception.', 'Determines whether new_id belongs to the final active set, including when both IDs are equal.', 'Correctly checks whether final active is a subset of permitted, including equality and an empty final set.', 'Returns the two Boolean results in order, modifying active itself while preserving permitted.'],
            'skills': [(1, 'Apply unique set membership while updating a mutable set.', 'partial'), (3, 'Construct membership, add, safe remove and subset operations with a defined update order.', 'direct')],
            'limits': 'Does not test a superset operator separately or union/intersection/difference calculations. Equivalent safe removal methods are accepted; no arbitrary built-in ban.'
        },
    ]
    results = {}
    for d in definitions:
        assert d['question_id'] not in existing, 'Refuse duplicate/overwrite: ' + d['question_id']
        namespace = {}; exec(d['reference'], namespace)
        count = 0
        if d['question_id'].endswith('001'):
            with tempfile.TemporaryDirectory() as td:
                source, output = Path(td)/'in.txt', Path(td)/'out.txt'
                for content, expected in [('', (0,0)), ('-7\n', (1,-7)), ('4\n-1\n0\n9\n',(4,12)), ('12',(1,12))]:
                    source.write_text(content); output.write_text('old content must disappear\n')
                    assert namespace['load_totals'](str(source),str(output)) == expected
                    assert output.read_text() == str(expected[0])+'\n'+str(expected[1])+'\n'
                    count += 1
                opened = []; real_open = open
                def tracked_open(*args, **kwargs):
                    handle = real_open(*args, **kwargs); opened.append(handle); return handle
                namespace['open'] = tracked_open
                namespace['load_totals'](str(source),str(output))
                assert len(opened)==2 and all(h.closed for h in opened)
                count += 1
        elif d['question_id'].endswith('002'):
            for left in range(16):
                for right in range(16):
                    a=[i for i in range(4) if left>>i&1]; b=[i for i in range(4) if right>>i&1]
                    a += a[:1]; b += b[:1]; before=(a[:],b[:])
                    expected=tuple({i for i in range(4) if mask>>i&1} for mask in [left&right,left&~right,left|right])
                    assert namespace['compare_members'](a,b)==expected and (a,b)==before
                    count += 1
        else:
            for initial in range(16):
                for permitted_mask in range(16):
                    for new_id, leaving_id in itertools.product(range(4),repeat=2):
                        active={i for i in range(4) if initial>>i&1}; permitted={i for i in range(4) if permitted_mask>>i&1}; saved=permitted.copy()
                        final_mask=(initial|(1<<new_id))&~(1<<leaving_id)
                        final={i for i in range(4) if final_mask>>i&1}
                        expected=(bool(final_mask&(1<<new_id)),not bool(final_mask&~permitted_mask))
                        assert namespace['update_access'](active,new_id,leaving_id,permitted)==expected
                        assert active==final and permitted==saved
                        count += 1
        results[d['question_id']]={'passed':True,'cases':count,'code_sha256':hashlib.sha256(d['reference'].encode()).hexdigest()}
    atomic(P/'audits/chunk-3/ORIGINAL_GAP_BATCH_CHECKS.json',{'method':'Executed exact reference functions against independent fixture/bitmask oracles; source scope read in full; mark sums and alternatives manually checked by coordinator. Original questions are author-verified, not independent C4 verified.','results':results})
    for d in definitions:
        qid=d['question_id']; code=d['code_id']; stamp=datetime.now(timezone.utc).isoformat()
        record={'question_id':qid,'source_question_ids':[],'derivation_status':'original_unofficial','unofficial':True,
                'question_text':d['prompt'],'syllabus_codes':[code],'theme':'B','level':d['level'],'marks':6,
                'command_term':'Construct','difficulty':'medium','question_type':'Python code construction',
                'adaptation_rationale':'Original coordinator-authored question for a zero-linked C2 objective; no historical source question or official marking status claimed.',
                'solution':d['reference'],'marking_points':[{'marks':1,'criterion':x} for x in d['criteria']],
                'acceptable_alternatives':['Any correct Python implementation meeting the stated input/output, mutation and file requirements. Equivalent set methods/operators and correct context-manager or explicit file closing accepted. Do not double-credit the same achieved criterion.'],
                'partial_credit_notes':'Award each independent achieved step up to six marks; a minor syntax slip need not erase an otherwise clearly demonstrated algorithmic step. Accept equivalent valid algorithms. No credit for contradicting the stated operation order or output contract.',
                'common_errors':[],'verification':{'technical':'Exact reference executed; see audits/chunk-3/ORIGINAL_GAP_BATCH_CHECKS.json.','scope':d['limits']},
                'code':d['reference'],'test_code':'','assets':[],'markscheme_status':'preliminary_unofficial_verified_by_coordinator_author',
                'record_path':f'question-bank/records/{qid}.json','question_path':f'question-bank/questions/{qid}.json','markscheme_path':f'question-bank/markschemes/{qid}.json',
                'coordinator_status':'author_content_scope_answer_marking_execution_checks_passed; independent_Chunk4_audit_pending','independent_verification_status':'pending'}
        assert sum(m['marks'] for m in record['marking_points'])==record['marks']
        question={k:v for k,v in record.items() if k in ['question_id','source_question_ids','derivation_status','unofficial','question_text','syllabus_codes','theme','level','marks','command_term','difficulty','question_type','assets']}
        answer={k:record[k] for k in ['question_id','unofficial','solution','marking_points','acceptable_alternatives','partial_credit_notes','common_errors','verification','code','markscheme_status']}
        for rel,data in [(record['record_path'],record),(record['question_path'],question),(record['markscheme_path'],answer)]:atomic(P/rel,data)
        record_hash=hashlib.sha256((P/record['record_path']).read_bytes()).hexdigest()
        review={'question_id':qid,'record_sha256':record_hash,'reviewer':'/root','reviewed_at':stamp,
                'question_type':'Python code construction','review_scope':'Coordinator author review of new original; independent Chunk4 review pending.',
                'verification':{dim:{'status':'verified','evidence':evidence} for dim,evidence in {
                    'mapping':'Read complete exact statement and guidance; mapped only described aspects; omitted scope explicitly retained.',
                    'technical':f'Executed reference function in {results[qid]["cases"]} domain/edge cases; independent fixture or bitmask oracle; output/mutation/file closing checked.',
                    'answer':'Stored full reference matches tested function and defined domain; separate student file contains no reference solution.',
                    'markscheme':'Six independent positive criteria manually checked against command and complete solution; alternatives/partial credit included; unofficial preliminary author criteria.',
                    'assets':'All necessary input/domain information and function contract contained in prose; no missing diagram/table or code stimulus required.',
                    'provenance':'Original coordinator authorship recorded; historical source IDs intentionally empty; official syllabus evidence is not claimed as an original question source.'}.items()},
                'mappings':[{'code':code,'scope_bullet_id':f'{code}:G{i:02d}','exact_guidance':scope[code]['guidance_paragraphs'][i-1],'assessed_skill':skill,'relevance':rel,'evidence':'The actual code-construction contract and independent marking steps require this aspect. '+d['limits'],'coverage_limit':d['limits'],'statement_relevance':'direct','statement_evidence':'Prompt explicitly requires construction of the scoped Python function.'} for i,skill,rel in d['skills']],
                'issues':[],'scope_not_assessed':[d['limits']],'execution_evidence':'audits/chunk-3/ORIGINAL_GAP_BATCH_CHECKS.json'}
        atomic(P/f'question-bank/original-review-drafts/{qid}.json',{'reviews':[review]})
        row={f:'' for f in fields}
        for k in ['question_id','record_path','question_path','derivation_status','theme','level','marks','command_term','difficulty','markscheme_path']:row[k]=record[k]
        row.update({'source_question_ids':'[]','syllabus_codes':json.dumps(record['syllabus_codes']),'verification_status':record['coordinator_status']})
        rows.append(row)
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    temp=P/'question-bank/QUESTION_BANK.csv.tmp';temp.write_text(stream.getvalue());os.replace(temp,P/'question-bank/QUESTION_BANK.csv')
    print(json.dumps({'originals_saved':len(definitions),'total_bank_rows':len(rows),'checks':results,'next':'Approve new exact scope review versions, refresh coverage/index and import canonical DB; then Phase2 handover.'}))


if __name__=='__main__':main()
