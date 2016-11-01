# -*- coding: utf-8 -*-

from perizie.models.base_reperto import BaseReperto
from openerp import models, fields, api


class Reperto(models.Model):
    _name = 'perizie.reperto'
    _inherit = ['base.reperto']

    _description = 'Reperto'
    _order = 'name'

    descrizione_verbale = fields.Char(string='Descrizione come da Verbale',
                                      required=True, translate=False)

    numero_reperto = fields.Integer(string='Numero del Reperto', readonly=True)

    reperto_id = fields.Many2one('perizie.perizia', 'Perizia')

    immagine_ids = fields.One2many(
        'perizie.img.reperto', 'reperto_img_id',
        String='Immagini')
