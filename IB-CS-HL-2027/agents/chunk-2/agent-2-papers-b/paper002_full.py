from paper002_more import *
add('14:a',['B3.1.1','B3.1.4'],'Describe the difference between the Reservation class and an individual reservation object in a booking program.','The class defines the attributes and methods shared by reservations. An object is one concrete instance with its own state,such as one customer’s dates and rate. Many objects can be created from the same definition.',[(1,'Class definition/template.'),(1,'Object instance with own values.'),(1,'Contextual example or multiple instances distinction.')],status='B')
add('14:b-i',['B3.1.4'],'A Python constructor is def __init__(self,rate,priority=False). Outline how callers can create reservations both with and without specifying priority.','A call with only rate uses the default False. A call providing priority overrides it. One constructor handles both forms through an optional parameter,rather than separate signature-selected __init__ definitions.',[(1,'Omitted argument uses False.'),(1,'Supplied argument replaces default.'),(1,'One default-parameter constructor supports both forms.')],status='B',adapt='Replaces Java constructor overloading with accurate Python optional-argument initialization.')
add('14:b-ii',['B3.1.4'],'State what happens to the first __init__ definition if a Python class body later defines another method named __init__.','The later definition replaces the earlier binding for that name; Python does not select between these two definitions by signature.',[(1,'Later definition replaces earlier binding.')],status='B',adapt='Retains constructor-definition reasoning while correcting language-specific overloading assumptions.')
add('14:c',['B3.1.1','B3.1.5'],'Outline one benefit of representing a booking date with a DateValue class that validates its fields, rather than unrelated unvalidated variables.','The class groups the date’s data and validation rules,so callers can reuse a coherent valid-date representation instead of duplicating checks.',[(1,'Groups related state/validation.'),(1,'Explains reuse/integrity benefit.')],status='B')
add('14:d',['B3.1.2'],'A Reservation.summary() method returns a readable string containing the booking ID,rate and priority. Outline why this method is useful.','It provides a consistent readable representation for display/logging while keeping the formatting logic within the class.',[(1,'Readable display/log representation.'),(1,'Consistent formatting/modular responsibility.')],status='B')
c='''def get_cost(self):
    days = self.get_days()
    return days * self.rate'''
add('14:e',['B3.1.4'],'Construct the Python method get_cost(self). The instance attribute rate is the charge per day,and self.get_days() returns the nonnegative rental duration. Return the total charge.','One solution:\n'+c,[(1,'Correct method/instance reference.'),(1,'Calls get_days().' ),(1,'Multiplies duration by rate.'),(1,'Returns calculated charge.')],status='B',code=c,test_code=c+'\nclass R:\n rate=18.5\n def get_days(self):return 4\nassert get_cost(R())==74',check='Executed duration4/rate18.5; formula also giveszero forzeroduration.')
add('15:a',['B3.1.4'],'Class Depot has constructor __init__(self,location). Construct a Python statement assigning a new Depot for "North Pier" to variable depot.','depot = Depot("North Pier")',[(1,'Calls Depot constructor.'),(1,'Correct location string argument.'),(1,'Stores reference in depot.')],status='B')
add('15:b',['B3.1.5'],'A Python class names an internal helper _add_booking. Describe what the single underscore communicates and whether it prevents outside calls.','It signals a non-public implementation convention. Python does not enforce a protected access boundary merely from this underscore; outside code can still call the method.',[(1,'Non-public/internal-use convention.'),(1,'No automatic access enforcement.')],status='B',adapt='Replaces Java protected semantics with accurate Python naming convention; does not claim enforced privacy.')
c='''def bookings_on(self, day):
    result = []
    for i in range(self.used):
        booking = self.bookings[i]
        if booking.start_day == day:
            result.append(booking)
    return result'''
add('15:c',['B2.2.2','B2.3.2','B2.3.3','B3.1.4'],'Construct bookings_on(self,day) in Python. self.bookings is a list whose first self.used entries are booking objects; later entries may be None. Each booking has a start_day string in YYYY-MM-DD format. Return a new list of all active bookings starting on day, in stored order.','One solution:\n'+c,[(1,'Initializes output list.'),(1,'Loops only over active prefix.'),(1,'Accesses each booking object.'),(1,'Compares its start_day with day.'),(1,'Appends matching objects.'),(1,'Returns complete result,including empty list when no match.')],status='B',code=c,test_code=c+'\nfrom types import SimpleNamespace as N\na=N(start_day="2027-01-03");b=N(start_day="2027-01-04");d=N(bookings=[a,b,None],used=2)\nassert bookings_on(d,"2027-01-03")==[a]\nassert bookings_on(d,"2027-02-01")==[]\nassert bookings_on(N(bookings=[],used=0),"2027-01-03")==[]',check='Executed matching,absent andemptyactiveprefix cases.')
add('15:d',['B3.2.4'],'A Reservation currently stores only customer_id. A reusable Customer class will now hold customer details independently of reservations. Outline two changes that let reservations refer to Customer objects.','Add a customer reference attribute to Reservation and accept/store it during initialization. Update methods that need customer details to call that referenced object’s interface. Customers can exist independently and be referenced by several reservations,an aggregation relationship.',[(1,'Reference attribute replaces/augments ID as specified.'),(1,'Constructor accepts/stores Customer object.'),(1,'Methods use the referenced object’s interface.'),(1,'Explains independent lifetime/shared references or consistent updating of callers.')],status='B')
trace_context='''from types import SimpleNamespace as N
stores = [N(location="West Bay", bookings=[N(customer_id=310,end_day="2027-02-08")]),
          N(location="Hilltop", bookings=[]),
          N(location="Canal", bookings=[N(customer_id=520,end_day="2027-04-03"),
                                       N(customer_id=610,end_day="2027-04-10")])]'''
