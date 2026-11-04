from build_shard import *
import shutil
D=O/'evidence/SRC-002';D.mkdir(exist_ok=True)
for f in (P/'audits/chunk-2/ocr/SRC-002').glob('page-*.txt'):shutil.copyfile(f,D/f.name)
RAW='''1:a|3|2|Construct an entity-relationship diagram (ERD) that shows the relationships between programmer, manager and project.
1:b|3|2|Outline one benefit of using a database to track changes to source code.
1:c|3|2|Outline the role of timestamps in maintaining data consistency.
1:d|3|5|Explain one way in which concurrency can be managed in the database when two programmers update the same line of code at the same time.
1:e-i|3|2|Outline what is meant by a consistent database state.
1:e-ii|3|3|Describe one recovery method that can be used to restore a database.
2:a|4|2|Suggest a primary key for the PROJECT table.
2:b|4|2|Outline an appropriate data type for the Priority field.
2:c|5|5|Construct a query to find ClientName and ContactNumber for projects managed by Sehee Choi that are High priority.
2:d|5|5|Construct the database in3rd normal form (3NF) for the entities shown in Figure4. You should use the following notation: TABLE (Key,Field1,Field2,...)
3:a|6|2|Outline the role of conceptual schema.
3:b|6|2|Outline the purpose of a data dictionary.
3:c|6|3|Describe the role of a data definition language in implementing a data model.
3:d|6|3|List three tasks that a database administrator carries out to ensure data security.
3:e|6|5|Explain the benefits of allowing external regulators to view the database.
4:a|7|3|List three benefits of using a multidimensional database model for data mining.
4:b|7|1|Define the term data warehouse.
4:c|7|5|Explain the need for data transforming in the ETL process.
4:d|7|4|Describe how predictive modelling using decision trees can help predict programming errors.
4:e|7|2|Describe how deviation detection could be used to identify copyrighted code.
4:f|7|5|Compare cluster analysis and classification techniques in this scenario.
5:a-i|8|1|State Elaine Anaya Khan's percentage for semester1.
5:a-ii|8|2|Construct the formula to calculate the percentage for cellD2.
5:b|9|3|Construct a formula to automatically add Elaine Anaya Khan's grade (shown in columnI) to cellE2.
5:c|9|2|Outline why cellF4 produced an error.
5:d|11|3|Construct a formula for cellF4 as described.
5:e|11|4|Explain how a last name could be extracted while ignoring a middle name.
6:a|12|2|Calculate KS to one decimal place, where SSS=60. You must show your working.
6:b|13|3|Construct an algorithm in pseudocode as described.
6:c|13|3|Describe one other automated check the Ministry of Education might use to ensure the data is accurate.
6:d|13|4|Construct an algorithm in pseudocode as described.
7:a|14|2|Outline what is meant by real-time simulation.
7:b|14|3|Identify three other variables that would be required to model this simulation effectively.
7:c|14|4|Outline two categories of hardware needed for this simulation.
7:d|14|5|Discuss one factor that could be used to judge the effectiveness of this test case for assessing the accuracy of the simulation model.
7:e|14|4|Outline two factors that would affect the memory needs of a2D visualization such as the heat map shown in Figure10.
8:a|15|4|Outline two steps, other than the ones already stated, that must be taken for the genetic algorithm to find the most suitable locations for new schools.
8:b-i|15|2|Outline one advantage of using a chatbot.
8:b-ii|15|2|Outline one disadvantage of using a chatbot.
8:c|15|2|Identify two key structures of natural language.
8:d|15|4|Evaluate the effectiveness of natural language processing for analysing student essays.
8:e|15|6|Explain two principles of language learning that should be applied in this educational tool.
9:a|16|2|State two characteristics of aURL.
9:b|16|2|Outline two functions of a web browser.
9:c|16|3|Hypertext transfer protocol secure (HTTPS) is an example of a protocol. Explain why protocols are important.
9:d|16|2|Identify two characteristics of extensible mark-up language (XML).
9:e|17|2|With reference to Class.xml and Class_style.xsl, describe how a page connects to the underlying data source.
9:f|17|3|Identify three characteristics of transmission control protocol (TCP).
10:a|17|2|Outline one difference between the deep web and the surface web.
10:b|17|1|Define the term web crawler.
10:c|17|3|Outline the web crawling process.
10:d|17|4|Describe two advantages of parallel web crawling.
10:e|17|5|Evaluate two white hat techniques that may be used in search engine optimization.
11:a|18|4|Distinguish between ubiquitous computing and mobile computing.
11:b|18|2|Describe how open standards support interoperability.
11:c|18|6|Explain how distributed social networks support decentralization of the web.
11:d|18|4|Discuss the challenges faced by distributed social networks with reference to intellectual property.
12:a|18|2|Outline why Figure12 is best described as a weighted and directed graph.
12:b|18|4|Explain why some nodes in Figure12 are described as weakly connected and some as strongly connected.
12:c|18|4|Explain which three nodes in Figure12 would rank highest using the PageRank algorithm.
13:a|19|2|Describe one difference between ambient intelligence and collective intelligence.
13:b|19|6|Discuss one benefit and one limitation of IoT-enabled weather stations providing accurate weather data.
13:c|19|2|Outline why this metadata is not considered an ontology.
14:a|21|3|Describe, using the Rental class as an example, the difference between a class and an instance of a class.
14:b-i|21|3|Outline why having multiple constructors in the Rental class is not a problem when creating a new Rental object.
14:b-ii|21|1|State the object-oriented programming (OOP) concept that allows two methods in the same class to share the same name but have different parameters.
14:c|21|2|Outline one benefit of creating the RentDate class to store the dates of car rentals.
14:d|21|2|Outline the purpose of the toString() method in the Rental class.
14:e|21|4|Construct the code for the getCost() method.
15:a|22|3|Construct the code required to create this instance of the RentalShop class.
15:b|22|2|Describe the use of the modifier protected, with reference to methods in the RentalShop class.
15:c|22|6|Construct the method getTodaysRentals(RentDate today), which will return an array of all the rentals starting on that day. You can use any previously constructed methods.
15:d|22|4|Outline two changes that would need to be made to the existing classes to accommodate this.
16:a-i|23|1|State the outcome from IBIO.output(shops[1].getLocation());
16:a-ii|23|1|State the outcome from IBIO.output(shops[0].getRental(0).getCustomerID());
16:a-iii|23|1|State the outcome from IBIO.output(shops[2].getRental(1).getEndDate());
16:b|23|2|Outline one ethical issue programmers need consider when developing code for financial transactions.
16:c|23|5|Construct the code for the method getTotalIncome(). You can use any previously constructed methods.
16:d|23|3|Explain one reason why the programmers would want to reduce dependencies.
16:e|23|2|Describe one advantage of working as a team.
17:a|24|6|Construct the method public int changePreferredShop(LinkedList customers,String preferredShop,String newShop).
17:b|24|4|Outline two benefits of using a library when developing code.
18:a|25|2|Outline one benefit of recursion.
18:b|25|4|Copy and trace the recursive algorithm when called with X(5);
18:c|25|1|Identify why calling the algorithm with X(-3); would cause an error.
18:d|25|3|Explain one action a programmer could take to improve the readability of code.'''
xs=[]
for line in RAW.splitlines():
 key,page,marks,text=line.split('|',3);q,sub=key.split(':');xs.append(dict(key=key,question=int(q),subquestion=sub,original_marks=int(marks),original_text=text,source_pdf_pages=[int(page)]))
(O/'papers/SRC-002/manual_leaves.json').write_text(json.dumps(xs,ensure_ascii=False,indent=2))
print('SRC002 manual census',len(xs),'leaves',sum(x['original_marks'] for x in xs),'marks')
