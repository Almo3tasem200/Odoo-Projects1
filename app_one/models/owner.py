from odoo import models, fields


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=1)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property','owner_id') #owner_id: foreign key in other table

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is already taken! ')
    ]