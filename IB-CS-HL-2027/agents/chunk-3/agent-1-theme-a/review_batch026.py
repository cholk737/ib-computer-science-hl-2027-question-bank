from checkpoint_reviews import *
hexvalue='00CC33';binary=''.join(f'{int(n,16):04b}' for n in hexvalue);assert binary=='000000001100110000110011' and len(binary)==24
colours=(2**5)*(2**5)*(2**5);assert colours==2**15==32768
atomic(O/'checks/P-SRC005-Q05-representation-check.json',{'questions':['P-SRC005-Q05-a','P-SRC005-Q05-b'],'hex':hexvalue,'binary_24bits':binary,'five_bit_RGB_colours':colours,'methods':['Independent nibble conversion preserves leading zeros','Per-channel cardinality product equals total-bit cardinality'],'passed':True})
R26=[]
R26.append(review('P-SRC005-Q04-b',[
 m('A2.3.2',3,'Outline insufficient available bandwidth causing streaming disruption.','partial','Bandwidth/usable-rate factor only; no fibre/twisted-pair/wireless comparison or full must-include factor set.'),
], 'If encoded video consumes bits faster than connection delivers useful data, buffering is depleted and playback pauses or adaptive quality can reduce demand. Wireless is context, not proof wireless always slower.', 'Arrival-versus-consumption mismatch plus buffering/pause/reduced quality consequence is correct Outline2.', 'Two1-mark causal points total2; no credit for unexplained wireless is bad assertion.'))
R26.append(review('P-SRC005-Q05-a',[
 m('A1.2.1',3,'Convert a six-digit hexadecimal integer to its fixed-width24-bit binary form.','partial','Hex-to-binary direction only; inverse direction not tested here.'),
 m('A1.2.2',2,'Use an RGB binary colour representation supplied in the prompt.','supporting','RGB/8-bit allocation is GIVEN, not elicited. The task assesses number conversion, not explaining image-storage mechanism; image keyword cannot certify that knowledge.'),
], 'Every hex digit maps to four bits;00CC33 maps to00000000 11001100 00110011 with leading zeros retained for24-bit width.', 'Saved independent nibble conversion matches entire24-bit answer; checks/P-SRC005-Q05-representation-check.json passes.', 'Single1-mark exact conversion criterion; grouped/ungrouped equivalent24-bit notation accepted, leading zero requirement follows specified width.'))
R26.append(review('P-SRC005-Q05-b',[
 m('A1.2.2',1,'Calculate representable colour patterns from a fixed total15-bit encoding.','partial','Cardinality of binary encoding assessed, not storage/retrieval trade-off explanation generally.'),
 m('A1.2.2',2,'Combine independent5-bit RGB channel values into image colour count.','partial','Image channel encoding capacity only, no audio/text/video mechanisms.'),
], 'Five bits permit32 values per channel; independent red/green/blue choices yield32×32×32=32768 colours, equivalently2^15.', 'Independent product and total-bit calculation agree; saved representation check passes.', 'One1-mark result criterion matches State. Correct32768 or equivalent power expression accepted.'))
for r,t,e in zip(R26,['explanation','calculation','calculation'],['Outline bandwidth limitation consequence.','Fixed-width hexadecimal-to-binary conversion.','Calculate colour capacity from binary bit allocation.']):r['question_type']=t;r['question_type_review']={'status':'verified','reviewer':'/root/theme_a_coverage','evidence':e}
save_batch(R26,26,'Review P-SRC005-Q07, P-SRC005-Q10-a, P-SRC005-Q10-b; save batch-027.', ['review_batch026.py','checks/P-SRC005-Q05-representation-check.json'])
