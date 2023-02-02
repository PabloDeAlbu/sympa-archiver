import datetime
import glob
import os
import pdb
from pathlib import Path
from shutil import make_archive, rmtree, unpack_archive
import argparse

ARCDIR = 'rootfs/var/lib/sympa/arc'
MAIL_LIST = os.listdir(ARCDIR)
today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)

parser = argparse.ArgumentParser(description='Deinput_filees a new domain in Sympa.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('--action', '-a', default='status', choices=['status','compress','uncompress'])
parser.add_argument('--list', default='*')
parser.add_argument('--domain', required=False, default='forums.rio20.net')
parser.add_argument('--date', default='2019-02')
parser.add_argument('--since', default='2019-02')
parser.add_argument('--until', default=last_month.strftime("%Y-%m"))

args = parser.parse_args()

def need_procesing(date_input, archive):
    date_archive = datetime.datetime.strptime(archive.stem, '%Y-%m')
    return (date_input >= date_archive)

def do_status(archive_path, date_input):
    for archive in sorted(archive_path.iterdir()):
        if archive.is_dir():
            print(archive.stem)
        if archive.suffix == '.zip':
            print(archive.stem + " COMPRESSED")

def do_compress(archive_path, date_input):
    for archive in archive_path.iterdir():
        if archive.is_dir():
            if (need_procesing(date_input, archive)):
                a = str(archive.resolve())
                zip_file = make_archive(base_name=a, root_dir=a, verbose=True, format='zip')
                if (zip_file): 
                    print(zip_file)
                    rmtree(archive)
    
def do_uncompress(archive_path, date_input):
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
until = args.until
since = args.since

archive_dir = f"{ARCDIR}/{list}@{domain}"
archive_path = Path(archive_dir)
date_input = datetime.datetime.strptime(date, '%Y-%m')

mail_lists = []
dirs = glob.glob(f"{archive_path}")

dispatcher = {
    'status': do_status,
    'compress': do_compress,
    'uncompress': do_uncompress
}

for dir in dirs:
    list_dir = Path(dir)
    mail_lists.append(list_dir)

try:
    print(f"{action.upper()} since: {since} until: {until}")
    for l in mail_lists:
        archive_path = Path(l)
        list_str = str(archive_path).split('/')[-1]
        print("*********************************************")
        print(f"{list_str}\n")
        dispatcher[action](archive_path, date_input)
except Exception as err:
    print('ERROR:', err)