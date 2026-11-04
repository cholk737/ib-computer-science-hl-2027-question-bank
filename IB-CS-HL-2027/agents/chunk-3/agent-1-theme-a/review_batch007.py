from checkpoint_reviews import *
R7=[]
R7.append(review('P-SRC002-Q01-a',[
 m('A3.2.2',2,'Construct supervisor-to-production and production-to-editor one-to-many relationships.','direct','Two explicitly specified relationships translated into ERD, each1 mark.'),
 m('A3.2.2',3,'Show mandatory one-and-one-or-more participation on both ERD relationships.','direct','Every child exactly one parent and every parent at least one child stated. Criteria explicitly include cardinality/modality.'),
], 'The four stated minimum/maximum constraints yield Supervisor1→Production1..many and Production1→Editor1..many, with each child exactly1 parent.', 'Textual answer correctly describes each relation and mandatory participation; candidate expected an actual equivalent labelled ERD.', 'Two independently marked relationship/cardinality/modality criteria total2. Equivalent standard ERD notations accepted through partial-credit note. Output diagram required, no missing stimulus diagram.'))
R7.append(review('P-SRC002-Q01-b',[
 m('A3.1.1',2,'Outline one relational database retrieval/consistency benefit for document change histories.','partial','Only one contextual benefit tested, not features or limitations or all listed benefits.'),
], 'Shared related records support coherent queries and avoid manually joining independent change files; database use still requires correct identifiers and transactional updates.', 'Model gives a concrete benefit (consistent query retrieval) developed in document-history context, meeting Outline2.', 'One valid retrieval/consistency/duplication benefit plus contextual development yields2. Alternatives phrased as equivalent technically valid solutions in partial-credit note.'))
R7.append(review('P-SRC002-Q01-c',[
 m('A3.3.6',1,'Explain how a supplied version check avoids stale overwrite/lost update.','partial','Concurrency/isolation facet assessed through provided mechanism; no requirement to know timestamp protocol, full ACID definitions or transaction commands.'),
], 'Optimistic concurrency can detect stale version7 after committed version8 and reject/retry that attempted update; comparing and applying must be controlled as one conditional update in a correct implementation.', 'The mismatch7 versus8 and rejection/retry prevent overwriting a committed edit, appropriate two-stage outline.', 'One detection point plus one prevention point total2; retry must use refreshed state rather than blindly replay stale overwrite.'))
save_batch(R7,7,'Review P-SRC002-Q01-d, P-SRC002-Q01-e-i, P-SRC002-Q01-e-ii; save batch-008.', ['review_batch007.py'])
