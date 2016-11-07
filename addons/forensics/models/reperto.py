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

    # def _get_numero_sequence(self, cr, uid, ids, context=None):
    #     if 'active_id' in ids.keys():
    #         return self.pool.get('ir.sequence').get(cr, uid, 'forensics.reperto.def')

    # lambda self, cr, uid, context={}: self.pool.get('ir.sequence').get(cr, uid, 'code')

    _defaults = {
        'perizia_id': _get_perizia_id,
        # 'numero_reperto': _get_numero_reperto,
        # 'sequence_numero_reperto': _get_numero_sequence
    }

    # _defaults = { ‘field_name’: lambda self, cr, uid, context={}: self.pool.get(‘ir.sequence’).get(cr, uid, ‘code’), }
    # 
    @api.model
    def default_get(self, vals):
        result = super(Reperto, self).default_get(vals)
        if 'perizia_id' in result.keys():
            perizia_id = result['perizia_id']
            perizia_obj = self.pool.get('forensics.perizia')
            perizia = perizia_obj.browse(self.env.cr, self.env.uid, perizia_id)
            result['numero_reperto'] = len(perizia.reperti) + 1

            # result['numero_reperto'] = int(self.pool.get('ir.sequence').get(self.env.cr, self.env.uid, 'forensics.reperto.def'))
            # reperti = perizia.reperti.ids
        #     result['sequence_numero_reperto'] = self.pool.get('ir.sequence').get(self.env.cr, self.env.uid, 'forensics.reperto.def')
        return result

    # @api.model
    # def default_get(self, context=None):
    #     # rep = super(Reperto, self).default_get(context)
    #     pass
    #     # def default_get(self, vals):
    #     rep = super(Reperto, self).default_get(context)

    #     res = {}
    #     if context:
    #         context_keys = context.keys()
    #         next_sequence = 1
    #         if 'ref_ids' in context_keys:
    #             if len(context.get('ref_ids')) > 0:
    #                 next_sequence = len(context.get('ref_ids')) + 1
    #     res.update({'sequence': next_sequence})
    #     return res
    #     pass

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

    numero_reperto = fields.Integer(string='Numero', store=True)
    # sequence_numero_reperto = fields.Many2one('ir.sequence',
    #                                           'Sequenza',
    #                                           store=True,
    #                                           required=False, readonly=True)

    perizia_id = fields.Many2one('forensics.perizia', 'Perizia')

    immagine_ids = fields.One2many(
        'forensics.img.reperto', 'reperto_id',
        String='Immagini')

    # def create(self, cr, uid, vals, context=None):
    #     reperto = super(Reperto, self).create(cr, uid, vals, context=context)
    #     return reperto

    def write(self, cr, uid, ids, vals, context=None):
        if 'dossier_type' in vals and vals['dossier_type'] == 'fascicolo':
            vals['parent_id'] = False
        return super(Reperto, self).write(cr, uid, ids, vals, context=context)

    def unlink(self, cr, uid, ids, context=None):
        super(Reperto, self).unlink(cr, uid, ids, context=context)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
