#GET_IPLAYER DLZ QUEUER

#REMOTE SCRIPT

welcome_message = '''

************************************************************************************************
Welcome to the remote server, comrade.

Enter iPlayer URL or PID to queue and hit enter to add to queue.
Add Extra flags if needed, eg. --subtitles-only
Then:
- Type \'go\' to download all, then auto-synchronise this remote directory with your local one.
- Type \'skip\' to skip straight to synchronising remote and local directories.
************************************************************************************************

'''

import logging
import sys
import os

logging.basicConfig(filename='iplayerdlz.log', level=logging.DEBUG)

_MY_SECRET_IP = os.environ.get('UK_IP')
_SCP_DESTINATION = '/Volumes/Gigantosaur/Media/iPlayer/'
_SCP_SOURCE = '''rsh='ssh -p22257 porter@%s/home/porter/iPlayer/''' % _MY_SECRET_IP
_POST_TAGS = '--subtitles --whitespace'

def cdRemoteDirectory(directory):
    os.chdir(directory)

# Analyse url to determine if series/brand or individual episode
def url_is_series(url):
    if '/episode/' in url:
        return False
    return True

#Extract the PID from the URL
def get_pid(url):
    try:
        if len(url) == 8:
            pid = url
        if url_is_series(url) == False:
            pid = url[url.index('/episode/')+len('/episode/'):url.rindex('/')]
        elif url_is_series(url):
            pid = url[url.index('/episodes/')+len('/episodes/'):url.rindex('/')]
        return pid
    except NameError:
        raise ValueError('Could not find a valid PID in %s' % url)

def get_extra_flags(url):
    if ' --' in url:
        flags = url[url.index(' --')+1:]
        return flags
    else:
        return ''

def download(url):
    command = 'nohup get_iplayer '
    usr_flags = get_extra_flags(url)
    pid = get_pid(url)
    logging.debug('PID identified as %s from URL %s' % (pid, url))
    logging.debug('User flags identified as %s from URL %s' % (usr_flags, url))
    command += '--pid=%s %s %s' % (pid, usr_flags, _POST_TAGS)
    if url_is_series(url):
        command += ' --pid-recursive'
    os.system(command)

def download_list(theList):
    for url in theList:
        try:
            download(url)
        except Exception as e:
            print(repr(e), file=sys.stderr)
            logging.error(repr(e))

def add_url_to_file(url):
    with open('iplayerhistory.txt', 'a') as textfile:
        textfile.write(url + '\n')

def queue_and_download_programs():
    dlz_list = []
    i = 1
    print(welcome_message)
    while True:
        dlz_url = input(str(i) +') >> ')
        if dlz_url.lower() == 'go':
            download_list(dlz_list)
            return('All downloaded.')
        if dlz_url.lower() == 'skip':
            return('Downloads skipped.')
        else:
            dlz_list.append(dlz_url)
            add_url_to_file(dlz_url)
            i += 1


#### HERE WE GOOOOO!

cdRemoteDirectory('/home/porter/iplayer')
queue_and_download_programs()
