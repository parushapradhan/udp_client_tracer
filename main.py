import socket
import struct

def main (HostName):
    dest_addr           = socket.gethostbyname(HostName)
    msgFromClient       = "Hello UDP Echo Service"
    bytesToSend         = str.encode(msgFromClient)
    serverPort          = 11023
    ttl                 = 1
    bufferSize          = 1024
    maxHops             = 30
    while True:
        ICMP_socket = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_ICMP) 
        ICMP_socket.bind(("",serverPort))

        UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)    
        UDP.setsockopt(0,4,ttl)
        
        UDP.sendto(msgFromClient.encode(),(dest_addr, serverPort))

        Router_addr = None
        try:
            Data, Router_addr = ICMP_socket.recvfrom(1024)
            
            ICMP_header = Data[20:28] 
            type_, code, *_ = struct.unpack('bbHHh', ICMP_header)                      
 
            if Router_addr == ('127.0.0.1', 0) : #checking if network is unresponsive
                print("***")
            else:
                print(f"{Router_addr} TTL: [{TTL}] type: [{type_}] code: [{code}]")
        except Exception as e:
            print(e)
        finally:
            ICMP_socket.close()
            UDP.close()
        
        ttl = ttl + 1
        
        if Router_addr[0] == dest_addr or ttl == maxHops:
            break
    
    
if __name__ =="__main__":
    main('ec2-3-6-93-42.ap-south-1.compute.amazonaws.com')