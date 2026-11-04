from build_shard import *
E=[]
def add(key,codes,prompt,answer,criteria,ms,**kw):E.append(dict(key=key,codes=codes,prompt=prompt,answer=answer,criteria=criteria,ms=ms,concept=kw.pop('concept',prompt.split('.')[0]),**kw))
def exclude(key,ms,reason):E.append(dict(key=key,codes=[],status='C',ms=ms,exclude=reason,concept=reason))
exclude('1',[4],'Application user-interface features are not explicitly prescribed by an individual2027 statement; OS GUI function is a different objective.')
add('2:a',['A1.1.7'],'Outline the purpose of an external SSD used to store a photographer’s completed work.','It retains the image files after power is removed so they can be retrieved later or transported to another computer.',[(1,'Persistent/nonvolatile file storage.'),(1,'Later retrieval/portability in context.')],[4])
exclude('2:b',[5],'Virtual memory/paging as an extension of primary memory is not explicitly required by2027 detailed guidance.')
add('3',['A1.1.2','A1.1.4'],'Outline how adding RAM and using a suitable GPU can improve a workstation that trains large image models.','More RAM holds more of the working data available for CPU processing. A GPU can carry out many similar numerical operations in parallel, helping model calculations.',[(1,'RAM increase.'),(1,'Larger working data capacity relevant to processing.'),(1,'GPU parallel computational architecture.'),(1,'Links repeated numerical/model operations to its benefit.')],[5],status='B',adapt='Narrows generic hardware-upgrade responses to explicit primary-memory and GPU roles; no unsupported peripheral specification.')
exclude('4',[6],'Survey methods for gathering user requirements are outside the2027 individual-statement scope.')
add('5',['A1.2.4'],'Construct the truth table for X = (NOT A) OR (B AND C) OR (NOT B). Use row order000 through111 for A,B,C.','1,1,1,1,1,1,0,1.',[(1,'Rows000/001 both1.'),(1,'Rows010/011 both1.'),(1,'Rows100/101 both1.'),(1,'Rows110→0 and111→1.')],[6],check='Enumerated all8 combinations with correct precedence.',test_code='assert [int((not a) or (b and c) or (not b)) for a in [0,1] for b in [0,1] for c in [0,1]]==[1,1,1,1,1,1,0,1]')
exclude('6',[6],'System implementation/changeover methods are obsolete for individual2027 syllabus mapping.')
add('7',['A2.2.2'],'Describe the role of a DNS server when a user accesses a service using a hostname.','It resolves the hostname to an associated IP address, enabling the client to address requests to the relevant host. It may answer from cached records or obtain the information through DNS queries.',[(1,'Hostname/domain→IP resolution.'),(1,'Enables addressed connection or valid resolution detail.')],[7])
add('8',['A2.1.1','A2.4.3'],'Explain why a project team may provide a VPN endpoint for staff connecting from home to internal resources.','An authenticated VPN establishes a protected tunnel to the office network. Encryption reduces disclosure of traffic over the public path, while the endpoint can restrict access to authorized resources.',[(1,'Contextual remote internal-resource access.'),(1,'Encrypted tunnel/appropriate VPN feature.'),(1,'Explains confidentiality or authenticated access benefit.')],[8],source_issues=['Original MS includes overly broad anonymity/interception claims; adaptation limits protection to the tunnel path.'])
exclude('9:a-i',[9],'CAD product definition is not a2027 individual learning requirement.')
exclude('9:a-ii',[9],'Benefits/features of CAD software are not an explicit2027 objective.')
add('9:b',['A1.1.8'],'Explain why a surveyor may compress a large set of image files before archiving and sending them.','Compression reduces their encoded size, allowing more files in the same storage capacity. At the same network bit rate, fewer bits require less transmission time.',[(1,'Reduced encoded file size.'),(1,'Less storage used.'),(1,'Reduced transfer time at fixed bit rate.')],[10])
exclude('9:c-i',[11],'General disaster recovery/backup or disk-failure downtime management is not an individual2027 requirement; no case-study mapping fabricated.')
add('9:c-ii',['A2.4.2'],'Outline how each of ransomware and phishing can lead to a business losing access to its confidential data.','Ransomware encrypts files so authorized users cannot read them without recovery/decryption. Phishing can steal a valid login and let an attacker delete, encrypt or exfiltrate data.',[(1,'Ransomware encrypts/locks files.'),(1,'Explains loss of legitimate access.'),(1,'Phishing tricks user into disclosure/action.'),(1,'Explains attacker access and resulting data loss.')],[11],status='B',adapt='Narrows generic data-loss causes to threats explicitly included in2027 network-vulnerability guidance.')
add('10:a',['A1.3.2'],'A shared server has administrators, analysts and visitors. Explain how OS account and file-permission controls can give these groups different access.','Authenticate each user to an account. Assign accounts to role groups. Grant administrators management rights, analysts read/write access only to their project files, and visitors no access to confidential files. The OS checks permissions on file operations, applying least privilege rather than granting every login full access.',[(1,'Authenticated user identities.'),(1,'Role/group membership.'),(1,'Appropriate administrator rights.'),(1,'Restricted analyst project rights.'),(1,'Visitors denied sensitive files.'),(1,'OS permission enforcement/least-privilege reasoning.')],[12,13],status='B')
add('10:b-i',['A2.3.2'],'Suggest a wired medium for a high-bandwidth inter-building campus link and justify the choice.','Fibre optic cable: high bandwidth and resistance to electromagnetic interference suit a long inter-building connection.',[(1,'Fibre optic cable.'),(1,'Appropriate contextual bandwidth/range/interference justification.')],[14],status='B',new_command='Suggest')
add('10:b-ii',['A2.4.1','A2.4.3'],'Suggest two network-security measures for a college LAN and explain how each reduces a threat.','A firewall rejects connections that violate access rules. Regular software patching removes known vulnerabilities that attackers might exploit.',[(1,'Firewall.'),(1,'Explains rule-based filtering threat reduction.'),(1,'Patching/updating.'),(1,'Explains fixing known vulnerabilities.')],[14,15],new_command='Suggest')
add('10:c',['A2.4.2'],'List three security threats that users may encounter through organizational email.','Phishing; malware in attachments/links; account compromise due to weak authentication.',[(1,'Phishing.'),(1,'Malware.'),(1,'Weak-authentication/account-compromise threat.')],[15],status='B',new_command='List')
add('11:a-i',['A1.3.6'],'Describe an embedded controller in an automatic door system.','A processor-based component within the door system reads sensors and runs a specific control algorithm to operate the door actuator.',[(1,'Processor/controller inside larger device.'),(1,'Specific sensor-processing-actuator control task.')],[15],status='B')
add('11:a-ii',['A1.3.7'],'State two everyday applications of computer control systems other than traffic signals.','A thermostat regulating heating; an automatic washing machine.',[(1,'One appropriate control application.'),(1,'Second distinct application.')],[15],status='B')
add('11:b',['A2.1.2'],'Discuss replacing independent junction controllers with one networked central traffic controller.','A central system can coordinate signals to reduce queues across several junctions and simplify updates. However, the central computer or its communication links become critical failure points; loss of communication may disrupt many junctions. Local fallback control can reduce the risk while retaining coordination benefits.',[(1,'Central coordination advantage.'),(1,'Develops effect on traffic/management.'),(1,'Failure/dependence drawback.'),(1,'Develops limitation or balanced mitigation.')],[16],status='B')
add('11:c',['A1.3.6'],'List two sensors that could provide input when counting vehicles at a junction.','An inductive-loop sensor and an infrared beam sensor.',[(1,'One appropriate vehicle-detection sensor.'),(1,'Second distinct appropriate sensor.')],[16],status='B',new_command='List')
add('11:d',['A1.3.4'],'Describe one difference between interrupt-driven input and polling in a control system.','With interrupts, the device signals when it needs attention; with polling, the processor repeatedly checks device status even when no event has occurred.',[(1,'Event/device signals in interrupt approach.'),(1,'Processor actively/repeatedly checks in polling.')],[17],source_issues=['Original MS treats polling as having no priority and interrupts as hardware-only; these are not universal and not repeated.'])
exclude('11:e',[18],'Generic benefits of real-time traffic information to drivers do not assess a specific2027 individual statement without changing the objective.')
c='''def balance(n):
    if n <= 0:
        return 0
    previous = balance(n - 1)
    if n % 2 == 0:
        return previous - n
    return previous + n'''
