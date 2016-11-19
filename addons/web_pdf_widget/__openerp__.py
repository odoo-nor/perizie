{
    'name': 'Pdf Viewer Widget',
    'description': '''
This module add a pdf preview to binary data

This module works with OpenERP 9.0.
''',
    'version': '9.0.1.0.0',
    'author': 'Innoviu Srl',
    'category': 'Usability',
    'website': 'https://www.example.com',
    'license': 'AGPL-3',
    'depends': [
        'web',
        ],
    'python': ['magic'],
    'data': ['base_data.xml'],
    'js': ['static/src/js/web_pdf_widget.js'],
    'qweb': ['static/src/xml/web_pdf_widget.xml'],
    'installable': True,
    'auto_install': False,
}
