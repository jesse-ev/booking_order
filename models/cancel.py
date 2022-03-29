from odoo import api, fields, models

class Cancel(models.TransientModel):
    _name = 'booking.order.cancel'
    _description = 'Cancel'

    work_order_id = fields.Many2one(
        comodel_name='sale.work.order',
        string='Work Order Ref',
        readonly=True,
        default=lambda self: self._context.get('active_id', False),
    )

    reason = fields.Text(string = 'Reason')

    @api.model
    def create(self, vals):
        work_order = self.env['sale.work.order'].browse(self._context.get('active_id', False))
        work_order.write(
            {'state': 'cancel', 
            'notes': str(work_order.notes) + " Cancel reason : " + str(vals['reason'])})
        return super(Cancel, self).create(vals)
    

    
