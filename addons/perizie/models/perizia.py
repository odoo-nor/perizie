# -*- coding: utf-8 -*-

from perizie.models.base_perizia import BasePerizia
from openerp import models, fields, api
from openerp.fields import Date as fDate
import time, datetime


class Perizia(models.Model):
    _name = 'perizie.perizia'
    _inherit = ['base.perizia']

    _description = 'Perizia'
    _order = 'name'
    # _rec_name = 'short_name'

    _defaults = {
        'inizio_operazioni': lambda *a: time.strftime("%Y-%m-%d"),
    }

    # # Database constraint
    # _sql_constraints = [
    #     ('name_uniq',
    #      'UNIQUE (name)',
    #      'Book title must be unique.')
    # ]

    # Python code constraint
    @api.constrains('fine_operazioni')
    def _check_release_date(self):
        for r in self:
            if r.fine_operazioni is not False and r.fine_operazioni < self.inizio_operazioni:
                raise models.ValidationError(
                    'La Data di Consegna deve essere successiva alla data di Inizio Operazioni!')

    short_name = fields.Char(
        string='Short Title of Perizia',
        size=100,  # For Char only
        translate=False,  # also for Text fields
    )
    name = fields.Char('Title', required=True)

    # Il numero della perizia è identificato come:  numero anno mod.xxx
    numero_procedimento = fields.Char(
        string='Numero Procedimento',
        search='_search_numero_procedimento',
        required=True,
        size=20,
        translate=False,
        # compute_sudo=False,
    )
    numero_procedimento_anno = fields.Selection([(num, str(num)) for num in range((datetime.datetime.now().year - 10),
                                                                                  (datetime.datetime.now().year + 1))],
                                                required=True, )

    numero_procedimento_mod = fields.Char(
        string='Mod.',
        search='_search_numero_procedimento_mod',
        required=True,
        size=10,
        translate=False,
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

    inizio_operazioni = fields.Date('Inizio Operazioni')
    fine_operazioni = fields.Date('Data di Consegna')
    giorni_consegna = fields.Float(
        string='Giorni Dalla Consegna',
        compute='_compute_age',
        inverse='_inverse_age',
        store=False,
        compute_sudo=False,
    )

    reperti = fields.One2many(
        'perizie.reperto', 'reperto_id',
        String='Reperti')

    @api.depends('fine_operazioni')
    def _compute_age(self):
        # today = fDate.from_string(fDate.today())
        self._check_release_date()
        for perizia in self.filtered('fine_operazioni'):
            delta = fDate.from_string(perizia.fine_operazioni) - fDate.from_string(self.inizio_operazioni)
            # delta = fDate.from_string(days)
            perizia.giorni_consegna = delta.days

    # TODO da aggiungere il completamento con l'inserimento dei giorni senza la data
    def _inverse_age(self):
        pass
