# -*- coding: utf-8 -*-

from perizie.models.base_perizia import BasePerizia
from openerp import models, fields, api


class Perizia(models.Model):
    _name = 'perizie.perizia'
    _inherit = ['base.perizia']

    _description = 'Perizia'
    _order = 'name'
    _rec_name = 'short_name'

    short_name = fields.Char(
        string='Short Title of Perizia',
        size=100,  # For Char only
        translate=False,  # also for Text fields
    )
    name = fields.Char('Title', required=True)

    # Il numero della perizia è identificato come:  numero anno mod.xxx
    numero_procedimento = fields.Integer(
        string='Numero Procedimento',
        search='_search_numero_procedimento',
        # compute_sudo=False,
    )
    numero_procedimento_anno = fields.Integer(
        search='_search_numero_procedimento_anno',
    )
    numero_procedimento_mod = fields.Integer(
        string='Mod.',
        search='_search_numero_procedimento_mod',
    )
    descrizione = fields.Text('Descrizione')

    # Consulente Tecnico
    ct_id = fields.Many2one(
        'res.partner', string='Consulente Tecnico',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    # Pubblico Ministero
    pm_id = fields.Many2one(
        'res.partner', string='Pubblico Ministero',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    # Indagato
    indagati_ids = fields.Many2many(
        'res.partner',
        string='Indagati')

    # Numero perizia
    # Indagato
    # PM
    # Consulente Tecnico
    # Data Inizio Operazioni
    # Data Scadenza o giorni disponibili
    # Descrizione
    # Reperti
