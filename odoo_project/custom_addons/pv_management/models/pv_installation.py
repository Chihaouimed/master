# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PVInstallation(models.Model):
    _name = 'pv.installation'
    _description = 'Solar PV Installation'
    _order = 'id desc'

    # Fields
    name = fields.Char(string='Nom', required=True)
    client_central = fields.Many2one('res.partner', string='Client Central')
    address_id = fields.Many2one(
        'res.partner',
        string='Adresse',
        ondelete='set null'
    )
    capacity = fields.Float(string='Capacité (kW)')

    # State Field
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('in_progress', 'En cours'),
            ('pending', 'En attente'),
            ('in_production', 'En production'),
            ('in_stop', 'En arrêt'),
            ('canceled', 'Annulé'),
        ],
        string='État',
        default='draft',
        tracking=True
    )

    # State Change Methods
    def action_draft(self):
        self.write({'state': 'draft'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_pending(self):
        self.write({'state': 'pending'})

    def action_in_production(self):
        self.write({'state': 'in_production'})

    def action_in_stop(self):
        self.write({'state': 'in_stop'})

    def action_cancel(self):
        self.write({'state': 'canceled'})