for key,expr,ans in [('16:a-i','stores[1].location','Hilltop'),('16:a-ii','stores[0].bookings[0].customer_id','310'),('16:a-iii','stores[2].bookings[1].end_day','2027-04-10')]:
 add(key,['B2.2.2','B3.1.4'],'Given the following Python setup,state the value of '+expr+'.\n'+trace_context,ans,[(1,'Correct value '+ans+'.')],status='B',code=trace_context,test_code=trace_context+'\nassert '+expr+'=='+repr(int(ans) if ans.isdigit() else ans),check='Executed supplied object/list expression.',flags=['Original RentDate printed-output format unspecified; adaptation supplies an explicit string field.'] if key=='16:a-iii' else [])
add('16:b',['A4.4.2'],'Outline one ethical issue when a financial application records customers’ transaction details.','The records can reveal sensitive behaviour; developers should restrict collection/access to what is necessary and protect the data from unauthorized disclosure.',[(1,'Identifies relevant privacy/confidentiality concern.'),(1,'Explains consequence or appropriate ethical response.')],status='B')
c='''def total_income(stores):
    total = 0
    for store in stores:
        for booking in store.bookings:
            total += booking.get_cost()
    return total'''
add('16:c',['B2.2.2','B2.3.3','B3.1.4'],'Construct total_income(stores) in Python. Each store has a bookings list of active reservation objects; booking.get_cost() returns its charge. Return the sum of all charges across every store.','One solution:\n'+c,[(1,'Initializes total.'),(1,'Visits every store.'),(1,'Visits every booking in the store.'),(1,'Calls cost method and accumulates charge.'),(1,'Returns complete total,includingzero whenempty.')],status='B',code=c,test_code=c+'\nfrom types import SimpleNamespace as N\ns=[N(bookings=[N(get_cost=lambda:12),N(get_cost=lambda:8)]),N(bookings=[])]\nassert total_income(s)==20\nassert total_income([])==0',check='Executed multiple bookings,emptystore andemptyinput.')
add('16:d',['B3.2.3'],'Explain why depending on a small abstract interface rather than the internal fields of another class can improve maintainability.','Client code uses a stable set of operations. The other class can change its internal representation without forcing changes throughout clients,provided the interface remains consistent. This localizes modifications and reduces error risk.',[(1,'Stable abstract interface.'),(1,'Internal representation can change independently.'),(1,'Explains reduced ripple changes/testing risk.')],status='B')
exclude('16:e','Generic teamwork benefits are not individual2027 computer-science learning statements.')
c='''def change_preference(head, old, new):
    changed = 0
    current = head
    while current is not None:
        if current.customer.preferred_shop == old:
            current.customer.preferred_shop = new
            changed += 1
        current = current.next
    return changed'''
add('17:a',['B4.1.3','B3.1.4'],'Construct change_preference(head,old,new) in Python. head identifies a singly linked list of nodes with customer and next attributes; the final next is None. Each customer has preferred_shop. Replace old with new for every matching customer and return the number changed. Return0 for an empty list.','One solution:\n'+c,[(1,'Initializes change count andhead traversal.'),(1,'Correct while/end test.'),(1,'Compares customer preference with old.'),(1,'Updates all matching preferences.'),(1,'Increments count only on match andadvances references.'),(1,'Returns count withcorrectemptycase.')],status='B',code=c,test_code=c+'\nfrom types import SimpleNamespace as N\nc1=N(preferred_shop="A");c2=N(preferred_shop="B");c3=N(preferred_shop="A")\nh=N(customer=c1,next=N(customer=c2,next=N(customer=c3,next=None)))\nassert change_preference(h,"A","C")==2\nassert [c1.preferred_shop,c2.preferred_shop,c3.preferred_shop]==["C","B","C"]\nassert change_preference(None,"A","C")==0',check='Executed multiple matches,nonmatch andemptylist.')
add('17:b',['B2.3.4'],'Outline two benefits of reusing a tested library function through its documented interface rather than reimplementing it at every call site.','Reuse reduces repeated development effort. A well-tested shared implementation can reduce duplicated defects and can be replaced centrally through the same interface,although its suitability still needs checking.',[(1,'Reduced repeated implementation effort.'),(1,'Explains time/maintenance effect.'),(1,'Tested shared implementation/reduced duplicated defects.'),(1,'Explains reliability or central update benefit without treating all libraries as infallible.')],status='B')
add('18:a',['B2.4.4'],'Outline one benefit of recursion for a problem that naturally decomposes into a smaller instance of itself.','The recursive definition expresses the repeated structure directly; the same function handles each smaller case until a base case,which can make the solution clearer.',[(1,'Natural repeated subproblem structure.'),(1,'Explains reuse/clarity withbasecase.')])
c='''def sum_down(n):
    if n <= 1:
        return n
    return n + sum_down(n - 1)'''
