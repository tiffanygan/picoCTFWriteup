# [Safe Opener 2](https://play.picoctf.org/practice/challenge/375?page=1&search=safe)

## Initial exploration
After downloading the [Java class file](https://artifacts.picoctf.net/c/286/SafeOpener.class), I first noted that it's a `.class` file. This is different from the [first Safe Opener problem](https://play.picoctf.org/practice/challenge/294?page=1&search=safe), which was a `.java` file. The `.class` file is compiled and is difficult to read directly.
## Using a Java decompiler
I used [Bytecode Viewer](https://github.com/Konloch/bytecode-viewer). Using this tool, I decompiled the `.class` file as follows:

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Base64;

public class SafeOpener {
   public static void main(String[] args) throws IOException {
      BufferedReader keyboard = new BufferedReader(new InputStreamReader(System.in));
      Base64.Encoder encoder = Base64.getEncoder();
      String encodedkey = "";
      String key = "";

      for(int i = 0; i < 3; ++i) {
         System.out.print("Enter password for the safe: ");
         key = keyboard.readLine();
         encodedkey = encoder.encodeToString(key.getBytes());
         System.out.println(encodedkey);
         boolean isOpen = openSafe(encodedkey);
         if (isOpen) {
            break;
         }

         System.out.println("You have  " + (2 - i) + " attempt(s) left");
      }

   }

   public static boolean openSafe(String password) {
      String encodedkey = "picoCTF{SAf3_0p3n3rr_y0u_solv3d_it_3dae8463}";
      if (password.equals(encodedkey)) {
         System.out.println("Sesame open");
         return true;
      } else {
         System.out.println("Password is incorrect\n");
         return false;
      }
   }
}
```

So, our flag is `picoCTF{SAf3_0p3n3rr_y0u_solv3d_it_3dae8463}`.
## Alternate methods
Instead of downloading Bytecode Viewer, we could also pair `strings` with `grep` to get the flag:

```
tiffanygan-picoctf@webshell:/tmp$ strings SafeOpener.class | grep pico
,picoCTF{SAf3_0p3n3rr_y0u_solv3d_it_3dae8463}
```

We can also use `grep` directly, but need to add the option of `-a` since it is a compiled binary file:

```
tiffanygan-picoctf@webshell:/tmp$ grep -a pico SafeOpener.class 
You have  
          z{
            z| attempt(s) left
                              }t,picoCTF{SAf3_0p3n3rr_y0u_solv3d_it_3dae8463}
                                                                             ~
                                                                              Sesame openPassword is incorrect
```
