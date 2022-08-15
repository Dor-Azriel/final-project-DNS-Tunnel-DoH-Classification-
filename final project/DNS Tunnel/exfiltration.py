from Crypto import Random

class exfiltration ():
    def padd_message(self, msg):
        while len(msg) % 16 != 0:
            msg += " "
        return msg


    def unpadd_message(self, msg):
        return msg.strip(" ")
