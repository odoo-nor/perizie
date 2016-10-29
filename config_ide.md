## Avviare Odoo

### Configurazione per IDE Intellij

<project_dir> = percorso assoluto in cui è stato clonato il repository

**/etc/odoo.cfg/** file in cui sono presenti le configurazioni di base per avviare Odoo

[DEFAULT]
project = <project_dir>/platform/
addons = %(project)s/odoo/addons/,%(project)s/odoo/openerp/addons/,%(project)s/addons/

Cambiare i parametri in base alle proprie configurazioni
'''
data_dir = ~.local/share/Odoo
db_host = localhost
db_name = db_name
db_password = db_password
db_user = db_user
dbfilter = dbfilter
xmlrpc_port = port
'''

In **Edit Configuration** creare una nuova configurazione Python con i seguenti parametri:
Script: **<project_dir>/odoo/odoo.py**
Script Parameters: **-c etc/odoo.cfg**


Per le cartelle 
'''
**platform/addons** 
**platform/odoo** 
'''
Mark Directory As -> Sources Root