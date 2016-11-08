# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time, datetime
from openerp import api


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

    @api.model
    def default_get(self, vals):
        result = super(wizard, self).default_get(vals)
        perizia_id = self.env.context['active_id']

        # if 'numero_procedimento' in result.keys() and \
        #                 'numero_procedimento_anno' in result.keys() and \
        #                 'numero_procedimento_mod' in result.keys():
        perizia_obj = self.pool.get('forensics.perizia')
        perizia = perizia_obj.browse(self.env.cr, self.env.uid, perizia_id)

        numero_reperto = len(perizia.reperti) + 1
        info_procedimento_visualizzate = perizia.name + "_" + str(perizia.numero_procedimento_anno) + " mod. " + perizia.numero_procedimento_mod
        pm_id = perizia.pm_id
        ct_id = perizia.ct_id

        result.update({'numero_reperto': numero_reperto,
                       'info_procedimento_visualizzate': info_procedimento_visualizzate,
                       'pm_id': pm_id,
                       # 'ct_id': ct_id
                       })

        return result

    _columns = {

        'info_procedimento_visualizzate': fields.char(string='Informazioni Visualizzate',
                                                      required=True, size=50, readonly=True, translate=False),

        'name': fields.char(string='Marca',
                            required=True, size=50, translate=False),
        # 'perizia_id': fields.many2one('forensics.perizia', 'Perizia'),
        'numero_reperto': fields.integer(string='Numero Reperto', readonly=True, store=True),
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

        # Consulente Tecnico
        'ct_id': fields.many2one(
            'res.partner', string='Consulente Tecnico', readonly=True,
        ),

        # Pubblico Ministero
        'pm_id': fields.many2one(
            'res.partner', string='Pubblico Ministero', readonly=True,
        ),
        # Indagato
        'indagati_ids': fields.many2many(
            'res.partner',
            string='Indagati',
            relation='forensics_perizia_indagati_res_partner_rel', readonly=True,
        )

    }

    def action_request(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        if 'active_id' in context.keys():
            protocollo_id = context['active_id']

        pass
        # wizard = self.browse(cr, uid, ids[0], context)
