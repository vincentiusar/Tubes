from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

class MyTopo ( Topo ):
    def __init__( self, **opts ):
    Topo.__init__( self, **opts )
    # Membuat objek host
    H1 = self.addHost( 'H1', ip='10.0.0.1/24' )
    H2 = self.addHost( 'H2', ip='10.0.0.2/24' )
    H3 = self.addHost( 'H3', ip='10.0.0.3/24' )
    H4 = self.addHost( 'H4', ip='10.0.0.4/24' )

    # Membuat objek switch
    S1 = self.addSwitch( 'S1' )
    S2 = self.addSwitch( 'S2' )
    S3 = self.addSwitch( 'S3' )
    S4 = self.addSwitch( 'S4' )
    S5 = self.addSwitch( 'S5' )
    # Membuat link antar objek
    self.addLink( H1, S2 )
    self.addLink( H2, S3 )
    self.addLink( H3, S4 )
    self.addLink( H4, S5 )
    self.addLink( S1, S2, bw=50 )
    self.addLink( S1, S3, bw=50 )
    self.addLink( S1, S4, bw=50 )
    self.addLink( S1, S5, bw=10 )

def runTopo():
    # Memastikan mininet bersih dari cache sebelumnya
    os.system('mn –c')
    # Membangun Topologi
    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    # Konfigurasi congestion control
    print(net['H1'].cmd('sysctl –w net.ipv4.tcp_congestion_control=[reno/vegas]'))
    print(net['H2'].cmd('sysctl –w net.ipv4.tcp_congestion_control=[reno/vegas]'))
    print(net['H3'].cmd('sysctl –w net.ipv4.tcp_congestion_control=[reno/vegas]'))
    print(net['H4'].cmd('sysctl –w net.ipv4.tcp_congestion_control=[reno/vegas]'))
    # Memasukan objek host pada variabel
    h1, h2, h3, h4 = net.get ('H1', 'H2', 'H3', 'H4')
    # Menjalankan iPerf dibackground process
    h4.cmd('iperf –s&')
    h2.cmd('iperf –c 10.0.0.4&')
    h3.cmd('iperf –c 10.0.0.4&')
    h1.cmd('iperf –c 10.0.0.4 –i 1&')
    time.sleep(15)
    # Menampilkan hasil iPerf dari H1 ke H4
    h1.cmdPrint('fg')
    CLI(net)
    net.stop()

if __name__== '__main__':
    setLogLevel('info')
    runTopo()