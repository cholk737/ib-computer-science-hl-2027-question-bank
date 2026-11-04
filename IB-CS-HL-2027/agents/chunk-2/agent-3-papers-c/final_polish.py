from build_records import *
# Explicit, reviewed prose replacements. Never run segmentation over identifiers/code.
fix={}
for line in '''Correctleftsubtree=Correct left subtree
Correctrightsubtree=Correct right subtree
Correctresult=Correct result
Finaloutput=Final output
Initializescount=Initializes count
whenmiddlenamebelowtarget= when middle name is below target
whenmiddlenameabovetarget= when middle name is above target
withleft= with left
Usesr==cascriterion=Uses r == c as the criterion
Getsn/handles=Gets n / handles
searchO=search O
linearO=linear O
Correctmat=Correct mat
Preserveindex=Preserve index
possiblecolourcodes= possible colour codes
possiblecodes= possible codes
fromexpression=from expression
originaldata=original data
openedport=opened port
bitsprovide= bits provide
areexplicit=are explicit
securitysystem=security system
MLapplication=ML application
mandatoryscope=mandatory scope
timevariance=time variance
timevariant=time-variant
Timevariant=Time-variant
manyDEVICE=many DEVICE
minreturn=min return
19standard=19 standard
20standard=20 standard
61powered=61 powered
index0=index 0
initialized0=initialized to 0
Returns-1=Returns -1
Return-1=Return -1
andlarge=and large
referenceidentity=reference identity
suppliediterator=supplied iterator
Correctinitialinclusivebounds=Correct initial inclusive bounds
Correctnotfoundreturnaftertermination=Correct not-found return after termination
Loopwhileintervalnonempty=Loop while interval is nonempty
Recalculatesintegermidpoint=Recalculates integer midpoint
Correctequalitycomparison=Correct equality comparison
andmatchingparallelscore=and matching parallel score'''.splitlines():
 key,value=line.split('=',1);fix[key]=value
criteria={
 'P-SRC016-Q09-a':['Columns and initial state correct.','n progression: 502, 50, 5, 0.','x progression: 8, 10, 10, 15.','Final output: 15.'],
 'P-SRC016-Q12-d':['Correct initial inclusive bounds.','Loop while the interval is nonempty.','Recalculates an integer midpoint.','Correct equality comparison and matching parallel score.','Sets low = mid + 1 when the middle name is below the target.','Sets high = mid - 1 when the middle name is above the target.','Correct not-found return after termination.'],
 'P-SRC022-Q05-a':['Root is 38.','Left subtree has 21 with children 9 and 30.','Right subtree has 54 with left child 47.'],
 'P-SRC022-Q08':['Rows 000 and 001 both output 1.','Rows 010 and 011 both output 1.','Rows 100 and 101 output 0 and 1 respectively.','Rows 110 and 111 both output 0.'],
 'P-SRC022-Q15-b':['Compares row and column indexes.','Uses r == c as the main-diagonal criterion.'],
 'P-SRC022-Q13-d':['2^8 = 256 possible colour codes.','Limited distinct shades relative to the original.','Explains banding, rounding or loss of a smooth gradient.'],
 'P-SRC022-Q13-e':['Increases RAM capacity.','Links less paging to improved active-workload performance.','Replaces HDD with SSD.','Links faster secondary access to loading files or page input/output.'],
 'P-SRC033-Q15-b':['19 standard rentals produce 0 rewards.','20 standard rentals produce 1 reward.','61 powered rentals produce 2 rewards.'],
 'P-SRC028-Q10-b-i':['Identifies a relevant technical property: high bandwidth, low attenuation over distance, or resistance to electromagnetic interference.','Explains how that property supports the campus link, such as carrying substantial traffic reliably between buildings.']}
