# -*- coding: utf-8 -*-Book model, where it will be used:

from openerp import models, fields


# ToDo In futuro Inserire qui le funzionalità di base dell'oggeto
class BasePerizia(models.AbstractModel):
    _name = 'base.perizia'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active
