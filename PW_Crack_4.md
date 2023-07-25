# [PW Crack 4](https://play.picoctf.org/practice/challenge/248?page=7&search=)

## Initial exploration
After downloading the [password checker](https://artifacts.picoctf.net/c/21/level4.py), [encrypted flag](https://artifacts.picoctf.net/c/21/level4.flag.txt.enc), and [hash](https://artifacts.picoctf.net/c/21/level4.hash.bin), I quickly discovered that the encrypted flag and hash files were of no immediate use. Running the Python script merely prompted for a password.
## Analyzing the python script
Upon opening the script, this is what we see:

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

flag_enc = open('level4.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level4.hash.bin', 'rb').read()


def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()


def level_4_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    user_pw_hash = hash_pw(user_pw)
    
    if( user_pw_hash == correct_pw_hash ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return
    print("That password is incorrect")



level_4_pw_check()



# The strings below are 100 possibilities for the correct password. 
#   (Only 1 is correct)
pos_pw_list = ["8c86", "7692", "a519", "3e61", "7dd6", "8919", "aaea", "f34b", "d9a2", "39f7", "626b", "dc78", "2a98", "7a85", "cd15", "80fa", "8571", "2f8a", "2ca6", "7e6b", "9c52", "7423", "a42c", "7da0", "95ab", "7de8", "6537", "ba1e", "4fd4", "20a0", "8a28", "2801", "2c9a", "4eb1", "22a5", "c07b", "1f39", "72bd", "97e9", "affc", "4e41", "d039", "5d30", "d13f", "c264", "c8be", "2221", "37ea", "ca5f", "fa6b", "5ada", "607a", "e469", "5681", "e0a4", "60aa", "d8f8", "8f35", "9474", "be73", "ef80", "ea43", "9f9e", "77d7", "d766", "55a0", "dc2d", "a970", "df5d", "e747", "dc69", "cc89", "e59a", "4f68", "14ff", "7928", "36b9", "eac6", "5c87", "da48", "5c1d", "9f63", "8b30", "5534", "2434", "4a82", "d72c", "9b6b", "73c5", "1bcf", "c739", "6c31", "e138", "9e77", "ace1", "2ede", "32e0", "3694", "fc92", "a7e2"]
```

Similar to the previous problem, [PW Crack 3](https://play.picoctf.org/practice/challenge/247?page=6&search=), we are given a list of possible passwords, with only one being the correct one. However, in the previous problem, there were only 7 possible passwords, so it was easy to try them one by one. Since there are now 100 possible passwords, it doesn't make sense to do the same thing. As such, I adapted the code to automatically go through the list and identify the correct one.

The result:

```
tiffanygan-picoctf@webshell:/tmp$ python3 level4.py 
Welcome back... your flag, user:
picoCTF{fl45h_5pr1ng1ng_d770d48c}
```
## Modified code
I tweaked the `level_4_pw_check` function to accept a password as an argument and removed the user input prompt. I also removed the "incorrect password" message to declutter the output. Finally, I added a `for` loop at the end to automate the password checking process.

As a reference, here is the changed code:

```python
def level_4_pw_check(user_pw):
    user_pw_hash = hash_pw(user_pw)
    
    if( user_pw_hash == correct_pw_hash ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return

# The strings below are 100 possibilities for the correct password. 
#   (Only 1 is correct)
pos_pw_list = ["8c86", "7692", ... "fc92", "a7e2"]

for pw in pos_pw_list:
    level_4_pw_check(pw)
```
