from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.node import CPULimitedHost, Node, Controller
import time
import os

class MyTopo(Topo) :
	def __init__(self, **opts) :
		Topo.__init__(self, **opts)
		
		HA = self.addHost('HA', ip='192.168.1.2/24', mac='13:01:19:02:21:00:00:01', defaultRoute='via 192.168.2.2' )
		HB = self.addHost('HB', ip='192.168.1.3/24', mac='13:01:19:02:21:00:00:02', defaultRoute='via 192.168.4.2' )
		
		R1 = self.addHost('R1', ip='192.168.2.1/29')
		R2 = self.addHost('R2', ip='192.168.3.1/29')
		R3 = self.addHost('R3', ip='192.168.4.1/29')
		R4 = self.addHost('R4', ip='192.168.5.1/29')

		self.addLink( HA, R1, bw=1, intfName2='R1-eth1' )
		self.addLink( HA, R2, bw=1, intfName2='R2-eth1' )
		self.addLink( HB, R3, bw=1, intfName2='R3-eth1' )
		self.addLink( HB, R4, bw=1, intfName2='R4-eth1' )
		self.addLink( R1, R3, bw=0.5, intfName1='R1-eth2', intfName2='R3-eth2' )
		self.addLink( R1, R4, bw=1, intfName1='R1-eth3', intfName2='R4-eth2' )
		self.addLink( R2, R3, bw=1, intfName1='R2-eth2', intfName2='R3-eth3' )
		self.addLink( R2, R4, bw=0.5, intfName1='R2-eth3', intfName2='R4-eth3' )
			
def runTopo() :
	os.system('mn -c')
	
	topo = MyTopo()
	net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
	net.start()
	
	HA, HB, R1, R2, R3, R4 = net.get('HA', 'HB', 'R1', 'R2', 'R3', 'R4')
	
	net[ 'R1' ].cmd( 'ip addr add 192.168.2.2/29 brd + dev R1-eth1' )
	net[ 'R1' ].cmd( 'ip addr add 192.168.2.3/29 brd + dev R1-eth2' )
	net[ 'R1' ].cmd( 'ip addr add 192.168.2.4/29 brd + dev R1-eth3' )
	net[ 'R2' ].cmd( 'ip addr add 192.168.3.2/29 brd + dev R2-eth1' )
	net[ 'R2' ].cmd( 'ip addr add 192.168.3.3/29 brd + dev R2-eth2' )
	net[ 'R2' ].cmd( 'ip addr add 192.168.3.4/29 brd + dev R2-eth3' )
	net[ 'R3' ].cmd( 'ip addr add 192.168.4.2/29 brd + dev R3-eth1' )
	net[ 'R3' ].cmd( 'ip addr add 192.168.4.3/29 brd + dev R3-eth2' )
	net[ 'R3' ].cmd( 'ip addr add 192.168.4.4/29 brd + dev R3-eth3' )
	net[ 'R4' ].cmd( 'ip addr add 192.168.5.2/29 brd + dev R4-eth1' )
	net[ 'R4' ].cmd( 'ip addr add 192.168.5.3/29 brd + dev R4-eth2' )
	net[ 'R4' ].cmd( 'ip addr add 192.168.5.4/29 brd + dev R4-eth3' )
	
	print(net['HA'].cmd('sysctl -w net.ipv4.tcp_congestion_control=cubic'))
	print(net['HB'].cmd('sysctl -w net.ipv4.tcp_congestion_control=cubic'))
	
	print(HB.cmd('iperf -s&'))
	print(HA.cmd('iperf -c 192.168.1.3 -i 1&'))
	
	time.sleep(2)
	
	HA.cmd('fg')
	CLI(net)
	net.stop()
	
if __name__=='__main__' :
	setLogLevel('info')
	runTopo()

'''
class CustomNode( Node ):

    def config( self, **params ):
        super( CustomNode, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( CustomNode, self ).terminate()
        
class CustomNet( Topo ):
    def build( self, **opts ):
        # Hosts
        h1 = self.addHost('h1',cls=Host,ip='192.1.1.20/24',defaultRoute=None)
        h2 = self.addHost('h2',cls=Host,ip='192.1.2.20/24',defaultRoute=None)

        #Routers
        r1 = self.addNode( 'r1', cls=CustomNode, ip="192.1.1.1/24")
        r2 = self.addNode( 'r2', cls=CustomNode, ip="192.2.1.1/24")

        # Links
        self.addLink(h1,r1,intfName1='h1-eth0',params1={'ip':'192.1.1.20/24'},intfName2='r1-eth0',params2={'ip':'192.1.1.1/24'})
        self.addLink(h2,r1,intfName1='h2-eth0',params1={'ip':'192.1.2.20/24'},intfName2='r1-eth1',params2={'ip':'192.1.2.1/24'})
        self.addLink(h1,r2,intfName1='h1-eth1',params1={'ip':'192.2.1.20/24'},intfName2='r2-eth0',params2={'ip':'192.2.1.1/24'})
        self.addLink(h2,r2,intfName1='h2-eth1',params1={'ip':'192.2.2.20/24'},intfName2='r2-eth1',params2={'ip':'192.2.2.1/24'})

def run():

    net = Mininet( topo=CustomNet(),controller=None )

    net[ 'h1' ].cmd('route add -net 192.1.2.0 netmask 255.255.255.0 gw 192.1.1.1')
    net[ 'h1' ].cmd('route add -net 192.2.2.0 netmask 255.255.255.0 gw 192.2.1.1')
    net[ 'h2' ].cmd('route add -net 192.1.1.0 netmask 255.255.255.0 gw 192.1.2.1')
    net[ 'h2' ].cmd('route add -net 192.2.1.0 netmask 255.255.255.0 gw 192.2.2.1')
    net[ 'r1' ].cmd('ip route add 192.2.1.0/24 dev r1-eth0')
    net[ 'r1' ].cmd('ip route add 192.2.2.0/24 dev r1-eth1')
    net[ 'r2' ].cmd('ip route add 192.1.1.0/24 dev r2-eth0')
    net[ 'r2' ].cmd('ip route add 192.1.2.0/24 dev r2-eth1')
    
    net.start()
    CLI(net)
    net.stop()
'''