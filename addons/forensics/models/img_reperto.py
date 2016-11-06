# -*- coding: utf-8 -*-

from openerp import models, fields
from openerp import api


class ImgReperto(models.Model):
    _name = 'forensics.img.reperto'

    _description = 'Immagine Reperto'
    _order = 'name'

    # def _get_perizia_id(self, cr, uid, ids, context=None):
    #     if 'active_id' in ids.keys():
    #         return ids['active_id']

    # _defaults = {
    #     'perizia_id': _get_perizia_id,
    # }

    # @api.model
    # def default_get(self, vals):
    #     res = super(ImgReperto, self).default_get(vals)

    name = fields.Text(string='Descrizione foto reperto',
                       required=True, size=100, translate=False)

    image = fields.Binary("Image", attachment=True, help="Immagine limited to 1024x1024px")

    reperto_id = fields.Many2one('forensics.reperto', 'Reperto')

    perizia_id = fields.Many2one('forensics.perizia', 'Perizia',
                                 compute='_compute_perizia',
                                 inverse='_inverse_perizia',
                                 store=False,
                                 compute_sudo=False,
                                 )

    @api.depends('reperto_id')
    def _compute_perizia(self):
        for img_reperto in self.filtered('name'):
            self.perizia_id = img_reperto.reperto_id.perizia_id

    def _inverse_perizia(self):
        pass

    # def create(self, cr, uid, vals, context=None):
    #     reperto = super(ImgReperto, self).create(cr, uid, vals, context=context)
    #     return reperto
