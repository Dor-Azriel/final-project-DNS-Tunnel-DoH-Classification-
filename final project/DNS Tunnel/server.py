#import scapy

import socket
import ssl
import sys
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import createCertificate


class Server:

    clients_list = []
    senders_list=[]

    last_received_message = ""

    def __init__(self):
        self.key_socket = None
        self.server_socket = None
        self.public_key=None
        self.private_key=None
        self.init_keys()
        self.create_listening_server()
        createCertificate()

    #listen for incoming connection

    def init_keys(self):
        key = RSA.generate(1024)
        pri = key.exportKey()
        pub = key.publickey().exportKey()
        self.private_key = RSA.importKey(pri)
        self.public_key = RSA.importKey(pub)
        #print(self.public_key.exportKey())


    def create_listening_server(self):

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('selfsigned.crt', 'private.key')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('127.0.0.1', 8443))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as socc:
                print("**")
                self.server_socket = socc
        print ("server is listening on port 443 for new connections  ")
        self.receive_messages_in_a_new_thread()
    #fun to receive new msgs

    def receive_messages(self, client):
        so,(ip,port)=client[0]
        key=client[1]
        while True:
            incoming_buffer = so.recv(1024) #initialize the buffer
            print(incoming_buffer)
            if not incoming_buffer:
                break
            try:
                if incoming_buffer[:3]=="key" and not key:
                    key=incoming_buffer.split(".",2)[1]
                    client= (client[0],key)
                    self.senders_list.append(client)
                    incoming_buffer=None
                    #print(client)
            except:
                print ("worng init client")
            if incoming_buffer:
                print(self.last_received_message)
                self.last_received_message=self.decrypt_msg(incoming_buffer,key)
        so.close()



    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            key=None
            client=(client,key)
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(client,))
            t.start()

    #add a new client
    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            soc,(ip,port)=client[0]
            key=client[1]
            print(self.public_key.exportKey())
            soc.sendall(self.public_key.exportKey())
            self.clients_list.append(client)

    def padd_message(self,msg):
        while len(msg)%16!=0:
            msg+=" "
        return msg

    def unpadd_message(self,msg):
        return msg.strip(" ")

    def encrypt_msg(self,msg,key):
        msg=self.padd_message(msg)
        rand_vector= os.urandom(16)
        enc_chiper = AES.new(key,AES.MODE_CBC,rand_vector)
        return rand_vector+enc_chiper.encrypt(msg)

    def decrypt_msg(self,msg,key):
        rand_vector=msg[:16]
        print("----------------rand_vector----------------")
        print(rand_vector)
        print("-----------message before decrypt----------")
        print(msg)
        dec_chiper = AES.new(key,AES.MODE_CBC,rand_vector)
        return dec_chiper.decrypt(msg[16:])


if __name__ == "__main__":
    Server()