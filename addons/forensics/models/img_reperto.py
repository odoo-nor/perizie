# -*- coding: utf-8 -*-

from openerp import models, fields


class ImgReperto(models.Model):
    _name = 'perizie.img.reperto'

    _description = 'Immagine Reperto'
    _order = 'name'

    name = fields.Text(string='Descrizione foto reperto',
                       required=True, size=100, translate=False)

    image = fields.Binary("Image", attachment=True, help="Immagine limited to 1024x1024px")

    reperto_img_id = fields.Many2one('perizie.reperto', 'Reperto')
