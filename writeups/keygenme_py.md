# [keygenme-py](https://play.picoctf.org/practice/challenge/121?bookmarked=1&page=1)

## Initial exploration
Upon downloading the [python script](https://mercury.picoctf.net/static/0c363291c47477642c72630d68936e50/keygenme-trial.py), executing it reveals various options:

```
===============================================
Welcome to the Arcane Calculator, MORTON!

This is the trial version of Arcane Calculator.
The full version may be purchased in person near
the galactic center of the Milky Way galaxy. 
Available while supplies last!
=====================================================


___Arcane Calculator___

Menu:
(a) Estimate Astral Projection Mana Burn
(b) [LOCKED] Estimate Astral Slingshot Approach Vector
(c) Enter License Key
(d) Exit Arcane Calculator
What would you like to do, MORTON (a/b/c/d)? a


SOL is detected as your nearest star.
To which system do you want to travel? sun

Star not found.


___Arcane Calculator___

Menu:
...
What would you like to do, MORTON (a/b/c/d)? b


You must buy the full version of this software to use this feature!


___Arcane Calculator___

Menu:
...
What would you like to do, MORTON (a/b/c/d)? c

Enter your license key: test

Key is NOT VALID. Check your data entry.


___Arcane Calculator___

Menu:
...
What would you like to do, MORTON (a/b/c/d)? d
Bye!
```

* Option `a` doesn't appear to have a significant function
* Option `b` is locked
* Option `d` exits the game
* Option `c` is our main point of interest, as it prompts us for a key (most likely our flag)

## Analyzing the python script
The python script is a pretty long file, so let's focus on the two most important bits.

Near the beginning of the file, we have some details about our trial, including the username and part of the flag.

```python
username_trial = "MORTON"
bUsername_trial = b"MORTON"

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
```

The other important part is the `check_key` function:

```python
def check_key(key, username_trial):

    global key_full_template_trial

    if len(key) != len(key_full_template_trial):
        return False
    else:
        # Check static base key part --v
        i = 0
        for c in key_part_static1_trial:
            if key[i] != c:
                return False

            i += 1

        # TODO : test performance on toolbox container
        # Check dynamic part --v
        if key[i] != hashlib.sha256(username_trial).hexdigest()[4]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[5]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[3]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[6]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[2]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[7]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[1]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[8]:
            return False



        return True
```

This function validates the license key. It first checks the static part of the key, and then compares the dynamic part with the hashed username. So we need to reverse engineer this process to obtain the complete flag.

Just for fun, once you have the flag, you can give it to the program to unlock the full version of the game.

The code is [here](https://github.com/tiffanygan/picoCTFWriteup/blob/main/src/main/python/keygenme_py.py)