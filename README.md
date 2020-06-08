Create strong passwords from easy-to-remember strings
==============

**strong-passgen** allows you to create a strong password from relatively simple strings in an easy method.

Pick a password seed and a service-specific name, and run the script like this:

    $ ./passgen
    Enter your salt: # for example, "banana"
    Confirm: # repeat it.
    Enter your string: example.com # creating a password for https://example.com
    Suggested username: 9b740ffa59f0
    Password copied to the clipboard. Press enter to clear.

Or, alternatively, put the service name explicitly as an argument for the script:

    $ ./passgen example.com
    Enter your salt: # for example, "banana"
    Confirm: # repeat it.
    Suggested username: 9b740ffa59f0
    Password copied to the clipboard. Press enter to clear.

If you have the `xsel` utility installed (some distros have it by default), strong-passgen automatically copies your password into the clipboard for usage. After you press Enter, it gets cleared so you don't risk pasting it elsewhere.

## Installation ##

### Dependencies

Assuming you're running Linux or something similar:

 1. `bash` or compatible shell
 2. `python3` (sorry, no more python2 support)
 3. `pygtk` for GUI (optional)

### Installing and running

Simply copy these three files into `/usr/local/bin` or the desired folder in your executable `$PATH`:

 - `passgen`
 - `passgen.py`
 - `main.py` (graphical interface)

Then run the program by invoking `passgen` or as shown in the previous section.

## Graphical Interface ##

`strong-passgen` now comes with a **graphical interface** that makes it much easier to use in text-poor environments such as Microsoft Windows and Mac that don't play very well with copying text from the command-line. It requires Python's PyGTK module, which is available from most package managers and also bundled in portable versions of Python for Windows.

To use it graphically, double-click the `main.py` file, enter a password seed and an identifier and click Generate. You can now copy the password and paste it easily into other programs and websites.

## Browser-based javascript generator ##

As the latest installment, strong-passgen has also been ported to Javascript and will run in any modern browser. You don't have to trust any website to provide it the engine for you either: download the files from the `js` folder yourself to a local folder and open `page.html` in your browser.

This way you can have your passwords anywhere you go without having to install anything!

## Motivation and improvements ##

This is a fork of the Password generator from the one in JXSelf's post:

https://jxself.org/password-generator.shtml

My modifications over the original algorithm initially included the insertion of additional methods for making the reversibility harder, and the usage of more non-alphanumeric characters through the usage of tr. However, seeing that not all base64 shell implementations work in the same way (especially for decoding), strong-passgen now implements a different algorithm, involving multiple hashing and sampling based on the input of the program.

## Limitations and security considerations ##

`strong-passgen` is a password *generator*, not a password *manager*. Functions such as secure storage and retrieval, autocomplete macros are completely out of scope. 

Although the `xsel` feature greatly reduces the risk of this happening, please note that the clearing of the clipboard after the password has been used is also your responsibility. You should immediately copy something else after usage to avoid having your password pasted somewhere unintendedly, especially when using the graphical or browser interfaces.

This software has NOT been audited from a security standpoint (I welcome somebody to do it anytime, though), and therefore should NOT be considered fail-proof. Use `strong-passgen` at your own risk!
