from paper032 import *
exclude('9:a',[17],'URL definition is not an explicit2027 individual requirement.')
add('9:b',['A2.2.2'],'Describe how DNS helps a client contact a named internet service.','The client requests the IP address associated with the hostname. DNS can answer using a cached record or resolve it through other DNS servers. The client then uses the returned address to contact the host.',[(1,'Requests/resolves hostname toIP.'),(1,'Cache/other DNS resolution detail.'),(1,'Client uses returned IP tocontact host.')],[17],source_issues=['Source MS says web addresses are resolved inTCP and that a resolvedURL is returned; DNS returns relevant resource records,not aTCP URL transformation.'])
add('9:c',['A2.1.4','A2.4.4'],'Identify two security properties provided by a correctly configured HTTPS connection.','Confidentiality of transmitted content and integrity protection; server authentication through certificates is another valid property.',[(1,'One correct HTTPS security property.'),(1,'Second distinct property.')],[17])
exclude('9:d',[17],'Standards-versus-protocol taxonomy is not itself an individual2027 requirement.')
add('9:e',['A2.1.4'],'Outline what connectionless means for UDP transport.','The sender can send datagrams without first establishing a transport connection/handshake. Each datagram is handled independently rather than as part of a guaranteed reliable ordered stream.',[(1,'No connection-establishment handshake.'),(1,'Independent datagrams/no guaranteed reliable ordered stream.')],[17],status='B',adapt='Retains connectionless communication concept using UDP,an explicitly named2027 transport protocol,in place of unrestrictedIP taxonomy.')
add('10:a-i',['A3.3.3'],'Describe the effect of INSERT INTO Guest(FirstName,Surname,Email) VALUES(\'Mina\',\'Rao\',\'mina@example.org\'); on a suitable SQL table.','It creates one new row in Guest,assigning the supplied values to the named columns. Existing rows remain unless a constraint error prevents the insertion.',[(1,'Inserts a new row.'),(1,'Correct table/column value association.'),(1,'Explains successful insertion/constraint qualification without claiming an update to allrows.')],[18],status='B',adapt='Retains SQL insertion semantics; obsoletePHP/CGI execution mechanics excluded.')
for key in ['10:a-ii','10:b-i','10:b-ii','10:c','10:d']:exclude(key,[18] if key!='10:d' else [19],'CGI,search-engine optimization,indexing and deep-web access are obsolete2027 option content.')
add('11:a',['A2.2.3'],'Identify two characteristics of a peer-to-peer networking model.','A peer can both request and supply resources; peers communicate/share directly without a mandatory central server for every resource interaction.',[(1,'Peers can act asclients andservers.'),(1,'Direct sharing/decentralized resource provision.')],[20])
add('11:b',['A1.1.8'],'Evaluate using lossy compression for a music preview and for the exact text of a digital contract.','For a preview,removing some perceptually less important audio data can reduce size and transfer time,though high compression may produce audible artifacts. Contract text must remain exact; irreversible loss could alter wording,so lossless compression is appropriate. The choice depends on tolerable loss,not simply which file is larger.',[(1,'Reduced audio size/time benefit.'),(1,'Audio quality/artifact tradeoff.'),(1,'Text requires exact reconstruction.'),(1,'Loss could change legally/semantically important wording.'),(1,'Justified lossyaudio versuslosslesstext choice.'),(1,'Balanced quality/size conclusion.')],[20],status='B',source_issues=['Original eBook discussion focuses on image quality; rewritten task explicitly distinguishes exact text fromaudio.'])
add('11:c',['A1.1.9'],'Identify two characteristics of using a cloud-hosted software service rather than installing it solely on a local computer.','The provider hosts/runs the application on remote infrastructure; users access it over a network,with provider-managed resource availability and potential scaling.',[(1,'Remote provider-hosted application.'),(1,'Network access/provider management/scalability characteristic.')],[20],status='B')
exclude('11:d',[21],'Browser save-menu scripting and websitecopyright protection mechanics are not explicit2027 scope; no generic ethics label used to import obsolete technical details.')
for key in ['12:a-i','12:a-ii','12:b','12:c','12:d','12:e','12:f']:exclude(key,[22] if key not in ['12:e','12:f'] else [23],'Web-bowtie graph topology,strong connectivity,collective intelligence and semantic-web ontologies/folksonomies are obsolete for2027 individual statements.')
add('13:a',['B2.1.1'],'State the Python data type suitable for a whole-number count of available rooms.','int.',[(1,'int.')],[24],status='B',adapt='Replaces Java primitive-type taxonomy with an explicitly required Python-compatible basic data type.')
add('13:b-i',['B3.1.2','B2.1.1'],'State a Boolean attribute appropriate for an Accommodation class.','has_accessible_entrance,storing True or False.',[(1,'Appropriate yes/no attribute.')],[24],status='B')
add('13:b-ii',['B3.1.2','B2.1.1'],'State an integer attribute appropriate for an Accommodation class.','number_of_rooms.',[(1,'Appropriate whole-number attribute.')],[24],status='B')
add('13:c-i',['B3.2.4'],'A Building object stores a reference to an Owner object. The owner exists independently and may be associated with several buildings. State this object relationship.','Aggregation.',[(1,'Aggregation.')],[24],status='B',adapt='Makes independent lifetime explicit rather than relying only on a vaguehas-a phrase.')
add('13:c-ii',['B3.2.1'],'Class Cottage extends Accommodation and inherits its attributes and methods. State the relationship between Cottage and Accommodation.','Inheritance; Cottage is a subclass of Accommodation.',[(1,'Inheritance/subclass relationship.')],[24])
add('13:d',['B3.1.1'],'Distinguish a class from an object using Accommodation as context.','Accommodation defines common state and behaviour. A particular Accommodation object stores concrete values,such as one address and room count.',[(1,'Class definition versusconcreteinstance.'),(1,'Contextual attribute/example.')],[24],new_command='Distinguish')
add('13:e',['B3.1.3'],'Outline the difference between a Python class attribute and an instance attribute when recording a total count.','A class attribute belongs to the class and can be shared/accessed through it. Each instance attribute is stored as part of a particular object’s state,so individual objects can hold different values.',[(1,'Class-level/shared association.'),(1,'Instance-specific state distinction.')],[24],status='B',errors=['Assigning self.count may create an instance attribute that shadows the class attribute.'])
add('13:f',['B3.1.3'],'All Cottage and Apartment objects call Accommodation.__init__ once. Outline how one shared counter can track their combined number.','Initialize Accommodation.count=0 at class level and increment Accommodation.count in the shared initializer. Reading Accommodation.count retrieves the combined count without using an instance-specific counter.',[(1,'One counter oncommonclass.'),(1,'Increment thatclasscounter once for eachobject.')],[25],status='B')
add('13:g',['B2.2.2'],'Construct a Python assignment creating wishlist as a list of ten empty slots for later object references. Do not instantiate any accommodation objects.','wishlist = [None] * 10',[(1,'Assignment to wishlist.'),(1,'Creates a Python list.'),(1,'Exactly ten None slots,no objectinstances.')],[25],status='B',adapt='Replaces fixed Java array allocation with aPython list of slots; no claim thatPython list capacity is fixed.')
add('14:a',['B3.1.5'],'Define encapsulation in OOP.','Bundling an object’s state with the operations that manage it,using a controlled interface to protect representation details.',[(1,'State andmanagingoperations grouped withcontrolledinterface.')],[26],new_command='Define')
add('14:b',['B3.1.5'],'Explain how using an Account.withdraw(amount) interface rather than editing its balance everywhere can help preserve valid state.','The class can validate each withdrawal and enforce an invariant,such as rejecting an amount that exceeds the available balance. Clients use the same rule through the interface,reducing inconsistent direct updates.',[(1,'Validation/constraint centralized.'),(1,'Concrete invariant/example.'),(1,'Explains consistency across callers.')],[26])
add('14:c',['B3.2.1'],'Explain one benefit of deriving StudentRoom from Accommodation when both need address and price behaviour.','StudentRoom can inherit the common attributes/methods instead of duplicating them. It adds its room-specific behaviour,and shared fixes can remain in the superclass,which reduces maintenance duplication.',[(1,'Reuses inherited attributes/methods.'),(1,'Contextual commonbehaviour.'),(1,'Explains reduced duplication/maintenance.')],[27])
add('14:d',['A1.2.2'],'Explain how a shared Unicode character representation helps a Python application store names written in different scripts.','Unicode assigns code points to characters across many scripts. An agreed encoding represents them as bytes,so compatible systems can preserve the intended text rather than replacing unsupported characters. Unicode is not universally a fixed16-bit encoding.',[(1,'Character repertoire acrossscripts.'),(1,'Encoding represents agreedcharacters inbinary.'),(1,'Explains preserved text/interoperability.')],[27],status='B',source_issues=['Source MS incorrectly limitsUnicode to2^16 and describesASCII as8-bit; not copied.'])
add('15:a',['B2.3.4'],'Define what the name and parameter list specify in a Python function interface.','The name identifies the callable operation; the parameter list specifies the inputs accepted by that operation.',[(1,'Functionidentifier role.'),(1,'Parameter/input interface role.')],[28],status='B',new_command='Define')
add('15:b',['B2.1.1','B2.3.4'],'A function receives a string parameter text and executes text="Updated". Describe why the caller’s name variable is unchanged,and how the caller can receive the new string.','The assignment rebinds the function’s local parameter rather than the caller’s variable. Return the new string and assign it in the caller,for example name=update(name).',[(1,'Local rebinding does notchange callerbinding.'),(1,'Return value assignedbycaller.')],[28],status='B')
code='''def visit(entries, city):
    for item in entries:
        if item.city == city:
            print(item.address)'''
