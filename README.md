needham-schroeder
=================
The authentication and network services are using Needham-Schroeder mutual authentication. 
Messages are formatted using JSON, and RC4 is used for confidentiality. 

AUTHENTICATION

The first task is to authenticate to the network service to obtain a secret value. Your implementation must take the following into account:

The server ID must be secret.
The client ID must be your gitlab username.
Session keys and blobs are base64-encoded.
The shared secret between the authentication server and your client is the binary value eb:b0:18:bd:a2:09:de:bb:c4:5e:77:00:dc:0e:99:b5.
The operation you should perform on the challenge nonce n sent by the network service is n−1.

Messages are exchanged using JSON, where the format of the initial message to the authentication service is the following.

{
    "client_id": <gitlab_username>,
    "server_id": "secret",
    "nonce": <random_integer>
}
The remaining messages are encrypted according to the Needham-Schroeder protocol. Each message, whether encrypted or not,
is prefixed by a 32 bit big-endian value indicating the length of the following JSON object. For instance, to send the JSON message 
{"x":"y"}, a compliant client will send 00000009<message>.

Collect the secret sent to you by the network service after successful authentication.

REPLAY

Use a stolen session key and blob these values to implement the replay attack to steal a secret from the network service.