add('18:b',['B2.4.5'],'Trace sum_down(4),showing call arguments and returned values.\n'+c,'Calls4,3,2,1; return values1,3,6,10 while unwinding. Final10.',[(1,'Correct decreasing call sequence.'),(1,'Base returns1.'),(1,'Intermediate returns3 and6.'),(1,'Final10.')],status='B',new_command='Trace',code=c,test_code=c+'\nassert sum_down(4)==10\nassert sum_down(1)==1',check='Executed non-branching recursion andbasecase.')
add('18:c',['B2.4.5'],'For the following Python function,state the result of sum_down(-3).\n'+c,'-3; the base condition is immediately true.',[(1,'-3,without an invented recursion error.')],status='B',new_command='State',code=c,test_code=c+'\nassert sum_down(-3)==-3',check='Executed negativeinput; returnsimmediately.',source_issues=['Original Q18c falsely presupposes an error for X(-3); printed Y<=1 returns-3 immediately. No uploaded MS exists.'],adapt='Repairs false source presupposition while retaining correct base-case tracing.')
add('18:d',['B2.3.4'],'Explain how replacing a repeated block with a clearly named function can improve the readability of a program.','The name summarizes the task at each call site,while detailed implementation is grouped in one place. Readers can follow the main flow without repeatedly scanning the same low-level operations.',[(1,'Clear function name summarizes task.'),(1,'Implementation details grouped/hidden.'),(1,'Explains easier main-flow understanding/reduced repetition.')],status='B')
# Coordinator scope/credit review: avoid claiming class-definition coverage for ordinary method bodies or traces.
for e in E:
 if e['key'] in ['14:e','15:c','16:c']:
  e['codes']=[c for c in e['codes'] if c!='B3.1.4']
  if 'B2.3.4' not in e['codes']:e['codes'].append('B2.3.4')
 if e['key'].startswith('16:a-'):
  e['codes']=['B2.1.1','B2.2.2']
 if e['key']=='17:a':e['codes']=['B4.1.3']
 if e['key']=='14:a':e['codes']=['B3.1.1']
 if e['key']=='14:b-i':
  e['prompt']='A Python class Reservation has constructor __init__(self,rate,priority=False). Construct two calls: one reservation at rate40 using the default priority,and another at rate40 with priorityTrue. Outline why one constructor supports both.'
  e['answer']='a = Reservation(40); b = Reservation(40,True). The optional parameter supplies False when omitted and accepts the caller’s value when supplied.'
  e['criteria']=[(1,'Correct default-priority constructor call.'),(1,'Correct explicit-True constructor call.'),(1,'Explains default versus supplied parameter.')]
 if e['key']=='11:c':
  e['criteria'][4]=(1,'Develops resilience: failure of one server can leave other independent servers running,although affected accounts or cross-server messages may be unavailable.')
  e['answer']+=' If one server fails,other independent servers may continue local service,but affected accounts and cross-server exchanges can still be disrupted; this is resilience rather than universal availability.'
if __name__=='__main__':
 prepare()
 for e in E:
  if e.get('test_code'):exec(e['test_code'],{})
 finish('SRC-002',E,260)
 audit=json.loads((O/'papers/SRC-002/paper_audit.json').read_text())
 audit.update(expected_candidate_marks=65,option_totals={'A':65,'B':65,'C':65,'D':65},markscheme_checked=False,markscheme_status='not_uploaded',source_physical_printed_page_offset=0,visual_pages_inspected=list(range(3,26)),blank_pages=[2,10],source_issues=['Q18c false error premise for negativeinput; grade69 overlap; FINDargumentorder; toString sample malformed/Date output formatting unspecified.'])
 (O/'papers/SRC-002/paper_audit.json').write_text(json.dumps(audit,indent=2))
