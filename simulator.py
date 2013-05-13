# coding: utf-8
"""
turk simulator
mitcho (Michael Yoshitaka Erlewine), mitcho@mitcho.com, March 2013

Simulates Amazon Mechanical Turk's substitution of CSV file fields into an HTML template.

The MIT License (MIT)
Copyright (c) 2013 Michael Yoshitaka Erlewine

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function
from os.path import splitext
from sys import argv
from csv import DictReader
import re
from platform import system

def graceful_exit():
	if system() == 'Windows':
		raw_input('Press enter to close the window...')
	exit()

def graceful_read(filename):
	try:
		return open(filename, 'r').read()
	except IOError as e:
		print( "ERROR: ", e.strerror )
		graceful_exit()

template_string = ''
if len(argv) > 1:
	template = argv[1]
	template_string = graceful_read(template)
while re.search(r'\$\{(\w+)\}', template_string) is None:
	if template_string != '':
		print( "WARNING: This doesn't look like a template file!" )
	template = raw_input("Please enter the template file name: ")
	template_string = graceful_read(template)

csv = argv[2] if len(argv) > 2 else raw_input("Please enter the turk CSV file name: ")

data = {}
try:
	f = open(csv, 'rb')
except IOError as e:
	print( "ERROR: ", e.strerror )
	graceful_exit()

csvreader = DictReader(f)
while True:
	try: row = csvreader.next()
	except: break
	data[row['list']] = row

list_number = int(argv[3] if len(argv) > 3 else raw_input("Please enter the list number (0.." + str(len(data) - 1) + ") you want to simulate: "))

substitution = data[str(list_number)]
def replacement(matchobj):
	global substitution
	return substitution[matchobj.group(1)]

output = re.sub(r'\$\{(\w+)\}', replacement, template_string)

name_part, extension = splitext(template)
filename = name_part + '-simulation' + extension
output_file = open(filename, 'w')
output_file.write("<h1>This is a simulation! Do not upload this file to Turk!</h1><hr/>")
output_file.write(output)

print( 'Successfully wrote simulation to ' + filename )
graceful_exit()
