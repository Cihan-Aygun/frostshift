import argparse,json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from .engine import compare,experiment
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  u=urlparse(self.path)
  try:
   if u.path=='/':body=Path(__file__).with_name('index.html').read_bytes();mime='text/html; charset=utf-8'
   elif u.path=='/api/scenario':
    q=parse_qs(u.query);result=compare(int(q.get('seed',['42'])[0]),int(q.get('heat',['25'])[0]),int(q.get('fee',['35'])[0]));result['experiment']=experiment(int(q.get('heat',['25'])[0]),int(q.get('fee',['35'])[0]));body=json.dumps(result).encode();mime='application/json'
   else:self.send_error(404);return
   status=200
  except ValueError as e:body=json.dumps({'error':str(e)}).encode();mime='application/json';status=400
  self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8002);a=p.parse_args();s=ThreadingHTTPServer(('127.0.0.1',a.port),Handler)
 print(f'FrostShift: http://127.0.0.1:{a.port}',flush=True)
 try:s.serve_forever()
 except KeyboardInterrupt:pass
 finally:s.server_close()
if __name__=='__main__':main()
