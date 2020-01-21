#GET_IPLAYER DLZ QUEUER

#REMOTE SCRIPT

welcome_message = '''

************************************************************************************************
Welcome to the remote server, comrade.

Enter iPlayer URL to queue and hit enter to add to queue. Then:
- Type \'go\' to download all, then auto-synchronise this remote directory with your local one.
- Type \'skip\' to skip straight to synchronising remote and local directories.
************************************************************************************************

'''

import logging
import os

logging.basicConfig(filename='log.log', level=logging.DEBUG)


DL_DESTINATION = '/Volumes/Gigantosaur/Media/iPlayer/'
_POST_TAGS = '--subtitles --whitespace'

prox_usr = 'lewis'
prox_pwd = os.environ.get('UK_PROX_PWD')
prox_add = os.environ.get('UK_IP')
prox_port= '3128'

_GLOBAL_COMMAND = 'get_iplayer --proxy=https://%s:%s@%s:%s' % (prox_usr, prox_pwd, prox_add, prox_port)

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
        if url_is_series(url) == False:
            pid = url[url.index('/episode/')+len('/episode/'):url.rindex('/')]
        elif url_is_series(url):
            pid = url[url.rindex('/')+1:]
        elif len(url) == 8:
            pid = url
        return pid
    except NameError:
        raise ValueError('Could not find a valid PID in %s' % url)
    

def download(url):
    command = _GLOBAL_COMMAND
    pid = get_pid(url)
    logging.debug('PID identified as %s from URL %s' % (pid, url))
    command += ' --pid=%s %s' % (pid, _POST_TAGS)
    if url_is_series(url):
        command += ' --pid-recursive'
    print(command)
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

cdRemoteDirectory(DL_DESTINATION)
queue_and_download_programs()
