"""Regression: related concepts must not be treated as the same assessed skill."""
from pathlib import Path
import json
import bank_db

negative = [
    ('information hiding', 'encapsulation'),
    ('counted loop', 'construct a for-each loop'),
    ('counted loop', 'construct a generic for loop'),
    ('pre-condition loop', 'use a while loop'),
    ('linear regression', 'interpret slope and intercept'),
    ('or', 'explain information encoding'),
    ('AND', 'explain bandwidth constraints'),
]
positive = [
    ('counted loops', 'construct a count-controlled loop'),
    ('pre-condition loop', 'trace a pretest loop'),
    ('post-condition loop', 'describe repeat-until control'),
]
for request, skill in negative:
    assert not bank_db.skill_match(request, skill), (request, skill)
for request, skill in positive:
    assert bank_db.skill_match(request, skill), (request, skill)
result = {'passed': len(negative) + len(positive), 'failed': 0,
          'negative_concept_equivalences_rejected': negative,
          'narrow_loop_aliases_accepted': positive,
          'limits': 'These are matching-precision checks, not a claim of unrestricted semantic recall.'}
Path(__file__).with_name('semantic_precision_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'passed': result['passed'], 'failed': result['failed']}))
