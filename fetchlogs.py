#!/usr/bin/python
import os
import re
def fetch_apps():
	for parent, dirs, files in os.walk('.'):
		for d in dirs:
			if d.endswith(".elasticbeanstalk"):
				appdir = parent
				yield appdir

'''
issues eb logs -z, once finished return full path to zip file
'''
def logs_zip(folder):
	result = os.popen("(cd %(folder)s && eb logs -z)" % locals()).read()
	path = re.search(r"Logs were saved to (.+)$",result,flags=re.MULTILINE).group(1)
	return path
def unzip(folder, zipfile):
	result = os.popen("(cd %(folder)s && unzip %(zipfile)s)" % locals()).read()
	return result


for appdir in fetch_apps():
	zippath = logs_zip(appdir)
	items = re.findall(r"inflating: (.+)$",unzip(appdir,zippath),flags=re.MULTILINE)
	items = map(lambda i: appdir+"/.elasticbeanstalk/logs/"+i, items)
	for i in items:
		print i
	



