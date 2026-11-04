from build_records import *
from functools import lru_cache
import math
freq=collections.Counter()
for f in (O/'source-text').glob('*-compact.txt'):freq.update(re.findall(r'\b[a-z]+\b',f.read_text().lower()))
for r in S.values():freq.update(re.findall(r'\b[a-z]+\b',r['statement'].lower()+' '+r['guidance'].lower()))
lex=set(Path('/usr/share/dict/words').read_text().lower().splitlines())|set(freq)
lex|={w+suffix for w in list(lex) if len(w)>2 for suffix in ['s','ed','ing','ly']}
lex|={w[:-1]+suffix for w in list(lex) if w.endswith('e') for suffix in ['ed','ing']};lex|={'none','lifo','fifo','bst','ram','cpu','gpu','hdd','ssd','vpn','sql','true','false','nonempty','runtime','timevariant','reallocation','initialization','enqueues','dequeues','reconstructs'}
manual={'Comparerandc':'Compare r and c','Mcorrectly':'M correctly','Oandremainingpageaccess':'O and remaining page access','Recalculatesintegermidpoint':'Recalculates integer midpoint','Correctinitialinclusivebounds':'Correct initial inclusive bounds','Correctnotfoundreturnaftertermination':'Correct not-found return after termination','Loopwhileintervalnonempty':'Loop while interval is nonempty','Correctequalitycomparison':'Correct equality comparison','andmatchingparallelscore':'and matching parallel score','middlenamebelowtarget':'middle name below target','middlenameabovetarget':'middle name above target'}
@lru_cache(None)
def segment(token):
 low=token.lower()
 if low in lex:return token
 n=len(low);dp=[None]*(n+1);dp[0]=(0,[])
 for end in range(1,n+1):
  for start in range(max(0,end-30),end):
   if dp[start] is None:continue
   w=low[start:end]
   if w not in lex and len(w)>1:continue
   if len(w)==1 and w not in 'ai':continue
   cost=5+1/(freq[w]+1)+(5 if len(w)==1 else 0)
   v=(dp[start][0]+cost,dp[start][1]+[token[start:end]])
   if dp[end] is None or v[0]<dp[end][0]:dp[end]=v
 if dp[n] is None:return token
 return ' '.join(dp[n][1])
changes={}
def clean(s):
 if not isinstance(s,str):return s
 if s.lstrip().startswith(('def ','class ','SELECT ')):return s
 # Source code included after a blank line in trace prompts is left byte-for-byte unchanged.
 prose,sep,code=s.partition('\n\n')
 def word(m):
  t=m[0];new=manual.get(t,segment(t) if len(t)>14 else t)
  if new!=t:changes[t]=new
  return new
 prose=re.sub(r'\b[A-Za-z]{7,}\b',word,prose)
 prose=re.sub(r',(?=[A-Za-z])',', ',prose)
 prose=re.sub(r'\b(Construct|State|Identify|Describe|of|for|to|with|in|from|than|least|exactly|through)(?=\d)',r'\1 ',prose)
 return prose+sep+code
for f in sorted((O/'batches').glob('*.json')):
 b=json.loads(f.read_text())
 for p in b['practice_questions']:
  for k in ['question_text','solution','adaptation_rationale','partial_credit_notes']:
   p[k]=clean(p[k])
  for m in p['marking_points']:m['criterion']=clean(m['criterion'])
  for k in ['acceptable_alternatives','common_errors']:p[k]=[clean(s) for s in p.get(k,[])]
  # Command metadata follows adapted wording,while source record preserves original command.
  match=re.search(r'\b(State|Identify|Outline|Explain|Construct|Sketch|Describe|Compare|Calculate|Trace|Distinguish|Discuss|Evaluate)\b',p['question_text'])
  if match:p['command_term']=match[1]
 atomic(f,b)
atomic(O/'spacing_repair_audit.json',changes)
print('\n'.join(k+' -> '+v for k,v in changes.items()))
