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
