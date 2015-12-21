#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pafy
import sys
import webbrowser
import subprocess

import pygtk
pygtk.require('2.0')

import gobject
import gtk
gtk.gdk.threads_init()

import threading


class EntryExample:
    def get_video(self, widget, entry):
        url = entry.get_text()
        self.video = pafy.new(url)
        
        self.label2.set_text(self.video.duration + "  likes: "+ 
               str(self.video.likes) +" dislikes: "+ str(self.video.dislikes)
                                     +" viwes: "+ str(self.video.viewcount))
        self.label.set_text(self.video.title.encode('utf-8'))
        print "URL: %s\n" % url

    def play (self, widget, entry):
        best = self.video.getbest(preftype="webm")
        print best.url
        webbrowser.open(best.url)
    
    def saveHelper(self, widget, entry):
        self.label2.set_text("Downloading ...")
        threading.Thread(target=self.save, args=(widget, entry)).start()

    def save (self, widget, entry):
        best = self.video.getbest()
        fileChk1 = os.path.isfile(self.video.title.encode('utf-8') + '.' + best.extension)
        fileChk2 = os.path.isfile(self.video.title.encode('utf-8') + '.' + best.extension +'.temp')
        print fileChk1
        print fileChk2
        if not ((fileChk1 == True) or (fileChk2 == True)):
            print 'file not exist'
            filename = best.download(quiet=False)
            self.label2.set_text("Done !!")
        else:
            print 'file exist !!!'
            self.label2.set_text("File exist !!!!")


    def __init__(self):
        self.video = None
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(400, 300)
        self.window.set_title("YOUTUBE LINK")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())

        vbox = gtk.VBox(False, 5)
        self.window.add(vbox)
        vbox.show()
        
        self.label = gtk.Label()
        self.label.set_use_markup(True)
        vbox.add(self.label)
        self.window.show_all()
        self.label.set_text("Video Name")
     
        self.label2 = gtk.Label()
        self.label2.set_use_markup(True)
        vbox.add(self.label2)
        self.window.show_all()
        self.label2.set_text("Info")

        entry = gtk.Entry()
        vbox.pack_start(entry, True, True, 0)
        entry.show()

#############################################################
        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()

        button = gtk.Button("get video")
        button.connect("clicked", self.get_video, entry)
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        self.window.show()

        button = gtk.Button("Play")
        button.connect("clicked", self.play, entry)
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        self.window.show()

        button = gtk.Button("SAVE")
        button.connect("clicked", self.saveHelper, entry)
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        self.window.show()


        button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button.connect("clicked", lambda w: gtk.main_quit())
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        self.window.show()


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    EntryExample()
    gtk.gdk.threads_enter()
    main()
    gtk.gdk.threads_leave()
