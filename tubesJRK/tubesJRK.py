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
'''
def testIperf( net, server='h0', clients=('h1') ):
    popens = {}
    tperf = 20
    tout = ( tperf + 1 ) * 4
    stopPerf = time() + tout + 5
    inv = 4

    popens[ net[ server ] ] = net[ server ].popen( 'iperf -s -t '+str( tout ) )
    for client in clients:
        client = 'h1'
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
'''
def routerNet():
    # Run Mininet
    net = Mininet( link=TCLink )
    
    # Add Router
    r1 = net.addHost( 'r1', ip='10.1.1.1/24' )
    r2 = net.addHost( 'r2', ip='10.2.1.1/24' )
    r3 = net.addHost( 'r3', ip='10.1.2.1/24' )
    r4 = net.addHost( 'r4', ip='10.2.2.1/24' )
    
    # Add Host h0,h1,h2,h3
    h0 = net.addHost( 'h0', ip='10.1.1.4/29', defaultRoute = None )
    h1 = net.addHost( 'h1', ip='10.1.2.4/29', defaultRoute = None )
    
    # Add Link
    net.addLink(h0, r1, intfName1='h0-eth0',intfName2='r1-eth0', bw=1 )
    net.addLink(h1, r3, intfName1='h1-eth0',intfName2='r3-eth0', bw=1 ) 
    net.addLink(h0, r2, intfName1='h0-eth1',intfName2='r2-eth0', bw=1 )
    net.addLink(h1, r4, intfName1='h1-eth1',intfName2='r4-eth0', bw=1 )
    net.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth1')
    net.addLink(r2, r4, intfName1='r2-eth1', intfName2='r4-eth1')
    net.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth2')
    net.addLink(r2, r3, intfName1='r2-eth2', intfName2='r3-eth2')
   
    # Add IP host
    h0.cmd( 'ip addr add 10.1.1.4/24 brd + dev h0-eth0' )
    h0.cmd( 'ip addr add 10.2.1.4/24 brd + dev h0-eth1' )
    
    h1.cmd( 'ip addr add 10.1.2.4/24 brd + dev h1-eth0' )
    h1.cmd( 'ip addr add 10.2.2.4/24 brd + dev h1-eth1' )
      
    # Add IP Address for Router
    r1.cmd( 'ip addr add 10.1.1.1/24 brd + dev r1-eth0' )
    r1.cmd( 'ip addr add 10.1.255.1/24 brd + dev r1-eth1' )
    r1.cmd( 'ip addr add 10.1.255.15/24 brd + dev r1-eth2' )
    
    r2.cmd( 'ip addr add 10.2.1.1/24 brd + dev r2-eth0' )
    r2.cmd( 'ip addr add 10.2.255.9/24 brd + dev r2-eth1' )
    r2.cmd( 'ip addr add 10.2.255.19/24 brd + dev r2-eth2' )

    r3.cmd( 'ip addr add 10.1.2.1/24 brd + dev r3-eth0' )
    r3.cmd( 'ip addr add 10.1.255.2/24 brd + dev r3-eth1' )
    r3.cmd( 'ip addr add 10.2.255.20/24 brd + dev r3-eth2' )
    
    r4.cmd( 'ip addr add 10.2.2.1/24 brd + dev r4-eth0' )
    r4.cmd( 'ip addr add 10.2.255.10/24 brd + dev r4-eth1' )
    r4.cmd( 'ip addr add 10.2.255.16/24 brd + dev r4-eth2' )
    
    # Start IP Forward on Router
    r1.cmd( 'sysctl net.ipv4.ip_forward=1' )
    r2.cmd( 'sysctl net.ipv4.ip_forward=1' )
    r3.cmd( 'sysctl net.ipv4.ip_forward=1' )
    r4.cmd( 'sysctl net.ipv4.ip_forward=1' )
    # r4.cmd( 'sysctl net.ipv4.ip_forward=1' )

    ### STATIC ROUTING ###
    # r1 -- r3 -- r2
    
    r3.cmd('ip route add 10.1.1.0/24 via 10.1.255.1 dev r3-eth1')
    r1.cmd('ip route add 10.1.2.0/24 via 10.1.255.2 dev r1-eth1')

    r4.cmd('ip route add 10.2.1.0/24 via 10.2.255.9 dev r4-eth1')
    r2.cmd('ip route add 10.2.2.0/24 via 10.2.255.10 dev r2-eth1')
    
    r4.cmd('ip route add 10.1.1.0/24 via 10.2.255.15 dev r4-eth2')
    r1.cmd('ip route add 10.2.2.0/24 via 10.1.255.16 dev r1-eth2')
    
    r3.cmd('ip route add 10.2.1.0/24 via 10.2.255.19 dev r3-eth2')
    r2.cmd('ip route add 10.1.2.0/24 via 10.1.255.20 dev r2-eth2')
    # Start Network
    net.start()
    
    # Ping All Host
    info( '\n', net.ping() ,'\n' )
    # info( '\n', net.ping() ,'\n' )
    # info(net['h0'].cmd('ifconfig'))
    # info(net['r1'].cmd('ifconfig'))
    # info(net['r2'].cmd('ifconfig'))
    # info(net['r3'].cmd('ifconfig'))


    
    # # Set Queue Discipline to CBQ
    # info( '\n*** Queue Disicline :\n' )
    
    # # reset queue discipline
    # r1.cmdPrint( 'tc qdisc del dev r1-eth0 root' ) 

    # # add queue discipline root here
     
    
    # # add queue dicipline classes here 
    

    # # add queue dicipline filters
    # r1.cmdPrint( 'tc filter add dev r1-eth0 parent 1: protocol ip u32 match ip src '+h1.IP()+' flowid 1:1' ) 
    # r1.cmdPrint( 'tc filter add dev r1-eth0 parent 1: protocol ip u32 match ip src '+net[ 'h2' ].IP()+' flowid 1:2' ) 
    # r1.cmdPrint( 'tc qdisc show dev r1-eth0' )
    # info( '\n' )

    # Test Iperf
    #testIperf( net, 'h0', ('h1') )

    # Stop Network
    # net.stop()
    CLI(net)	

if __name__ == '__main__':
    os.system('mn -c')
    os.system( 'clear' )
    setLogLevel( 'info' )
    routerNet()

