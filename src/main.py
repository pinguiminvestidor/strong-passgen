#!/usr/bin/env python
#
# Graphical interface for passgen.py!
# 
# This interface requires PyGTK to work. In GNU/Linux, please install it using
# your package manager (apt, yum, pacman, emerge, etc). Windows users can 
# use it out of the box from a portable python installation.
#
# If you cannot install PyGTK for some reason, you can use the passgen.py file
# instead.
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

import os
import sys
import gtk
import passgen

class GUI(object):
    '''
    A simple windowed form. Takes two inputs (salt, string) and returns a
    password.
    '''

    def destroy(self, widget, data=None):
        gtk.main_quit()
        return False
    
    def showpass(self, widget, data=None):
        '''
        Needed to connect the hover event.
        '''
        self.passentry.set_visibility(True)
        
    def hidepass(self, widget, data=None):
        '''
        Needed to connect the hover event.
        '''
        self.passentry.set_visibility(False)


    def entersubmit(self, widget, event, data=None,):
        '''
        Enables user to press Enter instead of clicking to generate.
        '''
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == "Return":
            self.generate()


    def generate(self, widget=None, data=None):
        '''
        Wrapper function for the password generation
        '''
        salt = self.saltentry.get_text()
        string = self.stringentry.get_text()

        if salt == "" or string == "":
            return
        else:
            self.passentry.set_text(passgen.generate(salt, string))
            self.nameentry.set_text(passgen.generate_name(salt, string))
            self.passfield.show()
            self.namefield.show()
            self.saltentry.set_text("")
            self.stringentry.set_text("")

    def __init__(self):
        self.itemlist = []

        # Containers
        self.saltfield = gtk.HBox(False, 2)
        self.itemlist.append(self.saltfield)

        self.stringfield = gtk.HBox(False, 2)
        self.itemlist.append(self.stringfield)

        self.buttonfield = gtk.HBox(True, 2)
        self.itemlist.append(self.buttonfield)

        self.maingrid = gtk.VBox(False, 3)
        self.itemlist.append(self.maingrid)

        # These two don't get shown until the button is clicked:
        self.passfield = gtk.HBox(False, 2)
        self.namefield = gtk.HBox(False, 2)


        # Widget overlay:
        self.instructions = gtk.Label("Enter your salt, password and click Generate")
        self.itemlist.append(self.instructions)

        self.genbutton = gtk.Button("_Generate")
        self.itemlist.append(self.genbutton)

        self.saltlabel = gtk.Label("Password seed (salt): ")
        self.itemlist.append(self.saltlabel)
        
        self.saltentry = gtk.Entry()
        self.itemlist.append(self.saltentry)
        
        self.stringlabel = gtk.Label("Enter a service-specific string: ")
        self.itemlist.append(self.stringlabel)
        
        self.stringentry = gtk.Entry()
        self.itemlist.append(self.stringentry)

        self.passlabel = gtk.Label("Your password: ")
        self.itemlist.append(self.passlabel)
        
        self.passentry = gtk.Entry()
        self.itemlist.append(self.passentry)

        self.namelabel = gtk.Label("Suggested username: ")
        self.itemlist.append(self.namelabel)
        
        self.nameentry = gtk.Entry()
        self.itemlist.append(self.nameentry)

        self.seclevellabel = gtk.Label("Hash how many times? (Default: %s)" %
            passgen.seclevel
            )
        self.itemlist.append(self.seclevellabel)

        # This selector will allow you to choose how many times to hash:

        # Wire buttons together
        self.genbutton.connect("clicked", self.generate)
        self.saltentry.set_visibility(False)
        self.passentry.set_visibility(False)

        # Show-hide password!
        self.passentry.connect("focus-in-event", self.showpass)
        self.passentry.connect("focus-out-event", self.hidepass)

        # pack em up:
        self.saltfield.pack_start(self.saltlabel, False, False, 2)
        self.saltfield.pack_start(self.saltentry, True, True, 2)
        self.stringfield.pack_start(self.stringlabel, False, False, 2)
        self.stringfield.pack_start(self.stringentry, True, True, 2)
        self.passfield.pack_start(self.passlabel, False, False, 2)
        self.passfield.pack_start(self.passentry, True, True, 2)
        self.namefield.pack_start(self.namelabel, False, False, 2)
        self.namefield.pack_start(self.nameentry, True, True, 2)
        self.buttonfield.pack_start(self.genbutton, True, True, 2)
        self.maingrid.pack_start(self.instructions, True, True, 0)
        self.maingrid.pack_start(self.saltfield, False, True, 0)
        self.maingrid.pack_start(self.stringfield, False, True, 0)
        self.maingrid.pack_start(self.buttonfield, True, True, 0)
        self.maingrid.pack_start(self.namefield, False, True, 0)
        self.maingrid.pack_start(self.passfield, False, True, 0)

        for widget in self.itemlist:
            widget.show()

        # The main window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Password Generator by kzimmermann")
        self.window.connect("destroy", self.destroy)
        self.window.connect("key-press-event", self.entersubmit)
        
        self.window.set_border_width(5)
        self.window.add(self.maingrid)
        self.window.show()

    def main(self):
        gtk.main()
        return 0


if __name__ == "__main__":
    app = GUI()
    app.main()
