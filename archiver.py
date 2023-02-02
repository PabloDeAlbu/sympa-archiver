import datetime
import glob
import os
import pdb
from pathlib import Path
from shutil import make_archive, rmtree, unpack_archive
import argparse

ARCDIR = 'rootfs/var/lib/sympa/arc'
MAIL_LIST = os.listdir(ARCDIR)

parser = argparse.ArgumentParser(description='Deinput_filees a new domain in Sympa.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('--action', '-a', default='status', choices=['status','compress','uncompress'])
parser.add_argument('--list', default='*')
parser.add_argument('--domain', required=True, default='forums.rio20.net')
parser.add_argument('--date', default='2019-02')
args = parser.parse_args()

def status(archive_path):
    print("*********************************************")
    print(f"{archive_path} status\n")
    for archive in sorted(archive_path.iterdir()):
        if archive.is_dir():
            print(archive.stem)
        if archive.suffix == '.zip':
            print(archive.stem + " COMPRESSED")

def need_procesing(date_input, archive):
    date_archive = datetime.datetime.strptime(archive.stem, '%Y-%m')
    return (date_input >= date_archive)


def compress(archive_path, date_input):
    for archive in archive_path.iterdir():
        if archive.is_dir():
            if (need_procesing(date_input, archive)):
                a = str(archive.resolve())
                zip_file = make_archive(base_name=a, root_dir=a, verbose=True, format='zip')
                if (zip_file): 
                    print(zip_file)
                    rmtree(archive)
    
def uncompress(archive_path, date_input):
    for archive in archive_path.iterdir():
        if archive.suffix == '.zip':
            if (need_procesing(date_input, archive)):
                zip_file = str(archive.resolve())
                archive_dir = f"{Path(archive_path).resolve()}/{archive.stem}"
                os.makedirs(archive_dir, exist_ok=True)
                print(f"{archive.stem} uncompressed")
                unpack_archive(zip_file, extract_dir=archive_dir)
                os.remove(zip_file)

action = args.action
list = args.list
domain = args.domain
date = args.date

archive_dir = f"{ARCDIR}/{list}@{domain}"
archive_path = Path(archive_dir)
dt = datetime.datetime.strptime(date, '%Y-%m')

mail_lists = []
dirs = glob.glob(f"{archive_path}")
for dir in dirs:
    list_dir = Path(dir)
    mail_lists.append(list_dir)

try:
    if action == 'status': 
        for l in mail_lists:
            status(Path(l))
    if action == 'compress': 
        compress(archive_path, dt)
    if action == 'uncompress': 
        uncompress(archive_path, dt)
except Exception as err:
    print('ERROR:', err)