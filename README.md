# SDN-Based-Stateless-Firewall-Project
Custom mininet topology configuration file

# Running POX controller on port 6655 using custom l2 and l3 configuration files
sudo ./pox.py openflow.of_01 --port=6655 forwarding.l2_learning forwarding.L3Firewall --l2config="l2firewall.config" --l3config="l3firewall.config"