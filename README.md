# OrientInvest: Instrument pentru optimizarea portofoliului de investiții în ETF-uri din zona Europei de Est

## Instalare
**Atenție! `tensorflow` necesită Python 3.11!** Pentru downgrade, folosiți `pyenv`:
```bash
$ pyenv install 3.11
Downloading Python-3.11.12.tar.xz...
-> https://www.python.org/ftp/python/3.11.12/Python-3.11.12.tar.xz
Installing Python-3.11.12...
Installed Python-3.11.12 to /home/USER/.pyenv/versions/3.11.12
$ pyenv local 3.11
```

Apoi, instalați modulele din `requirements.txt`:
```bash
$ pip3.11 install -r requirements.txt
```

Rulați fișierele Python cu `python3.11`, sau `python3` pe MacOS (nu `python`).

## Funcționalități
Deschideți serverul (`localhost` port `8000`):
```bash
$ cd src
$ python3.11 main.py
```

## Dataset
Pentru a schimba parametri precum numărul de zile din *time window*, doar ștergeți fișierul din `json` din `data`; el se va
redescărca automat la rularea programului.