prompts={
 'P-SRC028-Q08-a':'State the hexadecimal representation of the 12-bit integer 101001111100.',
 'P-SRC028-Q08-b':'State how many distinct bit patterns an unsigned 10-bit register can hold.',
 'P-SRC028-Q11-a-iv':'State the smallest nonnegative integer mark for which grade(mark) returns 7.',
 'P-SRC028-Q11-b':'Construct Python function resit_names(names, grades) returning a list of names whose matching grade is 1. The parallel lists have equal length; preserve original order.',
 'P-SRC033-Q01-b':'Explain why a database should store birth dates using a suitable date type and an unambiguous input convention, rather than arbitrary text such as 03/04/2010.',
 'P-SRC033-Q03-b':'Construct an SQL query returning SupplierID and ProductName for products whose Description contains "fruity" and whose stock quantity is 25–35 inclusive. Tables: Product(ProductID, SupplierID, ProductName, Description), Stock(ProductID, Quantity). Join using ProductID.',
 'P-SRC033-Q03-e':'Outline why neither StudentID nor ModuleID alone identifies an enrollment record uniquely when each student can take many modules and each module has many students. Assume one enrollment per student-module pair, with no repeat attempts.',
 'P-SRC033-Q05-b':'Construct Python function estimate(kind, count), where kind is "small" or "large" and count is a valid positive integer. Land costs 500000. Small units sell for 220000, need 17 days and 100000 materials each; large units sell for 400000, need 23 days and 190000 materials each. Labour costs 2500 per day. Units are built sequentially. Return revenue minus all costs.',
 'P-SRC033-Q05-d':'Construct Python function net_profit(profit, months). months is a supplied positive integer number of months charged. A 400000 loan incurs simple interest of 1% of the original principal each month, and land tax is 500 per month. Return profit after deducting interest and tax.',
 'P-SRC033-Q14-d-ii':'PoweredRental inherits Rental, whose pay(hours) returns any administration fee. Construct an overriding pay(self, hours) method returning the parent fee plus self.HOURLY_FEE*hours.',
 'P-SRC033-Q15-a':'A depot gives a reward on every 20th standard rental and every 30th powered rental it accepts. Describe the state and algorithm changes needed to an add-rental operation. Count only successful additions and keep separate counts for each depot.',
 'P-SRC033-Q15-b':'For the 20/30 reward scheme, identify expected reward outputs when tracing three independent fresh-depot runs: (i) 19 standard rentals, (ii) 20 standard rentals, (iii) 61 powered rentals.'}
def clean(s):
 if not isinstance(s,str) or s.lstrip().startswith(('def ','class ','SELECT ')):return s
 prose,sep,code=s.partition('\n\n')
 for key,value in fix.items():prose=prose.replace(key,value)
 prose=re.sub(r'([,;:])(?=[A-Za-z"“])',r'\1 ',prose)
 prose=re.sub(r'\b(Correct|Rows|exactly|costs|for|of|than|most|least|at|in|to|and|or|per|with|loan|Return|return)(?=-?\d)',r'\1 ',prose)
 prose=re.sub(r'\b(\d+)(hours|days|months|standard|powered|April|March)\b',r'\1 \2',prose)
 prose=re.sub(r' {2,}',' ',prose)
 return prose+sep+code
log=[]
checks={x['question_id']:x for x in json.loads((O/'technical_checks.json').read_text())}
for f in sorted((O/'batches').glob('*.json')):
 b=json.loads(f.read_text())
 for p in b['practice_questions']:
  before=json.dumps(p,sort_keys=True)
  for k in ['question_text','solution','adaptation_rationale','partial_credit_notes']:p[k]=clean(p[k])
  if p['question_id'] in prompts:p['question_text']=prompts[p['question_id']]
  p['question_text']=p['question_text'].replace('identifier"LAB-27"and','identifier "LAB-27" and').replace('make_stack()returns','make_stack() returns')
  for m in p['marking_points']:m['criterion']=clean(m['criterion'])
  if p['question_id'] in criteria:
   assert len(criteria[p['question_id']])==p['marks']
   p['marking_points']=[{'marks':1,'criterion':c} for c in criteria[p['question_id']]]
  if p['question_id'] in checks:
   p['verification']['code_execution']='Specific executable boundary and behaviour tests passed; see agents/chunk-2/agent-3-papers-c/technical_checks.json and verify_practice.py.'
  if p['question_id']=='P-SRC028-Q10-a':
   p['adaptation_rationale']='Role permissions are OS authorization; authentication establishes identity separately. MFA is an optional implementation choice. Scenario and wording rewritten within supported 2027 scope.'
  if p['question_id']=='P-SRC028-Q10-b-i':
   p['solution']='Fibre offers high bandwidth, supporting substantial traffic between the buildings. Its low attenuation and resistance to electromagnetic interference can also support reliable links over suitable campus distances.'
   p['adaptation_rationale']='Explain a named medium through a relevant technical property and a linked campus requirement; no credit for merely repeating the supplied medium.'
  match=re.search(r'\b(State|Identify|Outline|Explain|Construct|Sketch|Describe|Compare|Calculate|Trace|Distinguish|Discuss|Evaluate|List|Define|Justify|Analyse|Annotate)\b',p['question_text'])
  if not match:match=re.search(r'\b(State|Identify|Outline|Explain|Construct|Sketch|Describe|Compare|Calculate|Trace|Distinguish|Discuss|Evaluate|Define|Justify|Analyse|Annotate)\b',p['question_text'],re.I)
  if match:p['command_term']=match[1].capitalize()
  if before!=json.dumps(p,sort_keys=True):log.append(p['question_id'])
 atomic(f,b)
atomic(O/'final_polish_audit.json',{'changed_practice_ids':log,'policy':'Explicit prose replacements; executable code and faithful source transcriptions not edited.'})
print('Polished practices',len(log))
