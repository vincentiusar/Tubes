from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.node import CPULimitedHost, Node, Controller
import time
import os

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class MyTopo(Topo) :
	def __init__(self, **opts) :
		Topo.__init__(self, **opts)
		
		HA = self.addHost('HA', ip='192.168.1.1/24', mac='13:01:19:02:21:00:00:01')
		HB = self.addHost('HB', ip='192.168.1.2/24', mac='13:01:19:02:21:00:00:02')
		
		R1 = self.addHost('R1', cls=LinuxRouter, ip='192.168.0.1/29')
		R2 = self.addHost('R2', cls=LinuxRouter, ip='192.168.0.2/29')
		R3 = self.addHost('R3', cls=LinuxRouter, ip='192.168.0.3/29')
		R4 = self.addHost('R4', cls=LinuxRouter, ip='192.168.0.4/29')

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
	
	HA, HB = net.get('HA', 'HB')
	
	print(net['HA'].cmd('sysctl -w net.ipv4.tcp_congestion_control=cubic'))
	print(net['HB'].cmd('sysctl -w net.ipv4.tcp_congestion_control=cubic'))
	
	print(HB.cmd('iperf -s&'))
	print(HA.cmd('iperf -c 192.168.1.2 -i 1&'))
	
	time.sleep(2)
	
	HA.cmd('fg')
	CLI(net)
	net.stop()
	
if __name__=='__main__' :
	setLogLevel('info')
	runTopo()
