from checkpoint_reviews import *
R20=[]
R20.append(review('P-SRC004-Q10-a',[
 m('A2.4.3',1,'Outline how an independent additional authentication factor limits stolen-password access.','partial','MFA only from long countermeasure list; does not assess password policy/training/IDS or other measures.'),
], 'An attacker holding only a password cannot complete properly configured MFA without an independent factor; two knowledge passwords are not two independent factor categories.', 'Second factor requirement and stolen-password insufficiency give correct cause/consequence pair.', 'Two1-mark elements total2. Correct independent factor examples accepted; no claim MFA makes all attacks impossible.'))
R20.append(review('P-SRC004-Q10-b-i',[
 m('A2.4.2',1,'Identify ransomware or other file-damaging malware causing unavailable clinic files.','partial','One malware threat only; no other named vulnerability or detailed mechanism required for Identify1.'),
], 'Unauthorized file encryption by ransomware can deny legitimate access; destructive malware is another valid unavailable-data threat.', 'Ransomware encrypting files meets requested single threat and effect.', 'One1-mark criterion explicitly accepts file-damaging/unavailability malware alternatives; not fixed ransomware-only answer.'))
R20.append(review('P-SRC004-Q10-b-ii',[
 m('A2.4.3',1,'Describe security patching closing a known exploitable flaw.','partial','Software updating only; no guarantee against other vulnerabilities or all malware.'),
], 'Installing an applicable security fix removes the particular known exploitation path; does not make unpatched/zero-day/social-engineering attacks impossible.', 'Patches/security fixes plus removal of known exploit path accurately explains risk reduction.', 'Two1-mark components total2. Equivalent vulnerability-fix explanation accepted; merely newer features is insufficient for security mechanism.'))
for r,t,e in zip(R20,['explanation','conceptual recall','explanation'],['Outline MFA mechanism and consequence.','Identify one malware threat.','Describe patching mechanism and risk reduction.']):r['question_type']=t;r['question_type_review']={'status':'verified','reviewer':'/root/theme_a_coverage','evidence':e}
save_batch(R20,20,'Review P-SRC004-Q10-d, P-SRC004-Q10-e, P-SRC004-Q11-d; save batch-021.', ['review_batch020.py'])
