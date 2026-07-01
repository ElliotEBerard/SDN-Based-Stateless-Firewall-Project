#Psuedo code
#Initiate a port table (PT); 
#For any newly received flow, F originated from the source MAC address F.SrcMAC; 
#	if F.SrcIP is new; 
#		update PT with the mapping F.SrcMAC <--> F.SrcIP; 
#	else 
#		block F.SrcMAC % Block a MAC address that had spoofed multiple IP addresses 
#end

import subprocess
import re

port_table = {}
blocked_addr = {}

def monitor_flows():
	#capture dump
	flow_dump = subprocess.run(['sudo', 'ovs-ofctl', 'dump-flows', 's1'], capture_output=True, text=True)
	#split into individual dumps	
	flows = flow_dump.stdout.splitlines()
	#optain source MAC/IP address from flows
	flow_addr = {}
	for flow in flows:
		#flow = re.split(r',', flow)
		mac_match = re.search(r'dl_src=([^,]*)', flow)
		ip_match = re.search(r'nw_src=([^,]*)', flow)
		
		if mac_match and ip_match:
			mac_addr = mac_match.group(1)
			ip_addr = ip_match.group(1)
			#store addresses
			flow_addr[mac_addr] = ip_addr
	return flow_addr

def block_address(mac_addr):
	#add flow to black malicous source MAC address
	subprocess.run(['sudo', 'ovs-ofctl', 'add-flow', 's1', 'table=0,priority=65535,dl_src=' + mac_addr + ',actions=drop'])
	blocked_addr[mac_addr] = 'blocked'
	return

print('Monitoring network activity...')

def port_monitoring():
	#continuosly monitor flows
	while True:
		flow_addr = monitor_flows()	
		for mac_addr in flow_addr:
			ip_addr = flow_addr[mac_addr] 
			#add new mapping
			if mac_addr not in port_table:
				port_table[mac_addr] = ip_addr
				print(f'new mapping added: {mac_addr} - {ip_addr}')
			#if existing MAC doesn't match correct mapping
			elif port_table[mac_addr] != ip_addr and mac_addr not in blocked_addr:
				block_address(mac_addr)
				print(f'Attack detectected! blocking MAC address {mac_addr}')

if __name__ == '__main__':
	port_monitoring()