
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reclamation(models.Model):
    _name = 'reclamation'
    _description = 'Réclamation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    # Champs principaux
    name = fields.Char(string='Référence', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('reclamation.sequence') or 'Nouveau')
    date_heure = fields.Datetime(string='Date et Heure', required=True, default=fields.Datetime.now)
    adresse = fields.Char(string='Adresse', required=True)
    contrat_id = fields.Many2one('res.partner', string='Contrat')  # À adapter selon votre modèle de contrat
    nom_central_id = fields.Many2one('pv.installation', string='Nom Central')
    description = fields.Text(string='Description', required=True)
    code_alarm_id = fields.Many2one('alarm.management', string='Code Alarm')
    cause_alarme = fields.Text(string='Cause de l\'Alarme')

    # État de la réclamation
    state = fields.Selection([
        ('draft', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('closed', 'Fermé'),
        ('block', 'Bloqué')
    ], string='État', default='draft', tracking=True)

    # Champ pour lier à fiche.intervention (si ce modèle existe ou sera créé)
    intervention_ids = fields.One2many('fiche.intervention', 'reclamation_id', string='Fiches d\'intervention')

    # Méthodes pour changer d'état
    def action_draft(self):
        self.write({'state': 'draft'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_closed(self):
        self.write({'state': 'closed'})
        # Déclencher l'email après le changement d'état
        self._send_notification_email()

    def action_block(self):
        self.write({'state': 'block'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('reclamation.sequence') or 'Nouveau'
        return super(Reclamation, self).create(vals)

    def _send_notification_email(self):
        """Envoi d'email lors de la fermeture d'une réclamation"""
        self.ensure_one()
        if not self.contrat_id or not self.contrat_id.email:
            return False

        template = self.env.ref('pv_management.email_template_reclamation_closed', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def action_create_intervention(self):
        """Bouton pour créer une fiche d'intervention"""
        self.ensure_one()
        return {
            'name': 'Créer une fiche d\'intervention',
            'view_mode': 'form',
            'res_model': 'fiche.intervention',
            'type': 'ir.actions.act_window',
            'context': {
                'default_reclamation_id': self.id,
                'default_installation_id': self.nom_central_id.id,
                'default_adresse': self.adresse,
                'default_code_alarm_id': self.code_alarm_id.id,
            },
        }