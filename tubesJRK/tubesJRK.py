from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.util import pmonitor
from signal import SIGINT
from time import time
import os

def testIperf( net, server, clients=() ):
    popens = {}
    tperf = 20
    tout = ( tperf + 1 ) * 4
    stopPerf = time() + tout + 5
    inv = 4

    popens[ net[ server ] ] = net[ server ].popen( 'iperf -s -t '+str( tout ) )
    for client in clients:
        client = clients
        popens[ net[ client ] ] = net[ client ].popen( 'iperf -c '+net[ server ].IP()+' -i '+str(inv)+' -t '+str( tperf ) )
        break

    logserver = logclient1 = logclient2 = logclient3 = ""

    for host, line in pmonitor(popens, timeoutms=(tperf + tout) * 4):
        if host:
            if host.name == server: logserver += (host.name +": "+line)
            elif host.name == clients[0]: logclient1 += (host.name +": "+line)
            # elif host.name == clients[1]: logclient2 += (host.name +": "+line)
            # elif host.name == clients[2]: logclient3 += (host.name +": "+line)

        if time() >= stopPerf:
            for p in popens.values(): p.send_signal(SIGINT)

    print(logserver)
    print(logclient1)
    print(logclient2)
    print(logclient3)

def routerNet():
    # Run Mininet
    net = Mininet( link=TCLink )
    
    # Add Router R1, R2, R3, R4
    R1 = net.addHost( 'R1', ip='10.1.1.1/27', buffer=100 )
    R2 = net.addHost( 'R2', ip='10.2.1.1/27', buffer=100 )
    R3 = net.addHost( 'R3', ip='10.3.1.1/27', buffer=100 )
    R4 = net.addHost( 'R4', ip='10.4.1.1/27', buffer=100 )
    
    # Add Host HA, HB
    HA = net.addHost( 'HA', ip='10.1.1.4/27', defaultRoute = 'via 10.1.1.1' )
    HB = net.addHost( 'HB', ip='10.3.1.4/27', defaultRoute = 'via 10.3.1.1' )
    
    # Add Link
    net.addLink(HA, R1, intfName1='HA-eth0',intfName2='R1-eth0', bw=1 )
    net.addLink(HB, R3, intfName1='HB-eth0',intfName2='R3-eth0', bw=1 ) 
    net.addLink(HA, R2, intfName1='HA-eth1',intfName2='R2-eth0', bw=1 )
    net.addLink(HB, R4, intfName1='HB-eth1',intfName2='R4-eth0', bw=1 )
    net.addLink(R1, R3, intfName1='R1-eth1', intfName2='R3-eth1', bw=1 )
    net.addLink(R2, R4, intfName1='R2-eth1', intfName2='R4-eth1', bw=1 )
    net.addLink(R1, R4, intfName1='R1-eth2', intfName2='R4-eth2', bw=0.5 )
    net.addLink(R2, R3, intfName1='R2-eth2', intfName2='R3-eth2', bw=0.5 )
   
    # Add IP host
    HA.cmd( 'ip addr add 10.1.1.4/27 brd + dev HA-eth0' )
    HA.cmd( 'ip addr add 10.2.1.4/27 brd + dev HA-eth1' )
    
    HB.cmd( 'ip addr add 10.3.1.4/27 brd + dev HB-eth0' )
    HB.cmd( 'ip addr add 10.4.1.4/27 brd + dev HB-eth1' )
      
    # Add IP Address for Router
    R1.cmd( 'ip addr add 10.1.1.1/27 brd + dev R1-eth0' )
    R1.cmd( 'ip addr add 10.1.255.1/29 brd + dev R1-eth1' )
    R1.cmd( 'ip addr add 10.2.255.29/29 brd + dev R1-eth2' )
    
    R2.cmd( 'ip addr add 10.2.1.1/27 brd + dev R2-eth0' )
    R2.cmd( 'ip addr add 10.1.255.9/29 brd + dev R2-eth1' )
    R2.cmd( 'ip addr add 10.2.255.19/29 brd + dev R2-eth2' )

    R3.cmd( 'ip addr add 10.3.1.1/27 brd + dev R3-eth0' )
    R3.cmd( 'ip addr add 10.1.255.2/29 brd + dev R3-eth1' )
    R3.cmd( 'ip addr add 10.2.255.20/29 brd + dev R3-eth2' )
    
    R4.cmd( 'ip addr add 10.4.1.1/27 brd + dev R4-eth0' )
    R4.cmd( 'ip addr add 10.1.255.10/29 brd + dev R4-eth1' )
    R4.cmd( 'ip addr add 10.2.255.30/29 brd + dev R4-eth2' )
    
    # Start IP Forward on Router
    R1.cmd( 'sysctl net.ipv4.ip_forward=1' )
    R2.cmd( 'sysctl net.ipv4.ip_forward=1' )
    R3.cmd( 'sysctl net.ipv4.ip_forward=1' )
    R4.cmd( 'sysctl net.ipv4.ip_forward=1' )
    
    ### STATIC ROUTING ###
    
    HA.cmd('route add -net 10.1.1.0 netmask 255.255.255.224 gw 10.1.1.1')
    HA.cmd('route add -net 10.2.1.0 netmask 255.255.255.224 gw 10.2.1.1')
    HB.cmd('route add -net 10.3.1.0 netmask 255.255.255.224 gw 10.3.1.1')
    HB.cmd('route add -net 10.4.1.0 netmask 255.255.255.224 gw 10.4.1.1')
    
    R1.cmd('ip route add 10.1.1.0/27 dev R1-eth0')
    R2.cmd('ip route add 10.2.1.0/27 dev R2-eth0')
    R3.cmd('ip route add 10.3.1.0/27 dev R3-eth0')
    R4.cmd('ip route add 10.4.1.0/27 dev R4-eth0')
    
    R3.cmd('ip route add 10.1.1.0/27 via 10.1.255.1 dev R3-eth1')
    R1.cmd('ip route add 10.3.1.0/27 via 10.1.255.2 dev R1-eth1')

    R4.cmd('ip route add 10.2.1.0/27 via 10.1.255.9 dev R4-eth1')
    R2.cmd('ip route add 10.4.1.0/27 via 10.1.255.10 dev R2-eth1')
    
    R4.cmd('ip route add 10.1.1.0/27 via 10.2.255.29 dev R4-eth2')
    R1.cmd('ip route add 10.4.1.0/27 via 10.2.255.30 dev R1-eth2')
    
    R3.cmd('ip route add 10.2.1.0/27 via 10.2.255.19 dev R3-eth2')
    R2.cmd('ip route add 10.3.1.0/27 via 10.2.255.20 dev R2-eth2')
    
    R1.cmd('route add -net 10.2.255.16/29 gw 10.1.255.2')
    R1.cmd('route add -net 10.1.255.8/29 gw 10.2.255.30')
    R1.cmd('route add -net 10.2.1.0/27 gw 10.1.255.2')
    R2.cmd('route add -net 10.1.1.0/27 gw 10.1.255.10')
    R2.cmd('route add -net 10.1.255.0/29 gw 10.2.255.20')
    R2.cmd('route add -net 10.2.255.26/29 gw 10.1.255.10')
    
    R3.cmd('route add -net 10.2.255.26/29 gw 10.1.255.1')
    R3.cmd('route add -net 10.1.255.8/29 gw 10.2.255.19')
    R3.cmd('route add -net 10.4.1.0/27 gw 10.1.255.1')
    R4.cmd('route add -net 10.3.1.0/27 gw 10.1.255.9')
    R4.cmd('route add -net 10.1.255.0/29 gw 10.2.255.29')
    R4.cmd('route add -net 10.2.255.16/29 gw 10.1.255.9')
    
    R1.cmd('ip route add 10.1.2.0/27 via 10.1.255.2 dev R1-eth1')
    R2.cmd('ip route add 10.1.1.0/27 via 10.1.255.10 dev R2-eth1')
    
    R3.cmd('ip route add 10.4.1.0/27 via 10.1.255.1 dev R3-eth1')
    R4.cmd('ip route add 10.3.1.0/27 via 10.1.255.9 dev R4-eth1')
    
    # Start Network
    net.start()
    
    # Ping All Host
    info( '\n', net.ping() ,'\n' )
    # info(net['h0'].cmd('ifconfig'))
    # info(net['r1'].cmd('ifconfig'))
    # info(net['r2'].cmd('ifconfig'))
    # info(net['r3'].cmd('ifconfig'))
    
    # Test iperf
    #testIperf( net, 'HA', ('HB') )
    #x = input()
    
    # # Set Queue Discipline to CBQ
    info( '\n*** Queue Disicline :\n' )
    
    # # reset queue discipline
    R1.cmdPrint( 'tc qdisc del dev R1-eth0 root' ) 
    R2.cmdPrint('tc qdisc del dev R2-eth0 root')
    R3.cmdPrint('tc qdisc del dev R3-eth0 root')
    R4.cmdPrint('tc qdisc del dev R4-eth0 root')

    # # add queue discipline root here
    info('\n*** QUEUE Disicline : CBQ\n')
    R1.cmdPrint('tc qdisc add dev R1-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
    R2.cmdPrint('tc qdisc add dev R2-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
    R3.cmdPrint('tc qdisc add dev R3-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
    R4.cmdPrint('tc qdisc add dev R4-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
    
    R1.cmdPrint('tc class add dev R1-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
    R1.cmdPrint('tc filter add dev R1-eth0 parent 1: protocol ip u32 match ip src '+ HA.IP()+' flowid 1:1')
    R2.cmdPrint('tc class add dev R2-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
    R2.cmdPrint('tc filter add dev R2-eth0 parent 1: protocol ip u32 match ip src '+ HA.IP()+' flowid 1:1')
    R3.cmdPrint('tc class add dev R3-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
    R3.cmdPrint('tc filter add dev R3-eth0 parent 1: protocol ip u32 match ip src '+ HB.IP()+' flowid 1:1')
    R4.cmdPrint('tc class add dev R4-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
    R4.cmdPrint('tc filter add dev R4-eth0 parent 1: protocol ip u32 match ip src '+ HB.IP()+' flowid 1:1')
    
    info('\n')
     
    # # add queue dicipline classes here 
    R1.cmdPrint('tc class add dev R1-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
    R2.cmdPrint('tc class add dev R2-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
    R3.cmdPrint('tc class add dev R3-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
    R4.cmdPrint('tc class add dev R4-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
    
    
    # # add queue dicipline filters
    R1.cmdPrint( 'tc filter add dev R1-eth0 parent 1: protocol ip u32 match ip src '+HA.IP()+' flowid 1:1' ) 
    R2.cmdPrint( 'tc filter add dev R2-eth0 parent 1: protocol ip u32 match ip src '+HA.IP()+' flowid 1:1' ) 
    R3.cmdPrint( 'tc filter add dev R3-eth0 parent 1: protocol ip u32 match ip src '+HB.IP()+' flowid 1:1' ) 
    R4.cmdPrint( 'tc filter add dev R4-eth0 parent 1: protocol ip u32 match ip src '+HB.IP()+' flowid 1:1' ) 
    R1.cmdPrint( 'tc qdisc show dev R1-eth0' )
    R2.cmdPrint( 'tc qdisc show dev R2-eth0' )
    R3.cmdPrint( 'tc qdisc show dev R3-eth0' )
    R4.cmdPrint( 'tc qdisc show dev R4-eth0' )
    info( '\n' )

    # Test Iperf
    #testIperf( net, 'HA', ('HB') )

    # Stop Network
    # net.stop()
    CLI(net)	

if __name__ == '__main__':
    os.system('mn -c')
    os.system( 'clear' )
    setLogLevel( 'info' )
    routerNet()

