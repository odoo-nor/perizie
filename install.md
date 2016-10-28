 
## Installazione

### GIT clone

```
git clone http://git.flosslab.com/git/r/alimenta/platform.git
cd odoo
git submodule init
git submodule update --depth=1
```

### Dipendenze di sistema

```
apt-get install wkhtmltopdf
```

Occorre installare il modulo **less** aggiornato insieme a NodeJS.

Da Ubuntu 14.04 in poi è sufficiente eseguire questo comando: 

```
apt-get install node-less
```

### Dipendenze per **_**virtualenv**_**

Ubuntu (in comune a tutte le versioni):

```
apt-get install build-essential automake autoconf libtool pkg-config python-dev python-virtualenv python-pip python-setuptools
apt-get install libjpeg-dev libgif-dev libpng12-dev libpq-dev libxml2-dev libxslt1-dev libldap2-dev libssl-dev libfreetype6-dev libwebp-dev libdotconf-dev libsasl2-dev libyaml-dev
```

Dipendenze in aggiunta per OS:
- Ubuntu (12.04): `apt-get install libtiff4-dev`
- Ubuntu (14.04): `apt-get install libtiff5-dev`
- Ubuntu (16.04): `apt-get install libtiff5-dev`

### Virtualenv

All'interno della directory del progetto:

```
virtualenv venv
./venv/bin/pip install -r odoo/requirements.txt
```

La directory **venv** è già inserita nel gitignore 

## Avviare Odoo

### Configurazione per IDE

Per avviare Odoo utilizzare il seguente comando sostituendo <project_dir> con il percorso assoluto in cui Ã¨ stato clonato il repository
