import subprocess
import re

blocked_port = {}

def monitor_flows():
	#capture dump
	flow_dump = subprocess.run(['sudo', 'ovs-ofctl', 'dump-flows', 's1'], capture_output=True, text=True)
	#split into individual dumps	
	flows = flow_dump.stdout.splitlines()
	#monitor amount of traffic from in port
	port_traffic = {}
	for flow in flows:
		in_port = re.search(r'in_port=([^,]*)', flow)
		if in_port:
			src_port = in_port.group(1)
			if src_port in port_traffic:
				port_traffic[src_port] += 1
			else:
				port_traffic[src_port] = 1
	return port_traffic

def block_port(in_port):
	#add flow to block traffic from in port
	subprocess.run(['sudo', 'ovs-ofctl', 'add-flow', 's1', 'table=0,in_port=' + in_port + ',actions=drop'])
	blocked_port[in_port] = 'blocked'
	return

print('Monitoring network activity...')

def network_monitoring():
	#continuosly monitor flows
	while True:
		port_traffic = monitor_flows()	
		for in_port in port_traffic:
			count = port_traffic[in_port] 
			#if amount traffic coming from one port exceeds certain threshold block port
			if count > 10 and in_port not in blocked_port:
				block_port(in_port)
				print(f'Malicous activity detected from port {in_port}! blocking traffic from port')

if __name__ == '__main__':
	network_monitoring()