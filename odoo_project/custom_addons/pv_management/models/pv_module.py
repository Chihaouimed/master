from odoo import models, fields, api

class PVModule(models.Model):
    _name = 'pv.module'
    _description = 'PV Module'
    installation_id = fields.Many2one('pv.installation', string='Installation')

    reference = fields.Char(string='Reference Module PV')
    brand = fields.Many2one( 'marque.onduleur' , string='Marque Onduleur')
    power = fields.Char(string='Puissance Module PV (WC)')





