#!/bin/bash
# setup_network.sh
# Provisions network namespaces for 5G Network Slicing Emulation

set -e

echo "Setting up network namespaces for 5G slices..."

slices=("embb" "urllc" "mmtc")
ips=("1" "2" "3")

# Enable IP forwarding on the host kernel
sysctl -w net.ipv4.ip_forward=1

for i in "${!slices[@]}"; do
    slice="${slices[$i]}"
    idx="${ips[$i]}"
    ns="ue_${slice}"
    veth_host="veth_${slice}"
    veth_ns="veth0"
    tun_if="ogstun${idx}"
    table_id="10${idx}"

    echo "--- Configuring Slice: $slice ---"

    # [CORRECTION 2]: Clean up existing interfaces/rules so the script can be run multiple times safely
    ip netns del $ns 2>/dev/null || true
    ip link del $veth_host 2>/dev/null || true
    ip rule del from 10.${idx}.1.0/24 table $table_id 2>/dev/null || true
    
    # 1. Create Network Namespace
    ip netns add $ns
    
    # 2. Create veth pair
    ip link add $veth_host type veth peer name $veth_ns netns $ns
    
    # 3. Configure Host side of veth
    ip addr add 10.${idx}.1.1/24 dev $veth_host
    ip link set $veth_host up
    
    # 4. Configure Namespace side of veth
    ip netns exec $ns ip addr add 10.${idx}.1.2/24 dev $veth_ns
    ip netns exec $ns ip link set $veth_ns up
    ip netns exec $ns ip link set lo up
    
    # 5. Set default route inside the Namespace to the Host veth IP
    ip netns exec $ns ip route add default via 10.${idx}.1.1
    
    # [CORRECTION 1]: Policy-Based Routing on the Host
    # Create a dedicated routing table for this slice and force its traffic into the UPF TUN
    ip rule add from 10.${idx}.1.0/24 table $table_id
    ip route add default dev $tun_if table $table_id
    
    # 6. NAT/Masquerade traffic leaving the UPF tunnel
    iptables -t nat -A POSTROUTING -o $tun_if -j MASQUERADE || true
    
    echo "Successfully mapped $ns to $tun_if (Routing Table: $table_id)"
done

echo "Network namespace setup complete. Digital Twin is active."