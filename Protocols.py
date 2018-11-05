from math import sqrt
from helpers import dist, colour
from Packet import Packet
from Yard import Yard

import matplotlib.pyplot as plt 

class CyclicRouting:
	def __init__(self, yard):
		self.yard = yard

		rings = max(self.yard.l/self.yard.grid_size, self.yard.b/self.yard.grid_size) + 1

		self.rings = {}
		for i in range(0, rings):
			self.rings[i] = []

	def eval_rings(self):
		for row in self.yard.grid:
			for cell in row:
				if cell.head is None:
					continue
				d_x = abs(cell.row - self.yard.sink.cell.row)
				d_y = abs(cell.col - self.yard.sink.cell.col)

				self.rings[max(d_x, d_y)].append(cell)

		self.rings[0] = [self.yard.sink.cell]

		for x, cells in self.rings.items():
			print x, [cell.head.id for cell in cells]

	def execute(self, panda_x, panda_y) :
		self.eval_rings()
	
	def execute2(self, panda_x, panda_y):
		num_col = self.yard.l/self.yard.grid_size
		num_row = self.yard.b/self.yard.grid_size
		maxd = dist(0, 0, self.yard.l, self.yard.b)
		ring_size = int(maxd/Yard.rings);
		panda_ring_no = round((dist(panda_x, panda_y, self.yard.sink.x, self.yard.sink.y) + ring_size - 1)/ring_size);
		panda_grid_no = (panda_y/self.yard.grid_size)*num_col + (panda_x/self.yard.grid_size) 

		# communication range of a node : sqrt(5)*grid_size
		comm_range = sqrt(5)*self.yard.grid_size

		trans = self.energy.trans
		rec = self.energy.rec
		data_aggr = self.energy.data_aggr
		free_space = self.energy.free_space
		multi_path = self.energy.multi_path
		packet = Packet()
		packet_length = packet.packet_length
		ctr_packet_length = packet.ctr_packet_length
		dummy_packet_length = packet.dummy_packet_length
		num_cluster = 0
		num_nodes = 0
		d0 = sqrt(free_space / multi_path)
		
		for node in self.yard.nodes:
			num_nodes += 1
			if node.is_cluster_head == True :
				num_cluster += 1


		for sensor_node in self.yard.ring[panda_ring_no] :
			# alive nodes
			if sensor_node.energy > 0 :
				# determining the energy of Non-CH Nodes
				if sensor_node.is_cluster_head == False :					
					distance = dist(sensor_node.x, sensor_node.y, panda_x, panda_y)
					source_factor = 1
					if distance <= comm_range :
						sensor_node_factor = 2

					min_dis = maxd

					# determining nearest cluster_node
					for node in self.yard.nodes :
						if node.is_cluster_head == True :
							distance = dist(sensor_node.x, sensor_node.y, node.x, node.y)
							if min_dis > distance :
								min_dis = distance
								cluster_node = node

					# total energy dissipitated for transmission
					if min_dis > d0 :
						sensor_node.energy = sensor_node.energy - source_factor*(ctr_packet_length*trans + multi_path*packet_length*(min_dis ** 4)) 
					else :
						sensor_node.energy = sensor_node.energy - source_factor*(ctr_packet_length*trans + free_space*packet_length*(min_dis ** 4)) 
					
					# total energy dissipitated while receiving packets
					if cluster_node.energy > 0 :
						cluster_node.energy = cluster_node.energy - (rec + data_aggr)*packet_length

				# determining the energy of CH Nodes
				else :
					distance = dist(sensor_node.x, sensor_node.y, self.yard.sink.x, self.yard.sink.y)
					
					# total energy dissipitated for transmission + data aggregation
					if distance >= d0 :
						sensor_node.energy = sensor_node.energy - ((trans + data_aggr)*packet_length + multi_path*packet_length*(distance ** 4))
					else :
						sensor_node.energy = sensor_node.energy - ((trans + data_aggr)*packet_length + free_space*packet_length*(distance ** 4)) 

					# total energy dissipitated while receiving packets 
					sensor_node.energy = sensor_node.energy - rec*ctr_packet_length*(round(num_nodes/num_cluster))

		# for node in self.yard.ring[panda_ring_no] :
		# 	print node.energy, node.is_cluster_head


