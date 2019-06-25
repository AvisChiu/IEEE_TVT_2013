import queue
import numpy as np


class Event():
	
	index = -1
	type = ""

	def __init__(self, type):
		self.type = type
	
	def set_index(self, index):
		self.index = index
		
	def __str__(self):
		return "EVENT "+str({'index':self.index, 'type':self.type})
	
	def __lt__(self, other):
		return self.index < other.index
	

class EventSimulation():

	event_index = 0
	event_queue = queue.PriorityQueue()
	
	# wi-fi capacity
	capacity_C = 58
	
	# number of share channel, number of guard channel = C - S
	share_S = 50
	
	queue_size_K = 12
	
	# handoff call arrival rate
	lambda_H = 24.0
	
	# new call arrival rate
	lambda_N = 44.0
	
	# dwell time at stop or moving phase
	xi_S = 3.0
	xi_M = 6.0
	
	# call duration time at stop or moving phase
	mu_S = 6.0
	mu_M = 6.0
	
	# max number of phase
	max_phase = 1000
	
	phase_length_mean = 10
	phase_length_variance = 5
	
	current_phase = False
		
	phase_counter_P = 0
	using_channel_N = 0
	remaining_queue_size_Kr = 0
	waiting_queue = queue.Queue()
	
	# analysis
	new_call = 0
	handoff_call = 0
	
	new_call_blocking = 0
	handoff_call_dropping = 0
	
	def __init__(self, lambda_N, queue_size_K):
		self.lambda_N = lambda_N
		self.queue_size_K = queue_size_K

	def add_event(self,time,event):
		event.set_index(self.event_index)
		self.event_index += 1
		self.event_queue.put((time,event))
	
	def get_event(self):
		return self.event_queue.get()
		
		
	# macac event list

	# pcm > phase change to moving (generate next stop event)

	# pcs > phase change to stop (generate next moving event)

	# hca > handoff call arrival (generate next handoff call arrival & block or generate departure ?)

	# nca > new call arrival (generate next new call arrival & block or genetate departure ?)

	# cd > call departure

	def handle_event(self,event_tuple):
		#print(self.using_channel_N)
		#print(np.random.exponential(1.0/self.lambda_H))
		#print(np.random.exponential(self.mu_M))
		time = event_tuple[0]
		event = event_tuple[1]
		#print(str(time)+" "+str(event))
		
		if event.type == 'pcs':
			self.phase_counter_P += 1
			self.current_phase = False

			phase_length = np.random.exponential(self.xi_S)
			next_event_time = time + phase_length
			next_event = Event('pcm')
			self.add_event(next_event_time,next_event)
			
		elif event.type == 'pcm':
			self.phase_counter_P += 1
			self.current_phase = True

			phase_length = np.random.exponential(self.xi_M)
			next_event_time = time + phase_length
			next_event = Event('pcs')
			self.add_event(next_event_time,next_event)
			
		elif event.type == 'nca':
			self.new_call += 1
			next_event_time = time + np.random.exponential(1.0/self.lambda_N)
			next_event = Event('nca')
			self.add_event(next_event_time,next_event)
			
			if self.current_phase: # moving phase
				if self.using_channel_N < self.capacity_C:
					# accept channel ++
					self.using_channel_N += 1
					
					
					next_duration_time = time + np.random.exponential(self.mu_M)
					next_event = Event('cd')
					self.add_event(next_duration_time,next_event)

				else:
					#block
					self.new_call_blocking += 1
			else: # stop phase
				if self.using_channel_N < self.share_S:
					# accept channel ++
					self.using_channel_N += 1
					next_duration_time = time + np.random.exponential(self.mu_S)
					
					next_event = Event('cd')
					self.add_event(next_duration_time,next_event)
					
				else:
					# block
					self.new_call_blocking += 1
					
		elif event.type == 'hca':
			
			next_event_time = time + np.random.exponential(1.0/self.lambda_H)
			next_event = Event('hca')
			self.add_event(next_event_time,next_event)
			
			if self.current_phase: # moving, ignore this handoff event
				return
			
			# stop phase
			self.handoff_call += 1
			
			#if self.waiting_queue.full():
			#if self.remaining_queue_size_Kr == 0:
			#	self.handoff_call_dropping += 1
			#	pass
			#else:
			#	if self.using_channel_N < self.capacity_C:
					# accept
			#		self.using_channel_N += 1
			#		if self.current_phase:
			#			next_duration_time = time + np.random.exponential(self.mu_M)
			#		else:
			#			next_duration_time = time + np.random.exponential(self.mu_S)
					
			#		next_event = Event('cd')
			#		self.add_event(next_duration_time,next_event)
					
			#	else:
					# put to queue, wait to serve
			#		self.waiting_queue.put(event_tuple)
			#		self.remaining_queue_size_Kr -= 1
			if self.using_channel_N < self.capacity_C:
				# accept
				self.using_channel_N += 1
				if self.current_phase:
					next_duration_time = time + np.random.exponential(self.mu_M)
				else:
					next_duration_time = time + np.random.exponential(self.mu_S)
					
				next_event = Event('cd')
				self.add_event(next_duration_time,next_event)
			else:
				# check queue
				if self.remaining_queue_size_Kr == 0:
					# drop
					self.handoff_call_dropping += 1
				else:
					# queue
					self.waiting_queue.put(event_tuple)
					self.remaining_queue_size_Kr -= 1
			
					
		
		elif event.type == 'cd':
			self.using_channel_N -= 1
			
			#if not self.waiting_queue.empty():
			if self.remaining_queue_size_Kr != self.queue_size_K:
				# pop queue and serve
				waiting_event = self.waiting_queue.get()
				self.remaining_queue_size_Kr += 1
				self.using_channel_N += 1
				if self.current_phase:
					next_duration_time = time + np.random.exponential(self.mu_M)
				else:
					next_duration_time = time + np.random.exponential(self.mu_S)
					
				
				next_event = Event('cd')
				self.add_event(next_duration_time,next_event)
				self.waiting_queue.task_done()
				
				
		
		
	def run(self):
		self.add_event(0,Event('pcs'))
		self.add_event(0,Event("nca"))
		self.add_event(0,Event("hca"))
		self.remaining_queue_size_Kr = self.queue_size_K
		#while self.event_queue.empty() is False:
		#	self.handle_event(self.get_event())
		while self.phase_counter_P < 1000:
			self.handle_event(self.get_event())
		
		#print("")
		#print("New Call Arrival Rate: "+str(self.lambda_N))
		#print(self.new_call)
		#print(self.new_call_blocking)
		#print("New Call Blocking: "+str(self.new_call_blocking/self.new_call))
		#print(self.handoff_call)
		#print(self.handoff_call_dropping)
		#print("Handoff Call Dropping: "+str(self.handoff_call_dropping/self.handoff_call))
		
	def get_ncbp(self):
		return self.new_call_blocking/self.new_call
		
	def get_hcdp(self):
		return self.handoff_call_dropping/self.handoff_call

