# -*- coding: utf-8 -*-

from perizie.models.base_reperto import BaseReperto
from openerp import models, fields, api
from openerp.fields import Date as fDate
import time, datetime


class RepertoCellulare(models.Model):
    _name = 'perizie.reperto.cellulare'
    _inherit = ['base.reperto']

    _description = 'Reperto Cellulare'
    _order = 'name'
    _rec_name = 'short_name'


class RepertoHardDisk(models.Model):
    _name = 'perizie.reperto.hd'
    _inherit = ['base.reperto']

    _description = 'Reperto Hard Disk'
    _order = 'name'
    _rec_name = 'short_name'


class RepertoMemoriaUsb(models.Model):
    _name = 'perizie.reperto.usb'
    _inherit = ['base.reperto']

    _description = 'Reperto Memoria USB'
    _order = 'name'
    _rec_name = 'short_name'


class RepertoTablet(models.Model):
    _name = 'perizie.reperto.tablet'
    _inherit = ['base.reperto']

    _description = 'Reperto Tablet'
    _order = 'name'
    _rec_name = 'short_name'


class RepertoMacchinaFotografica(models.Model):
    _name = 'perizie.reperto.fotografica'
    _inherit = ['base.reperto']

    _description = 'Reperto Macchina Fotografica'
    _order = 'name'
    _rec_name = 'short_name'
