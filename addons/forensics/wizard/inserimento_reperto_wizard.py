# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time, datetime


class forensics_img_reperto_wizard(osv.TransientModel):
    _name = 'forensics.img.reperto.wizard'

    _columns = {
        # TODO: inserire anche AOO in type?
        'reperto_id': fields.many2one('forensics.inserimento.reperto.wizard',
                                      'Inserisci Immagine'),

        'name': fields.text(string='Descrizione foto reperto',
                            required=True, size=100, translate=False),
        'image': fields.binary("Image", attachment=True, help="Immagine limited to 1024x1024px"),

    }


class wizard(osv.TransientModel):
    """
        Wizard per la richiesta di annullamento protocollo
    """
    _name = 'forensics.inserimento.reperto.wizard'
    _description = 'Inserimento Reperto Wizard'
    _columns = {
        'name': fields.char(string='Marca',
                            required=True, size=50, translate=False),
        # 'perizia_id': fields.many2one('forensics.perizia', 'Perizia'),
        'numero_reperto': fields.integer(string='Numero', store=True),
        'categoria': fields.many2one(
            'base.reperto.categoria', 'Categoria',
            required=True,
            help="...si possono inserire nuove categorie dal menu Categorie."),
        'modello': fields.char(string='Modello',
                               required=True, size=50, translate=False),
        'serial_number': fields.char(string='Serial Number',
                                     required=True, size=50, translate=False),
        'descrizione_verbale': fields.text(string='Descrizione come da Verbale',
                                           required=False, translate=False),
        'immagine_ids': fields.one2many(
            'forensics.img.reperto.wizard',
            'reperto_id',
            String='Immagini'),

        'numero_procedimento': fields.char(
            string='Numero Procedimento',
            search='_search_numero_procedimento',
            required=True,
            size=20,
            translate=False,
            # compute_sudo=False,
        ),
        'numero_procedimento_anno': fields.selection([(num, str(num)) for num in range((datetime.datetime.now().year - 10),
                                                                                       (datetime.datetime.now().year + 1))],
                                                     required=True, ),

        'numero_procedimento_mod': fields.char(
            string='Mod.',
            search='_search_numero_procedimento_mod',
            required=True,
            size=10,
            translate=False,
        ),

    }

    def action_request(self, cr, uid, ids, context=None):
        pass
        # wizard = self.browse(cr, uid, ids[0], context)
