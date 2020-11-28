# Introduction

- Script to post photos or album on instagram with a description. It is going to search for folder inside the folder given in parameter, and it will post any photos inside this folder on Instagram adding the description contained in `desc.txt` file. This folder will be then renamed, and the next folder will be posted during the next execution.

```bash
$ python3 myinstabot.py -f folder -u $USER -p $PASSWORD
```

You can prepare all you photos in advance, and add a shell scrip in your crontab, in order to post photo regularly.

## Dependencies

- https://github.com/ohld/igbot
