# Instruction Set 1
## *Additional Notes*
If you are unsure where to start, I would recommend reviewing the simplified [wikipedia page](https://simple.wikipedia.org/wiki/RSA_algorithm) on RSA, which contains a good walk-through example of encrypting and decrypting a message with RSA.

### Cracking User 0
The vulnerability in public key used by user 0, is that the modulus `n` is a very small number (at least as far as RSA keys are concerned).

### Cracking User 1
The vulnerability in the public key used by user 1, is that the public exponent is incredibly small, and the message is not padded at all. 

### Cracking User 2
The vulnerability if the public key used by user 2, is that the two prime numbers are incredibly close to each other. 

## *Still Stuck*
If you have any other questions, you can reach out to me at bky@umass.edu. 

***As a final reminder, please do not look at the other instructions.***
