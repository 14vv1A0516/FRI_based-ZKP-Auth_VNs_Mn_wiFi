from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.term import makeTerm

def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', wlans=1, mac='00:00:00:00:00:01', ip='192.168.10.1/24', min_v=5.0, max_v=10.0, range=3, color="red")
    sta2 = net.addStation('sta2', wlans=1, mac='00:00:00:00:00:02', ip='192.168.10.2/24', min_v=5.0, max_v=10.0, range=3, color="red")
    
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:03', ip='192.168.10.3/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:04', ip='192.168.10.4/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:05', ip='192.168.10.5/24', min_v=5.0, max_v=10.0, range=5, color="red")
    
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:06', ip='192.168.10.6/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta7 = net.addStation('sta7', mac='00:00:00:00:00:07', ip='192.168.10.7/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta8 = net.addStation('sta8', mac='00:00:00:00:00:08', ip='192.168.10.8/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta9 = net.addStation('sta9', mac='00:00:00:00:00:09', ip='192.168.10.9/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta10 = net.addStation('sta10', mac='00:00:00:00:00:10', ip='192.168.10.10/24', min_v=5.0, max_v=10.0, range=5, color="red")
    # '''
    sta11 = net.addStation('sta11', mac='00:00:00:00:00:11', ip='192.168.10.11/24', min_v=5.0, max_v=10.0, range=5, color="red")
    
    sta12 = net.addStation('sta12', mac='00:00:00:00:00:12', ip='192.168.10.12/24', min_v=5.0, max_v=10.0, range=5, color="red")
    
    sta13 = net.addStation('sta13', mac='00:00:00:00:00:13', ip='192.168.10.13/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta14 = net.addStation('sta14', mac='00:00:00:00:00:14', ip='192.168.10.14/24', min_v=5.0, max_v=10.0, range=5, color="red")
    sta15 = net.addStation('sta15', mac='00:00:00:00:00:15', ip='192.168.10.15/24', min_v=5.0, max_v=10.0, range=5, color="red")
    
    sta16 = net.addStation('sta16', mac='00:00:00:00:00:16', ip='192.168.10.16/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta17 = net.addStation('sta17', mac='00:00:00:00:00:17', ip='192.168.10.17/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta18 = net.addStation('sta18', mac='00:00:00:00:00:18', ip='192.168.10.18/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta19 = net.addStation('sta19', mac='00:00:00:00:00:19', ip='192.168.10.19/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta20 = net.addStation('sta20', mac='00:00:00:00:00:20', ip='192.168.10.20/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    # '''
    sta21 = net.addStation('sta21', mac='00:00:00:00:00:21', ip='192.168.10.21/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta22 = net.addStation('sta22', mac='00:00:00:00:00:22', ip='192.168.10.22/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta23 = net.addStation('sta23', mac='00:00:00:00:00:23', ip='192.168.10.23/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta24 = net.addStation('sta24', mac='00:00:00:00:00:24', ip='192.168.10.24/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta25 = net.addStation('sta25', mac='00:00:00:00:00:25', ip='192.168.10.25/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    
    sta26 = net.addStation('sta26', mac='00:00:00:00:00:26', ip='192.168.10.26/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta27 = net.addStation('sta27', mac='00:00:00:00:00:27', ip='192.168.10.27/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta28 = net.addStation('sta28', mac='00:00:00:00:00:28', ip='192.168.10.28/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta29 = net.addStation('sta29', mac='00:00:00:00:00:29', ip='192.168.10.29/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    sta30 = net.addStation('sta30', mac='00:00:00:00:00:30', ip='192.168.10.30/24', position='90,60,0', min_v=5.0, max_v=10.0, range=5, color="red")
    # '''
    RSU1 = net.addStation(f'RSU1', wlans=2, ip=f'192.168.10.100/24', position='75,65,0', range=60)
    RSU2 = net.addStation(f'RSU2', wlans=2, ip=f'192.168.20.200/24', position='170,65,0', color="blue", range=60)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Setting links\n")

    RSU1.setMasterMode(intf=f'RSU1-wlan0', ssid='RSU1-ssid', channel=1, mode='g')
    RSU1.cmd('ifconfig RSU1-wlan1 192.168.1.1 netmask 255.255.0.0')
    RSU1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    net.addLink(RSU1, intf='RSU1-wlan1', cls=adhoc, ssid='adhoc-ssid', channel=5, proto='olsrd', proto_args='-hint 6')
    
    RSU2.setMasterMode(intf=f'RSU2-wlan0', ssid='RSU2-ssid', channel=1, mode='g')
    RSU2.cmd('ifconfig RSU2-wlan1 192.168.1.2 netmask 255.255.0.0')
    RSU2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    net.addLink(RSU2, intf='RSU2-wlan1', cls=adhoc, ssid='adhoc-ssid', channel=5, proto='olsrd', proto_args='-hint 6')

    info("*** Plotting Graph\n")
    net.plotGraph(max_x=230, max_y=135)

    print ("Starting Mobility")
    net.startMobility (time=0, seed=1, model='RandomDirection') #, AC='ssf')

    net.mobility(sta1, 'start', time=10, position='1,70,0')
    net.mobility(sta1, 'stop', time=40, position='210,70,0')

    net.mobility(sta2, 'start', time=15, position='1,70,0')
    net.mobility(sta2, 'stop', time=45, position='210,70,0')

    net.mobility(sta3, 'start', time=20, position='1,70,0')
    net.mobility(sta3, 'stop', time=50, position='210,70,0')

    net.mobility(sta4, 'start', time=25, position='1,70,0')
    net.mobility(sta4, 'stop', time=55, position='210,70,0')

    net.mobility(sta5, 'start', time=30, position='1,70,0')
    net.mobility(sta5, 'stop', time=60, position='210,70,0')
      
    net.mobility(sta6, 'start', time=35, position='1,70,0')
    net.mobility(sta6, 'stop', time=65, position='210,70,0')

    net.mobility(sta7, 'start', time=40, position='1,70,0')
    net.mobility(sta7, 'stop', time=70, position='210,70,0')

    net.mobility(sta8, 'start', time=45, position='1,70,0')
    net.mobility(sta8, 'stop', time=75, position='210,70,0')

    net.mobility(sta9, 'start', time=50, position='1,70,0')
    net.mobility(sta9, 'stop', time=80, position='210,70,0')

    net.mobility(sta10, 'start', time=55, position='1,70,0')
    net.mobility(sta10, 'stop', time=85, position='210,70,0')
    # '''
    net.mobility(sta11, 'start', time=60, position='1,70,0')
    net.mobility(sta11, 'stop', time=90, position='210,70,0')
    
    net.mobility(sta12, 'start', time=65, position='1,70,0')
    net.mobility(sta12, 'stop', time=95, position='210,70,0')
    
    net.mobility(sta13, 'start', time=70, position='1,70,0')
    net.mobility(sta13, 'stop', time=100, position='210,70,0')

    net.mobility(sta14, 'start', time=75, position='1,70,0')
    net.mobility(sta14, 'stop', time=105, position='210,70,0')

    net.mobility(sta15, 'start', time=80, position='1,70,0')
    net.mobility(sta15, 'stop', time=110, position='210,70,0')
    
    net.mobility(sta16, 'start', time=85, position='1,70,0')
    net.mobility(sta16, 'stop', time=115, position='210,70,0')

    net.mobility(sta17, 'start', time=90, position='1,70,0')
    net.mobility(sta17, 'stop', time=120, position='210,70,0')

    net.mobility(sta18, 'start', time=95, position='1,70,0')
    net.mobility(sta18, 'stop', time=125, position='210,70,0')

    net.mobility(sta19, 'start', time=100, position='1,70,0')
    net.mobility(sta19, 'stop', time=130, position='210,70,0')

    net.mobility(sta20, 'start', time=105, position='1,70,0')
    net.mobility(sta20, 'stop', time=135, position='210,70,0')
    # '''
    net.mobility(sta21, 'start', time=110, position='1,70,0')
    net.mobility(sta21, 'stop', time=140, position='210,70,0')

    net.mobility(sta22, 'start', time=115, position='1,70,0')
    net.mobility(sta22, 'stop', time=145, position='210,70,0')

    net.mobility(sta23, 'start', time=120, position='1,70,0')
    net.mobility(sta23, 'stop', time=150, position='210,70,0')

    net.mobility(sta24, 'start', time=125, position='1,70,0')
    net.mobility(sta24, 'stop', time=155, position='210,70,0')

    net.mobility(sta25, 'start', time=130, position='1,70,0')
    net.mobility(sta25, 'stop', time=160, position='210,70,0')
        
    net.mobility(sta26, 'start', time=135, position='1,70,0')
    net.mobility(sta26, 'stop', time=165, position='210,70,0')

    net.mobility(sta27, 'start', time=140, position='1,70,0')
    net.mobility(sta27, 'stop', time=170, position='210,70,0')

    net.mobility(sta28, 'start', time=145, position='1,70,0')
    net.mobility(sta28, 'stop', time=175, position='210,70,0')

    net.mobility(sta29, 'start', time=150, position='1,70,0')
    net.mobility(sta29, 'stop', time=180, position='210,70,0')

    net.mobility(sta30, 'start', time=155, position='1,70,0')
    net.mobility(sta30, 'stop', time=185, position='210,70,0')
    # '''
    
    net.stopMobility (time=400)
    info("*** Starting network\n")
    net.build()

    makeTerm (RSU2, cmd = "bash -c 'python3 Provable_RSU_Hand.py;'")
    #time.sleep(1)
    # makeTerm (RSU1, cmd = "bash -c 'python3 Provable_RSU_Auth.py ;'")

    veh_rsui_auth_check = {} # for initial auth
    veh_rsuj_hand_auth_check = {}  # for handover to RSU j
    
    veh_rsu_assoc = {}  # for RSU handover

    ip_ct = 0
    while True :
        for sta in net.stations:
            if str(sta) not in veh_rsui_auth_check and sta.wintfs[0].associatedTo is not None : 
                veh_rsui_auth_check[str(sta)] = 0
                
                RSUx = sta.wintfs[0].associatedTo.node
                RSUx = str(RSUx)
                veh_rsu_assoc[str(sta)] = RSUx
                
                print ("---- Associated to RSU1")
                if RSUx == 'RSU1' and veh_rsui_auth_check[str(sta)] == 0:
                    # send NVID, HPW, p(x), h(x)
                    if str(sta) == 'sta1':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'R7Q9OV5'  > auth_sta1.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta2':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'K3SNB55'  > auth_sta2.txt;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta3':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '3S5P1R8'  > auth_sta3.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta4':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'Z567SYS'  > auth_sta4.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta5':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'V92I2IC'  > auth_sta5.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta6':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '5DTZP1C'  > auth_sta6.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta7':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'F4SLPHQ'  > auth_sta7.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta8':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'VAY3YB5'  > auth_sta8.txt ;'") 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta9':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'ANL8LN7'  > auth_sta9.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta10':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'JZ0SVVC'  > auth_sta10.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta11':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'GKHD3HF'  > auth_sta11.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta12':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '7WX7G05'  > auth_sta12.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta13':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '2RW4N3V'  > auth_sta13.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta14':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'UAE2J4J'  > auth_sta14.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta15':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '0WQ6ODX'  > auth_sta15.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta16':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'TCDHFHE'  > auth_sta16.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta17':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'CUO7DTK'  > auth_sta17.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta18':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '5OJ9ARD'  > auth_sta18.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                
                    if str(sta) == 'sta19':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '3N45OYH'  > auth_sta19.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta20':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'LLHBX4A'  > auth_sta20.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta21':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'AXZDWBK'  > auth_sta21.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta22':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '162QX53'  > auth_sta22.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta23':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '0AC17Z2'  > auth_sta23.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta24':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'BBHO7LE'  > auth_sta24.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta25':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'Y15AWT5'  > auth_sta25.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta26':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'MMLTIFD'  > auth_sta26.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta27':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'P4XYRVP'  > auth_sta27.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta28':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'GX7OG3H'  > auth_sta28.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta29':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py '9839UJP'  > auth_sta29.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    if str(sta) == 'sta30':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Auth.py 'ORTJ9Z7'  > auth_sta30.txt ;'") 
                        
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                             

            elif str(sta) in veh_rsui_auth_check and sta.wintfs[0].associatedTo is not None : 
                RSUx = sta.wintfs[0].associatedTo.node
                RSUx = str(RSUx)
                veh_rsu_assoc[str(sta)] = RSUx   

                if RSUx == 'RSU2' and str(sta) not in veh_rsuj_hand_auth_check:    
                    ip_ct = ip_ct + 1
                    IP = '192.168.20.' + str(ip_ct)
                    
                    #print ("Handover ",str(sta)," associated with RSU ", str(sta.wintfs[0].associatedTo.node))

                    if str(sta) == 'sta1':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta1-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '3S5P1R8' > hand_sta1.txt ;'") 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta2':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta2-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'Z567SYS'  > hand_sta2.txt ;'") 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta3':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta3-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'F4SLPHQ' > hand_sta3.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta4':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta4-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'JZ0SVVC' > hand_sta4.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta5':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta5-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'GKHD3HF' > hand_sta5.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    
                    if str(sta) == 'sta6':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta6-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '7WX7G05' > hand_sta6.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta7':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta7-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '0WQ6ODX' > hand_sta7.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta8':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta8-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'CUO7DTK' > hand_sta8.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta9':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta9-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'AXZDWBK' > hand_sta9.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta10':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta10-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'BBHO7LE' > hand_sta10.txt ;'") 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    # '''
                    if str(sta) == 'sta11':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta11-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'MMLTIFD' > hand_sta11.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta12':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta12-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'ORTJ9Z7' > hand_sta12.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta13':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta13-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '3S5P1R8' > hand_sta13.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta14':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta14-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'Z567SYS' > hand_sta14.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta15':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta15-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'F4SLPHQ' > hand_sta15.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta16':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta16-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'JZ0SVVC' > hand_sta16.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta17':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta17-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'GKHD3HF' > hand_sta17.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta18':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta18-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '7WX7G05' > hand_sta18.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta19':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta19-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '0WQ6ODX' > hand_sta19.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta20':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta20-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'CUO7DTK' > hand_sta20.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    # '''
                    if str(sta) == 'sta21':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta21-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'AXZDWBK' > hand_sta21.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta22':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta22-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'BBHO7LE' > hand_sta22.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta23':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta23-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'ORTJ9Z7' > hand_sta23.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta24':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta24-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'MMLTIFD' > hand_sta24.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta25':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta25-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '3S5P1R8' > hand_sta25.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta26':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta26-wlan0')
                        #x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'Z567SYS' > hand_sta26.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta27':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta27-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'F4SLPHQ' > hand_sta27.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta28':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta28-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'JZ0SVVC' > hand_sta28.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta29':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta29-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py 'GKHD3HF' > hand_sta29.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    if str(sta) == 'sta30':
                        print ("IP of ", str(sta), "is ", IP)
                        sta.setIP(IP, intf='sta30-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Provable_Veh_Hand.py '7WX7G05' > hand_sta30.txt ;'") 

                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    # '''
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()



    
