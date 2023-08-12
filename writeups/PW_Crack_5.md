# [PW Crack 5](https://play.picoctf.org/practice/challenge/249?page=1&search=pw)

## Initial exploration
After downloading the provided files: [password checker](https://artifacts.picoctf.net/c/32/level5.py), [encrypted flag](https://artifacts.picoctf.net/c/32/level5.flag.txt.enc), [hash](https://artifacts.picoctf.net/c/32/level5.hash.bin), and [dictionary](https://artifacts.picoctf.net/c/32/dictionary.txt), I first opened all of the files to see what was inside and tried running the python script.
## Analyzing the python script
After opening the python script, this is what we see:

```python
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

flag_enc = open('level5.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level5.hash.bin', 'rb').read()


def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()


def level_5_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    user_pw_hash = hash_pw(user_pw)
    
    if( user_pw_hash == correct_pw_hash ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return
    print("That password is incorrect")



level_5_pw_check()
```

Similar to what I did in the [previous PW Crack problem](https://play.picoctf.org/practice/challenge/248?page=7&search=), I will be writing a python script to go through the passwords in the `dictionary` file to find the correct one.

The result:

```
tiffanygan-picoctf@webshell:/tmp$ python3 level5.py 
Welcome back... your flag, user:
picoCTF{h45h_sl1ng1ng_40f26f81}
```
## Modified code
I refactored the `level_5_pw_check` function to accept a password as an argument (`user_pw`), replacing the user input prompt. This allowed for an iterative call with each dictionary password. Furthermore, I loaded the potential passwords from `dictionary.txt` into a list and used a `for loop` to check each password.

As a reference, here is the code that I changed:

```python
def level_5_pw_check(user_pw):
    user_pw_hash = hash_pw(user_pw)
    
    if( user_pw_hash == correct_pw_hash ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return

dictionary = open('dictionary.txt', 'r').read().split()
for pw in dictionary:
    level_5_pw_check(pw)
```
