import socket
import sys
from datetime import datetime

def banner_grabber(ip, port):
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        
       
        if port in [80, 8080]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        return banner if banner else "No banner retrieved"
    except:
        return "No banner retrieved"

def scan_target(target, ports):
   
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("\n[!] Error: Hostname could not be resolved.")
        return

    print("=" * 50)
    print(f" Scanning Target: {target_ip}")
    print(f" Time started: {str(datetime.now())}")
    print("=" * 50)

    for port in ports:
        try:
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
        
            result = s.connect_ex((target_ip, port))
            
            if result == 0:
                print(f"[+] Port {port}: OPEN")
               
                banner = banner_grabber(target_ip, port)
                if banner != "No banner retrieved":
                    print(f"    └── Banner: {banner[:60]}...")
            s.close()

        except KeyboardInterrupt:
            print("\n[!] Exiting Scanner.")
            sys.exit()
        except socket.error:
            print(f"\n[!] Could not connect to server.")
            sys.exit()

if __name__ == "__main__":
   
    target_host = input("Enter Target IP or Hostname (e.g., scanme.nmap.org): ")
    
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
    
    scan_target(target_host, common_ports)
