from odoo import models, fields

class PVInverter(models.Model):
    _name = 'pv.inverter'
    _description = 'PV Inverter'
    installation_id = fields.Many2one('pv.installation', string='Installation')

    number_of_inverters = fields.Selection([
        ('1', '1'),
        ('2', '2')
    ], string='Number of Inverters')

    # Inverter 1
    reference_onduleur_pv_id = fields.Char(string='Reference Onduleur PV')
    marque_onduleur_pv_id = fields.Many2one('marque.onduleur', string='Marque Onduleur PV')
    puissance_onduleur_pv = fields.Char(string='Puissance Onduleur (KVA)')
    calibre_disjoncteur_onduleur_pv = fields.Many2one('configuration.district.steg' , string='Calibre Disjoncteur (A)')



    puissance_totale_ag = fields.Char(string='Puissance Totale AG (KVA)')