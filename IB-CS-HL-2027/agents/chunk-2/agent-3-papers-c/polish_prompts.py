from build_records import *
prompts={
'P-SRC022-Q02':'State the purpose of the MDR while the CPU reads data from main memory.',
'P-SRC022-Q03':'Identify two physical or transmission characteristics of fibre-optic communication.',
'P-SRC022-Q04-a':'State the eight-bit binary representation of hexadecimal B4.',
'P-SRC022-Q04-b':'State the hexadecimal representation of binary 01011110.',
'P-SRC022-Q05-a':'Insert 38, 21, 54, 47, 9 and 30 into an empty BST using smaller values on the left. Sketch the final tree.',
'P-SRC022-Q05-b':'A BST has root 38, left child 21 (with children 9 and 30) and right child 54 (with left child 47). State how many nodes have at least one child.',
'P-SRC022-Q06':'Identify two distinct ways malware can make files on a network unavailable or incorrect.',
'P-SRC022-Q07':'Outline how paging can let an operating system run a process whose virtual address space is larger than the RAM currently available to it.',
'P-SRC022-Q08':'Construct a truth table for Y = (NOT P) OR ((NOT Q) AND R). List all eight input rows in binary order P, Q, R.',
'P-SRC022-Q09':'Describe how a microprocessor controls a freezer alarm using a temperature sensor and a buzzer.',
'P-SRC022-Q10-a':'State what makes a function recursive.',
'P-SRC022-Q10-b-i':'State how many values echo(-3) prints.',
'P-SRC022-Q10-b-ii':'For a positive integer n, state a formula for the total number of print calls made by echo(n).',
'P-SRC022-Q11-a':'Identify three devices that may connect wireless clients to a wired LAN and the internet.',
'P-SRC022-Q11-b':'Outline two benefits of wireless rather than fixed cable connections for handheld scanners used throughout a warehouse.',
'P-SRC022-Q11-c':'Describe two layers that can protect the confidentiality of data crossing a public wireless network.',
'P-SRC022-Q11-d':'Explain how a properly configured remote-access VPN lets a researcher use private laboratory services securely from home.',
'P-SRC022-Q12-c':'Compare local storage and a cloud-storage service for a small design studio in terms of security responsibility, cost and accessibility. Refer to both approaches throughout.',
'P-SRC022-Q13-b':'State why data saved on an SSD can remain available after power is removed.',
'P-SRC022-Q13-c':'Outline two limitations a video archive should consider when compressing files: one associated with lossy compression and one with lossless compression.',
'P-SRC022-Q13-d':'Describe the effect of using eight bits per pixel to encode colour in an image of a smooth sunset.',
'P-SRC022-Q13-e':'A workstation has sufficient CPU and GPU power but frequently pages because RAM is full, and loads files from a slow HDD. Explain two hardware upgrades that address these bottlenecks.',
'P-SRC022-Q14-a':'List three characteristics of a dynamically resizable list compared with a fixed-capacity array.',
'P-SRC022-Q14-b-i':'Describe the reference structure of a nonempty singly circular linked list used for turns in a game.',
'P-SRC022-Q14-b-ii':'State two situations in which repeatedly following a circular linked list can be useful.',
'P-SRC022-Q14-c-i':'Identify two differences between an ordinary stack and an ordinary queue.',
'P-SRC022-Q14-c-ii':'Construct Python function route(stack, early, late). The supplied stack offers isEmpty() and pop(); the two initially empty queues offer enqueue(value). Every name is nonempty and begins with an uppercase letter A–Z. Remove all names from the stack, enqueuing names beginning A–M in early and N–Z in late, in pop order. Use the supplied access methods.',
'P-SRC022-Q15-a':'For matrix [[4,2,0],[1,8,3],[7,0,6]], state its main diagonal entries in order.',
'P-SRC022-Q15-b':'Describe how an algorithm using row index r and column index c can recognize a main-diagonal entry in a square two-dimensional list.',
'P-SRC022-Q15-c':'Construct Python function is_upper(mat). The input is a square list of numeric rows. Return True exactly when every entry whose row index is greater than its column index is zero. Diagonal values are unrestricted. A matrix with no rows may return True.',
'P-SRC022-Q15-d':'Supplied functions is_upper(mat) and is_lower(mat) return whether all entries below and above the main diagonal, respectively, are zero. Construct Python function identify(mat), returning "BOTH", "UPPER", "LOWER" or "NONE" as appropriate. Call both helpers; they are already correct.',
}
# A code-construction question contains its solution separately, not in the student prompt.
show_code={'P-SRC022-Q10-b-i','P-SRC022-Q10-b-ii'}
for f in sorted((O/'batches').glob('SRC-022-*.json')):
 b=json.loads(f.read_text())
 for p in b['practice_questions']:
  if p['question_id'] in prompts:
   p['question_text']=prompts[p['question_id']]+(('\n\n'+p['code']) if p['question_id'] in show_code else '')
 atomic(f,b)
print('Polished',len(prompts),'SRC022 prompts')
