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
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#


files = (sys.argv[1],sys.argv[3])
write_output_file = sys.argv[2]
(labels1,header1,data1) = read_starfile(files[0])
parts1 = {}		# {imagename"[line1,line2,line3]}
for i in data1:
	parts1[i[labels1['_rlnImageName ']]] = i


(labels2,header2,data2) = read_starfile(files[1])
parts2 = {}		# {imagename"[line1,line2,line3]}
for i in data2:
    parts2[i[labels2['_rlnImageName ']]] = i




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

print('{0} Particles in {1}'.format(len(parts1),sys.argv[1]))
print('{0} Particles in {1}'.format(len(parts2),sys.argv[3]))

if write_output_file == 'AND':
	outputfile = 'staroverlap_AND.star'
	output = open(outputfile,'w')
	for i in thishead[1]:
		output.write('{0}\n'.format(i))
	# d1list = []
	# for i in data1:
	# 	d1list.append(i[labels1['_rlnImageName ']])
	overlap = set(list(parts1)).intersection(list(parts2))			
	for i in overlap:		
		line = []
		for j in thishead[1]:
			if '_rln' in j and '#' in j:
				jsplit = j.split('#')
				line.append(parts1[i][labels1[jsplit[0]]])
		if len(line) > 1:
			output.write('\n{0}'.format('   '.join(line)))
	
	print '{0} particles in common'.format(len(overlap))
	if len(overlap) > 0.25*len(parts1):
		print "Much particles So overlap. Wow."

if write_output_file == 'NOT':
	outputfile = 'staroverlap_NOT.star'
	output = open(outputfile,'w')
	for i in thishead[1]:
		output.write('{0}\n'.format(i))
	overlap = set(list(parts1)).difference(list(parts2))			
	for i in overlap:		
		line = []
		for j in thishead[1]:
			if '_rln' in j and '#' in j:
				jsplit = j.split('#')
				line.append(parts1[i][labels1[jsplit[0]]])
		if len(line) > 1:
			output.write('\n{0}'.format('   '.join(line)))
	
		
	print '{0} particles in {1} NOT in {2}'.format(len(overlap),sys.argv[1],sys.argv[3])
