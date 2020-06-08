/*

 A fork of strong-passgen into javascript.

 You can even use it locally. To use it, download the bundle (page.html,
 generator.js) anywhere in your computer and open `page.html` with a modern
 browser (IE9 and above, recent versions of Firefox or chrome). You can also
 host it somewhere and use it, but please include its SHA-256 hash as a proof
 that the file has not been tampered with and won't do malicious
 or remote actions with your input.

 Copyright 2020 by Pinguim Investidor - https://pinguiminvestidor.com
 This program is part of strong-passgen, and follows its same license terms.
 Licensed under the terms of the GNU GPL v3. 
 See http://gnu.org/licenses for more information

 jsSHA is authored by Brian Turek (https://github.com/Caligatio), under the 
 following cunditions:

Copyright (c) 2008-2015, Brian Turek
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * The names of the contributors may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
ANDANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIEDWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT,INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING,BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE,DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OFLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCEOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISEDOF THE POSSIBILITY OF SUCH DAMAGE.
 
 */

(function () {
    "use strict";
    var pwfield = document.querySelectorAll("#pwd")[0],
        unfield = document.querySelectorAll("#uname")[0],
        trig = document.querySelectorAll("#trigger")[0];

    pwfield.value = "";
    unfield.value = "";
    

    /*
      Recent ECMAScript standards have some rudimentary Crypto API.
      Although I woudldn't really trust it to do encryption and all that,
      there's enough support to make hash functions usable, and that's good
      enough to me :)
      
      There are examples from the MDN's reference webpage, but they didn't work:
      https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest

      Instead we make use of this JS library, available here:
      https://github.com/Caligatio/jsSHA
     */ 

    function securehash (token, seclevel = 7) {
        var tmp = token;
        for (var i = 0; i < seclevel; i++) {
            // yes, I have to reconstruct the object every time :\
            var hashobj = new jsSHA("SHA-256", "TEXT");
            hashobj.update(tmp);
            tmp = hashobj.getHash("HEX");
        }
        return tmp;
    }

    // Implementation here covers strong-passgen's username and password
    // generation functions:
    function gen() {
        var salt = document.querySelectorAll('input')[0].value,
            service = document.querySelectorAll('input')[1].value,
            start = (salt + service).length,
            hash = securehash(salt + service),
            raw = btoa(hash);
        pwfield.value = raw.slice(start, start + 32);
        unfield.value = hash.slice(start, start + 12)
        document.querySelectorAll('input')[0].value = "";
        document.querySelectorAll('input')[1].value = "";
    }

    // Bind Enter key to generate your password:
    window.addEventListener("keypress", function (e) {
        if (e.keyCode === 13) {
            gen();
        }
    });

    // also bind it to the 'trigger' div-button thingy:
    trig.addEventListener("click", gen);

    // finally, as a more-or-less privacy protection measure, make it so that
    // your password only becomes visible when you focus the field:
    pwfield.addEventListener("focus", function() {
        this.type = "text";
    });
    pwfield.addEventListener("blur", function() {
        this.type = "password";
    });
}());
