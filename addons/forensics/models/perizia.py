# -*- coding: utf-8 -*-

from forensics.models.base_perizia import BasePerizia
from openerp import models, fields, api
from openerp.fields import Date as fDate
import time, datetime
from datetime import timedelta as td
import os
import subprocess
import shutil
import mimetypes
import base64
import magic
import datetime
import time
import logging


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

    # all_verbale_incarico = fields.Many2many('ir.attachment', string="Conferimento Incarico")
    # all_verbale_consegna = fields.Many2many('ir.attachment', string="Consegna in affidamento")
    all_vari = fields.Many2many('ir.attachment', string="Vari")

    mimetype = fields.Char('Mime Type', size=64)

    STATE_SELECTION = [
        ('draft', 'Compilazione'),
        ('registered', 'Registrato'),
        ('notified', 'Notificato'),
        ('waiting', 'Pec Inviata'),
        ('error', 'Errore Pec'),
        ('sent', 'Inviato'),
        ('canceled', 'Annullato'),
    ]
    state = fields.Selection(
        STATE_SELECTION, 'Stato', readonly=True,
        help="Lo stato del protocollo.", select=True),

    reserved = fields.Boolean('Riservato',
                              readonly=True,
                              help="Se il protocollo e' riservato \
        il documento risulta visibile solo \
        all'ufficio di competenza")

    datas = fields.Binary('File Documento', required=False)

    @api.onchange('datas')
    def on_change_datas(self, cr, uid, ids,
                        datas,
                        context=None):
        values = {}
        if datas:
            ct = magic.from_buffer(base64.b64decode(datas), mime=True)
            values = {
                'preview': datas,
                'mimetype': ct
            }
        return {'value': values}

    @api.depends('datas')
    def _get_preview_datas(self):
        if isinstance(self.ids, (list, tuple)) and not len(self.ids):
            return []
        if isinstance(self.ids, (long, int)):
            self.ids = [self.ids]
        res = dict.fromkeys(self.ids, False)
        # self.browse(self.env.cr, self.env.uid, self.ids[0], context=None)

        prot = self.browse(self.ids[0])
        if prot.datas is not None:
            res[prot.id] = prot.datas

        res[self.id] = self.datas
        self.preview = res
        # return res

    def _inverse_preview(self):

        pass

    preview = fields.Binary(string='Preview',
                            compute='_get_preview_datas',
                            inverse='_inverse_preview',
                            store=False,
                            compute_sudo=False, )

    reperti = fields.One2many(
        'forensics.reperto', 'perizia_id',
        String='Reperti', store=True)

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
