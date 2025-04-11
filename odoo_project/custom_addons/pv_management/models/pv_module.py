from odoo import models, fields, api

class PVModule(models.Model):
    _name = 'pv.module'
    _description = 'PV Module'
    installation_id = fields.Many2one('pv.installation', string='Installation')

    reference = fields.Many2one('configuration.district.steg', string='Reference Module PV')
    brand = fields.Char(string='Marque Module PV')
    size = fields.Char(string='N° de Série Module PV')
    power = fields.Char(string='Puissance Module PV (WC)')
    number_of_modules = fields.Integer(string='Nombre de Module', compute='_compute_nombre_module_pv')
    nombre_onduleur = fields.Selection([
        ('1', '1'),
        ('2', '2')
    ], string="Nombre d'Onduleur")
    total_power = fields.Float(string='Total Power', compute='_compute_total_power')

    @api.depends('power', 'number_of_modules')
    def _compute_total_power(self):
        for record in self:
            record.total_power = record.power * record.number_of_modules