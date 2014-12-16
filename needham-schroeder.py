import os
import json
import socket
import base64
import struct
from Crypto.Cipher import ARC4
def msgoperation(sock,m) :
        sock.sendall(struct.pack('>I', len(m)))
        sock.sendall(m)
        response = struct.unpack('>I',sock.recv(4))[0]
        buf = sock.recv(response)
        msg = json.loads(enc.decrypt(buf))
        return msg
key1='\xeb\xb0\x18\xbd\xa2\x09\xde\xbb\xc4\x5e\x77\x00\xdc\x0e\x99\xb5'
enc = ARC4.new(key1)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('127.0.0.1',5452)
sock.connect(server_address)
statInfo=os.stat("initial.json")
size=statInfo.st_size
character=chr(size)
message="\0\0\0"+character
with open("initial.json") as f:
        message+=f.read()
sock.sendall(message)
strg= struct.unpack('>I',sock.recv(4))[0]
buf = sock.recv(strg)
firstmsg = json.loads(enc.decrypt(buf))
blob_as= firstmsg["blob"]
key_ab= base64.b64decode(firstmsg["session_key"])
blob_ab=base64.b64decode(blob_as)
sock.close()
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('127.0.0.1',5453)
sock.connect(server_address)
enc=ARC4.new(key_ab)
msg = msgoperation(sock,blob_ab)
nb=msg['nonce']
nb1 = nb - 1
msgAB=json.dumps({"nonce": nb1 })
msgAB = enc.encrypt(msgAB)
msg = msgoperation(sock,msgAB)
print msg
sock.close()