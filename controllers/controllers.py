# -*- coding: utf-8 -*-
# from odoo import http


# class BookingOrderJess(http.Controller):
#     @http.route('/booking_order_jess/booking_order_jess/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order_jess/booking_order_jess/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order_jess.listing', {
#             'root': '/booking_order_jess/booking_order_jess',
#             'objects': http.request.env['booking_order_jess.booking_order_jess'].search([]),
#         })

#     @http.route('/booking_order_jess/booking_order_jess/objects/<model("booking_order_jess.booking_order_jess"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order_jess.object', {
#             'object': obj
#         })
