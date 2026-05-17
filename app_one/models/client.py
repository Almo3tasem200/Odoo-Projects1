from odoo import models, fields

# model inheritance
class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'
