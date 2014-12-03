
import os, os.path
import sys

NJOB_PER_MACHINE = 100

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
#print VERTICES

#### Then, find all merable nodes
MERABLE_VERTICES = {}
for v in VERTICES:
	if VERTICES[v]['mergable'] == True:
		MERABLE_VERTICES[v] = 1
print "~~~~~", MERABLE_VERTICES

#### Then, decompose the graph into
# multiple connected components that
# are conditionally independent given
# mergable vertices
EXECUTION_GROUPs = {}

## TODO: Lets start from simple, each variable is a 
# connected components.
ct = 0
for v in VERTICES:
	if v not in MERABLE_VERTICES:
		EXECUTION_GROUPs[ct] = [v,]
		ct = ct + 1
print EXECUTION_GROUPs

## Partition groups to machines
ct = 0
os.system('rm -rf _tmp_jobs')
os.system('mkdir -p _tmp_jobs')
CGROUP = 0
os.system('mkdir -p _tmp_jobs/shared')
os.system('cp common/localexec.py _tmp_jobs/shared')
os.system('cp common/do.sh _tmp_jobs/shared')
os.system('mkdir -p _tmp_jobs/job{0}/_vertices'.format(CGROUP))

for mergable in MERABLE_VERTICES:
	os.system('mkdir -p _tmp_jobs/job{0}/_vertices/{1}'.format(CGROUP, mergable))
	os.system('cp -r data/{0}/state _tmp_jobs/job{1}/_vertices/{2}'.format(mergable, CGROUP, mergable))
	os.system('touch _tmp_jobs/job{0}/_vertices/{1}/f.sh'.format(CGROUP, mergable))


for group in EXECUTION_GROUPs:

	for v in EXECUTION_GROUPs[group]:
		os.system('cp -r data/{0} _tmp_jobs/job{1}/_vertices'.format(v, CGROUP))

	ct = ct + len(EXECUTION_GROUPs[group])
	if ct % NJOB_PER_MACHINE == 0:
		CGROUP = CGROUP + 1
		os.system('mkdir -p _tmp_jobs/job{0}/_vertices'.format(CGROUP))
		for mergable in MERABLE_VERTICES:
			os.system('mkdir -p _tmp_jobs/job{0}/_vertices/{1}'.format(CGROUP, mergable))
			os.system('cp -r data/{0}/state _tmp_jobs/job{1}/_vertices/{2}'.format(mergable, CGROUP, mergable))
			os.system('touch _tmp_jobs/job{0}/_vertices/{1}/f.sh'.format(CGROUP, mergable))

## Execute























