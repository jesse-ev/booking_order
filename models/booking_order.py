from odoo import models, api, fields
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class BookingOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(
        string='Is Booking Order'
    )
    booking_team_id = fields.Many2one(
        comodel_name='service.team',
        string='Service Team',
        default=False,
        required=True,
    )    

    team_leader_id = fields.Many2one(
        comodel_name='res.users',
        string='Service Team Leader',
        compute='_compute_team_leader',
    )
    team_member_ids = fields.Many2many(
        comodel_name='res.users',
        string='Service Members',
        compute='_compute_team_member',
        readonly=True
    )

    team_availability = fields.Selection(string='Team Availability', 
        selection=[
            ('not_selected', 'Please select a team...'), 
            ('available', 'Available'),
            ('not_available', 'Not Available'),
            ],
        readonly=True,
        default='not_selected',
    )
    

    booking_start = fields.Date(
        string='Booking Start',
        default=fields.datetime.now(),
        required=True,
    )

    booking_end = fields.Date(
        string='Booking End',
        default=date_utils.add(fields.datetime.now(), days=1),
        required=True,
    )                                

    def check_team_availability(self):
        other_project = None
        has_another_work = self.env['sale.work.order'].search([('booking_team_id', '=', self.booking_team_id.id), ('state', 'not in', ['cancel', 'done'])])
        another_work_start_date = fields.Date.from_string(has_another_work.planned_start)   #StartA 
        another_work_end_date = fields.Date.from_string(has_another_work.planned_end)       #EndA
        new_start_date = self.booking_start                                                 #StartB
        new_end_date = self.booking_end                                                     #EndB
        other_project = has_another_work.sale_order_id.name
        return another_work_end_date <= new_start_date or another_work_start_date >= new_end_date, other_project

    def button_check_team_availability(self):
        pass

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

    # @api.onchange('booking_team_id', 'booking_start', 'booking_end')
    # def _onchange_booking_team_id(self):
    #     has_another_work = self.env['sale.work.order'].search([('booking_team_id', '=', self.booking_team_id.id), ('state', 'not in', ['cancel', 'done'])])
    #     if self.booking_team_id and has_another_work:
    #         avail, other_project = self.check_team_availability()
    #         if avail:
    #             #no overlap
    #             return {
    #                 'warning': {
    #                     'title': 'Team status : Available',
    #                     'message': 'Team has other work but date not overlapping is free'
    #                 }
    #             }
    #         else:
    #             #overlap
    #             return {
    #                 'warning': {
    #                     'title': 'Team status : Not Available',
    #                     'message': 'Team has other work and date overlapping is not free' + '\n' + 'Project : ' + str(other_project)
    #                 }
    #             }
    #     elif self.booking_team_id:
    #         return {
    #             'warning': {
    #                 'title': 'Team status : Available',
    #                 'message': 'Team is free'
    #             }
    #         }

    @api.onchange('booking_team_id', 'booking_start', 'booking_end')
    def _onchange_check_member_availability(self):
        #TODO : Actually showing the member whose cant work on the date
        unavailable_name_list = []
        unavailable_job_list = []
        if self.booking_team_id:
            for member in self.booking_team_id.team_member_ids:
                has_another_work = self.env['sale.work.order'].search([('team_member_ids', 'in', member.id), ('state', 'not in', ['cancel', 'done'])])
                if has_another_work:
                    for work in has_another_work:
                        another_work_start_date = fields.Date.from_string(work.planned_start)   #StartA 
                        another_work_end_date = fields.Date.from_string(work.planned_end)       #EndA
                        new_start_date = self.booking_start                                     #StartB
                        new_end_date = self.booking_end                                         #EndB
                        if another_work_end_date <= new_start_date or another_work_start_date >= new_end_date: #if true, available
                            pass
                        else:
                            unavailable_name_list.append(member.name)
                            unavailable_job_list.append(work.name)
        if unavailable_name_list:
            final = '\n'.join([str(unavailable_name_list[i]) + " " + str(unavailable_job_list[i]) for i in range(0, len(unavailable_name_list))])
            self.team_availability = 'not_available'
            self.booking_team_id = None
            return {
                'warning': {
                    'title': 'Member status : Not Available',
                    'message': 'Member is not available on this team' + '\n' + str(final)
                }
            }
        elif len(unavailable_name_list) == 0 and self.booking_team_id:
            self.team_availability = 'available'
            return {
                'warning': {
                    'title': 'Member status : Available',
                    'message': 'All member is available on this team'
                }
            }


    @api.constrains('booking_end')
    def _date_check(self):
        for record in self:
            start = record.booking_start
            end = record.booking_end
            if start and end:
                if start > end:
                    raise models.ValidationError("Booking Start Date should be less than Booking End Date")

    @api.model
    def create(self, vals):
        if vals['is_booking_order']:
            record = super(BookingOrder, self).create(vals)
            if record.is_booking_order:
                self.env['sale.work.order'].create({
                    'name' : self.env['ir.sequence'].next_by_code('sequence.order'),
                    'sale_order_id' : record.id,
                    'booking_team_id' : record.booking_team_id.id,
                    'planned_start' : record.booking_start,
                    'planned_end' : record.booking_end,
                    'state' : 'waiting'
                })
            return record
        else:
            raise ValidationError("Please choose other team or date")
    
    