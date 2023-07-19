# [PW Crack 2](https://play.picoctf.org/practice/challenge/246?page=6&search=)

## Initial exploration
After downloading the [password checker](https://artifacts.picoctf.net/c/13/level2.py) and [encrypted flag](https://artifacts.picoctf.net/c/13/level2.flag.txt.enc), my initial attempt was to open the flag, but that doesn't give us anything.

```
tiffanygan-picoctf@webshell:/tmp$ cat level2.flag.txt.enc 

TY'1qM
      :
X:]RW]J
```

Next, I ran the python script to see what it does.

```
tiffanygan-picoctf@webshell:/tmp$ python3 level2.py 
Please enter correct password for flag: password
That password is incorrect
```
## Analyzing the python script
Upon viewing the python script, we see:
```python
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

flag_enc = open('level2.flag.txt.enc', 'rb').read()



def level_2_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    if( user_pw == chr(0x64) + chr(0x65) + chr(0x37) + chr(0x36) ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return
    print("That password is incorrect")



level_2_pw_check()
```

This line provides a hint to the required password:

```python
def level_2_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    if( user_pw == chr(0x64) + chr(0x65) + chr(0x37) + chr(0x36)>
        print("Welcome back... your flag, user:")
```

In python, `chr(0x64)` is a function to convert hexadecmial to characters by [ASCII encoding](https://www.asciitable.com/). To see the characters easily (instead of checkign the table), we can add a `print` statement at the start of the `level_2_pw_check()` function, which will then display the correct password.

```python
def level_2_pw_check():
    print(chr(0x64) + chr(0x65) + chr(0x37) + chr(0x36))
```

Upon executing the script, we get:

```
tiffanygan-picoctf@webshell:/tmp$ python3 level2.py 
de76
Please enter correct password for flag: de76
Welcome back... your flag, user:
picoCTF{tr45h_51ng1ng_489dea9a}
```

So, the correct password is `de76` and our flag is `picoCTF{tr45h_51ng1ng_489dea9a}`.

It is important to note that similar to the [first PW Crack problem](https://play.picoctf.org/practice/challenge/245?page=1&search=pw), tampering with the `if` statement by setting it to always be true won't yeild the desired result, because the program requires the correct password in order to correctly decrypt the flag.

```python
decryption = str_xor(flag_enc.decode(), user_pw)
print(decryption)
```
