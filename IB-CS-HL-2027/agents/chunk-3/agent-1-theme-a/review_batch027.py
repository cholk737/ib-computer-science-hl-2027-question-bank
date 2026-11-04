from checkpoint_reviews import *
R27=[]
R27.append(review('P-SRC005-Q07',[
 m('A1.1.4',1,'Explain generic cache capacity retaining a repeatedly accessed working set.','partial','Cache purpose only, no L1/L2/L3 distinction or other memory-type breadth.'),
 m('A1.1.4',2,'Explain increased cache residency reducing slower-RAM waits and runtime.','direct','Explicit CPU/cache/RAM performance interaction and access-pattern qualification.'),
 m('A1.1.4',3,'Use higher cache-hit rate to explain potential runtime benefit.','partial','Hit rate assessed; cache-miss term/consequence not independently required, although reduced RAM accesses imply fewer misses.'),
], 'Larger cache may retain more working-set data and raise hit rate, reducing average slower-memory access waits. Not guaranteed for every access pattern/hardware design.', 'Three-stage retained data→hits/RAM reduction→less waiting/runtime chain is correct.', 'Three1-mark causal components total3, no double-credit for repeating bigger/faster without mechanism.'))
R27.append(review('P-SRC005-Q10-a',[
 m('A2.1.3',1,'Identify a wireless access point from its wireless-to-wired-LAN bridging function.','partial','Only WAP recognized; no other device functions or TCP/IP layer mapping.'),
], 'A wireless access point connects compatible wireless clients to a wired LAN; a combined wireless router may contain this function but function requested is AP.', 'Wireless access point is correct device identification.', 'Single1-mark identification criterion; integrated device answer should name its AP function rather than confuse routing with wireless bridging.'))
R27.append(review('P-SRC005-Q10-b',[
 m('A2.3.2',1,'Distinguish fibre and wireless transmission in a noisy factory.','partial','Two media compared; twisted pair omitted.'),
 m('A2.3.2',2,'Compare contextual reliability benefits and limitations of fibre versus wireless.','partial','Specific reliability/interference case, not full strengths/limitations across all three media.'),
 m('A2.3.2',3,'Explain obstruction/interference/attenuation effects on link reliability.','partial','Only subset of must-include factors: interference,attenuation/reliability. No installation/cost/security/full bandwidth/range comparison.'),
], 'Metal obstacles weaken radio; electrical noise can impair wireless reception. Optical fibre resists electromagnetic interference and confines light, but physical damage still causes failures.', 'Balanced context-specific distinction avoids saying fibre cannot fail or all wireless is unreliable.', 'Four1-mark contextual comparison elements total4 with both media addressed and causality. Equivalent paired contrasts accepted.'))
for r,t,e in zip(R27,['explanation','conceptual recall','comparison'],['Explain working-set cache performance.','Identify one network device by given function.','Distinguish two media using contextual mechanisms and reliability.']):r['question_type']=t;r['question_type_review']={'status':'verified','reviewer':'/root/theme_a_coverage','evidence':e}
save_batch(R27,27,'Review P-SRC005-Q10-c, P-SRC005-Q10-d, P-SRC005-Q10-e; save batch-028.', ['review_batch027.py'])
