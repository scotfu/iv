# !/usr/bin/env python

data = open('coordinates')
out = open('coor.csv','w')
for line in data:
    out.write(str(','.join([c for c in line if c!='\n'])+'\n'))
    
data.close()
out.close()
