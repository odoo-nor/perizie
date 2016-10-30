# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    pm_ids = fields.One2many(
        'perizie.perizia', 'pm_id',
        string='Pubblico Ministero')



    perizia_ids = fields.Many2many(
        'perizie.perizia',
        string='Authored Books',
    )

