import datetime
import glob
import os
from os.path import join, getsize
import pdb
from pathlib import Path
from shutil import make_archive, rmtree, unpack_archive
import argparse
from decouple import config
ARC_DIR = config('ARC_DIR')
MAIL_LIST = os.listdir(ARC_DIR)
today = datetime.date.today()
first = today.replace(day=1)
two_month_ago = first - datetime.timedelta(days=31)

parser = argparse.ArgumentParser(description='Deinput_filees a new domain in Sympa.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('--action', '-a', default=None, choices=['compress','uncompress'])
parser.add_argument('--list', default='*')
parser.add_argument('--domain', required=True)
parser.add_argument('--date')
parser.add_argument('--since', default='1900-01' , help="Enter the date from which you want to process the archive. Date in format %Y-%m. Example: 2019-03")
parser.add_argument('--until', default=two_month_ago.strftime("%Y-%m"), help="Enter the date up to which the file is to be processed. Date in format %Y-%m. Example: 2019-02")

args = parser.parse_args()

to_compress = []
to_uncompress = []

def need_procesing(since, until, archive):
    date_archive = datetime.datetime.strptime(archive.stem, '%Y-%m')
    return (since <= date_archive and until >= date_archive)

def do_status(since, until, archive):
    if need_procesing(since, until, archive):
        if archive.is_dir():
            to_compress.append(archive)
            print(archive.stem)
        if archive.suffix == '.zip':
            to_uncompress.append(archive)
            print(archive.stem + " COMPRESSED")

def do_compress(to_compress):
    for archive in to_compress:
        if archive.is_dir():
            a = str(archive.resolve())
            zip_file = make_archive(base_name=a, root_dir=a, verbose=True, format='zip')
            if (zip_file): 
                print(zip_file)
                rmtree(archive)
    
def do_uncompress(to_uncompress):
    for archive in to_uncompress:
        if archive.suffix == '.zip':
            zip_file = str(archive.resolve())
            archive_dir = f"{Path(archive).resolve()}/{archive.stem}"
            os.makedirs(archive_dir, exist_ok=True)
            print(f"{archive.stem} uncompressed")
            unpack_archive(zip_file, extract_dir=archive_dir)
            os.remove(zip_file)

action = args.action
list = args.list
domain = args.domain
date_input = args.date

if (date_input):
    until = datetime.datetime.strptime(date_input, '%Y-%m')
    since = datetime.datetime.strptime(date_input, '%Y-%m')
elif (args.until and args.since):
    until = datetime.datetime.strptime(args.until, '%Y-%m')
    since = datetime.datetime.strptime(args.since, '%Y-%m')

archive_dir = f"{ARC_DIR}/{list}@{domain}"
list_path = Path(archive_dir)

mail_lists = []
dirs = glob.glob(f"{list_path}")

for root, dirs, files in os.walk(ARC_DIR):
    print(root, "consumes")
    print(sum(getsize(join(root, name)) for name in files))
    print("bytes in", len(files), "non-directory files")
    if 'CVS' in dirs:
        dirs.remove('CVS')  # don't visit CVS directories


dispatcher = {
    'compress': do_compress,
    'uncompress': do_uncompress
}

to_process = {
    'compress': to_compress,
    'uncompress': to_uncompress
}

for dir in dirs:
    list_dir = Path(dir)
    mail_lists.append(list_dir)

try:
    print(f"Processing since: {since} until: {until}")
    for l in mail_lists:
        list_path = Path(l)
        list_str = str(list_path).split('/')[-1]
        print("*********************************************")
        print(f"{list_str}\n")
        for archive in sorted(list_path.iterdir()):
            do_status(since, until, archive)
            
        if action: dispatcher[action](to_process[action])

except Exception as err:
    print('ERROR:', err)