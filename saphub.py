#!/usr/bin/env python

import datetime, io, os, sys, zipfile

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
	from urllib.request import Request
except:
	# python 2.x
	from urllib2 import Request

try:
	# python 3.x
	from urllib.request import HTTPHandler
except:
	# python 2.x
	from urllib2 import HTTPHandler

try:
	# python 3.x
	from urllib.request import build_opener
except:
	# python 2.x
	from urllib2 import build_opener

try:
	# python 3.x
	from urllib.request import urlopen
except:
	# python 2.x
	from urllib2 import urlopen

try:
	# python 3.x
	from urlib.request import HTTPError
except:
	# python 2.x
	from urllib2 import HTTPError

parser = argparse.ArgumentParser(description='Deploy a sap hana application')

parser.add_argument('--host',
                   help='hana (ip:port)')

parser.add_argument('--usr',
                   help='hana user')

parser.add_argument('--pwd',
                   help='hana password')

parser.add_argument('--package',
                   help='hana package name')

parser.add_argument('--saphub',
                   help='saphub (ip:port)')

args = parser.parse_args()

DIR = os.getcwd()
HOST = args.host
USER = args.usr
PASS = args.pwd
PACK = args.package
SAPHUB = args.saphub

print("Deploy %s to %s as %s via %s" % (DIR, HOST, PACK, SAPHUB))

kickoff = datetime.datetime.now()

archive = io.BytesIO()
zipfile = zipfile.ZipFile(archive, 'w')

for path, dirs, files in os.walk(DIR):
	for file in files:
		if  os.path.isfile(os.path.join(path, file)):
			print("add %s" % os.path.relpath(os.path.join(path, file), DIR))
			zipfile.write(os.path.join(path, file), os.path.relpath(os.path.join(path, file), DIR))

zipfile.close()

archive.seek(0)

try:

	opener = build_opener(HTTPHandler)
	request = Request('http://%s/?host=%s&usr=%s&pwd=%s&package=%s' % (SAPHUB, HOST, USER, PASS, PACK), archive.read())
	request.add_header('Content-Type', 'application/zip')
	request.get_method = lambda: 'PUT'
	response = urlopen(request)

	print("")
	print(response.read())
	print("")
	print(datetime.datetime.now() - kickoff)

except HTTPError as u:

	print("")
	print("SAPHUBD Exception", u.read())
	print("")

except Exception as e:

	print("")
	print("SAPHUBD Exception", e)
	print("")



