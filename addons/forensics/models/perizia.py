# -*- coding: utf-8 -*-

from forensics.models.base_perizia import BasePerizia
from openerp import models, fields, api
from openerp.fields import Date as fDate
import time, datetime


class Perizia(models.Model):
    _name = 'forensics.perizia'
    _inherit = ['base.perizia']

    _description = 'Perizia'
    _order = 'name'

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
            if r.fine_operazioni is not False and r.fine_operazioni < r.inizio_operazioni:
                raise models.ValidationError(
                    'La Data di Consegna deve essere successiva alla data di Inizio Operazioni!')

    # Il numero della perizia è identificato come:  numero anno mod.xxx

    name = fields.Char(
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
        string='Indagati',
        relation='forensics_perizia_indagati_res_partner_rel'
    )

    # Parti
    parti_ids = fields.Many2many(
        'res.partner',
        string='Parti',
        relation='forensics_perizia_parti_res_partner_rel'
    )

    inizio_operazioni = fields.Date('Inizio Operazioni')

    giorni_consegna = fields.Float(
        string='Giorni alla Consegna',
        compute='_compute_age',
        inverse='_inverse_age',
        store=False,
        compute_sudo=False,
    )

    reperti = fields.One2many(
        'forensics.reperto', 'perizia_id',
        String='Reperti')

    fine_operazioni = fields.Date('Data di Consegna')

    @api.depends('fine_operazioni')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        self._check_release_date()
        for perizia in self.filtered('fine_operazioni'):
            delta = fDate.from_string(perizia.fine_operazioni) - fDate.from_string(perizia.inizio_operazioni)
            # delta = fDate.from_string(days)
            perizia.giorni_consegna = delta.days

    # TODO da aggiungere il completamento con l'inserimento dei giorni senza la data
    def _inverse_age(self):
        # self._check_release_date()
        # for perizia in self.filtered('fine_operazioni'):
        #     delta = fDate.from_string(perizia.fine_operazioni) - fDate.from_string(self.inizio_operazioni)
        #     # delta = fDate.from_string(days)
        #     perizia.giorni_consegna = delta.days
        pass
