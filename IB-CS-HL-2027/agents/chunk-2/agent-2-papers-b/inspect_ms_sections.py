from build_shard import *
R=re.compile(r'(?m)^\s*(\d{1,2})\.\s*(?=\([a-z]+\)|Award)')
for sid in ['SRC-012','SRC-015','SRC-021','SRC-027','SRC-035','SRC-039','SRC-046']:
 t=(O/'evidence'/sid/'all.txt').read_text()
 print(sid,[(m[1],t[m.start():m.start()+45].replace('\n',' ')) for m in R.finditer(t)])
