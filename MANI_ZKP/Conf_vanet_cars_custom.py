from mininet.log import setLogLevel, info
import time, sys, os
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


    makeTerm (RSU2, cmd = "bash -c 'python3 Conf_veh_rsu_j.py;'")
    time.sleep(1)
    makeTerm (RSU1, cmd = "bash -c 'python3 Conf_veh_rsu_i.py ;'")

    veh_rsui_auth_check = {} # for initial auth
    veh_rsuj_hand_auth_check = {}  # for handover to RSU j
    
    ip_ct = 0
    while True :
        for sta in net.stations:
            if str(sta) not in veh_rsui_auth_check and sta.wintfs[0].associatedTo is not None : 
                veh_rsui_auth_check[str(sta)] = 0
                
                apx = sta.wintfs[0].associatedTo.node
                apx = str(apx)
                #veh_rsu_assoc[str(sta)] = apx
                
                print ("---- Associated to RSU1")
                if apx == 'RSU1' and veh_rsui_auth_check[str(sta)] == 0:
                    # send NVID, HPW, p(x), h(x)
                    if str(sta) == 'sta1':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '38HODY3' 't1'  > auth_sta1.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta2':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '8F9446A' 't2'  > auth_sta29.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta3':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'E9D197R' 't3'  > auth_sta30.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta4':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'VS734O2' 't4'  > auth_sta2.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta5':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'J3MSJVE' 't5'  > auth_sta3.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta6':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '4GLIA4Q' 't6'  > auth_sta4.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta7':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'H6J5EEQ' 't7'  > auth_sta5.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta8':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'DA4D1JM' 't8'  > auth_sta6.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta9':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'HPHDDUF' 't9'  > auth_sta7.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta10':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'V3S520G' 't10'  > auth_sta8.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta11':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'GYOWJJ4' 't11'  > auth_sta9.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta12':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '4XS2WB3' 't12'  > auth_sta10.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta13':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'QPUEURA' 't13'  > auth_sta11.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta14':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '03N1IE4' 't14'  > auth_sta12.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta15':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'MA6KZ3P' 't15'  > auth_sta13.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta16':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '3QGTLNN' 't16'  > auth_sta14.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta17':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'HKXE6BB' 't17'  > auth_sta15.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta18':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'QPPSDHU' 't18'  > auth_sta16.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta19':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'VF9CQHC' 't19'  > auth_sta17.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta20':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '7UIQSMF' 't20'  > auth_sta18.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta21':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'T4MT5N7' 't21'  > auth_sta19.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta22':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'GJR25NZ' 't22'  > auth_sta20.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta23':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'AHSJDW1' 't23'  > auth_sta21.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta24':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'RVNH2AQ' 't24'  > auth_sta22.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta25':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'GGJ5CN5' 't25'  > auth_sta23.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta26':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'V8PI22R' 't26'  > auth_sta24.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta27':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '476IDW5' 't27'  > auth_sta25.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta28':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'BHHLXDM' 't28'  > auth_sta26.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta29':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py '6G78XMV' 't29'  > auth_sta27.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta30':
                        # x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_auth.py 'QYVG3BW' 't30'  > auth_sta28.txt ;'") # > auth_sta1.txt
                        print ("-------- Auth done for --- ", str(sta))
                        veh_rsui_auth_check[str(sta)] = 1
                    
                    
            elif str(sta) in veh_rsui_auth_check and sta.wintfs[0].associatedTo is not None:
                apx = sta.wintfs[0].associatedTo.node
                apx = str(apx)
                #veh_rsu_assoc[str(sta)] = apx   

                if str(sta) not in veh_rsuj_hand_auth_check and apx == 'RSU2':    
                    ip_ct = ip_ct + 1
                    IP = '192.168.20.' + str(ip_ct)
                    
                    
                    if str(sta) == 'sta1':
                        sta.setIP(IP, intf='sta1-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py '3VTGCM1'	'XNIM9BX'	'7940' > hand_sta1.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta2':
                        sta.setIP(IP, intf='sta2-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'FYWW98S'	'RI37LLP'	'2589' > hand_sta2.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta3':
                        sta.setIP(IP, intf='sta3-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'W5341SO'	'TPUAS7N'	'7171' > hand_sta3.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta4':
                        sta.setIP(IP, intf='sta4-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py '1DT0269'	'28PQJKH'	'8684' > hand_sta4.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta5':
                        sta.setIP(IP, intf='sta5-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py '3IRMY7A'	'HAHBDXR'	'4506' > hand_sta5.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta6':
                        sta.setIP(IP, intf='sta6-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'H9Y4IUD'	'BC4HHZA'	'5930' > hand_sta6.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta7':
                        sta.setIP(IP, intf='sta7-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'MWXA59E'	'Y87BUDC'	'4086' > hand_sta7.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta8':
                        sta.setIP(IP, intf='sta8-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'ETVA2UX'	'O6ZM6Q7'	'7601' > hand_sta8.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta9':
                        sta.setIP(IP, intf='sta9-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'GW7GO5G'	'505216T'	'8168' > hand_sta9.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta10':
                        sta.setIP(IP, intf='sta10-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'IZUR3YP'	'7D22S44'	'5581' > hand_sta10.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta11':
                        sta.setIP(IP, intf='sta11-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py '3CIZ96C'	'IWS450I'	'7148' > hand_sta11.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta12':
                        sta.setIP(IP, intf='sta12-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'VGCZDP2'	'BHDL5XI'	'7307' > hand_sta12.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta13':
                        sta.setIP(IP, intf='sta13-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py '43I1PMM'	'EN6XPFP'	'5620' > hand_sta13.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta14':
                        sta.setIP(IP, intf='sta14-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'GQ5YE2E'	'YRXWWTY'	'7559' > hand_sta14.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta15':
                        sta.setIP(IP, intf='sta15-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'DAFHOXK'	'UMPL43M'	'4617' > hand_sta15.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta16':
                        sta.setIP(IP, intf='sta16-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'D9531SQ'	'DSQ7RVW'	'4021' > hand_sta16.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta17':
                        sta.setIP(IP, intf='sta17-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'KDW2ERM'	'W0RH13R'	'7172' > hand_sta17.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta18':
                        sta.setIP(IP, intf='sta18-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'VSGRJM2'	'B5ULUJA'	'9374' > hand_sta18.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta19':
                        sta.setIP(IP, intf='sta19-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'S76PTMW'	'0ADT9V3'	'7312' > hand_sta19.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta20':
                        sta.setIP(IP, intf='sta20-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'MX71H64'	'QTAIZEX'	'4952' > hand_sta20.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
                    elif str(sta) == 'sta21':
                        sta.setIP(IP, intf='sta21-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'IB7UQD0'	'NGWP1Y3'	'4153' > hand_sta21.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta22':
                        sta.setIP(IP, intf='sta22-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'QTP3YBP'	'RZQ8RUS'	'3343' > hand_sta22.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta23':
                        sta.setIP(IP, intf='sta23-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'XJXADMA'	'PRII9MC'	'6141' > hand_sta23.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta24':
                        sta.setIP(IP, intf='sta24-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'B38KTJI'	'HDFDMI1'	'8081' > hand_sta24.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta25':
                        sta.setIP(IP, intf='sta25-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'Q3AFCAQ'	'9GTGXTC'	'8643' > hand_sta25.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta26':
                        sta.setIP(IP, intf='sta26-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'MLHTZAA'	'QB2TJR5'	'9140' > hand_sta26.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta27':
                        sta.setIP(IP, intf='sta27-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'T7JEZXD'	'ZNQ9FSC'	'3638' > hand_sta27.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta28':
                        sta.setIP(IP, intf='sta28-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'TXQNNCR'	'DG4L3ZO'	'6153' > hand_sta28.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta29':
                        sta.setIP(IP, intf='sta29-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py '5EQUFTB'	'VWRX3LZ'	'3958' > hand_sta29.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1

                    elif str(sta) == 'sta30':
                        sta.setIP(IP, intf='sta30-wlan0')
                        x = makeTerm (sta, cmd = "bash -c 'python3 Conf_veh_hand.py 'M7NGY4H' '3YJ14Y3' '4486' > hand_sta30.txt ;'") # VID, session key, auth_suc_r > hand_sta1.txt 
                        print ("Handover done for ",str(sta))
                        veh_rsuj_hand_auth_check[str(sta)] = 1
                    
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
