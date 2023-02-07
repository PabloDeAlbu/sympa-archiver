# sympa-archiver

This python script intend to help you in the task of administering the disk usage in your sympa installation.

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

### Archive status for domain **foo**
```
python3 archiver.py --domain foo
```


### Compress archive
```
python3 archiver.py --domain foo --action compress 
```

### Uncompress archive
```
python3 archiver.py --domain foo --action uncompress
```
