
import os, os.path
import sys

CHUNKSIZE = 2

#### First, get all vertices
VERTICES = {}
for f in os.listdir('data'):
	if f.startswith('.'): continue
	VERTICES[f] = {}

	# check whether the vertice is mergable
	if os.path.getsize('data/' + f + '/g.sh') > 0:
		VERTICES[f]['mergable'] = True
	else:
		VERTICES[f]['mergable'] = False

	VERTICES[f]['neighbors'] = []
	for n in os.listdir('data/' + f + '/neighbors'):
		if n.startswith('.'): continue
		VERTICES[f]['neighbors'].append(n)

#### BASELINE 1: RADNOM ALLOCATORS
print VERTICES 

