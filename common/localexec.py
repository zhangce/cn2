
import os, os.path
import select
import sys

NEPOCH = int(sys.argv[1])

# First, get the list of vertices
# on this execution node.
#
LIST_OF_VERTEX = []
for f in os.listdir('_vertices'):
	if os.path.isdir('_vertices/' + f) and os.path.getsize('_vertices/' + f + '/f.sh') > 0:
		LIST_OF_VERTEX.append('_vertices/' + f)

	#for f in LIST_OF_VERTEX:
	#	fifo = os.open("fifo", os.O_RDONLY)

JOBINPUTQUEUE = {}

def execute(job):

	if job not in JOBINPUTQUEUE:
		JOBINPUTQUEUE[job] = {}

	# second, get the list of input socket files
	INPUT_SOCKETS = []
	for input in os.listdir(job + '/neighbors'):
		if input.startswith('.'): continue
		INPUT_SOCKETS.append(input)

	# first, check whether the job is executable
	if len(INPUT_SOCKETS) == len(JOBINPUTQUEUE[job]):
		os.system('sh {0}/f.sh'.format(job))

		for socket in JOBINPUTQUEUE[job]:
			os.close(socket)
		return 1

	finished_inputs = []
	for sread in JOBINPUTQUEUE[job]:
		finished_inputs.append(JOBINPUTQUEUE[job][sread])

	sockets = []
	socket_to_input = {}
	for input in INPUT_SOCKETS:
		if input not in finished_inputs:
			socket = os.open('_closures/{0}'.format(input), os.O_NONBLOCK)
			sockets.append(socket)
			socket_to_input[socket] = input

	(sreads, swrites, swhatever) = select.select(sockets, [], [], 0.001)
	
	for sread in sreads:
		JOBINPUTQUEUE[job][sread] = socket_to_input[sread]

	for socket in sockets:
		if socket not in sreads:
			os.close(socket)

	return 0

def init(job):
	#print "try to execute", job

	# first, get the list of input socket files
	INPUT_SOCKETS = []
	for input in os.listdir(job + '/neighbors'):
		if input.startswith('.'): continue
		INPUT_SOCKETS.append(input)

	#os.system('rm -rf {}/inputs'.format(job))
	#os.system('mkdir -p {}/inputs'.format(job))
	for input in INPUT_SOCKETS:
		if os.path.isfile('_closures/' + input): 
			continue
		if not os.path.getsize(job + '/neighbors/' + input) > 0:
			os.system('mkfifo _closures/{0}'.format(input))
		else:
			for l in open(job + '/neighbors/' + input):
				if l.rstrip() == 'AVERAGE':
					os.system('touch _closures/{0}'.format(input))
				else:
					os.system('mkfifo _closures/{0}'.format(input))
				break

	return 0

os.system('rm -rf _closures')
os.system('mkdir -p _closures')
for job in LIST_OF_VERTEX:
	init(job)

for iepoch in range(0, NEPOCH):
	ExecutedJobs = {}
	JOBINPUTQUEUE = {}
	while len(ExecutedJobs) != len(LIST_OF_VERTEX):
		for job in LIST_OF_VERTEX:
			if job in ExecutedJobs: continue
			rs = execute(job)
			if rs == 0: continue
			ExecutedJobs[job] = 1
				# TODO fault tolerance


