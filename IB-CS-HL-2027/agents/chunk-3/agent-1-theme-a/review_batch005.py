from checkpoint_reviews import *
R5=[]
R5.append(review('P-SRC001-Q12-b-i',[
 m('A1.1.1',2,'State the MDR function in a memory-read transfer.','partial','One register function only: holds the returning word. No PC/MAR/IR/AC or other register operation/interactions tested.'),
], 'The MDR holds the data/instruction word read from addressed main memory before internal CPU use.', 'The one-sentence answer correctly identifies temporary data holding, not the memory address (MAR).', 'Single1-mark criterion matches State and accepts equivalent memory-buffer-register terminology.'))
R5.append(review('P-SRC001-Q12-b-ii',[
 m('A1.1.4',1,'Explain cache purpose using repeated instruction access.','partial','Cache function tested but levels L1/L2/L3 and other primary memories not distinguished.'),
 m('A1.1.4',2,'Explain CPU cache hits reducing slower main-RAM access waiting.','direct','Connects cached instruction copies, faster hits and lower CPU waiting to performance; no unsupported universal speedup guarantee.'),
 m('A1.1.4',3,'Use cache-hit behaviour to explain repeated instruction performance.','partial','Hit meaning/effect assessed; cache miss is not explicitly requested or independently marked.'),
], 'Temporal reuse can be served from faster cache when the relevant instruction is resident; lower access latency reduces waiting. Benefit depends on hits/access pattern.', 'Model answer gives retained copies, faster hit access versus RAM, and performance consequence, supporting Explain3.', 'Three1-mark linked explanation elements total3. Repetition of faster access alone cannot earn both mechanism and consequence without explanation.'))
R5.append(review('P-SRC001-Q12-b-iii',[
 m('A1.1.1',3,'Explain address/data/control bus roles in one CPU memory-read operation.','direct','All three named buses receive distinct roles and coordination; does not test processor types, all registers or a hardware diagram.'),
 m('A1.1.5',2,'Explain part of memory/register interaction during fetch-related memory read.','partial','Addresses/read signal/returned word/coordination assessed; full PC→MAR→MDR→IR register-transfer sequence and decode/execute absent.'),
], 'Address bus selects location; control bus requests read/coordinates; memory data is carried back by data bus to MDR. These roles are consistent in the stated simplified CPU model.', 'Four listed points correctly describe three bus roles plus timing/coordination; no read/write direction confusion.', 'Four1-mark components total4. Control command and coordination are distinguishable when each explained; avoid double-credit for repeating read signal alone.'))
save_batch(R5,5,'Review P-SRC001-Q13-a-i and P-SRC001-Q13-a-ii; save batch-006 and source001 Theme A topic checkpoint.', ['review_batch005.py'])