add('15:c',['B2.1.1','B2.3.3'],'State the intended task of this Python function,assuming entries contains objects with city and address attributes.\n'+code,'Print the address of every entry whose city equals the supplied city.',[(1,'All matching addresses printed.')],[28],status='B',code=code)

for entry in E:
 if entry['key']=='15:c':
  entry['test_code']=entry['code']+"""
from types import SimpleNamespace as N
import contextlib,io
out=io.StringIO()
with contextlib.redirect_stdout(out):
 visit([N(city='Bay',address='A'),N(city='Hill',address='B'),N(city='Bay',address='C')],'Bay')
assert out.getvalue()=='A\\nC\\n'
out=io.StringIO()
with contextlib.redirect_stdout(out):visit([],'Bay')
assert out.getvalue()==''
"""
  entry['check']='Executed two matching entries separated by a nonmatch,and empty list; output captured.'
add('15:d-i',['B2.1.3','B2.1.4'],'Outline why visit(entries,city) may raise an error if entries includes None.\n'+code,'The loop eventually binds item to None. Accessing item.city then raises AttributeError because None has no city attribute.',[(1,'None entry accessed.'),(1,'AttributeError onmissingattribute.')],[28],status='B',code=code,test_code=code+'\ntry:\n visit([None],"Bay")\n raise AssertionError("missing AttributeError")\nexcept AttributeError:pass',check='Executed nullable-entry failure.')
add('15:d-ii',['B2.1.4','B2.3.2'],'Outline how to repair visit so it ignores None entries while still printing every matching address.','Test item is not None before reading its attributes,for example if item is not None and item.city==city. Continue scanning after skipped entries.',[(1,'Explicit None guard.'),(1,'Guard precedesattributeaccess/continuesvalidentries.')],[28],status='B')
sortcode='''def house_sort(entries):
    result = [item for item in entries if item is not None]
    for end in range(len(result)-1, 0, -1):
        for i in range(end):
            if result[i].price > result[i+1].price:
                result[i], result[i+1] = result[i+1], result[i]
    return result'''
