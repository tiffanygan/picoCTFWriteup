# [Mind your Ps and Qs](https://play.picoctf.org/practice/challenge/162?bookmarked=1&page=1)

## Understanding RSA encryption
For a detailed review of RSA encryption and decryption, refer to the [picoPrimer chapter 6.5.2](https://primer.picoctf.org/#_modern_cryptography:~:text=6.5.2.%20Asymmetric%20crypto%20example%3A%20RSA).

From the [download](https://mercury.picoctf.net/static/3cfeb09681369c26e3f19d886bc1e5d9/values), we are given c (encrypted message), n, and e. Together, n and e make up the public key. So we will need to find the private key, d.

1. Start by factorizing n. A useful tool is [factordb](http://factordb.com/).


2. Once we have the two coprime factors, p and q, we can calculate phi, which is (p-1) * (q-1).


3. d will be the inverse modulo of e with respect to phi.


4. The numeric version of the message (m) is c<sup>d</sup> % n


5. Convert m to binary, and then into bytes to reveal the flag.

The code is [here](https://github.com/tiffanygan/picoCTFWriteup/blob/main/src/main/python/mind_your_ps_and_qs.py).