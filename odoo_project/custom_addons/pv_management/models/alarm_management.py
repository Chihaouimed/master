from odoo import models, fields, api

class AlarmManagement(models.Model):
    _name = 'alarm.management'
    _description = 'Alarm Management'
    
    name = fields.Char(string='Name', required=True, translate=True)
    type = fields.Char(string='Type', translate=True)
    partie = fields.Selection([
        ('onduleur', 'Onduleur'),
        ('module', 'Module'),
        ('installation', 'Installation'),
        ('batterie', 'Batterie'),
        ('autre', 'Autre')
    ], string='Partie', required=True, translate=True)
    marque_onduleur_id = fields.Many2one('pv.inverter', string='Marque Onduleur', translate=True)
    code_alarm = fields.Char(string='Code Alarm', required=True, translate=True)


