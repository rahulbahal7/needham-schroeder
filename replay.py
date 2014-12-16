import socket
import struct
import json
from Crypto.Cipher import ARC4
import base64

with open("/home/network-auth/key") as f:
        key = f.read()

with open("/home/network-auth/blob") as b:
        blob = b.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5453))
s.sendall(struct.pack('>I', len(blob)))
s.sendall(blob)

l= struct.unpack('>I',s.recv(4))[0]
buf = s.recv(l)
enc = ARC4.new(key)
msg = json.loads(enc.decrypt(buf))
challange_nonce = msg["nonce"]
challange_nonce = challange_nonce - 1
msgfinal = json.dumps({"nonce": challange_nonce})
print msgfinal
en_msgfinal = enc.encrypt(msgfinal)
print msgfinal
s.sendall(struct.pack('>I', len(en_msgfinal)))
s.sendall(en_msgfinal)

l= struct.unpack('>I',s.recv(4))[0]
buf = s.recv(l)
secret = json.loads(enc.decrypt(buf))
print secret