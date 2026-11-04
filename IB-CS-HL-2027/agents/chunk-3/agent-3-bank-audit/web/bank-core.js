(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.BankCore=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
function filterQuestions(questions,f={}) {const words=String(f.text||'').trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);return questions.filter(q=>{
 const hay=[q.question_id,q.question_text,...q.syllabus_codes,...q.topics,...(q.provenance||[]).map(p=>[p.source_filename,p.year,p.session,p.source_question_id].join(' '))].join(' ').toLocaleLowerCase();
 return words.every(w=>hay.includes(w)) && (!f.code||q.syllabus_codes.includes(f.code)) && (!f.topic||q.topics.includes(f.topic)) && (!f.theme||q.theme===f.theme) && (!f.level||q.level===f.level) && (!f.difficulty||q.difficulty===f.difficulty) && (f.minMarks===''||f.minMarks==null||q.marks>=Number(f.minMarks)) && (f.maxMarks===''||f.maxMarks==null||q.marks<=Number(f.maxMarks));
});}
function toggleSelection(selected,id){const next=new Set(selected);next.has(id)?next.delete(id):next.add(id);return next;}
function studentExport(questions,selected){return {title:'Unofficial IB Computer Science HL 2027 practice selection',unofficial:true,total_marks:questions.filter(q=>selected.has(q.question_id)).reduce((s,q)=>s+q.marks,0),questions:questions.filter(q=>selected.has(q.question_id)).map(q=>({question_id:q.question_id,question_text:q.question_text,marks:q.marks,syllabus_codes:q.syllabus_codes,command_term:q.command_term,assets:q.assets||[]}))};}
function textExport(data){return data.title+'\nTotal marks: '+data.total_marks+'\n\n'+data.questions.map((q,i)=>(i+1)+'. '+q.question_id+' ['+q.marks+']\n'+q.question_text).join('\n\n');}
return {filterQuestions,toggleSelection,studentExport,textExport};});
