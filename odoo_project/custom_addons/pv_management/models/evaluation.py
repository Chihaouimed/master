from odoo import models, fields, api


class Evaluation(models.Model):
    _name = 'pv.evaluation'
    _description = 'PV Installation Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('pv.evaluation.sequence') or 'New')
    installation_id = fields.Many2one('pv.installation', string='Installation', required=True)
    date_evaluation = fields.Date(string='Evaluation Date', default=fields.Date.today, required=True)
    evaluator_id = fields.Many2one('hr.employee', string='Evaluator')

    # Technical evaluation fields
    performance_ratio = fields.Float(string='Performance Ratio (%)',
                                     help='Actual output compared to theoretical output')
    energy_produced = fields.Float(string='Energy Produced (kWh)')
    system_efficiency = fields.Float(string='System Efficiency (%)')

    # Maintenance evaluation
    panel_condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], string='Panel Condition', tracking=True)

    inverter_condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], string='Inverter Condition', tracking=True)

    # Issues found
    issues_found = fields.Text(string='Issues Found')

    # Recommendations
    recommendations = fields.Text(string='Recommendations')

    # State for workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('canceled', 'Canceled')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pv.evaluation.sequence') or 'New'
        return super(Evaluation, self).create(vals)

    # Action methods for state changes
    def action_draft(self):
        self.write({'state': 'draft'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'canceled'})

    # Navigation method to related installation
    def action_view_installation(self):
        self.ensure_one()
        return {
            'name': 'Installation',
            'view_mode': 'form',
            'res_model': 'pv.installation',
            'res_id': self.installation_id.id,
            'type': 'ir.actions.act_window',
        }