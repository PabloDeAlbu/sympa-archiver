import os
import pdb

ARCDIR = '/var/lib/sympa/arc'
MAIL_LIST = os.listdir(ARCDIR)

archives = []

for list in MAIL_LIST:
    archive = f"{ARCDIR}/{list}"
    archive_dates = os.listdir(archive)
    for date in archive_dates:    
        archives.append(f"{ARCDIR}/{list}/{date}")
