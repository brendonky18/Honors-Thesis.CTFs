## *Additional Notes*
If you are unsure where to start, I would recommend reviewing the simplified [wikipedia page](https://simple.wikipedia.org/wiki/RSA_algorithm) on RSA, which contains a good walk-through example of encrypting and decrypting a message with RSA.

### Cracking User 0
The vulnerability in public key used by user 0, is that the modulus `n` is a very small number (at least as far as RSA keys are concerned). Even a naive approach to finding the prime factors should *roughly* take ~10 minutes (as tested on my own computer). Depending on how powerful your computer is, your speed will vary. A number of simple optimizations will also make this time significantly lower. 

### Cracking User 1
The vulnerability in the public key used by user 1, is that the public exponent is incredibly small, and the message is not padded at all. This means that the the message raised by the public exponent is still less than the modulus `n` used. 

### Cracking User 2
The vulnerability if the public key used by user 2, is that the two prime numbers are incredibly close to each other. Regardless of how large two primes factors are, if they are close to each other, then they can efficiently be solved for using [Fermat's factorization](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method).

***As a final reminder, please do not look at the other instructions.***