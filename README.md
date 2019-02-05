# starfile_overlap
compare starfiles, extract particles that overlap with AND, or NOT booleans


USAGE:
rln_starfile_overlap.py [file 1 ] AND [file 2]  : findes particles in both [file 1] and [file 2]

or

rln_starfile_overlap.py [file 1 ] NOT [file 2] : finds particles in [file 1] that are not in [file 2]


If the headers of the two files don't match it will write them in the format of [file 1].  If there are columns that don't appear in both files they will be dropped.

