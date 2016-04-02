#!/usr/bin/env python
# build.py
# run python build.py to create a .zip archive of the current project state suitable for deployment to the Chrome Web Store
import os
import fnmatch
import json
from pprint import pprint
from shutil import copy
from shutil import make_archive
import sys

# Check if string matches given list of patterns
def matches(str, patterns):
	output = []
	popList = []
	for i in str:
		for j in patterns:
			if fnmatch.fnmatch(i, j):
				popList.append(i)
		output.append(i)
	for k in popList:
		output.remove(k)
	return output

# Copy files to specified dir
def getMoveList(files, dirPath=''):
	toMove = []
	for i in files:
		if os.path.isfile(str(dirPath) + i) and fnmatch.fnmatch(i, '.DS_Store') != True:
			toMove.append(str(dirPath) + i)
		elif os.path.isdir(i) and fnmatch.fnmatch(i, '.DS_Store') != True:
			n = getMoveList(os.listdir(i), i + '/')
			for k in n:
				toMove.append(k)
		else:
			continue
	return toMove

# Releases folder
releasesDir = os.getcwd() + "/releases/"

# .gitignore
gitIgnoreFile = ".gitignore"
gitIgnorePred = [line.rstrip('\n') for line in open(gitIgnoreFile)]
gitIgnorePred.append('.git*')
gitIgnorePred.append('*.md')

# Iterate through all files/folder and get file paths
initFileList = os.listdir(os.getcwd())
moveList = getMoveList(matches(initFileList, gitIgnorePred))

# Get the current version number
with open('manifest.json') as manifest_file:
	app_json_data = json.load(manifest_file)
app_build_version = app_json_data['version']
app_name = app_json_data['name']
versionDirName = app_name + '_' + app_build_version
tmpDir = releasesDir + versionDirName

# Try to create /releases/tmpDir
if os.path.isdir(tmpDir):
	print('[WARNING] ' + tmpDir + ' already exists. Please increment the verison in manifest.json')
	print('No files were written')
	print('Exiting...')
	exit(0)
else:
	os.makedirs(tmpDir)

# Copy all files to tmpDir
for i in moveList:
	if os.path.dirname(i):
		try:
			os.makedirs(os.path.join(tmpDir, os.path.dirname(i)))
		except:
			pass
	fp = os.path.abspath(i)
	copy(fp, os.path.join(tmpDir, i))
	print('[Writing] ' + i + ' -> ' + os.path.join(tmpDir, i))

# Create a ZIP archive
make_archive(tmpDir, 'zip', tmpDir)
print('[Archiving] ' + tmpDir)