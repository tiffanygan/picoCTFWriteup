# [Transformation](https://play.picoctf.org/practice/challenge/104?bookmarked=1&page=1)

## Python analysis

In the problem description, they give us
an [encoded flag](https://mercury.picoctf.net/static/dd6004f51362ff76f98cb8c699510f23/enc) and the following encryption routine:

```python
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
```

Let's dissect the encryption: 

- `''.join`: This combines the resulting list of characters into a single string (our encoded flag).


- `ord(flag[i])`: Converts the current character to its ASCII value.


- `(ord(flag[i]) << 8`: Shifts the ASCII value of the character to the left by eight bits. This is equivalent to multiplying the number by 2<sup>8</sup>.


- `ord(flag[i + 1])`: Gets the ASCII value of the next character.


- `chr((ord(flag[i]) << 8) + ord(flag[i + 1]))`: Combines the first and second character's ASCII values into one integer, and converts that integer back to a character.


- `for i in range(0, len(flag), 2)`: This loop steps through the flag, two characters at a time.

In essence, the encryption combines pairs of characters into a single character (1 byte) using bit manipulation. Every two characters was combined into one large number, with the first one being the first eight bits and the second one being the second eight bits, and then converted into a character. To decrypt, we would need to reverse this process.

The code is [here](https://github.com/tiffanygan/picoCTFWriteup/blob/main/src/main/python/transformation.py).