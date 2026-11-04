from checkpoint_reviews import *
R13=[]
R13.append(review('P-SRC002-Q04-e',[
 m('A3.4.3',1,'Describe anomaly detection against a baseline to flag unusual changes.','partial','Only anomaly detection among six required mining techniques; no credit for classification/clustering/regression/association/sequential patterns.'),
 m('A3.4.3',2,'Interpret unusual change records as investigation leads rather than proof of infringement.','direct','Scenario requires interpreting information extracted from data and limits of what the flag establishes.'),
], 'Anomaly detection flags departures from an expected pattern; difference from baseline does not establish legal ownership/copying. No specific law needed.', 'Compare with normal patterns and flag departures for review accurately answers Describe2 with explicit inferential limit.', 'Two1-mark criteria total2 and combine method with appropriate interpretation; no marks for claiming deviation proves misconduct.'))
R13.append(review('P-SRC002-Q04-f',[
 m('A4.3.2',1,'Compare labelled supervised category prediction with unsupervised discovery.','partial','General labelled classification properties tested, not K-NN/decision-tree operation. No algorithm-specific coverage inferred.'),
 m('A4.3.4',1,'Explain clustering by feature similarity without target labels and contrast outputs with predefined classes.','direct','Clustering mechanism and interpretation explicitly assessed in support-request context; no need to force purchasing example.'),
], 'Classification targets predefined labels from supervised examples; clustering groups similar feature vectors without supplied target categories. Both can analyze the same request features for different goals.', 'One similarity plus label/training/output distinctions and cluster interpretation provides appropriate Compare5 depth.', 'Five1-mark points total5 cover similarity and meaningful paired distinctions; clustering without labels does not mean no features or no human interpretation.'))
R13.append(review('P-SRC002-Q07-c',[
 m('A1.1.2',1,'Explain GPU parallel computation suitability for a large numerical simulation.','direct','Numerous similar numerical operations can run in parallel; prompt does not assert every simulation is parallelizable.'),
 m('A1.1.2',2,'Apply GPU architecture to a large-simulation real-world workload.','direct','Large simulation is a listed may-include example; evidence is assessed parallel workload, not example-name mention alone.'),
 m('A1.1.4',1,'Outline RAM capacity holding a large model working state.','partial','RAM purpose/capacity only; no ROM/cache levels/register purposes or cache hits/misses.'),
], 'RAM stores actively used simulation state; a suitable GPU accelerates parallel numerical calculations. Working-set capacity and compute throughput are distinct requirements.', 'Two developed roles (RAM state/model size and GPU parallel workload) appropriately answer Outline4.', 'Four1-mark criteria total4 with two role+context pairs; no ban on CPU participation or guarantee GPU always faster.'))
save_batch(R13,13,'Review P-SRC002-Q07-e, P-SRC002-Q08-a, P-SRC002-Q08-b-i; save batch-014.', ['review_batch013.py'])
