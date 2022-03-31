# Instruction Set 2
## *Additional Notes*
If you are unsure where to start, I would recommend reviewing the simplified [wikipedia page](https://simple.wikipedia.org/wiki/RSA_algorithm) on RSA, which contains a good walk-through example of encrypting and decrypting a message with RSA.

### Cracking User 0
To view the messages being transmitted, connect to user 0 with the `remote_pcap.sh` script. 
This should launch wireshark and reveal quite a lot of traffic, we only care about a small portion of this.
In the display filter text box on top, enter the filter `tcp.flags.push==1`. 
This will show us only the messages we're interested in.
The client will contact the server a couple of times a minute.
To start we need to get the public key. 
Look for a message coming from the server that says `RSA_KEY_ACK`. 
This message will contain two other fields: `E` and `N`, which correspond to the public exponent and modulus respectively.
Together, these two numbers make the public key.
The vulnerability in public key used by user 0, is that the modulus `N` is a very small number (at least as far as RSA keys are concerned). 
Even a naive brute-force approach to finding the prime factors should only take ~10 minutes (as tested on my own computer). 
Depending on how powerful your computer is, your speed will vary. 
A number of simple optimizations will also make this time significantly lower. 
Once you've calculated the two factors `p` and `q`, you can easily use them to calculate the private key `d`. 
`d` is the [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of e (mod φ(n)). 
φ(n) is [Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function), and is equal to the LCM of `p-1` and `q-1`, given that `n=pq`.
Since we now know all of these values, it is trivial to calculate the secret key `d`.
In python, it can be calculated simply as `d=pow(e, -1, (p-1)*(q-1))`.
This use of the `pow` function requires at least python 3.8.
You can then use this private key to decrypt the symmetric key. 
The encrypted symmetric key is sent in a `SECRET_FLAG` message, in the field `XOR_KEY`, and the encrypted flag is in the field `ENC_FLAG`
Once you have the symmetric key, you xor it with the encrypted flag to reveal the flag. 
You then use this to get the password for the next user.

### Cracking User 1
The vulnerability in the public key used by user 1, is that the public exponent is incredibly small, and the message is not padded at all. This means that the the message raised by the public exponent is still less than the modulus `n` used. Because the encoded message (the symmetric key) `c` is calculated by taking the plain message to the power of `e`, you can reverse this process to get the symmetric key. Simply calculate the original message by taking the `e`th root of `c`, `c^(1/e)`.

### Cracking User 2
The vulnerability in the public key used by user 2, is that the two prime numbers are incredibly close to each other. Regardless of how large two primes factors are, if they are close to each other, then they can efficiently be solved for using [Fermat's factorization](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method). Using this approach will easily reveal the two factors. Once you have these, you can use the same approach from the first stage to reveal the symmetric key, and then the final flag.

***As a final reminder, please do not look at the other instructions.***
