#!/usr/bin/python
# finds the particles in common between two starfiles
# writes them into a new starfile if specified

import sys

errormsg = """
USAGE:
starfile-overlap.py [file 1 ] AND [file 2]  | findes particles in both [file 1] and [file 2]
or
starfile-overlap.py [file 1 ] NOT [file 2] | finds particles in [file 1] that are not in [file 2]
"""

if len(sys.argv) != 4:
	sys.exit(errormsg)
if sys.argv[2] not in ['AND','NOT']:
	sys.exit(errormsg)

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    for i in alldata:
        if '#' in i:
            labelsdic[i.split('#')[0]] = int(i.split('#')[1])-1
        if len(i.split()) > 3:
            data.append(i.split())
        if len(i.split()) < 3:
            header.append(i.strip("\n"))
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#


files = (sys.argv[1],sys.argv[3])
write_output_file = sys.argv[2]
(labels1,header1,data1) = read_starfile(files[0])
parts1 = []
for i in data1:
    parts1.append(i[labels1['_rlnImageName ']])


(labels2,header2,data2) = read_starfile(files[1])
parts2 = []
for i in data2:
    parts2.append(i[labels2['_rlnImageName ']])




if len(header1) < len(header2):
	thishead = (files[0],header1,labels1,labels2)
else:
	thishead = (files[1],header2,labels2,labels1)
if header1 != header2:
	print ('\n** Headers clash - writing particles in format of {0} **'.format(thishead[0]))
if len(header1) != len(header2):
	print('The following columns were dropped because they were not present in both files:')
	for i in thishead[3]:
		if i not in thishead[2]:
			print i


if write_output_file == 'AND':
	outputfile = 'staroverlap_AND.star'
	output = open(outputfile,'w')
	for i in thishead[1]:
		output.write('{0}\n'.format(i))
	n = 0
	for i in data1:
		line = []
		if i[labels1['_rlnImageName ']] in parts2:
			n+=1
			for j in thishead[1]:
				if '#' in j:
					jsplit = j.split('#')
					line.append(i[labels1[jsplit[0]]])
		if len(line) > 1:
			output.write('\n{0}'.format('   '.join(line)))
	
	print '{0} particles in common'.format(n)
	if n > 0.25*len(parts1):
		print "Much particles So overlap. Wow."

if write_output_file == 'NOT':
	outputfile = 'staroverlap_NOT.star'
	output = open(outputfile,'w')
	for i in thishead[1]:
		output.write('{0}\n'.format(i))
	n = 0
	for i in data1:
		line = []
		if i[labels1['_rlnImageName ']] not in parts2:
			n+=1
			for j in thishead[1]:
				if '#' in j:
					jsplit = j.split('#')
					line.append(i[labels1[jsplit[0]]])
		if len(line) > 1:
			output.write('\n{0}'.format('   '.join(line)))
	
		
	print '{0} particles'.format(n)