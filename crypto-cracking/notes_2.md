## *Additional Notes*
If you are unsure where to start, I would recommend reviewing the simplified [wikipedia page](https://simple.wikipedia.org/wiki/RSA_algorithm) on RSA, which contains a good walk-through example of encrypting and decrypting a message with RSA.

### Cracking User 0
The vulnerability in public key used by user 0, is that the modulus `n` is a very small number (at least as far as RSA keys are concerned). Even a naive brute-force approach to finding the prime factors should *roughly* take ~10 minutes (as tested on my own computer). Depending on how powerful your computer is, your speed will vary. A number of simple optimizations will also make this time significantly lower. Once you've calculated the two factors `p-1` and `q-1`, you can easily use them to calculate the private key. You can then use this private key to decrypt the symmetric key. Once you have the symmetric key, you xor it with the cipher text to reveal the secret message. You then enter this message as the password to unlock the next stage.

### Cracking User 1
The vulnerability in the public key used by user 1, is that the public exponent is incredibly small, and the message is not padded at all. This means that the the message raised by the public exponent is still less than the modulus `n` used. Because the encoded message (the symmetric key) `c` is calculated by taking the plain message to the power of `e`, you can reverse this process to get the symmetric key. Simply calculate the original message by taking the `e`th root of `c`, `c^(1/e)`.

### Cracking User 2
The vulnerability in the public key used by user 2, is that the two prime numbers are incredibly close to each other. Regardless of how large two primes factors are, if they are close to each other, then they can efficiently be solved for using [Fermat's factorization](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method). Using this approach will easily reveal the two factors. Once you have these, you can use the same approach from the first stage to reveal the symmetric key, and then the final flag.

***As a final reminder, please do not look at the other instructions.***
