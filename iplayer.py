#GET_IPLAYER DLZ QUEUER

#LOCAL SCRIPT

import os

_MY_SECRET_IP = os.environ.get('UK_IP')
_SCP_DESTINATION = '/Volumes/Media/iPlayer/'
_SCP_SOURCE = "porter@%s:/home/porter/iplayer/" % _MY_SECRET_IP


def loginSSH(loginCommand):
    os.system(loginCommand)

def syncItOverHere(flags):
    rsync = 'rsync %s' % flags
    command = ('%s %s %s' % (rsync, _SCP_SOURCE, _SCP_DESTINATION))
    print(command)
    os.system(command)


#### HERE WE GOOOOO!

loginSSH('''ssh -t porter@%s -p22257 "cd /home/porter/iplayer && python3 /home/porter/iplayerRemote.py"''' % _MY_SECRET_IP)
syncItOverHere('-avzhP --remove-source-files --append -e "ssh -p22257"')

