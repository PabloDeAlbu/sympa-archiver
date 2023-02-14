# sympa-archiver

This python script is intended to help you in the task of managing disk usage in your sympa installation by compressing the archive of managed mailing lists.
This script can receive as a parameter a domain, a mailing list and two dates (with the format %Y-%m, Example: 2019-01) that define the period to be processed.
It can also receive a parameter that defines what to do with the file. These values can be list (default), compress or decompress the file.


## Instalación

### Clone repository
```
git clone https://github.com/PabloDeAlbu/sympa-archiver
cd sympa-archiver
```

### if you don't already have virtualenv installed

```
pip install virtualenv
```

### create your new environment (called 'venv' here)

```
python3 -m venv venv
```

### Enter to the virtual environment

```
source venv/bin/activate
```

### Install the requirements in the current environment

```
pip install -r requirements.txt
```

## Configuration

Replace in .env **ARC_DIR** with the directory of archives of your Sympa installation. See [Directory layout](https://www.sympa.community/manual/layout.html) for more information.

## Example

### List status for domain **foo** from 2019-02 until 2021-09
```
python3 archiver.py --domain foo --action list --since 2019-02 --until 2021-09
```


### Compress archive
```
python3 archiver.py --domain foo --action compress 
```

### Uncompress archive
```
python3 archiver.py --domain foo --action uncompress
```
