from odoo import api, fields, models
import string, random

class res_users_ex(models.Model):
    _inherit = 'res.users'

    name = fields.Char(string='Name')
    
    

    # access_token = fields.Text(string='API Access Token', default=False)

    # def create(self, vals):
    #     key = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 48))
    #     user_id = super(res_users_ex, self).create(vals)
    #     if key:
    #         user_id.access_token = key

    #     return user_id