from odoo import models, fields

class PVInverter(models.Model):
    _name = 'pv.inverter'
    _description = 'PV Inverter'

    number_of_inverters = fields.Selection([
        ('1', '1'),
        ('2', '2')
    ], string='Number of Inverters')
    display_condition = fields.Char(string='Display Condition')
    reference = fields.Char(string='Reference', required=True)
    brand = fields.Char(string='Brand')
    power = fields.Float(string='Power (KVA)')
    generation_capacity = fields.Float(string='Generation Capacity (A)')
    total_power = fields.Float(string='Total Power (KVA)')