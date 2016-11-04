# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    pm_ids = fields.One2many(
        'forensics.perizia', 'pm_id',
        string='Pubblico Ministero')

    ct_idd = fields.One2many(
        'forensics.perizia', 'ct_id',
        string='Consulente Tecnico')

    indagati_ids = fields.Many2many(
        'forensics.perizia',
        string='Indagati',
        relation='forensics_perizia_indagati_res_partner_rel'
    )

    parti_ids = fields.Many2many(
        'forensics.perizia',
        string='Parti',
        relation='forensics_perizia_parti_res_partner_rel'
    )
