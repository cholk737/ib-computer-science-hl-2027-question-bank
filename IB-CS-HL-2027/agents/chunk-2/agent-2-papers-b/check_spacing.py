from pathlib import Path
import re,json,functools
O=Path(__file__).resolve().parent
vocab={w.strip().lower() for w in Path('/usr/share/dict/words').read_text().splitlines() if len(w.strip())>=2}
vocab.update('calls returns initializes traverses filters updates compares appends handles detects allocates chooses preserves excludes rows arrays lists inputs outputs objects slots indices values instances attributes loops getters setters helpers counts bounds fields operands criteria registers bitmaps datagrams lookups endpoints pointers parameters datatypes local global args kwargs none true false'.split())
@functools.lru_cache(None)
def split(w):
 if w in vocab:return [w]
 candidates=[]
 for i in range(2,len(w)-1):
  if w[:i] in vocab:
   tail=split(w[i:])
   if tail:candidates.append([w[:i]]+tail)
 return min(candidates,key=lambda x:(len(x),sum(1 for p in x if len(p)==2))) if candidates else None
changes={}
for f in (O/'batches').glob('*.json'):
 for p in json.loads(f.read_text())['practice_questions']:
  for c in p['marking_points']:
   for token in re.findall('[A-Za-z]{7,}',c['criterion']):
    if '_' in token or token.lower() in vocab:continue
    a=split(token.lower())
    if a and len(a)>1:
     text=' '.join(a);text=text[0].upper()+text[1:] if token[0].isupper() else text
     changes[token]=text
print(json.dumps(changes,indent=2))
(O/'word_spacing_proposals.json').write_text(json.dumps(changes,indent=2))
