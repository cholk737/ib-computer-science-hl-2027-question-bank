from checkpoint_reviews import *
R8=[]
R8.append(review('P-SRC002-Q01-d',[
 m('A3.3.6',1,'Explain locking/serialized competing writers preventing a booking lost update.','partial','Isolation and integrity preservation through a supplied locking model; no full ACID catalogue required.'),
 m('A3.3.6',2,'Explain commit boundary when locks protect a conflicting update.','partial','Commit/release boundary assessed conceptually; no BEGIN/ROLLBACK syntax construction.'),
], 'Exclusive lock before update blocks conflicting writer; reading current committed data before its own protected update avoids overwriting stale state. Lock lifetime must cover appropriate transaction boundary.', 'Answer gives lock, wait/retry, fresh ordered updates, commit/release, and why no lost update, all coherent.', 'Five1-mark components total5 and match Explain depth. Correct locking sequence—not just use a lock—needed for full marks; equivalent safe transaction behaviour acceptable.'))
R8.append(review('P-SRC002-Q01-e-i',[
 m('A3.3.6',1,'Outline ACID consistency with a conserved total in a two-account transfer.','partial','Consistency/integrity invariant only; atomicity/isolation/durability not directly requested.'),
], 'A valid no-fee transfer preserves declared account constraints and combined balance. Consistency is constraint preservation, not merely every user seeing the same value.', 'General constraint preservation plus debit/credit conserved total is correct contextual expansion for2.', 'Two1-mark criteria distinguish definition and valid invariant/example; other appropriate stated integrity rules accepted.'))
R8.append(review('P-SRC002-Q01-e-ii',[
 m('A3.3.6',1,'Describe atomic all-or-none transfer restoration after partial failure.','partial','Partial debit rollback preserves consistency/atomicity; isolation/durability untested.'),
 m('A3.3.6',2,'Describe ROLLBACK undoing the uncommitted transaction.','partial','ROLLBACK behaviour only; BEGIN/COMMIT not directly required.'),
], 'Rollback undoes uncommitted changes of that transaction, restoring the debit and consistent pre-transfer balances. It does not undo unrelated committed transactions.', 'All answer elements correctly target incomplete transaction, undo partial changes and restore previous balances.', 'Three1-mark elements total3 with partial credit for mechanism and state; do not accept merely completing the credit as explanation of ROLLBACK.'))
save_batch(R8,8,'Review P-SRC002-Q02-a, P-SRC002-Q02-b, P-SRC002-Q02-c with executed SQL answer check; save batch-009.', ['review_batch008.py'])
