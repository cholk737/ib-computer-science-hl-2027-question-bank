from checkpoint_reviews import *
R22=[]
R22.append(review('P-SRC004-Q11-e-i',[
 m('A1.1.8',1,'Describe lossless exact reconstruction and variable compressibility for medical diagrams.','partial','Lossless purpose/limitations assessed; no particular RLE/transform mechanism and no full lossy/lossless method comparison.'),
], 'Lossless decompression restores original data exactly. Compression exploits available structure/redundancy, and not every arbitrary input can shrink to a fixed guaranteed ratio; incompressible/already compressed content may shrink little or grow.', 'Exactness, redundancy and content-dependent reduction correctly address both why lossless and why size limit not guaranteed.', 'Three1-mark criteria total3. No unsupported assertion every file compresses; equivalent reversible encoding explanation acceptable.'))
R22.append(review('P-SRC004-Q12-a-i',[
 m('A1.3.6',2,'Identify two distinct vehicle-detection sensor types for a barrier.','partial','Sensor selection only; no sensor transduction explanation or controller/actuator/control algorithm roles.'),
], 'An inductive loop can detect vehicle metal above it; an infrared presence/beam sensor can detect crossing/approach in suitable position. Other appropriate detection devices are valid.', 'Two distinct feasible sensors satisfy Identify2.', 'Two1-mark criteria explicitly permit any suitable distinct sensors, avoiding fixed example restriction; repeated variants of same sensor not automatically distinct.'))
R22.append(review('P-SRC004-Q12-a-ii',[
 m('A1.3.6',1,'Outline automatic vehicle-presence input feeding prompt controller response.','partial','Input and its use for response assessed; no complete feedback cycle or open/closed-loop distinction.'),
 m('A1.3.6',2,'Explain sensor role replacing manual vehicle-count entry in a barrier controller.','partial','Sensor function only, not all component roles or physical transduction.'),
], 'Automatic sensing provides measurements/events without waiting for a person to enter a count, enabling timely control based on actual detected arrivals.', 'Automatic measurement plus link to prompt continuous/event-driven response gives appropriate Outline2.', 'Two1-mark elements total2. Does not require claiming sensors never fail or always more accurate than humans.'))
for r,t,e in zip(R22,['explanation','conceptual recall','explanation'],['Describe lossless suitability and content-dependent limit.','Identify2 input sensor components.','Outline contextual sensor-use reason and consequence.']):r['question_type']=t;r['question_type_review']={'status':'verified','reviewer':'/root/theme_a_coverage','evidence':e}
save_batch(R22,22,'Review P-SRC004-Q12-b, P-SRC004-Q12-c-i, P-SRC004-Q12-c-ii; save batch-023.', ['review_batch022.py'])
