import socket
import sys
import base64
import struct
import urllib.request
from dns import resolver
import requests
import dns
import ssl
import http.client
import hashlib
from OpenSSL import SSL
from Crypto import Random
from Crypto.PublicKey import RSA
from datetime import datetime
import scapy
#key =hashlib.sha256("passs")
# con = http.client.HTTPSConnection("www.cloudflare-dns.com",443)
# con.putrequest('GET','/')
# con.endheaders()
# r=con.getresponse()
# print(r.read())
# con.request('GET','/dns-query')
# print("####################################")
# r=con.getresponse()
# #print(r.read())
# print("zzzzzzzzzzzzzzzzzz")

print(datetime.now())
key =hashlib.sha256(Random.get_random_bytes(256)).digest()
print(len(key))
print (key)
url="https://cloudflare-dns.com/dns-query"
client= requests.session()
b=base64.urlsafe_b64encode(b"trytosxcxcxzxcxzcxcend this message")
params={
    'name': 'www.google.com',
    'type': 'A',
    'ct':   'application/dns-json',
}

#respo= dns.query.https(dns.message.Message("sdsdsdsd"),"https://www.facebook.com/nike")
#print(respo)
res = client.get(url,params=params)
print(res.status_code)
print(client.cert)
print("huhuhu")
print(res.text)
print("------------------------")
urlopen = urllib.request.urlopen
url_request = urllib.request.Request
server = "1.1.1.1"
path= "/dns-query"

localIp="127.0.0.1"
port= "443"
buffer = 1024
ssl._create_default_https_context = ssl._create_unverified_context
DOH_SERVER_1 = "1.1.1.1"
path = "/dns-query"
data=base64.b64encode(b"/nike")
name=base64.b64encode(b"www.finalprojectsce2022.com'")
print(name)
#name= name+data
print(name)
type="A"
req = url_request("https://%s%s?name=%s&type=%s" % (server,path,name,type),headers={"Accept": "application/dns-json"})
print(req)
ans = urlopen(req).read().decode()
print(ans)
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#soc2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print("Xxxxxx")
soc.connect(("www.google.com",443))
print("Xxxxxx")

#soc.send(b'GET / HTTP/1.1\r\n ')

print("Xxxxxx")

# while True:
#     print("run")
#     #soc2.bind((localIp,port))
#     print(soc.recv(65565))
#     packet=soc.recv(65565)
#     packet=struct.unpack("AAAAAAAAAAAA",packet)
#     print(packet)



#params for Cloudflare + google resolver api
params={
    'user-agent':'Mozilla/5.0',
    'name': b+b'.finalprojectsce2022.com',
    'type': 'A',
    'ct':   'application/dns-json',
}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket using TCP port and ipv4
#self.key_socket = ssl.create_default_context().wrap_socket(self.server_socket, server_side=Tru
local_ip = '127.0.0.1'
local_port = 443
# this will allow you to immediately restart a TCP server
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# this makes the server listen to requests coming from other computers on the network
#server_socket.bind((local_ip, local_port))
print("Listening for incoming messages..\n The amount of users in parallel is: " )
server_socket.listen() #listen for incomming connections / max 5
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind((local_ip, local_port))
client_socket.listen(100)
conn,addr = client_socket.accept()
while True:
    res= conn.recv(1024)
    print(res)