add('12:a',['B2.4.5'],'Trace balance(6), showing the returned value for each n from0 through6.\n'+c,'Values for n=0,1,2,3,4,5,6 are0,1,-1,2,-2,3,-3. Therefore balance(6)=-3.',[(1,'Base value0.'),(1,'n1→1,n2→-1.'),(1,'n3→2,n4→-2.'),(1,'n5→3.'),(1,'n6→-3 and correct final result.')],[19],status='B',new_command='Trace',code=c,ms_summary='Original recfn(5) returns3 with alternating +odd/-even unwind.',check='Executed all n0..6; each path has only one recursive call.',test_code=c+'\nassert [balance(i) for i in range(7)]==[0,1,-1,2,-2,3,-3]')
add('12:b',['B2.2.3'],'Describe push and peek for a stack.','push adds a new item at the top. peek returns the top item without removing it.',[(1,'push named.'),(1,'Adds at top.'),(1,'peek named.'),(1,'Returns top without removal.')],[19])
c2='''def retain_extremes(stack):
    first = stack.pop()
    smallest = largest = first
    while not stack.isEmpty():
        value = stack.pop()
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value
    stack.push(largest)
    stack.push(smallest)'''
add('12:c',['B2.2.3','B2.3.2','B2.3.3'],'Construct retain_extremes(stack) in Python for a nonempty numeric stack. Replace its contents with exactly two entries: maximum at the bottom and minimum at the top. If all values are equal, store that value twice. Use only pop,push,isEmpty to access the stack.','One solution:\n'+c2,[(1,'Initialize both extremes from a valid item.'),(1,'Loop until original stack empty.'),(1,'Pop each remaining item.'),(1,'Update minimum correctly.'),(1,'Update maximum correctly.'),(1,'Push maximum then minimum, including equal extremes.')],[20],status='B',new_command='Construct',code=c2,check='Executed mixed negative/positive,all-negative,singleton,equal-value cases with stack harness.',test_code=c2+'''\nclass S:
 def __init__(self,v):self.v=v[:]
 def pop(self):return self.v.pop()
 def push(self,x):self.v.append(x)
 def isEmpty(self):return not self.v
for original in [[2,-7,5],[-8,-3], [4], [6,6]]:
 s=S(original);retain_extremes(s);assert s.v==[max(original),min(original)]''',assets=[dict(kind='source_stack_diagram',description='Original numeric stack23,-54.9,-12.4,67,15.2 and desired extrema order',path='agents/chunk-2/agent-2-papers-b/papers/SRC-026/renders/page-06.png',source_pdf_page=6,visually_verified=True)])
