import ssl

#import client
import requests
from OpenSSL import SSL
import socket


#
# url = 'https://1.1.1.1'
# client = requests.session()
# params = {
#
#     'name':'asdsdsadsad.finalprojectsce2022.com',
#     'type':'A',
#     'ct':'application/dns-json'
# }
# res = client.get(url,params=params)
# print(res.text)
# hostname = "www.finalprojectsce2022.com"
# context = ssl.create_default_context()
#
# with socket.create_connection((hostname,443)) as sock:
#     with context.wrap_socket(sock,server_hostname=hostname) as sockk:
#         print (sockk.version())
#ssl.get_server_certificate(('127.0.0.1',443),)
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain('selfsigned.crt','private.key')
#
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
#     sock.bind(('127.0.0.1',8443))
#     sock.listen(5)
#     with context.wrap_socket(sock,server_side=True) as socc:
#         print("**")
#         conn,adrr = socc.accept()
#         print("**")
#     while True:
#         print("ssss")
#         print(socc.recv(1024))

path = "/home/dor/Desktop/new.txt"
file = open(path,"r")
print(file.read())