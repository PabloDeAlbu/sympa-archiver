import datetime
import os
import pdb
from pathlib import Path
from shutil import make_archive, rmtree
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

def status(archive_path):
    for archive in archive_path.iterdir():
        if archive.is_dir():
            print(archive.stem)
        if archive.suffix == '.zip':
            print(archive.stem + " COMPRESSED")

def compress(archive_path, date):
    for archive in archive_path.iterdir():
        if archive.is_dir():
            dt_archive = datetime.datetime.strptime(archive.stem, '%Y-%m')
            if (date >= dt_archive):
                a = str(archive.resolve())
                zip_file = make_archive(base_name=a, root_dir=a, verbose=True, format='zip')
                if (zip_file): 
                    print(zip_file)
                    rmtree(archive)
    


action = args.action
list = args.list
domain = args.domain
date = args.date

archive_dir = f"{ARCDIR}/{list}@{domain}"
archive_path = Path(archive_dir)
dt = datetime.datetime.strptime(date, '%Y-%m')

try:
    if action == 'status': status(archive_path)
    if action == 'compress': compress(archive_path, dt)
    if action == 'uncompress': compress(archive_path, dt)
except Exception as err:
    print('ERROR:', err)