import socket
import ipaddress


ip_addr = input("Current IP address of Lidar: (192.168.1.200) ") or "192.168.1.200"
port = input("Current Port for data (a.k.a MSOP port): (6699) ") or "6699"

print("=============================================")

header = b'\xAA\x00\xFF\x11\x22\x22\xAA\xAA'

rpm = int(input("Motor Speed Setting: (600) ") or "600").to_bytes(2, byteorder='big', signed=False)
lidar_ip = ipaddress.ip_address(input("Lidar IP: (192.168.1.200) ") or "192.168.1.200").packed
dest_ip = ipaddress.ip_address(input("Dest PC IP: (192.168.1.102) ") or "192.168.1.102").packed
mac_addr = bytes.fromhex((input("MAC address: (00:1C:23:17:4A:CC) ") or "00:1C:23:17:4A:CC").replace(':', ''))
MSOP_port_1 = int(input("MSOP port 1 (src): (6699) ") or "6699").to_bytes(2, byteorder='big', signed=False)
MSOP_port_2 = int(input("MSOP port 2 (dest): (6699) ") or "6699").to_bytes(2, byteorder='big', signed=False)
DIFOP_port_1 = int(input("DIFOP port 1 (src): (7788) ") or "7788").to_bytes(2, byteorder='big', signed=False)
DIFOP_port_2 = int(input("DIFOP port 2 (dest): (7788) ") or "7788").to_bytes(2, byteorder='big', signed=False)
FOV_start = int(float(input("FOV start (degree, in increments of 0.01): (0) ") or "0")*100).to_bytes(2, byteorder='big', signed=False)
FOV_end = int(float(input("FOV end (degree, in increments of 0.01): (360) ") or "360")*100).to_bytes(2, byteorder='big', signed=False)

# no need to set time if you are using the external time sync feature
time = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

moter_phase_lock = int(input("Motor phase lock(degree, in increments of 1): (0) ") or "0").to_bytes(2, byteorder='big', signed=False)

payload = header + rpm + lidar_ip + dest_ip + mac_addr + MSOP_port_1 + MSOP_port_2 + DIFOP_port_1 + DIFOP_port_2 + FOV_start + FOV_end + time + moter_phase_lock

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.sendto(payload,(ip_addr,int(port)))
udp_socket.close()