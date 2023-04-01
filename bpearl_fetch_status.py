import socket
import ipaddress

ip_addr = input("IP address of the network card you used on this PC for connecting to Lidar: (192.168.1.102) ") or "192.168.1.102"
port = input("Port for receiving Lidar status (a.k.a DIFOP port): (7788) ") or "7788"

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest_addr = (ip_addr, int(port))
udp_socket.bind(dest_addr)
udp_socket.settimeout(5)

while True:
    try:
        receive_data, client_address = udp_socket.recvfrom(102400)
        
        if receive_data[:8]==b'\xA5\xFF\x00\x5A\x11\x11\x55\x55':
            MOT_SPD = receive_data[8:8+2]
            ETH = receive_data[10:10+22]
            FOV_SET = receive_data[32:32+4]
            MOT_PHASE = receive_data[38:38+2]
            TOP_FRM = receive_data[40:40+5]
            BOT_FRM = receive_data[45:45+5]
            SN = receive_data[292:292+6]
            ZeroAngleCalibration_btye = receive_data[298:298+2]
            ReturnMode_btye = receive_data[300:300+1]
            SOFTWARE_VER = receive_data[301:301+2]
            UTC_TIME = receive_data[303:303+10]
            STATUS = receive_data[313:313+18]
            FALT_DIGS = receive_data[342:342+40]
            GPRMC = receive_data[382:382+86]
            COR_VERT_ANG = receive_data[468:468+96]
            COR_HOR_ANG = receive_data[564:564+96]

            motor_speed_setting = int.from_bytes(MOT_SPD, byteorder='big', signed=False)

            lidar_ip = ipaddress.ip_address(ETH[0:4])
            dest_pc_ip = ipaddress.ip_address(ETH[4:8])
            mac_address = ETH[8:14]
            MSOP_port_send = int.from_bytes(ETH[14:16], byteorder='big', signed=False)
            MSOP_port_dest = int.from_bytes(ETH[16:18], byteorder='big', signed=False)
            DIFOP_port_send = int.from_bytes(ETH[18:20], byteorder='big', signed=False)
            DIFOP_port_dest = int.from_bytes(ETH[20:22], byteorder='big', signed=False)

            fov_start = int.from_bytes(FOV_SET[0:2], byteorder='big', signed=False)/100
            fov_end = int.from_bytes(FOV_SET[2:4], byteorder='big', signed=False)/100
            motor_phase = int.from_bytes(MOT_PHASE, byteorder='big', signed=False)

            motor_speed_realtime = int.from_bytes(FALT_DIGS[31:33], byteorder='big', signed=False)/6
            
            print("Top Board Firmware Version: "+TOP_FRM.hex()+"  Bottom Board Firmware Version: "+BOT_FRM.hex())
            print("Serial Number: "+SN.hex())
            print()

            print("Lidar IP: "+str(lidar_ip)+"  Dest PC IP: "+str(dest_pc_ip))
            print("MAC Address: "+":".join([mac_address.hex()[2*i:2*i+2]for i in range(6)]))
            print("MSOP Port (Send): "+str(MSOP_port_send)+"  MSOP Port (Dest): "+str(MSOP_port_dest))
            print("DIFOP Port (Send): "+str(DIFOP_port_send)+"  DIFOP Port (Dest): "+str(DIFOP_port_dest))
            print()

            print("Motor Speed Setting: "+str(motor_speed_setting)+" rpm")
            print("FOV Start: "+str(fov_start)+" degree  FOV End: "+str(fov_end)+" degree")
            print("Motor Phase: "+str(motor_phase)+" degree")
            print()

            print("Motor Speed Realtime: "+str(motor_speed_realtime)+" rpm")
            print("Return Mode: "+["Dual", "Strongest", "Last"][int.from_bytes(ReturnMode_btye, byteorder='big', signed=False)])
            print()

            print("Time: 20"+str(UTC_TIME[0])+"-"+str(UTC_TIME[1])+"-"+str(UTC_TIME[2])+" "+str(UTC_TIME[3])+":"+str(UTC_TIME[4])+":"+str(UTC_TIME[5])+"."+str(UTC_TIME[6])+str(UTC_TIME[7]))
            print("GPRMC: "+GPRMC.decode('utf-8'))
            gps_st = FALT_DIGS[15]
            print("PPS_LOCK: "+ ("OK" if (gps_st&1)==1 else "NG")+"  GPRMC_LOCK: "+ ("OK" if (gps_st>>1&1)==1 else "NG")+"  UTC_LOCK: "+ ("OK" if (gps_st>>2&1)==1 else "NG"))
            print("------------------------------------\n")

        else:
            print("Received UDP packets with wrong header. Check your ip address and port number.")

    except TimeoutError:
        print("Received no packet on "+ip_addr+":"+port+" in last 5 secs")