add('13:a',['B2.3.4'],'List three benefits of dividing a quiz program into functions with clear inputs and outputs.','Reuse of validation logic; independent debugging/testing; localized maintenance of one task.',[(1,'Reuse.'),(1,'Independent debugging/testing.'),(1,'Maintainability/modularity or another distinct supported benefit.')],[21],new_command='List')
c3='''def read_in_range(read_integer):
    while True:
        value = read_integer()
        if 1 <= value <= 16:
            print("Accepted")
            return value
        print("Enter an integer from 1 to 16")'''
add('13:b',['B2.3.2','B2.3.3','B2.3.4'],'Construct read_in_range(read_integer) in Python. Calling read_integer() returns an integer entered by the user. Repeatedly request a value until it lies from1 to16 inclusive; print an appropriate rejection or acceptance message and return the valid value.','One solution:\n'+c3,[(1,'Repeated input loop.'),(1,'Correct inclusive range test.'),(1,'Reject/retry invalid entries with message.'),(1,'Accept and return valid entry.')],[21,22],status='B',new_command='Construct',code=c3,context_pages=[7,8],check='Executed invalid low/high thenvalid and boundary1/16 inputs.',test_code=c3+'\nimport io,contextlib\nfor values in [[0,17,9],[1],[16]]:\n it=iter(values)\n with contextlib.redirect_stdout(io.StringIO()):assert read_in_range(lambda:next(it))==values[-1]')
c4='''def correctly_completed(grid):
    flags = [False] * 16
    for row in grid:
        for value in row:
            flags[value - 1] = True
    for flag in flags:
        if not flag:
            return False
    return True'''
add('13:c',['B2.2.2','B2.3.2','B2.3.3'],'A4×4 grid contains16 integer entries, each from1 to16. Construct correctly_completed(grid) in Python to return True exactly when every integer1 to16 occurs once. Use a16-element flags list initialized False, mark each encountered value at index value-1, then inspect all flags.','One solution:\n'+c4+'\nSince there are exactly16 entries, seeing all16 possible values implies there are no duplicates.',[(1,'Allocates16 flags.'),(1,'Initializes every flag False.'),(1,'Traverses every row.'),(1,'Traverses every value.'),(1,'Maps value to value-1.'),(1,'Marks encountered index True.'),(1,'Detects any unmarked flag.'),(1,'Returns True only when all required values occur.')],[23,24,25,26],status='B',new_command='Construct',code=c4,context_pages=[7,8,9,10],check='Executed permutation,duplicate/missing value cases; correctness relies on stated16 entries/range.',test_code=c4+'\ng=[list(range(1+4*r,5+4*r)) for r in range(4)]\nassert correctly_completed(g)\nb=[row[:] for row in g];b[3][3]=1\nassert not correctly_completed(b)',source_issues=['Source description omits explicit value-to-zero-based-index subtraction; MS correctly uses value-1. Adapted prompt makes it explicit.'],assets=[dict(kind='source_matrices',description='Original valid/duplicate5x5 matrices',path='agents/chunk-2/agent-2-papers-b/papers/SRC-026/renders/page-09.png',source_pdf_page=9,visually_verified=True),dict(kind='source_flags',description='Original flags indices0..24; missing17 corresponds index16',path='agents/chunk-2/agent-2-papers-b/papers/SRC-026/renders/page-10.png',source_pdf_page=10,visually_verified=True)])
for e in E:
 if e['key']=='9:c-i':e.update(status='B',codes=['A2.1.2'],exclude='',reuse_practice_id='P-SRC028-Q09-c-i',rationale='Coordinator resolution: broad backup/downtime management is not direct2027 scope. Only explicit cloud-infrastructure purpose/benefit is retained in referenced adaptation P-SRC028-Q09-c-i.')
if __name__=='__main__':
 for e in E:
  if e.get('test_code'):exec(e['test_code'],{})
 finish('SRC-026',E)
