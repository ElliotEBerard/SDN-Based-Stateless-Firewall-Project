from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI

class MyTopo( Topo ):
	def build( self ):
		# Adding hosts and assigning correct IP/MAC addresses
		h1 = self.addHost( 'h1', ip='192.168.2.10/24', mac='00:00:00:00:00:01' )
		h2 = self.addHost( 'h2', ip='192.168.2.20/24', mac='00:00:00:00:00:02' )
		h3 = self.addHost( 'h3', ip='192.168.2.30/24', mac='00:00:00:00:00:03' )
		h4 = self.addHost( 'h4', ip='192.168.2.40/24', mac='00:00:00:00:00:04' )
		
		# Adding Switch
		s1 = self.addSwitch( 's1' )
		
		# Creating links between hosts and the switch
		self.addLink( h1, s1 )
		self.addLink( h2, s1 )
		self.addLink( h3, s1 )
		self.addLink( h4, s1 )

def network():
	topo = MyTopo()
	
	# Connecting custom topology with OVS switch and controller
	net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
	# Adding remote controller on the correct port
	net.addController('c0', controller=RemoteController, port=6655)

	# Entering containernet CLI after starting
	net.start()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	network()