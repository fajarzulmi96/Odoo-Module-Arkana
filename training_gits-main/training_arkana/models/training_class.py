from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TrainingClass(models.Model):
    _name = 'training.class'
    _description = 'Training Class'

    # basic
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    max_person = fields.Integer(string='Max Person')
    max_duration = fields.Float(string='Max Duration (in hours)')
    
    # advance
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], string='State', default='draft')
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    class_datetime = fields.Date(string='Datetime')
    price = fields.Monetary(string='Price')
    class_image = fields.Image(string='Image')
    class_file = fields.Binary(string='File')

    # relational
    currency_id = fields.Many2one('res.currency', string='Currency')
    mentor_ids = fields.Many2many('res.partner', string='Mentor')

    # compute
    total_days = fields.Integer('Days', compute='_compute_total_days')
    currency_symbol = fields.Char(string='Currency Symbol', related='currency_id.symbol')
    
    @api.depends('start_date', 'end_date')
    def _compute_total_days(self):
        for record in self:
            total_days = 0
            if record.end_date and record.start_date:
                total_days = (record.end_date - record.start_date).days
            record.total_days = total_days

    @api.constrains('name', 'description')
    def _check_description(self):
        for record in self:
            if record.name == record.description:
                raise ValidationError("Fields name and description must be different")
    
    @api.onchange('start_date')
    def _onchange_start_date(self):
        self.end_date = self.start_date
