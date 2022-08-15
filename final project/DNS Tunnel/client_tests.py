from client import client
import pandas as pd
import os

cli = client()

def test_send_from_file(client):
    cli.run()

test_send_from_file(cli)

# data = pd.read_csv(r'/home/dor/Desktop/packet.csv')
#
# print(data)
# print(data.info())
# print(os.getcwd())