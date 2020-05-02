from mininet.topo import Topo  


class MyTopo( Topo ):  
    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Host1 = self.addHost( 'h1' )
        Host2 = self.addHost( 'h2' )
        Switch1 = self.addSwitch('s1')
        # Add links
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch1 )
        
topos = { 'mytopo': ( lambda: MyTopo() ) }
