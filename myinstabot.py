#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import logging
import glob
import traceback

DESCRIPTION_FILE="desc.txt"
PHOTO_EXTENSIONS=["jpg"]
IGNORE_PREFIX = "_"

def parse_args():
    parser = argparse.ArgumentParser(description="Post on instagram")
    parser.add_argument("--user","-u",metavar="USER",help="Instgram user")
    parser.add_argument("--password","-p",metavar="PASSWORD",help="Instgram password")
    parser.add_argument("--folder","-f",metavar="PHOTO_FOLDER",required=True,help="Folder where photos will be retrieved")
    parser.add_argument("--base-path","-P",metavar="CONFIG_FOLDER",help="Temp folder for instabot")
    return parser.parse_args()


class Instagram(object):
    """ Wrapper API for Instagram """
    def __init__(self,user,password,base_path=None):
        from instabot import Bot
        self.user = user
        self.password = password
        self.bot = Bot(base_path=base_path)

    def login(self):
        self.bot.login(username=self.user,password=self.password)

    def convert_username(self,uname):
        try:
            return self.bot.convert_to_user_id(uname)
        except:
            print(f"Error: Unable to find userid of {uname}\n")
            sys.exit(0)

    def upload_photos(self,photos,caption="",user_tags=None):
        # Create user_tags
        if user_tags:
            user_tags = list(map(lambda x: {"user_id":self.convert_username(x),"x":0.5,"y":0.5},user_tags))
        if len(photos) == 1:
            res = self.bot.upload_photo(photos[0],caption,user_tags=user_tags,options={"rename":False})
        else:
            res = self.bot.upload_album(photos,caption,user_tags=user_tags,options={"rename":False})
        return res


def parse_file(path):
    if not os.path.exists(path):
        print(f"ERROR: {path} does not exist\n")
        sys.exit(0)
    content = open(path,"r").read()
    res = []
    for line in content.splitlines():
        line = line.rstrip().lstrip()
        if not line: continue
        x = parse_line(line)
        if x: res.extend(x)
    return res


def parse_line(line):
    """ line = 'ouin file:toto.txt ouin2' """
    TEMPLATE_FILE= "file:"
    res = []
    for elem in line.split(" "):
        if elem.startswith(TEMPLATE_FILE):
            res.extend(parse_file(elem[len(TEMPLATE_FILE):]))
        else:
            res.append(elem)
    return res


def build_metadata(path):
    """ Return tuple: desription, list of users """
    TEMPLATE_USER = "!user:"
    TEMPLATE_HASHTAG = "!hashtag:"

    if not os.path.exists(path):
        return "",None

    desc = []
    hashtags = []
    users = []
    content = open(path,"r").read()

    for line in content.splitlines():
        line = line.rstrip().lstrip()
        if line.startswith(TEMPLATE_USER):
            u = parse_line(line[len(TEMPLATE_USER):].rstrip().lstrip())
            if u: users.extend(u)
        elif line.startswith(TEMPLATE_HASHTAG):
            h = parse_line(line[len(TEMPLATE_HASHTAG):].rstrip().lstrip())
            if h: hashtags.extend(h)
        else:
            desc.append(line)
    
    # Remove duplicates
    hashtags = list(dict.fromkeys(hashtags))
    users = list(dict.fromkeys(users))

    if hashtags: desc.append(" ".join(hashtags))

    return "\n".join(desc),users
            

def main():
    """ Entry Point Program """
    args = parse_args()
    
    instagram = Instagram(args.user,args.password,args.base_path)
    instagram.login()

    try:
        for folder in sorted(os.listdir(args.folder)):
            path = os.path.join(args.folder,folder)
            if not os.path.isdir(path) or folder.startswith(IGNORE_PREFIX):
                continue
            pics = []
            desc,users = build_metadata("%s/%s" % (path,DESCRIPTION_FILE))
            for ext in PHOTO_EXTENSIONS:
                pics += [os.path.abspath(x) for x in sorted(glob.glob(path+"/*.{}".format(ext)))]

            if instagram.upload_photos(pics,desc,user_tags=users):
                logging.info("Photo %r uploaded" % (pics,))
                os.rename(path,os.path.join(args.folder,"%s%s" % (IGNORE_PREFIX,folder)))
                return 0
            else:
                logging.error("Unable to upload photo %r" % (pics,))
    except:
        print(f"ERROR: {traceback.format_exc()}")
        return 1

    return 0


if __name__ == "__main__":
   sys.exit(main())
