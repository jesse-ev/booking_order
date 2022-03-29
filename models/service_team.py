from odoo import api, fields, models


class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'New Description'

    name = fields.Char(
        string='Team Name', 
        placeholder='Team Name',
        required=True
    )
    team_leader_id = fields.Many2one(
        string='Team Leader',
        comodel_name='res.users',
        required=True,
    )
    team_member_ids = fields.Many2many(
        string='Team Members',
        comodel_name='res.users',
    )

    
    