add('15:e',['B2.4.3','B2.2.2'],'Construct house_sort(entries) in Python. entries may contain None slots or House objects with numeric price. Return the non-None objects sorted by ascending price using bubble sort. Do not use sorted or list.sort; the task assesses bubble sort.','One solution:\n'+sortcode,[(1,'Filters/ignoresNone slotscorrectly.'),(1,'Correct outerpassloop.'),(1,'Correct adjacentcomparisonloop.'),(1,'Compares pricesascending.'),(1,'Swaps wholeobjectreferences andreturnsresult.')],[29,30],status='B',code=sortcode,test_code=sortcode+'\nfrom types import SimpleNamespace as N\na,b,c=N(price=5),N(price=2),N(price=5)\nassert house_sort([a,None,b,c])==[b,a,c]\nassert house_sort([])==[]',check='Executed None filtering,duplicate prices,empty list; objects preserved.',source_issues=['Source MS sort samples loop over whole array despite earlierNone slots; corrected active entries explicit.'])
selectcode='''def select_three(entries, budget):
    ordered = house_sort(entries)
    eligible = []
    for item in ordered:
        if item.price <= budget:
            eligible.append(item)
    return eligible[-3:]'''
add('15:f',['B2.2.2','B2.3.2','B2.3.3','B2.3.4'],'You are given house_sort(entries),which returns the non-None House objects in ascending price order. Construct select_three(entries,budget) in Python. Return the three highest-priced objects costing no more than budget,in ascending price order. At least three eligible objects exist. Use the supplied helper.','One solution:\n'+selectcode,[(1,'Accepts entries andbudget.'),(1,'Calls suppliedsorthelper.'),(1,'Createseligible/resultlist.'),(1,'Visitsorderedobjects.'),(1,'Correct price<=budgetfilter.'),(1,'Selects thelastthree eligibleobjects.'),(1,'Returns thoseobjects inascendingorder.')],[31,32],status='B',code=selectcode,test_code=sortcode+'\n'+selectcode+'\nfrom types import SimpleNamespace as N\ne=[N(price=x) for x in [8,2,9,4,6]]\nassert [x.price for x in select_three(e,8)]==[4,6,8]\nassert [x.price for x in select_three(e,6)]==[2,4,6]',check='Executed budgetboundary andhighest-three selection,notlowestthree.')
add('16:a',['B4.1.1'],'Identify two defining features of an ADT.','Its permitted operations/behaviour are specified; the concrete implementation and memory representation are hidden from users of the interface.',[(1,'Specified operations/behaviour.'),(1,'Implementation abstraction.')],[33])
add('16:b',['B3.1.4','B4.1.3'],'A linked-list object waiting has append(node),which adds a node at its tail. Describe waiting.append(ClientNode("Ari Moon","070123")),where ClientNode constructs a new node from name and phone.','A new ClientNode is instantiated with the supplied name and phone,and that node is added to the end of waiting.',[(1,'New nodeobject created.'),(1,'Correct attributevalues.'),(1,'Added at tailofwaiting.')],[33],status='B')
appendcode='''def append(self, visitor):
    visitor.next = None
    if self.head is None:
        self.head = visitor
    else:
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = visitor'''
add('16:c',['B4.1.3'],'Construct append(self,visitor) in Python for a singly linked list whose head attribute is None when empty. visitor is a new unlinked node. Append it at the end,maintaining None as the last next reference.','One solution:\n'+appendcode,[(1,'Handlesemptylist.'),(1,'Assigns newhead whenempty.'),(1,'Initializestraversal athead.'),(1,'Followslinks untillastnode.'),(1,'Links visitorattail withcorrectNoneboundary.')],[33],status='B',code=appendcode,test_code=appendcode+'\nfrom types import SimpleNamespace as N\nl=N(head=None);a=N(next=None);b=N(next=None)\nappend(l,a);append(l,b)\nassert l.head is a and a.next is b and b.next is None',check='Executed empty andnonempty append; nodeidentity preserved.')
add('16:d',['B4.1.3'],'Without writing code,outline how to split a singly linked list into attended and absent lists according to each node’s Boolean attended field. Move the existing nodes,preserve order in each result,and leave the original list empty.','Create two empty result lists with head/tail references. Traverse the original list,saving the next reference before detaching a node. Append that node to the appropriate result tail according to attended. Advance using the saved reference and finally clear the original head.',[(1,'Initializes tworesultlists.'),(1,'Traverses everyoriginalnode andsavesnext.'),(1,'Chooses correctresult fromattended.'),(1,'Relinks/detaches safely,preservesorder andclearsoriginalhead.')],[34],status='B',source_issues=['Original marking summary does not spell out safe relinking; adapted requirement andsolution preventlosing traversal orcreating sharednextchains.'])
searchcode='''def find_owner(contacts, name, low, high):
    if low > high:
        return None
    middle = (low + high) // 2
    owner = contacts[middle]
    if owner.name == name:
        return owner
    if name < owner.name:
        return find_owner(contacts, name, low, middle - 1)
    return find_owner(contacts, name, middle + 1, high)'''
