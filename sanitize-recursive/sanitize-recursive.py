#!/usr/bin/python
import os
import sys
import shutil
import re
import errno
import argparse

parser = argparse.ArgumentParser(description='Recursively sanitize file and directory names. Running without --confirm will just print what would be done.')
parser.add_argument('dir_start', metavar='DIR_START', help='directory from which to start sanitizing')
parser.add_argument('--confirm', dest='confirm', action='store_true', help='confirm you want to go ahead with the renaming, as output from execution without confirm prints')
args = parser.parse_args()


def sanitize(filename):
    filename = re.sub('\s+$', '', filename)
    filename = re.sub('[^\w\.]', '_', filename)
    filename = re.sub('__+','_', filename)
    filename = re.sub('_+$', '', filename)
    filename = filename.lower()
    return filename

def sanitize_recursive(dirname):
    for f in os.listdir(dirname):
        filepath_abs = os.path.join(dirname, f)
        filepath_abs_new = os.path.join(dirname, sanitize(f))
        if filepath_abs_new != filepath_abs and not re.search('.*itmsp$', filepath_abs, flags=re.IGNORECASE) and not re.search('^\..*', filepath_abs, flags=re.IGNORECASE):
            try:
                print('%s\n%s\n' % (filepath_abs, filepath_abs_new))
                if args.confirm:
                    os.renames(filepath_abs, filepath_abs_new)
            except OSError, e:
                if e.errno != errno.EACCES:
                    # who cares!
                    pass
                    #raise(e)

        if os.path.isdir(filepath_abs_new):
            try:
                sanitize_recursive(filepath_abs_new)
            except:
                pass

dir_start = os.path.abspath(args.dir_start)
print 'Sanitizing recursive: %s' % dir_start
sanitize_recursive(dir_start)
if not args.confirm:
    print('Test run completed. To actually rename as per output, add argument "--confirm"\n')
