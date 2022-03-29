# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class booking_order_jess(models.Model):
#     _name = 'booking_order_jess.booking_order_jess'
#     _description = 'booking_order_jess.booking_order_jess'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
