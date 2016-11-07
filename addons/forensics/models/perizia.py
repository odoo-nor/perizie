# -*- coding: utf-8 -*-

from forensics.models.base_perizia import BasePerizia
from openerp import models, fields, api
from openerp.fields import Date as fDate
import time, datetime
from datetime import timedelta as td


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

    all_verbale_incarico = fields.Many2many('ir.attachment', string="Conferimento Incarico")
    all_verbale_consegna = fields.Many2many('ir.attachment', string="Consegna in affidamento")
    all_vari = fields.Many2many('ir.attachment', string="Vari")

    reperti = fields.One2many(
        'forensics.reperto', 'perizia_id',
        String='Reperti')

    # immagine_ids = fields.One2many(
    #     'forensics.img.reperto', 'perizia_id',
    #     String='Immagini')

    fine_operazioni = fields.Date(
        string='Data di Consegna',
        # compute='_compute_age_fine',
        # inverse='_inverse_age_fine',
        # store=False,
        # compute_sudo=False,
    )

    giorni_consegna = fields.Integer(
        string='Giorni alla Consegna',
        compute='_compute_age',
        inverse='_inverse_age',
        store=False,
        compute_sudo=False,
        readonly=True,
    )

    # @api.depends('giorni_consegna')
    # def _compute_age_fine(self):
    #     for perizia in self.filtered('giorni_consegna'):
    #         d = fDate.from_string(perizia.inizio_operazioni) + td(days=perizia.giorni_consegna)
    #         perizia.fine_operazioni = fDate.to_string(d)
    # 
    # def _inverse_age_fine(self):
    #     self._check_release_date()
    #     for perizia in self.filtered('fine_operazioni'):
    #         delta = fDate.from_string(perizia.fine_operazioni) - fDate.from_string(perizia.inizio_operazioni)
    #         # delta = fDate.from_string(days)
    #         perizia.giorni_consegna = delta.days

    @api.depends('fine_operazioni', 'inizio_operazioni')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        self._check_release_date()
        for perizia in self.filtered('fine_operazioni'):
            delta = fDate.from_string(perizia.fine_operazioni) - fDate.from_string(perizia.inizio_operazioni)
            # delta = fDate.from_string(days)
            perizia.giorni_consegna = delta.days

    # TODO da aggiungere il completamento con l'inserimento dei giorni senza la data
    def _inverse_age(self):
        self._check_release_date()
        for perizia in self.filtered('giorni_consegna'):
            d = fDate.from_string(perizia.inizio_operazioni) + td(days=perizia.giorni_consegna)
            # delta = fDate.from_string(perizia.inizio_operazioni) + perizia.giorni_consegna
            perizia.fine_operazioni = fDate.to_string(d)
            # todo fare il check se cambia solo inizio_operazioni con data successiva a fine_operazioni

    def write(self, cr, uid, ids, vals, context=None):
        if 'dossier_type' in vals and vals['dossier_type'] == 'fascicolo':
            vals['parent_id'] = False
        return super(Perizia, self).write(cr, uid, ids, vals, context=context)

    def unlink(self, cr, uid, ids, context=None):
        return super(Perizia, self).unlink(cr, uid, ids, context=context)
