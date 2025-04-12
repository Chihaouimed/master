# models/fiche_intervention.py
from odoo import models, fields, api


class FicheIntervention(models.Model):
    _name = 'fiche.intervention'
    _description = 'Fiche d\'intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_intervention desc, id desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code(
                           'fiche.intervention.sequence') or 'Nouveau')

    # Nouveaux champs selon les spécifications
    type_intervention = fields.Selection([
        ('preventive', 'Préventive'),
        ('corrective', 'Corrective'),
        ('installation', 'Installation'),
        ('mise_a_jour', 'Mise à jour'),
        ('autre', 'Autre')
    ], string='Type d\'intervention', required=True)

    equipe_intervention_ids = fields.Many2many('hr.employee', string='Équipe d\'Intervention')

    # État aligné avec le module Help Desk (réclamation)
    state = fields.Selection([
        ('draft', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('closed', 'Fermé'),
        ('block', 'Bloqué')
    ], string='État', default='draft', tracking=True)

    # Champs temporels
    date_intervention = fields.Date(string='Date d\'intervention', required=True, default=fields.Date.today)
    heure_intervention = fields.Float(string='Heure d\'intervention', help="Format 24h (ex: 13.5 pour 13h30)")
    agenda = fields.Text(string='Agenda', help="Planification détaillée de l'intervention")

    # Champ pour le bilan final qui apparaît uniquement à l'état fermé
    intervention_text = fields.Text(string='Bilan de l\'intervention',
                                    help="Rapport détaillé de l'intervention effectuée")

    # Champs relationnels
    reclamation_id = fields.Many2one('reclamation', string='Réclamation associée')
    installation_id = fields.Many2one('pv.installation', string='Installation')
    code_alarm_id = fields.Many2one('alarm.management', string='Code Alarm')
    adresse = fields.Char(string='Adresse')

    # Méthodes pour changer d'état
    def action_draft(self):
        self.write({'state': 'draft'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_closed(self):
        self.write({'state': 'closed'})

    def action_block(self):
        self.write({'state': 'block'})

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