# [PW Crack 3](https://play.picoctf.org/practice/challenge/247?page=6&search=)

## Initial exploration
After downloading the [password checker](https://artifacts.picoctf.net/c/17/level3.py), [encrypted flag](https://artifacts.picoctf.net/c/17/level3.flag.txt.enc), and [hash](https://artifacts.picoctf.net/c/17/level3.hash.bin), my first attempt was to view the encrypted flag, but that doesn't give us anything.

```
tiffanygan-picoctf@webshell:/tmp$ cat level3.flag.txt.enc 
{c'UT
SVPP
    _hRP]U
```

Then, I inspected the hash content:

```
tiffanygan-picoctf@webshell:/tmp$ cat level3.hash.bin 
mU]R>W+{
```

Running the password checker provided:

```
tiffanygan-picoctf@webshell:/tmp$ python3 level3.py 
Please enter correct password for flag: password
That password is incorrect
```

With no success, it was time to dive deeper.
## Analyzing the python script
Upon opening the script, this is what we see:
```python
tiffanygan-picoctf@webshell:/tmp$ cat level3.py 
import hashlib

### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ########################
def str_xor(secret, key):
    #extend key to secret length
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)        
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])
###############################################################################

flag_enc = open('level3.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level3.hash.bin', 'rb').read()


def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()


def level_3_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    user_pw_hash = hash_pw(user_pw)
    
    if( user_pw_hash == correct_pw_hash ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return
    print("That password is incorrect")



level_3_pw_check()


# The strings below are 7 possibilities for the correct password. 
#   (Only 1 is correct)
pos_pw_list = ["f09e", "4dcf", "87ab", "dba8", "752e", "3961", "f159"]
```

Turns out, the password is given at the bottom of the script! So this problem is pretty easy, all we need to do is try the passwords to get the correct one and the flag. I updated the python file as following to iterate all the passwords. The flag is `picoCTF{m45h_fl1ng1ng_cd6ed2eb}` with the password of `87ab`.

```python
pos_pw_list = ["f09e", "4dcf", "87ab", "dba8", "752e", "3961", "f159"]

def level_3_pw_check():
    for i in range(0, len(pos_pw_list)):
        user_pw = pos_pw_list[i]
        user_pw_hash = hash_pw(user_pw)

        if( user_pw_hash == correct_pw_hash ):
            print("Welcome back... your flag, user:")
            decryption = str_xor(flag_enc.decode(), user_pw)
            print(decryption)
            return
        print("That password is incorrect")



level_3_pw_check()
```

```
tiffanygan-picoctf@webshell:/tmp$ python3 level3.py 
That password is incorrect
That password is incorrect
Welcome back... your flag, user:
picoCTF{m45h_fl1ng1ng_cd6ed2eb}
```
