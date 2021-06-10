
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.node import OVSSwitch
from mininet.node import Node
from mininet.log import setLogLevel, info
import time
import os

class CustomNode( Node ):

    def config( self, **params ):
        super( CustomNode, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( CustomNode, self ).terminate()
        
class MyTopo(Topo) :
	def build( self, **opts ) :
		
		HA = self.addHost('HA', cls=Host, ip='10.1.1.4/24', defaultRoute=None )
		HB = self.addHost('HB', cls=Host, ip='10.1.1.3/24', defaultRoute=None )
		
		R1 = self.addNode('R1', cls=CustomNode, ip='10.1.1.1/24')
		R2 = self.addNode('R2', cls=CustomNode, ip='10.2.1.1/24')
		R3 = self.addNode('R3', cls=CustomNode, ip='10.1.1.2/24')
		R4 = self.addNode('R4', cls=CustomNode, ip='10.2.1.2/24')

		self.addLink( HA, R1, bw=1, intfName1='HA-eth0', params1={'ip':'10.1.1.4/24'}, intfName2='R1-eth0', params2={'ip':'10.1.1.1/24'} )
		self.addLink( HA, R2, bw=1, intfName1='HA-eth1', params1={'ip':'10.2.1.4/24'}, intfName2='R2-eth0', params2={'ip':'10.2.1.1/24'} )
		self.addLink( HB, R3, bw=1, intfName1='HB-eth0', params1={'ip':'10.1.1.3/24'}, intfName2='R3-eth0', params2={'ip':'10.1.1.2/24'} )
		self.addLink( HB, R4, bw=1, intfName1='HB-eth1', params1={'ip':'10.2.1.3/24'}, intfName2='R4-eth0', params2={'ip':'10.2.1.2/24'} )

		self.addLink( R1, R3, bw=0.5, intfName1='R1-eth1', params1={'ip':'10.100.1.1/24'}, intfName2='R3-eth1', params2={'ip':'10.100.1.2/24'} )
		self.addLink( R1, R4, bw=1, intfName1='R1-eth2', params1={'ip':'10.100.1.3/24'}, intfName2='R4-eth1', params2={'ip':'10.100.1.4/24'} )
		self.addLink( R2, R3, bw=1, intfName1='R2-eth1', params1={'ip':'10.100.1.5/24'}, intfName2='R3-eth2', params2={'ip':'10.100.1.6/24'} )
		self.addLink( R2, R4, bw=0.5, intfName1='R2-eth2', params1={'ip':'10.100.1.7/24'}, intfName2='R4-eth2', params2={'ip':'10.100.1.8/24'} )


def runTopo() :
	os.system('mn -c')
	
	topo = MyTopo()
	net = Mininet(topo=topo)
	
	info(net[ 'HA' ].cmd( 'route add -net 10.1.1.0 netmask 255.255.255.0 gw 10.1.1.1' ))
	info(net[ 'HA' ].cmd( 'route add -net 10.2.1.0 netmask 255.255.255.0 gw 10.2.1.1' ))
	info(net[ 'HB' ].cmd( 'route add -net 10.1.2.0 netmask 255.255.255.0 gw 10.1.1.2' ))
	info(net[ 'HB' ].cmd( 'route add -net 10.2.2.0 netmask 255.255.255.0 gw 10.2.1.2' ))
	info(net[ 'R1' ].cmd('ip route add 10.2.2.0/24 dev R1-eth0'))
	info(net[ 'R3' ].cmd('ip route add 10.1.2.0/24 dev R3-eth0'))
	info(net[ 'R2' ].cmd('ip route add 10.2.1.0/24 dev R2-eth0'))
	info(net[ 'R4' ].cmd('ip route add 10.1.1.0/24 dev R4-eth0'))

	info(net[ 'R1' ].cmd('ip route add 10.1.3.0/29 via 10.1.1.2 dev R1-eth1'))
	info(net[ 'R1' ].cmd('ip route add 10.1.4.0/29 via 10.1.1.4 dev R1-eth2'))
	info(net[ 'R2' ].cmd('ip route add 10.1.5.0/29 via 10.1.1.6 dev R2-eth1'))
	info(net[ 'R2' ].cmd('ip route add 10.1.6.0/29 via 10.1.1.8 dev R2-eth2'))
	info(net[ 'R3' ].cmd('ip route add 10.1.7.0/29 via 10.1.1.1 dev R3-eth1'))
	info(net[ 'R3' ].cmd('ip route add 10.1.8.0/29 via 10.1.1.5 dev R3-eth2'))
	info(net[ 'R4' ].cmd('ip route add 10.1.9.0/29 via 10.1.1.3 dev R4-eth1'))
	info(net[ 'R4' ].cmd('ip route add 10.1.10.0/29 via 10.1.1.7 dev R4-eth2'))
	
	net.start()
	CLI(net)
	net.stop()

if __name__=='__main__' :
	setLogLevel('info')
	runTopo()
