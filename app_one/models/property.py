from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=True)
    name = fields.Char(required=1, size=50, translate=True)
    description = fields.Text(tracking=True)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=True)
    expected_selling_date = fields.Date(required=1, tracking=True)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    # digits=(0, 5) 5 numbers after the decimal point
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', stored=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')

    owner_id = fields.Many2one('owner') # new field of var: owner_id ('table name')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')

    state = fields.Selection([
        ('draft', 'Draft'), #initial state
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ],default='draft')

    #important
    _sql_constraints = [
        ('unique_name','unique(name)','This name is already taken! ')
    ]

    line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False


    @api.depends('expected_price','selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                return {
                    'warning': {'title': 'Warning' , 'message': 'negative value', 'type': 'notification'}
                }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError("Please add valid number of bedrooms")

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state = 'draft'
            # rec.write({
            #     'state': 'draft',
            # })


    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state,'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state,'sold')
            rec.state = 'sold'
            rec.is_late = False

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        # print(property_ids)
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today() and rec.state != 'sold':
                rec.is_late = True

    def action(self):
        #like return Property1 and any similar to it but
        #ilike return P or p for property1 capital or small
        print(self.env['property'].search(['|', ('name', '=', 'Property1'), ('postcode', '!=', '12435')]))
        # | : or , & : and , ! : not
        # print(self.env['owner'].create({
        #     'name': 'name two',
        #     'phone': '0100000000',
        # }))
        # login=mail
        # uid = user.id
        # company
        # context
        # cr (cursor)


    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids],
                # 0 means create 0 for unexist record then  a dictionary {}
                # to put in our group of basic values to create our record or our line
                # line_ids that found in properties as bedrooms so in each line of it create a magic tuple
                # to create the line then take the id and assign to line_ids
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action


# CRUD Operation: create, read:search, update:write, delete:unlink
#     @api.model_create_multi
#     def create(self, vals):
#         res = super(Property, self).create(vals)
#         print("inside create method")
#         return res
#
#     @api.model
#     def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
#         res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
#         print("inside search method")
#         return res
#
#
#     def write(self, vals):
#         res = super(Property, self).write(vals)
#         print("inside write method")
#         return res


# def unlink(self):
#     res = super(Property, self).unlink()
#     print("inside unlink method")
#     return res


class PropertyLines (models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()




