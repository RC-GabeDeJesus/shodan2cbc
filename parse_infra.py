import re
import ipaddress

def extract_unique_post_ex_spawnto(file):
    unique_values = set()
    # Pattern now includes .exe at the end
    pattern = re.compile(r'(post-ex.spawnto_x(86|64)): (.*\.exe)(,|\n)')

    with open(file, 'r') as f:
        content = f.read()
        matches = pattern.findall(content)
        
        for match in matches:
            # Split by backslash and take the last part to get the filename only
            filename = match[2].split("\\")[-1]
            unique_values.add(filename)
    
    return list(unique_values)


def extract_unique_ip_addresses(file):
    unique_ips = set()
    # Regular expression pattern for IP address
    pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    with open(file, 'r') as f:
        content = f.read()
        matches = pattern.findall(content)
	# We need to exclude private IP addresses        
        for match in matches:
            ip_address = ipaddress.ip_address(match)
            if not ip_address.is_private:
	            unique_ips.add(match)
    
    return list(unique_ips)

def create_search_query(unique_values, unique_ips):
    value_query = " OR ".join([f"process_name:{value}" for value in unique_values])
    ip_query = " OR ".join([f"netconn_ipv4:{ip}" for ip in unique_ips])
    return f"({value_query}) AND ({ip_query})"


unique_values = extract_unique_post_ex_spawnto('shodan_results.csv')
unique_ips = extract_unique_ip_addresses('shodan_results.csv')

print(create_search_query(unique_values, unique_ips))

