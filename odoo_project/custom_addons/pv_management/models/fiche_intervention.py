
from odoo import models, fields, api


class FicheIntervention(models.Model):
    _name = 'fiche.intervention'
    _description = 'Fiche d\'intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code(
                           'fiche.intervention.sequence') or 'Nouveau')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    adresse = fields.Char(string='Adresse')
    installation_id = fields.Many2one('pv.installation', string='Installation')
    reclamation_id = fields.Many2one('reclamation', string='Réclamation associée')
    code_alarm_id = fields.Many2one('alarm.management', string='Code Alarm')
    description = fields.Text(string='Description de l\'intervention')
    actions_effectuees = fields.Text(string='Actions effectuées')

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('scheduled', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('canceled', 'Annulée')
    ], string='État', default='draft', tracking=True)

    technicien_id = fields.Many2one('hr.employee', string='Technicien')

    def action_view_reclamation(self):
        """Bouton pour revenir à la réclamation d'origine"""
        self.ensure_one()
        if not self.reclamation_id:
            return

        return {
            'name': 'Réclamation',
            'view_mode': 'form',
            'res_model': 'reclamation',
            'res_id': self.reclamation_id.id,
            'type': 'ir.actions.act_window',
        }