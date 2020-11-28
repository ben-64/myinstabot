#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import logging
import glob

DESCRIPTION_FILE="desc.txt"
PHOTO_EXTENSIONS=["jpg"]
IGNORE_PREFIX = "_"

def parse_args():
    parser = argparse.ArgumentParser(description="Post on instagram")
    parser.add_argument("--user","-u",metavar="USER",help="Instgram user")
    parser.add_argument("--password","-p",metavar="PASSWORD",help="Instgram password")
    parser.add_argument("--folder","-f",metavar="PHOTO_FOLDER",required=True,help="Folder where photos will be retrieved")
    return parser.parse_args()


class Instagram(object):
    """ Wrapper API for Instagram """
    def __init__(self,user,password):
        from instabot import Bot
        self.user = user
        self.password = password
        self.bot = Bot()

    def login(self):
        self.bot.login(username=self.user,password=self.password)

    def upload_photos(self,photos,caption=""):
        if len(photos) == 1:
            res = self.bot.upload_photo(photos[0],caption,options={"rename":False})
        else:
            res = self.bot.upload_album(photos,caption,options={"rename":False})
        return res


def main():
    """ Entry Point Program """
    args = parse_args()
    
    instagram = Instagram(args.user,args.password)
    instagram.login()

    try:
        for folder in sorted(os.listdir(args.folder)):
            path = os.path.join(args.folder,folder)
            if not os.path.isdir(path) or folder.startswith(IGNORE_PREFIX):
                continue
            pics = []
            desc_path = "%s/%s" % (path,DESCRIPTION_FILE)
            desc = ""
            if os.path.exists(desc_path):
                desc = open(desc_path,"r").read()
            for ext in PHOTO_EXTENSIONS:
                pics += [os.path.abspath(x) for x in glob.glob(path+"/*.{}".format(ext))]

            if instagram.upload_photos(pics,desc):
                logging.info("Photo %r uploaded" % (pics,))
                os.rename(path,os.path.join(args.folder,"%s%s" % (IGNORE_PREFIX,folder)))
                return 0
            else:
                logging.error("Unable to upload photo %r" % (pics,))
    except:
        print("ERROR")
        return 1

    return 0


if __name__ == "__main__":
   sys.exit(main())
