#!/usr/bin/env python
from base64 import (
    b64encode,
    b64decode,
) ##hello
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import hashlib
import time
#hello
message = "I want this stream signed"
message = message.encode('utf-8')
digest = SHA256.new()
digest.update(message)
# Read shared key from file
private_key = False
with open ("private_key.pem", "r") as myfile:
    private_key = RSA.importKey(myfile.read())
# Load private key and sign message
start_sign = time.time()
signer = PKCS1_v1_5.new(private_key)

sig = signer.sign(digest)
end_sign = time.time()
print (end_sign-start_sign)
# Load public key and verify message
start_v = time.time()
verifier = PKCS1_v1_5.new(private_key.publickey())
verified = verifier.verify(digest, sig)


assert verified, 'Signature verification failed'
end_v = time.time()
print (end_v-start_v)
print ('Successfully verified message');