#print("")
#print("K=0")
#for i in range(4,45,4):
#	event_simulation = EventSimulation(i*1.0,0)
#	event_simulation.run()

#print("")
#print("K=12")
#for i in range(4,45,4):
#	event_simulation = EventSimulation(i*1.0,12)
#	event_simulation.run()
	
	
simulation_bound = 360

k12_ncbp = np.zeros(11)
k12_hcdp = np.zeros(11)
k0_ncbp = np.zeros(11)
k0_hcdp = np.zeros(11)

for i in range(simulation_bound):
	print(i)
	for j in range(4,45,4):
		event_simulation = EventSimulation(j*1.0,12)
		event_simulation.run()
		k12_ncbp[int(j/4-1)] += event_simulation.get_ncbp()
		k12_hcdp[int(j/4-1)] += event_simulation.get_hcdp()
		
	for j in range(4,45,4):
		event_simulation = EventSimulation(j*1.0,0)
		event_simulation.run()
		k0_ncbp[int(j/4-1)] += event_simulation.get_ncbp()
		k0_hcdp[int(j/4-1)] += event_simulation.get_hcdp()

print("")
print("K=12")	
print("NCBP")
for i in range(11):
	print(k12_ncbp[i]/simulation_bound)

print("HCDP")
for i in range(11):
	print(k12_hcdp[i]/simulation_bound)
	
print("")
print("K=0")	
print("NCBP")
for i in range(11):
	print(k0_ncbp[i]/simulation_bound)

print("HCDP")
for i in range(11):
	print(k0_hcdp[i]/simulation_bound)
