from odoo import models, fields

class PVInverter(models.Model):
    _name = 'pv.inverter'
    _description = 'PV Inverter'
    installation_id = fields.Many2one('pv.installation', string='Installation')

    number_of_inverters = fields.Selection([
        ('1', '1'),
        ('2', '2')
    ], string='Number of Inverters')
    reference_onduleur_pv1_id = fields.Many2one('configuration.district.steg', string='Reference Onduleur PV1')
    marque_onduleur_pv1 = fields.Char(related='reference_onduleur_pv1_id.name', string='Marque Onduleur PV1', readonly=True)
    puissance_onduleur_pv1 = fields.Char(string='Puissance Onduleur 1 (kVA)')
    calibre_disjoncteur_onduleur_pv1 = fields.Char(string='Calibre Disjoncteur Onduleur 1 (A)')
    nombre_onduleur_pv1 = fields.Integer(string="Nombre d'Onduleur 1")
    puissance_totale_ag = fields.Char(string='Puissance Totale AG (KVA)')