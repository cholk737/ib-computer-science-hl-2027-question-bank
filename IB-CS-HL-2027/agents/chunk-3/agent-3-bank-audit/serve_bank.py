#!/usr/bin/env python3
"""Local persistent-bank UI/API. Bound to loopback; no external dependencies."""
import argparse,json,mimetypes,sqlite3,sys,traceback,urllib.parse
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import bank_db
HERE=Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
    def reply(self,status,body,content_type='application/json; charset=utf-8'):
        raw=body if isinstance(body,bytes) else json.dumps(body,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type',content_type);self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        db=bank_db.connect(self.server.db_path)
        try:
            url=urllib.parse.urlsplit(self.path);params={k:v[-1] for k,v in urllib.parse.parse_qs(url.query,keep_blank_values=True).items()};path=urllib.parse.unquote(url.path)
            if path=='/api/search':return self.reply(200,bank_db.public_search(bank_db.search(db,params)))
            if path=='/api/meta':
                scope=[dict(r) for r in db.execute('SELECT code,theme,topic,statement,level FROM objectives ORDER BY code')];types=[r[0] for r in db.execute('SELECT DISTINCT question_type FROM questions ORDER BY question_type')];years=[r[0] for r in db.execute("SELECT DISTINCT year FROM source_refs WHERE year!='' ORDER BY year DESC")];sessions=[r[0] for r in db.execute("SELECT DISTINCT session FROM source_refs WHERE session!='' ORDER BY session")];return self.reply(200,{'question_count':db.execute('SELECT count(*) FROM questions').fetchone()[0],'scope':scope,'question_types':types,'years':years,'sessions':sessions,'verification_dimensions':bank_db.DIMENSIONS})
            if path.startswith('/api/question/'):
                q=bank_db.detail(db,path.split('/')[-1]);return self.reply(200 if q else 404,bank_db.public_question(q) or {'error':'Unknown question'})
            if path.startswith('/api/review/'):
                q=bank_db.detail(db,path.split('/')[-1]);return self.reply(200 if q else 404,{'verification':q['verification'],'scope_evidence':q['scope_evidence'],'outstanding_issues':q['outstanding_issues']} if q else {'error':'Unknown question'})
            if path.startswith('/api/answer/'):
                row=db.execute('SELECT answer_json FROM answers WHERE question_id=?',(path.split('/')[-1],)).fetchone();return self.reply(200 if row else 404,json.loads(row[0]) if row else {'error':'Unknown answer'})
            if path.startswith('/source/'):
                root=Path(db.execute("SELECT value FROM meta WHERE key='project_root'").fetchone()[0]);inv={s['source_id']:s for s in json.loads((root/'sources/SOURCE_INVENTORY.json').read_text())};sid=path.split('/')[-1]
                if sid not in inv:return self.reply(404,{'error':'Unknown source'})
                f=(root/inv[sid]['project_path']).resolve()
                if not f.is_relative_to((root/'sources').resolve()):raise ValueError('Invalid source path')
                return self.reply(200,f.read_bytes(),'application/pdf')
            if path.startswith('/asset/'):
                # Only assets explicitly referenced by stored student question payloads are served.
                rel=path[len('/asset/'):];root=Path(db.execute("SELECT value FROM meta WHERE key='project_root'").fetchone()[0]);allowed=set()
                for row in db.execute('SELECT question_json FROM questions'):
                    for asset in json.loads(row[0]).get('assets',[]):
                        if isinstance(asset,dict) and asset.get('path'):allowed.add(asset['path'])
                if rel not in allowed:return self.reply(404,{'error':'Unknown asset'})
                f=(root/rel).resolve()
                if not f.is_relative_to(root.resolve()):raise ValueError('Invalid asset path')
                return self.reply(200,f.read_bytes(),mimetypes.guess_type(str(f))[0] or 'application/octet-stream')
            name='index.html' if path=='/' else path.lstrip('/');f=(HERE/'persistent-web'/name).resolve()
            if not f.is_relative_to((HERE/'persistent-web').resolve()) or not f.is_file():return self.reply(404,{'error':'Not found'})
            return self.reply(200,f.read_bytes(),mimetypes.guess_type(str(f))[0] or 'application/octet-stream')
        except (ValueError,TypeError) as e:self.reply(400,{'error':str(e)})
        except Exception as e:traceback.print_exc();self.reply(500,{'error':'Local bank operation failed; see server log.'})
        finally:db.close()
    def do_POST(self):
        origin=self.headers.get('Origin');expected='http://'+self.headers.get('Host','')
        if origin and origin!=expected:return self.reply(403,{'error':'Cross-origin writes refused'})
        if 'application/json' not in self.headers.get('Content-Type',''):return self.reply(415,{'error':'JSON required'})
        db=bank_db.connect(self.server.db_path)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size>2_000_000:raise ValueError('Request too large')
            body=json.loads(self.rfile.read(size));path=urllib.parse.urlsplit(self.path).path
            if path=='/api/selection':return self.reply(201,bank_db.save_selection(db,body['question_ids'],body.get('query'),body.get('metadata')))
            if path=='/api/usage':
                qid=body['question_id'];usage_id=str(bank_db.uuid.uuid4())
                if not db.execute('SELECT 1 FROM questions WHERE question_id=?',(qid,)).fetchone():raise ValueError('Unknown question')
                if not body.get('context'):raise ValueError('Usage context required')
                with db:db.execute('INSERT INTO usage_history VALUES(?,?,?,?,?,?)',(usage_id,qid,body.get('used_at') or bank_db.now(),body['context'],body.get('selection_id'),body.get('notes','')))
                return self.reply(201,{'usage_id':usage_id})
            if path=='/api/verification':
                with db:bank_db.update_verification(db,body['question_id'],body['dimension'],body['status'],body['evidence'],body['reviewer'],body['record_sha256'])
                return self.reply(200,{'updated':True})
            return self.reply(404,{'error':'Unknown operation'})
        except (ValueError,KeyError,TypeError,sqlite3.IntegrityError) as e:self.reply(400,{'error':str(e)})
        except Exception:traceback.print_exc();self.reply(500,{'error':'Local bank operation failed; see server log.'})
        finally:db.close()
def main():
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path,default=bank_db.DB);p.add_argument('--port',type=int,default=8765);a=p.parse_args();server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);server.db_path=a.db;print(f'Local question bank http://127.0.0.1:{a.port}/ (Ctrl-C to stop)',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=='__main__':main()
