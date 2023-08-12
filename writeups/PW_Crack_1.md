# [PW Crack 1](https://play.picoctf.org/practice/challenge/245?page=1&search=pw)

## Initial exploration
After downloading the [password checker](https://artifacts.picoctf.net/c/11/level1.py) (a python script) and [encrypted flag](https://artifacts.picoctf.net/c/11/level1.flag.txt.enc), my initial attempt was to open the encrypted flag, but all we get is some gibberish.

```
tiffanygan-picoctf@webshell:/tmp$ cat level1.flag.txt.enc 
A
 Rr1wQ  nVT_nPRVWtiffanygan-picoctf@webshell:/tmp$
```

Since that didn't work, I tried running the python script to get a sense of what it does.

```
tiffanygan-picoctf@webshell:/tmp$ python3 level1.py 
Please enter correct password for flag: hi
That password is incorrect
```
## Analyzing the python script
It looks like we'll need to take a look at the code in order to find out what the password is. After opening the python using `nano level1.py`, we get this code:

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


flag_enc = open('level1.flag.txt.enc', 'rb').read()



def level_1_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    if( user_pw == "1e1a"):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return
    print("That password is incorrect")



level_1_pw_check()
```

The function `level_1_pw_check()` check's the user-provided password with the correct one. A few lines down, we see:

```python
if( user_pw == "1e1a"):
        print("Welcome back... your flag, user:")
```

So this means that the password should be "1e1a." The code after it reads the encrypted flag and decrypts it.
When we try entering "1e1a" as the password, we get our flag, `picoCTF{545h_r1ng1ng_fa343060}`.

```
tiffanygan-picoctf@webshell:/tmp$ python3 level1.py 
Please enter correct password for flag: 1e1a
Welcome back... your flag, user:
picoCTF{545h_r1ng1ng_fa343060}
```
## Why a certain method would not work
However, it's essential to note that simply tampering with the code to make the if statement always evaluate as true would not yield the desired result. For instance, if we change the line:

```python
if( user_pw == "1e1a"):
```

to:

```python
if( True):
```

The program _does_ run but does _not_ give the flag. Running the program with a password of "notThePassword", for example, returns:

```
Please enter correct password for flag: notThePassword
Welcome back... your flag, user:
/c&ZT'{w"sfsn`"7c>b#!r9s3ow
```

As a matter of fact, the script relies on the correct password in order to decrypt the flag, as shown below:

```python
decryption = str_xor(flag_enc.decode(), user_pw)
```

So anything other than the correct password ("1e1a") will not work.
