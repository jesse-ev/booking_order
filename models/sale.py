from odoo import api, fields, models


class Booking(models.Model):
    _inherit = "sale.order"

    name = fields.Char(string='Name')
