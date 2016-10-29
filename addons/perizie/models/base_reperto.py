# -*- coding: utf-8 -*-Book model, where it will be used:

from openerp import models, fields


class BaseReperto(models.AbstractModel):
    _name = 'base.reperto'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


# Serial Number
# Marca
# Modello
# Tipologia