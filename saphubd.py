#!/usr/bin/env python

import argparse, io, os, shutil, subprocess, sys, tempfile, zipfile

try:
	import argparse
except:
	print("")
	print("The module argparse is not availble on your machine:")
	print("- upgrade to python 2.7 or higher, or")
	print("- download and install argparse from https://pypi.python.org/pypi/argparse")
	print("")
	sys.exit()

try:
	# python 3.x
	from http.server import BaseHTTPServer
except:
	# python 2.x
	import BaseHTTPServer

try:
	# python 3.x
	from urllib.parse import parse_qs
except:
	# python 2.x
	from urlparse import parse_qs



parser = argparse.ArgumentParser(description='saphub process')

parser.add_argument('--port', type=int,
                   help='port')

parser.add_argument('--regi',
                   help='path to the regi executable')

args = parser.parse_args()

PORT = args.port
REGI = args.regi

def regibase(host, usr, pwd, cwd):
	env = {'REGI_HOST': host, 'REGI_USER': usr, 'REGI_PASSWD': pwd}
	def _regibase(cmd):
		pro = subprocess.Popen([REGI] + cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = pro.communicate()
		if stderr:
			raise Exception('REGI %s' % stderr)
		return stdout
	return _regibase

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	protocol_version = "HTTP/1.0"

	def do_PUT(self):

		arg = parse_qs(self.path[2:])

		HOST = arg.get("host", [None])[0]
		USER = arg.get("usr", [None])[0]
		PASS = arg.get("pwd", [None])[0]
		PACK = arg.get("package", [None])[0]

		print("REQUEST", HOST, USER, PASS, PACK)

		# e.g. /var/folders/mh/nb413rbs6q959lqn0lcq1nb80000gn/T/tmpG5x0Bn
		root = tempfile.mkdtemp()

		# e.g. foo
		pack = os.path.join(root, PACK)

		print("----", pack)

		try:

			arc = io.BytesIO(self.rfile.read(int(self.headers['Content-Length'])))
	        
			zip = zipfile.ZipFile(arc, 'r')

			regi = regibase(HOST, USER, PASS, root)

			os.mkdir(pack)

			print("----", regi(['create', 'workspace', '--force']))

			print("----", regi(['track', PACK]))

			print("----", regi(['checkout']))

			print("----", regi(['rebase']))

			print("----", regi(['resolve', 'package', PACK, '--with=local']))

			shutil.rmtree(pack)

			os.mkdir(pack)

			zip.extractall(pack)

			print("----", regi(['commit']))

			print("----", regi(['activate']))

			self.send_response(200)

			self.end_headers()

			self.wfile.write("OKAY")
        	
			self.wfile.close()
		
		except Exception, e:

			print(e)

			self.send_response(400)

			self.end_headers()

			self.wfile.write(str(e))
        	
			self.wfile.close()

		finally:

			shutil.rmtree(root)


print("LISTENING", PORT)
BaseHTTPServer.HTTPServer(('0.0.0.0', PORT), MyHandler).serve_forever()
