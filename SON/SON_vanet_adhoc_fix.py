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
    
    
    net.stopMobility (time=400)
    info("*** Starting network\n")
    net.build()

    makeTerm (RSU2, cmd = "bash -c 'python3 SON_RSU_Hand.py;'")
    #time.sleep(1)
    #makeTerm (RSU1, cmd = "bash -c 'python3 SON_RSU_Auth.py ;'")

    veh_ap1_auth_check = {}
    veh_ap2_hand_check = {}
    
    ip_ct = 0
    while True :
        for sta in net.stations :
            if str(sta) not in veh_ap1_auth_check and sta.wintfs[0].associatedTo is not None :  
                veh_ap1_auth_check[str(sta)] = 0
                veh_ap2_hand_check[str(sta)] = 0
                apx = sta.wintfs[0].associatedTo.node
                apx = str(apx)          
                
                if apx == 'RSU1' and veh_ap1_auth_check[str(sta)] == 0 : 
                    
                    if str(sta) == 'sta1':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '8CSIXY2' > auth_sta1.txt  ;'")
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta2':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'PB6VJJL' > auth_sta2.txt ;'") # > auth_sta2.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1   

                    if str(sta) == 'sta3':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'ZS2WYFP' > auth_sta3.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta4':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '3IR0IFQ' > auth_sta4.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta5':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'VA7HITX' > auth_sta5.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 
                    
                    if str(sta) == 'sta6':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'TQHG3HN' > auth_sta6.txt  ;'") # 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta7':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'SOWNA0Z' > auth_sta7.txt ;'") # > auth_sta2.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1   
                    
                    if str(sta) == 'sta8':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'YJ01KV0' > auth_sta8.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta9':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'ZCFK3FL' > auth_sta9.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta10':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'OKR23PO' > auth_sta10.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 
                    
                    if str(sta) == 'sta11':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '7URZ2R4' > auth_sta11.txt  ;'") # 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta12':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'PJWNW2E' > auth_sta12.txt ;'") # > auth_sta2.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1   

                    if str(sta) == 'sta13':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '5CDBUUR' > auth_sta13.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta14':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'HNFJ4XP' > auth_sta14.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta15':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'HCGNFY4' > auth_sta15.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta16':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'YNA623T' > auth_sta16.txt  ;'") # 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1

                    if str(sta) == 'sta17':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '38HEY2P' > auth_sta17.txt ;'") # > auth_sta2.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1   

                    if str(sta) == 'sta18':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '60397L6' > auth_sta18.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta19':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '7ITGXL7' > auth_sta19.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta20':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'E0ZLDNX' > auth_sta20.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 
                    # '''
                    if str(sta) == 'sta21':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'HH6O4X5' > auth_sta21.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1
                    
                    if str(sta) == 'sta22':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'F8SNXR7' > auth_sta22.txt ;'") # > auth_sta2.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1   

                    if str(sta) == 'sta23':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'F54T55H' > auth_sta23.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta24':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'FN9GZR8' > auth_sta24.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta25':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'TA00HPZ' > auth_sta25.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 
                    
                    if str(sta) == 'sta26':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'PR3SP33' > auth_sta26.txt  ;'") # 
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1

                    if str(sta) == 'sta27':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'TFBNTPC' > auth_sta27.txt ;'") # > auth_sta2.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1   

                    if str(sta) == 'sta28':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '8R0HPNP' > auth_sta28.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta29':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py '2LTFV7B' > auth_sta29.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1 

                    if str(sta) == 'sta30':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Auth.py 'X6TGI9J' > auth_sta30.txt ;'") #  > auth_sta3.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_ap1_auth_check[str(sta)] = 1    
                    # '''
                    
            elif str(sta) in veh_ap1_auth_check and sta.wintfs[0].associatedTo is not None :
                if str(sta.wintfs[0].associatedTo.node) == 'RSU2' and veh_ap2_hand_check[str(sta)] == 0 : 
                        ip_ct = ip_ct + 1
                        IP = '192.168.20.' + str(ip_ct)
                        
                        if str(sta) == 'sta1' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta1.setIP(IP, intf='sta1-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'ff07e6b6b286d827c4cd79c6345e6a7cadec3a3d2a3ce56b51530fbc4c15d680' > hand_sta1.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta2' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta2.setIP(IP, intf='sta2-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '50c5c64bd7108d919dd353e3843d992649ff94448eb8e88723e35eb0792d0d49' > hand_sta2.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta3' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta3.setIP(IP, intf='sta3-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '59d55925b123b5315ad720fc9b3d15b4e8a5110310e4c25cfa1c85903edadccd' > hand_sta3.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta4' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta4.setIP(IP, intf='sta4-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '2ffc55b2274cc30ad9e90d48734800e6c503894859eefc0e7c6f32e1ef4b8bed' > hand_sta4.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta5' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta5.setIP(IP, intf='sta5-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '12db8bcbf64479799574f4933db32413fbbba379cbb6cda3bd6e289ae3d499da' > hand_sta5.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta6' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta6.setIP(IP, intf='sta6-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '138d8a65c07059326541bbae2c2652f011c937325c242e1f4f45f436d827c603' > hand_sta6.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta7' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta7.setIP(IP, intf='sta7-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'b1ca3230a138ddcd0fc64218c23e08f75989db2deca211c6b89220b770fb84aa' > hand_sta7.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta8' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta8.setIP(IP, intf='sta8-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '35ac6fda5c38a89702c9c92a7c721de7858418c4bd3f28a6ae438d33a5c4fe2c' > hand_sta8.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta9' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta9.setIP(IP, intf='sta9-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'e90996c3ed0e2e55b4739c75fea12701061268a8ffe4778a4aa48f72a6127ffa' > hand_sta9.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta10' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta10.setIP(IP, intf='sta10-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '566d700ebc51f7de61653dc3ed7cfc93837e69355c40e5a75698205645920d48' > hand_sta10.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta11' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta11.setIP(IP, intf='sta11-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '29cf017de3e294a344214489b4704da900a4990c2cafd33bc9a27bd41c613c85' > hand_sta11.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta12' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta12.setIP(IP, intf='sta12-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'a089e5dc304a591cd8b3836651ab190dfd034d503a0311099bdcbf21f4ec5277' > hand_sta12.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta13' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta13.setIP(IP, intf='sta13-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'd82bc76d62f21a7ad9473a157e6fabd765c512c7470e903eaa6aa562363305c1' > hand_sta13.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta14' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta14.setIP(IP, intf='sta14-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '7cd3821eb393997caf62d024113d0fca550d5b14193a2dad87082b3755408630' > hand_sta14.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta15' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta15.setIP(IP, intf='sta15-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '1042b2ebe2cbba58e3a0526b8b36247b1a9c9f7626a6f313f9194def048ff1cb' > hand_sta15.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta16' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta16.setIP(IP, intf='sta16-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '59042b26e809b6c19c0f57526c13a1723c1c0270d8cf1f7531e8693d6875ff27' > hand_sta16.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta17' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta17.setIP(IP, intf='sta17-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'befa933f6656aaa3c18cd519b0a2ecab2e6ce049a178beab535cbca42d8ae065' > hand_sta17.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta18' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta18.setIP(IP, intf='sta18-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '1ea577298c94999c286e3848c6ea82409ad807ca22bea2125e9f60424d88a41e' > hand_sta18.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta19' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta19.setIP(IP, intf='sta19-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '5ecbaeeb2ee46d1a48091c1a751c71c4fdcd6bdb5ee99fd6946a473d916cd3be' > hand_sta19.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta20' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta20.setIP(IP, intf='sta20-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '42fae0f35f48a08bcfea0031ba02eb720a356d665efd068136c299863e6dd972' > hand_sta20.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        
                        if str(sta) == 'sta21' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta21.setIP(IP, intf='sta21-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '64fedf0c983e744bcd01ea0d7e9793b7244cc159429694c10fcb053f699be77c' > hand_sta21.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta22' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta22.setIP(IP, intf='sta22-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'e5f528c89f4776d812fe87b0ba8fce5b3775d8ab1622485c27ced072151b71e9' > hand_sta22.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta23' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta23.setIP(IP, intf='sta23-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '66f019970cf2e81065022f60644a3744f1567a4e96522a0f68431a5efd6f5ed5' > hand_sta23.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta24' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta24.setIP(IP, intf='sta24-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '372bb1d47c069112a80d59e49cd9ed691f8ced3ba454143f8282fb056c267221' > hand_sta24.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta25' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta25.setIP(IP, intf='sta25-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '7a46e148b40fd2f107df0ecfcfa4edb706e6acd92e4e142c839bae98590f1306' > hand_sta25.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta26' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta26.setIP(IP, intf='sta26-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'c514ded3167d2e75c8ead31c4844142683a02f923f89a281840889018ffa187c' > hand_sta26.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta27' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta27.setIP(IP, intf='sta27-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'b62d0f7b27b6375795102b3f86032a8dc239b1f6f987d76bf1aa8790876cc21c' > hand_sta27.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta28' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta28.setIP(IP, intf='sta28-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py 'a6e0b484e7a5ecd7be710b00f1c4a99ece61dd12faba06ed5946a3d68a7ce05b' > hand_sta28.txt ;'") # > auth_sta1.txt
                            print ("Handover done for ",str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta29' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta29.setIP(IP, intf='sta29-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '0a62e5746facbee83cb24cb96397a20e93cc771d634cb73fbfa8ec7c4d51bc64' > hand_sta29.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1

                        if str(sta) == 'sta30' : # and veh_ap2_hand_check[str(sta)] == 0:
                            sta30.setIP(IP, intf='sta30-wlan0')
                            x = makeTerm (sta, cmd = "bash -c 'python3 SON_Veh_Hand.py '1a08cf04df92584b2a9c3a9bb4c01f3055e58b8fc360d07de85c89e1f8759786' > hand_sta30.txt ;'") # > auth_sta1.txt
                            print ("-------- Handover done for --- ", str(sta))
                            veh_ap2_hand_check[str(sta)] = 1
                        

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()



    
