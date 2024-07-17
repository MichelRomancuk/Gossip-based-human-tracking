import socket
import ipaddress
import threading
import time
    
def update_global_gossip(filename, new_entries):
     # Read the current entries from the file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Convert the current entries to a dictionary for easy updating
    current_entries = {}
    for line in lines:
        name, node, actions = line.strip().split(';')
        current_entries[name] = (node, int(actions))

    # Parse and process the new entries
    for entry in new_entries.strip().split('\n'):
        new_name, new_node, new_actions = entry.strip().split(';')
        new_actions = int(new_actions)
        
        if new_name in current_entries:
            current_node, current_actions = current_entries[new_name]
            if new_actions > current_actions:
                current_entries[new_name] = (new_node, new_actions)
        else:
            current_entries[new_name] = (new_node, new_actions)

    # Convert the dictionary back to a list of lines
    updated_lines = [f"{name};{node};{actions}\n" for name, (node, actions) in current_entries.items()]

    # Write the updated entries back to the file
    with open(filename, 'w') as file:
        file.writelines(updated_lines)


def get_broadcast_address(ip, subnet_mask):
    network = ipaddress.IPv4Network(f'{ip}/{subnet_mask}', strict=False)
    return network.broadcast_address
    
def broadcast_message_from_file(ip, subnet_mask, port=37020):
    broadcast_address = get_broadcast_address(ip, subnet_mask)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcasting mode
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        # Read the message from the file
        # TODO; Dont send local gossip, send global gossip
        with open("local_gossip.txt", "r") as file:
            input_data = file.read().strip()
            update_global_gossip("global_gossip.txt", input_data)
            file.close()
        with open("global_gossip.txt", "r") as file:
            message = file.read().strip()
            #message = gossip_handler(message)
        # Send the message
        sock.sendto(message.encode(), (str(broadcast_address), port))
        #print(f"Message sent: {message} to {broadcast_address} \n")
        time.sleep(5)  # Broadcast every 5 seconds

def listen_for_broadcast(port=37020):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)

    print(f"Listening for broadcasts on port {port}...")

    while True:
        data, address = sock.recvfrom(4096)
        print(f"Received message: {data.decode()} from {address} \n")
        input_data = data.decode()
        update_global_gossip("global_gossip.txt", input_data)
        

if __name__ == "__main__":
    ip = '192.168.2.5'  # Your IP address
    subnet_mask = '255.255.255.0'  # Your subnet mask
    
    
    # Start the broadcast thread
    broadcast_thread = threading.Thread(target=broadcast_message_from_file, args=(ip, subnet_mask))
    broadcast_thread.daemon = True
    broadcast_thread.start()

    # Start listening for broadcasts
    listen_for_broadcast()
    
