import datetime
import os
import pdb
from pathlib import Path
from shutil import make_archive
import argparse

ARCDIR = 'rootfs/var/lib/sympa/arc'
MAIL_LIST = os.listdir(ARCDIR)

parser = argparse.ArgumentParser(description='Deinput_filees a new domain in Sympa.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('--action', '-a', default='status', choices=['status','compress','uncompress'])
parser.add_argument('--list', default='equipazoprueba')
parser.add_argument('--domain', default='forums.rio20.net')
parser.add_argument('--date', default='2019-02')
args = parser.parse_args()

archives = []

def main(action, list, domain, date):
    archive_dir = f"{ARCDIR}/{list}@{domain}"
    archive_path = Path(archive_dir)
    dt = datetime.datetime.strptime(date, '%Y-%m')
    for archive in archive_path.iterdir():
        if archive.is_dir():
            dt_archive = datetime.datetime.strptime(archive.stem, '%Y-%m')
            print(dt >= dt_archive)
    


action = args.action
list = args.list
domain = args.domain
date = args.date


try:
    main(action, list, domain, date)
except Exception as err:
    print('ERROR:', err)