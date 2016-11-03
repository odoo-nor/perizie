# -*- coding: utf-8 -*-

from openerp import models, fields


class RepertoTypology(models.Model):
    _name = 'base.reperto.categoria'
    name = fields.Char('Title', required=True)


class BaseReperto(models.AbstractModel):
    _name = 'base.reperto'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active

    name = fields.Char(string='Marca',
                       required=True, size=50, translate=False)
    serial_number = fields.Char(string='Serial Number',
                                required=True, size=50, translate=False)
    modello = fields.Char(string='Modello',
                          required=True, size=50, translate=False)
    categoria = fields.Many2one(
        'base.reperto.categoria', 'Categoria',
        required=True,
        help="...si possono inserire nuove categorie dal menu Categorie.")

    dimensione = fields.Float(string='Dimensione')


