# -*- coding: utf-8 -*-

from openerp import models, fields
from openerp import api


class ImgReperto(models.Model):
    _name = 'forensics.img.reperto'

    _description = 'Immagine Reperto'
    _order = 'name'

    name = fields.Text(string='Descrizione foto reperto',
                       required=True, size=100, translate=False)

    image = fields.Binary("Image", attachment=True, help="Immagine limited to 1024x1024px")

    reperto_img_id = fields.Many2one('forensics.reperto', 'Reperto')

    perizia_id = fields.Many2one('forensics.perizia', 'Perizia',
                                 compute='_compute_perizia',
                                 inverse='_inverse_perizia',
                                 store=False,
                                 compute_sudo=False,
                                 )

    @api.depends('reperto_img_id')
    def _compute_perizia(self):
        pass

    def _inverse_perizia(self):
        pass
