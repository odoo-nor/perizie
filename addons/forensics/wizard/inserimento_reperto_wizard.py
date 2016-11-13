# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time, datetime
from openerp import api
from openerp.tools.translate import _

# ----------------------------------------------------------
# Shortcuts
# ----------------------------------------------------------
# The hard-coded super-user id (a.k.a. administrator, or root user).
SUPERUSER_ID = 1


class forensics_img_reperto_wizard(osv.TransientModel):
    _name = 'forensics.img.reperto.wizard'

    _columns = {
        'reperto_id': fields.many2one('forensics.inserimento.reperto.wizard',
                                      'Inserisci Immagine'),

        'name': fields.text(string='Descrizione foto reperto',
                            required=True, size=100, translate=False),
        'image': fields.binary("Image", attachment=True, help="Immagine limited to 1024x1024px"),
        'perizia_id': fields.many2one('forensics.perizia', 'Perizia'),

    }


class wizard(osv.TransientModel):
    """
        Wizard per la richiesta di annullamento protocollo
    """
    _name = 'forensics.inserimento.reperto.wizard'
    _description = 'Inserimento Reperto Wizard'

    def _get_ct_id(self, cr, uid, ids, context=None):
        if 'active_id' in ids.keys():
            perizia_id = ids['active_id']
            perizia_obj = self.pool.get('forensics.perizia')
            perizia = perizia_obj.browse(cr, uid, perizia_id)
            ct_id = perizia.ct_id.id
            return ct_id

    def _get_pm_id(self, cr, uid, ids, context=None):
        if 'active_id' in ids.keys():
            perizia_id = ids['active_id']
            perizia_obj = self.pool.get('forensics.perizia')
            perizia = perizia_obj.browse(cr, uid, perizia_id)
            pm_id = perizia.pm_id.id
            return pm_id

    def _get_indagati_ids(self, cr, uid, ids, context=None):
        if 'active_id' in ids.keys():
            perizia_id = ids['active_id']
            perizia_obj = self.pool.get('forensics.perizia')
            perizia = perizia_obj.browse(cr, uid, perizia_id)
            indagati = perizia.indagati_ids.ids
            return indagati

    _defaults = {
        'ct_id': _get_ct_id,
        'pm_id': _get_pm_id,
        'indagati_ids': _get_indagati_ids,
    }

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
        # pm_id = perizia.pm_id
        # ct_id = perizia.ct_id

        result.update({'numero_reperto': numero_reperto,
                       'info_procedimento_visualizzate': info_procedimento_visualizzate,
                       # 'pm_id': pm_id,
                       # 'ct_id': ct_id
                       })

        return result

    _columns = {

        'info_procedimento_visualizzate': fields.char(string='Informazioni Visualizzate',
                                                      size=50, readonly=True, translate=False),

        'name': fields.char(string='Marca', required=True,
                            size=50, translate=False),
        # 'perizia_id': fields.many2one('forensics.perizia', 'Perizia'),
        'numero_reperto': fields.integer(string='Numero Reperto', readonly=True, store=True),
        'categoria': fields.many2one(
            'base.reperto.categoria', 'Categoria', required=True,
            help="...si possono inserire nuove categorie dal menu Categorie."),
        'modello': fields.char(string='Modello', required=True,
                               size=50, translate=False),
        'serial_number': fields.char(string='Serial Number', required=True,
                                     size=50, translate=False),
        'descrizione_verbale': fields.text(string='Descrizione come da Verbale',
                                           translate=False),
        'immagine_ids': fields.one2many(
            'forensics.img.reperto.wizard',
            'reperto_id',
            String='Immagini'),

        'numero_procedimento': fields.char(
            string='Numero Procedimento',
            search='_search_numero_procedimento',

            size=20,
            translate=False,
            # compute_sudo=False,
        ),
        'numero_procedimento_anno': fields.selection([(num, str(num)) for num in range((datetime.datetime.now().year - 10),
                                                                                       (datetime.datetime.now().year + 1))],
                                                     ),

        'numero_procedimento_mod': fields.char(
            string='Mod.',
            search='_search_numero_procedimento_mod',

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
        ),
        'dimensione': fields.float(string='Dimensione'),

    }

    def action_request(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        if 'active_id' in context.keys():
            perizia_id = context['active_id']

            # creo i sender_receivers
            img_reperto_obj = self.pool.get('forensics.img.reperto')
            img_reperto = []
            for img_rep in wizard.immagine_ids:
                irvals = {
                    'name': img_rep.name,
                    'image': img_rep.image,
                    'perizia_id': perizia_id,
                }
                img_reperto.append(img_reperto_obj.create(cr, uid, irvals))

            reperto_vals = {
                'name': wizard.name,
                'serial_number': wizard.serial_number,
                'modello': wizard.modello,
                'categoria': wizard.categoria.id,
                'dimensione': wizard.dimensione,
                'descrizione_verbale': wizard.descrizione_verbale,
                'numero_reperto': wizard.numero_reperto,
                'perizia_id': perizia_id,
                'immagine_ids': [(6, 0, img_reperto)],
            }

            self.pool.get("forensics.reperto").create(cr, SUPERUSER_ID, reperto_vals, context=None)
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise osv.except_osv(_("Warning! - create.activity.wizard"), _("Errore nei campi!!."))
