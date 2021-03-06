# -*- coding: utf-8 -*-
{
    'name': "Perizie Forensi",
    'summary': "Investigazioni ed Analisi Forense: Gestione Catena di Custodia Perizie",
    'description': """Modulo per la gestione della Catena di Custodia Perizie Forensi""",
    'author': "Norman Argiolas",
    'license': "AGPL-3",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '9.0.1.0.0',
    'depends': ['base',
                'web',
                'decimal_precision',
                'document',
                'hr',
                'report_webkit',
                ],
    'data': [
        'wizard/inserimento_reperto_wizard_view.xml',
        'views/perizia.xml',
        'views/reperto.xml',
        'data/sequence.xml',
        'views/perizie_img_reperto.xml',
        'views/backend_menu.xml',
        'data/reperto_tipologia_data.xml',
        'views/templates.xml',
        'report/report_template.xml',
        # 'report/report.xml'

    ],
    "qweb": [],
}
