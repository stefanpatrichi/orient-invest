# OrientInvest: Instrument pentru optimizarea portofoliului de investiții în ETF-uri din zona Europei de Est

## Despre aplicație
OrientInvest folosește metode de Deep Learning, implementând modelul din articolul [„Deep Learning for Portfolio Optimization”](https://arxiv.org/abs/2005.13665) de Zihao Zhang, Stefan Zohren, Stephen Roberts (Oxford-Man Institute of Quantitative Finance, University of Oxford).

ETF-urile disponibile sunt enumerate în [`src/constants.py`](https://github.com/stefanpatrichi/orient-invest/blob/main/src/constants.py) și oferă expunere directă la piețe din Europa de Est.

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

## Funcționalități
Deschideți serverul (`localhost` port `8000`):
```bash
$ cd src
$ python3.11 main.py
```

Accesați `http://localhost:8000/`. De acolo, puteți să vizualizați istoricul oricărui ETF ales din listă sau să alegeți mai multe ETF-uri, în vederea determinării proporțiilor optime pentru investiție. Butonul va începe antrenarea modelului de Deep Learning (care poate dura ceva timp), după care vor fi afișate ponderile.

## Dataset
Pentru a schimba parametri precum numărul de zile din *time window*, doar ștergeți fișierul din `json` din `data`; el se va redescărca automat la rularea programului.