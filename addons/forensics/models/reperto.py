# -*- coding: utf-8 -*-

from forensics.models.base_reperto import BaseReperto
from forensics.utility.db_utils import DBUtils
from openerp import models, fields, api


class Reperto(models.Model):
    _name = 'forensics.reperto'
    _inherit = ['base.reperto']

    _description = 'Reperto'
    _order = 'numero_reperto asc'

    _sql_constraints = [
        ('numero_reperto_unique',
         'unique(numero_reperto)',
         'Il numero del reperto deve essere unico!')
    ]

    def __init__(self, pool, cr):
        super(Reperto, self).__init__(pool, cr)
        self.db_utils = DBUtils()

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

    # return res

    descrizione_verbale = fields.Text(string='Descrizione come da Verbale',
                                      required=False, translate=False)

    numero_reperto = fields.Integer(string='Numero', store=True)

    perizia_id = fields.Many2one('forensics.perizia', 'Perizia', required=True)

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
        if 'active_id' in context.keys():
            if 'active_id' in context.keys():
                reperto_obj = self.pool.get('forensics.reperto')
                num_rep_of_reperto_to_delete = reperto_obj.browse(cr, uid, ids).numero_reperto
                num_rep_max = self.db_utils.get_max_value(cr)
                reperto_with_max_num = self.pool.get("forensics.reperto").search(cr, uid, [('numero_reperto', '=', num_rep_max)])
                reperto = reperto_obj.browse(cr, uid, reperto_with_max_num)
                vals = {}
                vals['numero_reperto'] = num_rep_of_reperto_to_delete
                super(Reperto, self).unlink(cr, uid, ids, context=context)
                reperto.write(vals)

        # reperto = reperto_obj.browse(self.env.cr, self.env.uid, perizia_id)
        super(Reperto, self).unlink(cr, uid, ids, context=context)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
