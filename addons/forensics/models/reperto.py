# -*- coding: utf-8 -*-

from forensics.models.base_reperto import BaseReperto
from openerp import models, fields, api


class Reperto(models.Model):
    _name = 'forensics.reperto'
    _inherit = ['base.reperto']

    _description = 'Reperto'
    _order = 'name'

    descrizione_verbale = fields.Text(string='Descrizione come da Verbale',
                                      required=False, translate=False)

    numero_reperto = fields.Integer(string='Numero', readonly=True)

    perizia_id = fields.Many2one('forensics.perizia', 'Perizia')

    immagine_ids = fields.One2many(
        'forensics.img.reperto', 'reperto_img_id',
        String='Immagini')
