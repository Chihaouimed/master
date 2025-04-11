from odoo import models, fields, api

class PVModule(models.Model):
    _name = 'pv.module'
    _description = 'PV Module'

    reference = fields.Char(string='Reference', required=True)
    brand = fields.Char(string='Brand')
    size = fields.Char(string='Size')
    power = fields.Float(string='Power (W)')
    number_of_modules = fields.Integer(string='Number of Modules')
    total_power = fields.Float(string='Total Power', compute='_compute_total_power')

    @api.depends('power', 'number_of_modules')
    def _compute_total_power(self):
        for record in self:
            record.total_power = record.power * record.number_of_modules