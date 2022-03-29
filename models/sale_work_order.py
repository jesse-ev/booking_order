from odoo import api, fields, models


class ModuleName(models.Model):
    _name = 'sale.work.order'
    _description = 'Sale work order'

    name = fields.Char(
        string='WO Number',
        copy=False,
        readonly=True,
    )

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Booking Order Ref',
        required=True,
        readonly=True,
    )

    booking_team_id = fields.Many2one(
        comodel_name='service.team', 
        string='Service Team',
        readonly=True,
    )

    team_leader_id = fields.Many2one(
        comodel_name='res.users',
        string='Service Team Leader',
        compute='_compute_team_leader',
        readonly=True,
    )

    team_member_ids = fields.Many2many(
        comodel_name='res.users',
        string='Service Members',
        compute='_compute_team_member',
        readonly=True,
    )

    planned_start = fields.Datetime(
        string='Date Start',
        readonly=True,
    )

    planned_end = fields.Datetime(
        string='Date End',
        readonly=True,
    )

    date_start = fields.Datetime(
        string='Date Start',
        readonly=True,
    )

    date_end = fields.Datetime(
        string='Date End',
        readonly=True,
    )

    state = fields.Selection(
        string='Status', 
        selection=[
            ('waiting', 'Waiting'),
            ('pending', 'Pending'), 
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
        ],
        readonly=True,
    )

    notes = fields.Text(
        string='Notes'
    )

    @api.model
    def create(self, vals):
        res = super(ModuleName, self).create(vals)
        return res
    
    @api.depends('booking_team_id')
    def _compute_team_leader(self):
        for rec in self:
            service_team = self.env['service.team'].search([('id', '=', rec.booking_team_id.id)])
            rec.team_leader_id = service_team.team_leader_id.id

    @api.depends('booking_team_id')
    def _compute_team_member(self):
        for rec in self:
            service_team = self.env['service.team'].search([('id', '=', rec.booking_team_id.id)])
            rec.team_member_ids = service_team.team_member_ids.ids

    '''Button methods'''
    def start_work(self):
        self.write({
            'state': 'in_progress',
            'date_start': fields.datetime.now(),
        })

    def stop_work(self):
        self.write({
            'state': 'done',
            'date_end': fields.datetime.now(),
        })

    def reset_work(self):
        self.write({
            'state': 'waiting',
            'date_start': None,
        })
    
    def cancel_work(self):
        return {
            'name': 'Cancellation Reason',
            'domain': [],
            'res_model': 'booking.order.cancel',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'active_id': self.id},
            'target': 'new',
        }
        self.write({
            'state': 'cancel',
            'date_start': None,
        })