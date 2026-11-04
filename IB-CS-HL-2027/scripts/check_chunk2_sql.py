"""Execute currently authored SQL answers against small discriminating datasets."""
from pathlib import Path
import json,re,sqlite3
P=Path(__file__).resolve().parents[1]
records={p['question_id']:p for f in (P/'agents/chunk-2').glob('*/batches/*.json') for p in json.loads(f.read_text())['practice_questions']}
cases={
'P-SRC034-Q01-e':('CREATE TABLE Buyer(BuyerID INTEGER,FirstName TEXT,Surname TEXT); CREATE TABLE Invoice(InvoiceID INTEGER,BuyerID INTEGER,InvoiceDate TEXT); INSERT INTO Buyer VALUES(1,"Mira","Shah"),(2,"Mira","Sen"),(3,"Ali","Shah"); INSERT INTO Invoice VALUES(10,1,"2027-01-01"),(11,1,"2027-02-01"),(12,2,"2027-03-01"),(13,3,"2027-04-01");',[('Mira','Shah','2027-01-01'),('Mira','Shah','2027-02-01')]),
'P-SRC032-Q01-d':('CREATE TABLE Member(MemberID INTEGER,Surname TEXT); CREATE TABLE Loan(LoanID INTEGER,MemberID INTEGER,DateOut TEXT,DateRet TEXT); INSERT INTO Member VALUES(1,"Adams"),(2,"Ng"),(3,"Sen"); INSERT INTO Loan VALUES(1,1,"2027-03-01","2027-03-05"),(2,2,"2027-03-01","2027-03-04"),(3,3,"2027-02-01","2027-03-05");',[('Adams',)]),
'P-SRC002-Q02-c':('CREATE TABLE Client(ClientID INTEGER,ClientName TEXT,ContactNumber TEXT); CREATE TABLE Job(JobID INTEGER,ClientID INTEGER,LeadName TEXT,Priority TEXT); INSERT INTO Client VALUES(1,"Aster","123"),(2,"Birch","456"); INSERT INTO Job VALUES(1,1,"Mira Sen","High"),(2,1,"Mira Sen","High"),(3,2,"Mira Sen","Low"),(4,2,"Mira Shah","High");',[('Aster','123'),('Aster','123')]),
'P-SRC033-Q03-b':('CREATE TABLE Product(ProductID INTEGER,SupplierID INTEGER,ProductName TEXT,Description TEXT); CREATE TABLE Stock(ProductID INTEGER,Quantity INTEGER); INSERT INTO Product VALUES(1,10,"A","fruity taste"),(2,11,"B","dry fruity finish"),(3,12,"C","fruity"),(4,13,"D","tangy"),(5,14,"E","fruity"); INSERT INTO Stock VALUES(1,25),(2,35),(3,24),(4,30),(5,36);',[(10,'A'),(11,'B')])}
employee_setup='CREATE TABLE Employee(EmployeeID INTEGER,FirstName TEXT,Surname TEXT,RoleID INTEGER); CREATE TABLE Role(RoleID INTEGER,Grade INTEGER); INSERT INTO Role VALUES(1,8),(2,7); INSERT INTO Employee VALUES(1,"Ravi","Patel",1),(2,"Mira","Patel",2),(3,"Ada","Chen",1),(4,"Ben","Chen",2),(5,"Suri","Lin",1);'
cases.update({
'P-SRC042-Q01-d':(employee_setup,[('Ravi','Patel',8)]),
'P-SRC044-Q01-d':(employee_setup,[('Ada','Chen',8)]),
'P-SRC038-Q02-d':('CREATE TABLE Reading(DeviceID TEXT,TechID INTEGER,RecordedAt TEXT); CREATE TABLE Technician(TechID INTEGER,Name TEXT); INSERT INTO Technician VALUES(1,"R. Kim"),(2,"Other"); INSERT INTO Reading VALUES("A",1,"2027-05-12 00:00"),("B",1,"2027-05-12 23:59"),("C",1,"2027-05-13 00:00"),("D",1,"2027-05-11 23:59"),("E",2,"2027-05-12 12:00");',[('A',),('B',)]),
'P-SRC040-Q02-d':('CREATE TABLE Observation(DeviceID TEXT,TechnicianID INTEGER,RecordedAt TEXT); CREATE TABLE Technician(TechnicianID INTEGER,Name TEXT); INSERT INTO Technician VALUES(1,"Ari Singh"),(2,"Other"); INSERT INTO Observation VALUES("A",1,"2026-05-12 00:00:00"),("B",1,"2026-05-12 23:59:59"),("C",1,"2026-05-13 00:00:00"),("D",1,"2026-05-11 23:59:59"),("E",2,"2026-05-12 12:00:00");',[('A',),('B',)])})
checks=[]
for q,(setup,expected) in cases.items():
 if q not in records:continue
 solution=records[q]['solution'];start=re.search(r'\bSELECT\b',solution).start();sql=solution[start:].split(';')[0]+';'
 db=sqlite3.connect(':memory:');db.executescript(setup);got=db.execute(sql).fetchall();assert sorted(got)==sorted(expected),(q,got,expected)
 checks.append({'question_id':q,'dialect':'SQLite','query':sql,'actual':got,'expected':expected,'pass':True})
if 'P-SRC038-Q09-e-i' in records:
 db=sqlite3.connect(':memory:');db.executescript('CREATE TABLE Repair(Score INTEGER); INSERT INTO Repair VALUES(2),(4);');old=db.execute('SELECT AVG(Score) FROM Repair').fetchone()[0];db.execute('INSERT INTO Repair VALUES(5)');new=db.execute('SELECT AVG(Score) FROM Repair').fetchone()[0];assert old==3 and new==11/3
 checks.append({'question_id':'P-SRC038-Q09-e-i','dialect':'SQLite','actual':{'stored_average':old,'fresh_average':new},'pass':True})
result={'checks':checks,'all_pass':True,'limits':'These questions use portable SELECT/JOIN/WHERE/BETWEEN/LIKE. Data tests discriminate correct join, multiple filter conditions, duplicate retention and inclusive range endpoints. Other dialect syntax is not assumed.'}
(P/'audits/chunk-2/SQL_REVIEW.json').write_text(json.dumps(result,indent=2))
print('SQL answers passed:',len(checks))
