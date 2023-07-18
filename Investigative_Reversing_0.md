# [Investigative Reversing 0](https://play.picoctf.org/practice/challenge/70?page=1&search=inv)

## Running binary
After downloading the [binary file](https://jupiter.challenges.picoctf.org/static/70fd416f817ab1e59beaf19dc2b586cd/mystery) and [image](https://jupiter.challenges.picoctf.org/static/70fd416f817ab1e59beaf19dc2b586cd/mystery.png), the first thing I tried was running the binary file `mystery`. In order to do that, we first need to make the file runnable, so `chmod a+x mystery`. Now that it's converted, we can run it. However, the output is

```
No flag found, please make sure this is run on the server
Segmentation fault (core dumped)
```
## Steganography
Since the problem also comes with an image, it's possible that this is a steganography problem. I first checked if the file is an image using `file mystery.png`. It is indeed an image. Next, I try using `binwalk -e mystery.png`, `strings mystery.png | grep picoCTF`, and `exiftool image` to see if I can find the flag. Nothing there! Finally, I check the image using a hexeditor, `xxd mystery.png`. At the very bottom, we find

```
0001e870: 4260 8270 6963 6f43 544b 806b 357a 7369  B`.picoCTK.k5zsi
0001e880: 6436 715f 6431 6465 6564 6161 7d         d6q_d1deedaa}
```

So our "flag" is `picoCTK.k5zsid6q_d1deedaa}`.
Alternatively, you could also use `zsteg` to find the "flag". Note that `zsteg` isn't included in the webshell, so you will have to run it on your own terminal. (I used [this toolkit](https://github.com/DominicBreuker/stego-toolkit) from a Docker image.)

What we have now is most likely an encrypted version of the flag. Since it begins with picoCTK and not picoCTF, we weren't able to find it with `strings`. However, if we try running `strings mystery.png | grep pico` it will output part of the encrypted flag, but not the whole thing.
## Decrypting the flag
We now have the encrypted flag. However, we don't know how to decrypt it. The code for that is likely contained in the downloaded binary file, but we can't read it as is (ie using `cat binary` to see the instructions). We _could_ use `gdb`, but this means that we would need to read and understand assembly code, which is a bit difficult. In order to translate the binary to C, you will need Ghidra (pronounced [gee-druh](https://github.com/NationalSecurityAgency/ghidra/issues/61)). You can download it from Github [here](https://github.com/NationalSecurityAgency/ghidra/releases). There is also an [installation guide](https://ghidra-sre.org/InstallationGuide.html#Install). **Note that Ghidra will require a Java version of at least 11.**

To run Ghidra, run the binary file `./ghidraRun`. If you have any issues running Ghidra, check [this](https://github.com/NationalSecurityAgency/ghidra/issues/3477).

Next, we need to add the binary file to Ghidra so we can check it. Your screen should look somewhat like this:

![image](https://github.com/tiffanygan/picoCTFWriteup/assets/29723267/6b382c45-35c4-4133-8588-f7c03158d32f)

To open the file, double click on it or press the green dragon located under "Tool Chest," click File (top left corner), Open, and select `mystery`. In order to see the C version of the file, go to Symbol Tree (left side), Functions, main.

![image](https://github.com/tiffanygan/picoCTFWriteup/assets/29723267/35d7514a-702d-457c-8a66-805074812294)

The C code should look like this:

![image](https://github.com/tiffanygan/picoCTFWriteup/assets/29723267/626caaa9-9243-4627-8108-d20677d91c45)

* In lines 18-19, the code is opening `flag.txt` (which obviously was removed afterwards) and embedding it into the image, `mystery.png`. Next, we need to find out how the flag was encoded and reverse the process.

* Lines 32-37 don't do anything, they just add the first 6 characters to the encrypted flag. That's why the first part of the flag, picoCT, wasn't encoded.

```C
  fputc((int)local_38[0],__stream_00);
  fputc((int)local_38[1],__stream_00);
  fputc((int)local_38[2],__stream_00);
  fputc((int)local_38[3],__stream_00);
  fputc((int)local_34,__stream_00);
  fputc((int)local_33,__stream_00);
```

* Lines 38-40 after add `\x05` to each character, so we simply need to subtract `\x05`.

```C
  for (local_54 = 6; local_54 < 0xf; local_54 = local_54 + 1) {
    fputc((int)(char)(local_38[local_54] + '\x05'),__stream_00);
  }
```

* Line 41 subtracts 3 from a single character, so we will need to add 3 back to it.

```C
  fputc((int)(char)(local_29 + -3),__stream_00);
```

* Lines 42-44 add 1 to each character, so we will need to subtract 1.

```C
  for (local_50 = 0x10; local_50 < 0x1a; local_50 = local_50 + 1) {
    fputc((int)local_38[local_50],__stream_00);
  }
```

After putting all the pieces back together, we should get the decrypted version of the flag `picoCTF{f0und_1t_d1deedaa}`.

As a reference, here is the python code I wrote:

```python
with open('mystery.png', 'rb') as f:
    b = f.read()

print(b[-26:])
# Getting the last 26 characters, since the flag is 26 characters long and located at the end

encoded_flag = b[-26:]  # This is an array of bytes
decoded_flag = []  # This will be an array of chars
decode_start_idx = 6  # This is where we actually start decoding. The first part (picoCT) is ok already
decode_end_idx = 0xf  # This is where the first part of the encryption ends (line 40)

for i in range(decode_start_idx):
    decoded_flag.append(chr(encoded_flag[i]))  # Adding picoCT to the decoded flag

for i in range(decode_start_idx, decode_end_idx):
    decoded_flag.append(chr(encoded_flag[i] - 5))  # Subtracting 5 (reversing lines 38-40)

decoded_flag.append(chr(encoded_flag[decode_end_idx] + 3))  # Reversing line 41

for i in range(decode_end_idx + 1, 26):
    decoded_flag.append(chr(encoded_flag[i]))  # Reversing lines 42-44

print("".join(decoded_flag))  # Joining all of the decoded chars together to form the flag
```

