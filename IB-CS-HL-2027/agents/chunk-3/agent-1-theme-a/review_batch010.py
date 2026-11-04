from checkpoint_reviews import *
R10=[]
R10.append(review('P-SRC002-Q02-d',[
 m('A3.2.6',1,'Construct a three-table 3NF training-enrolment schema from supplied functional dependencies.','direct','Meaningful school/training management application. Dependencies assign learner facts to learner, event facts to event, and completion to the pair; source example list is non-exhaustive.'),
], 'LearnerID and EventID determine their separate entity facts; Completed depends on the combined pair. Decomposition removes both partial dependencies and leaves no stated transitive non-key dependency.', 'LEARNER/EVENT/ENROLMENT with composite enrolment PK and two FKs preserves all supplied fields and dependencies. Assumes one enrolment per learner/event pair as supplied dependency.', 'Five1-mark components total5: both entity groups, completion association, composite key, two FKs/no partial dependence. Equivalent table/attribute naming and semantically valid surrogate-key schema with unique pair may be accepted.'))
R10.append(review('P-SRC002-Q03-a',[
 m('A3.2.1',1,'Outline a conceptual schema for clinic entities and relationships.','partial','Conceptual level only; logical and physical structures not independently described.'),
 m('A3.2.1',2,'Explain a high-level structure independent of physical storage/DBMS.','partial','One abstraction level described and distinguished from implementation; no three-way schema hierarchy.'),
], 'Conceptual schema captures domain entities/relationships without committing to DBMS storage design.', 'High-level entities/relationships plus independence from implementation correctly outlines its planning role.', 'Two1-mark elements total2. Context-specific entities can illustrate but are not mandatory because prompt asks role, not construct clinic schema.'))
R10.append(review('P-SRC002-Q03-c',[
 m('A3.3.1',1,'Describe SQL DDL responsibilities when implementing a schema.','partial','DDL only, no DML comparison or full distinction between language categories.'),
 m('A3.3.1',2,'Describe creating structures, typed columns and key constraints.','partial','Data-definition statement purposes tested; manipulation operations not assessed.'),
], 'DDL specifies tables/columns/types and structural constraints. Description correctly distinguishes structure enforcement from processing row changes.', 'Three concrete DDL responsibilities appropriately describe implementing a relational model.', 'Three1-mark criteria total3. No SQL command syntax construction required; accurate DDL examples can substantiate equivalent description.'))
save_batch(R10,10,'Review P-SRC002-Q03-d, P-SRC002-Q03-e, P-SRC002-Q04-a; save batch-011 and keep direct-statement versus exact guidance distinctions explicit.', ['review_batch010.py'])