add('16:e',['B2.4.2','B2.4.5'],'Construct find_owner(contacts,name,low,high) in Python. contacts is a list of Owner objects sorted ascending by unique name. Search the inclusive index interval recursively,returning the matching object or None. Each recursive activation must make at most one further recursive call.','One solution:\n'+searchcode,[(1,'Absentinterval basecasereturnsNone.'),(1,'Correctmiddleindex andaccess.'),(1,'Equalityreturnscorrectobject.'),(1,'Choosescorrecthalf.'),(1,'Leftrecursiveboundary excludesmiddle.'),(1,'Rightrecursiveboundary excludesmiddle andreturnscallresult.')],[34],status='B',code=searchcode,test_code=searchcode+'\nfrom types import SimpleNamespace as N\ne=[N(name=x) for x in ["Ari","Bea","Cai","Dee"]]\nfor i in range(4):assert find_owner(e,e[i].name,0,3) is e[i]\nassert find_owner(e,"Ada",0,3) is None\nassert find_owner([],"Ari",0,-1) is None',check='Executed allhits,absent gap andemptyinterval; one recursive call perpath.',adapt='Replaces indexed JavaLinkedList with Pythonlist; retainsbinarysearch/recursive reasoning withoutclaimingLinkedList random-access efficiency.')
if __name__=='__main__':
 prepare()
 for e in E:
  if e.get('test_code'):exec(e['test_code'],{})
 finish('SRC-032',E,260)
 p=O/'papers/SRC-032/paper_audit.json';a=json.loads(p.read_text());a['expected_candidate_marks']=65;a['option_totals']={'A':65,'B':65,'C':65,'D':65};p.write_text(json.dumps(a,indent=2))
