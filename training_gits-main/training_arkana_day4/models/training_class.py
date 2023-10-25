from odoo import models, fields, api


class TrainingClass(models.Model):
    _inherit = 'training.class'
    
    name = fields.Char(string='Class Name')
    max_pertemuan = fields.Integer(string='Maximal Pertemuan')


    def action_state_confirm(self):
        self.state = 'confirm'