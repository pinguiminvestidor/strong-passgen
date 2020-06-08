#!/usr/bin/env python3
#
# This is a port of classical passgen (provided by jxself) into the python 
# language.
#
# Usage: passgen.py [service-specific string]
#
# Use this program if you do not have access to a graphical environment or if
# you can't install PyGTK. Otherwise, run main.py
# 
#    Copyright (C) 2020 - Pinguim Investidor <https://pinguiminvestidor.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import base64 as b64
import hashlib
from getpass import getpass

#---- Standard configuration variables:

seclevel = 7 # how many times tokens are hashed

#---- Functions:

def secure_hash(token, times=seclevel):
    """
    Hashes multiple times a given string so as to provide something that should
    not be easy to reverse. Standardized as seven times, but feel free to 
    change it to as much as your own paranoia needs.

    Returns a SHA-256 hash.
    """
    temp = str(token)
    for i in range(times):
        temp = hashlib.sha256(temp.encode()).hexdigest()
    return temp

def generate(salt, string):
    """
    Generates a 32-char long password based on the new algorithm.
    Arguments are a password seed (called a salt) and a service-specific string
    so all passwords generated will be different.

    The 32 characters are sampled from a different position depending on the
    salt used. This should always work provided that the salt isn't too long.
    """

    # So that the sampling is not that obvious ;)
    start = len("%s%s" % (salt, string)) 

    temp = secure_hash("%s%s" % (salt, string))
    encoded_str = b64.b64encode(temp.encode())[start:start+32]
    return encoded_str.decode()

#----------
# Hey, if we can create passwords, why not create a username as well to tie 
# everything together? That would be one less thing to memorize!

def generate_name(salt, string):
    """
    Generates a 12-char long username from the hashed combination. WIP.
    SHA-256 is always 64-characters in length, so we could take a nice slice
    all the way until the 56th character.
    """
    start = len("%s%s" % (salt, string))
    return secure_hash("%s%s" % (salt, string))[start:start+12]


def main():
    """
    Main interaction when module has not been imported
    It now can be used in a script, like this:
        passgen.py SALT SERVICE

        passgen.py -u SALT SERVICE (for usernames)

    Which is what `passgen` will be using to generate its own.
    """

    if "-u" in sys.argv:
        # for usernames
        print(generate_name(sys.argv[2], sys.argv[3]))
        sys.exit(0)

    if len(sys.argv) < 3: # no arguments passed, or a single SERVICE string
        while True:
            seed = getpass("Enter your salt: ")
            seed_confirm = getpass("Confirm: ") 
            
            if seed == seed_confirm:
                break
            else:
                print("Salts don't match. Try again.")

        if len(sys.argv) == 1:
            string = raw_input("Enter your string: ")
        elif len(sys.argv) == 2:
            string = sys.argv[1]

        print("Suggested username: %s" % generate_name(seed, string))
        print(generate(seed, string))
        raw_input("Copy this, clear your clipboard and press Enter. ")

        # Clear the screen to make difficult (but not impossible) to view the
        # password again.

        for i in range(500):
            print("\n\n\n\n\n")

    else:
        # running inside a script like `passgen SALT SERVICE`
        # the script must catch this to some variable to prevent leaking
        print(generate(sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()
    sys.exit(0)
