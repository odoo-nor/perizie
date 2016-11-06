# -*- coding: utf-8 -*-

from forensics.models.base_reperto import BaseReperto
from openerp import models, fields, api


class Reperto(models.Model):
    _name = 'forensics.reperto'
    _inherit = ['base.reperto']

    _description = 'Reperto'
    _order = 'name'

    def _get_perizia_id(self, cr, uid, ids, context=None):
        if 'active_id' in ids.keys():
            return ids['active_id']

    _defaults = {
        'perizia_id': _get_perizia_id,
    }

    # @api.model
    # def default_get(self, vals):
    #     res = super(Reperto, self).default_get(vals)
        # country_ids = self.env['res.country'].search([('code', '=', 'IN')])
        # 
        # if country_ids:
        #     res.update({
        #         'country_id': country_ids[0].id,  # Many2one field
        #         'city': 'Gandhinagar',
        #         'website': 'www.odootechnical.com',
        #         'email': 'contact@odootechnical.com'
        #     })
        # return res

    descrizione_verbale = fields.Text(string='Descrizione come da Verbale',
                                      required=False, translate=False)

    numero_reperto = fields.Integer(string='Numero', readonly=True)

    perizia_id = fields.Many2one('forensics.perizia', 'Perizia')

    immagine_ids = fields.One2many(
        'forensics.img.reperto', 'reperto_id',
        String='Immagini')

    # def create(self, cr, uid, vals, context=None):
    #     reperto = super(Reperto, self).create(cr, uid, vals, context=context)
    #     return reperto
