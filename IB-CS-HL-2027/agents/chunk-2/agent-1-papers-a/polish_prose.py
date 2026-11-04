from pathlib import Path
import re,json,functools,collections,math,sys
O=Path(__file__).resolve().parent
words={w.strip().lower() for w in Path('/usr/share/dict/words').read_text().splitlines() if w.strip().isalpha()}
extra='extrema earlier unset workstation workstations bitmap bitmaps largest smallest narrower widest greater less lower higher nonnegative nonempty Python FIFO LIFO CPU GPU RAM ROM SSD SQL HTTPS TLS LAN WLAN OS AI Unicode URL HTTP DNS TCP UDP VPN VLAN GUI ADT UML AND OR NAND NOR NOT XOR XNOR bit bits row rows grid grids dataset datasets max min flag flags src low high bool boolean index indices counter variables breakpoint dictionary mutable immutable initializes initialized initialization traverses traversal reads readings append appends loops returns updates unmarked marked nonempty empty reuses runtime runtimes input output integer integers string strings True False None from to each of in and or all the with without using before after until inside outside other required test tested tests code data'.lower().split()
words.update(extra)
for w in list(words):
 if len(w)>2:
  words.update([w+'s',w+'ed',w+'ing'])
  if w.endswith('e'):words.update([w+'d',w[:-1]+'ing'])
  if w.endswith('y'):words.update([w[:-1]+'ies',w[:-1]+'ied'])
protected=set(extra)|{'min','max','len','range','input','print','int','float','list','set','tuple','dict','abs','sum'}
for path in O.glob('src*.py'):
 protected.update(re.findall(r'def\s+(\w+)',path.read_text()))
protected.update(['isEmpty','isFull','read_number','proper_sum','lower_sum','same','staticmethod'])
corpus=' '.join(p.read_text() for p in (O/'source-text').glob('*.txt'))
corpus+=' '+(O.parents[2]/'sources/2027-guide/text/all-pages.txt').read_text()
freq=collections.Counter(re.findall(r'[A-Za-z]+',corpus.lower()))
for word in 'the and or in of to on for with without each all every before after until if is are as by at be from using into than then only not a'.split():freq[word]+=300
@functools.lru_cache(None)
def split_word(word):
 lower=word.lower()
 if word in protected or lower in words or freq[lower]>0 or '_' in word:return word
 if word[0].isupper() and word[1:].islower():
  result=split_word(lower)
  return result[0].upper()+result[1:]
 # Camel case natural prose is separated only where the lowercase prefix is a whole word.
 m=re.match(r'^([a-z]+)([A-Z][A-Za-z]*)$',word)
 if m and m[1] in words and (m[2].lower() in words or m[2].isupper()):return m[1]+' '+m[2]
 if not word.islower():return word
 n=len(word);dp={0:(0,[])}
 for i in range(n):
  if i not in dp:continue
  for j in range(i+1,n+1):
   w=word[i:j]
   if (w not in words and freq[w]==0) or len(w)==1 and w not in ['a','i']:continue
   weight=freq[w]
   if not weight and w.endswith('s'):weight=freq[w[:-1]]/8
   if not weight and w.endswith('ed'):weight=max(freq[w[:-2]],freq[w[:-1]])/8
   if not weight and w.endswith('ing'):weight=max(freq[w[:-3]],freq[w[:-3]+'e'])/8
   cost=dp[i][0]+math.log(100000/(weight+0.002))
   if j not in dp or cost<dp[j][0]:dp[j]=(cost,dp[i][1]+[w])
 if n in dp and 1<len(dp[n][1])<=10:return ' '.join(dp[n][1])
 return word

def polish(text):
 # Protect executable fenced/code tails and inline underscores; only prose fields supplied.
 lines=[]
 for line in text.splitlines():
  if re.match(r'^\s*(SELECT |CREATE |INSERT |UPDATE |DELETE |def |class |return |if |elif |else:|for |while |assert |import |from |[A-Za-z_][\w.]*\s*[=+])',line):lines.append(line);continue
  # Keep inline code identifiers and CamelCase class/field names intact.
  keep={}
  def protect(m):
   token='ZZTOKEN'+chr(65+len(keep))+'ZZ';keep[token]=m[0];return token
  line=re.sub(r'\b(?:[0-9A-F]*[0-9][A-F0-9]*|[23]D|3NF)\b',protect,line)
  line=re.sub(r'(CPU|GPU|RAM|ROM|SSD|SQL|VPN|FIFO|LIFO)(?=[a-z])',r'\1 ',line)
  line=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])',' ',line)
  line=re.sub(r'\b[A-Za-z]+\b',lambda m:split_word(m[0]),line)
  line=re.sub(r',(?=[A-Za-z])',', ',line)
  line=re.sub(r';(?=[A-Za-z])','; ',line)
  for token,value in keep.items():line=line.replace(token,value)
  line=line.replace('A4×4','A 4×4').replace('A4×4','A 4×4')
  line=line.replace('andis Empty','and isEmpty').replace('theLIFOend','the LIFO end').replace('NOTP','NOT P').replace('NOTR','NOT R').replace('ANDoutput','AND output').replace('toproduceOUT','to produce OUT')
  lines.append(line)
 return '\n'.join(lines)
fields={'question_text','solution','adaptation_rationale','partial_credit_notes','common_errors','acceptable_alternatives','criterion'}
changes=[]
def walk(value,key=''):
 if isinstance(value,dict):return {k:walk(v,k) for k,v in value.items()}
 if isinstance(value,list):return [walk(v,key) for v in value]
 if isinstance(value,str) and key in fields:
  new=polish(value)
  if new!=value:changes.append({'old':value,'new':new})
  return new
 return value
for path in sorted((O/'batches').glob('*.json')):
 if sys.argv[1:] and not any(path.name.startswith(sid) for sid in sys.argv[1:]):continue
 b=json.loads(path.read_text())
 b['practice_questions']=walk(b['practice_questions'])
 path.write_text(json.dumps(b,ensure_ascii=False,indent=2))
(O/'checks/prose_spacing_changes.json').write_text(json.dumps(changes,indent=2))
print('Prose fields corrected:',len(changes))
for w in ['togetherwith','inPython','negativevaluesandtiesarepossible','initializes','everyrow','allremainingitems','loopsthrough','highest','foreach']:print(w,'=>',polish(w))
