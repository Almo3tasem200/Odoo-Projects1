from addons.web.controllers import action
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

from odoo.tools.populate import compute
# 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

class TodoTask(models.Model):
    _name = "todo.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Task"

    name = fields.Char('Task Name', required=True)
    assign_to_id = fields.Many2one('res.partner')
    description = fields.Text('Description')
    due_date = fields.Date('Due Date')
    estimated_time = fields.Float(string="Estimated Time in Hours")
    is_late = fields.Boolean()
    total_time = fields.Float(compute="_compute_total_time")

    timesheet_ids = fields.One2many('timesheet.line', 'timesheet_id')

    created_time = fields.Datetime(default=fields.Datetime.now(), str='Created Time', groups="todo_management.task_manager_group")
    updated_time = fields.Datetime(str='Updated Time')

    state = fields.Selection([
        ("new", "New"),
        ("in_progress", "In Progress ..."),
        ("completed", "Completed"),
        ('closed', 'Closed')
    ],default="new")

    active = fields.Boolean(default=True)

    def action_in_progress(self):
        for rec in self:
            rec.state = "in_progress"

    def action_completed(self):
        for rec in self:
            rec.state = "completed"
            rec.is_late = False


    def action_new(self):
        for rec in self:
            rec.state = "new"

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def check_due_date(self):
        todo_task_ids = self.search([])
        for rec in todo_task_ids:
            if rec.due_date and rec.due_date < fields.Date.today() :
                rec.is_late = True

    @api.depends("timesheet_ids.hours")
    def _compute_total_time(self):
        for rec in self:
            rec.total_time = sum(rec.timesheet_ids.mapped("hours"))

    @api.constrains("estimated_time", "total_time")
    def _check_timesheet_hours(self):
            for rec in self:
                if rec.total_time > rec.estimated_time:
                    raise ValidationError(
                        "Total timesheet hours cannot exceed estimated time"
                    )

    def action_change_states_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('todo_management.change_states_wizard_action')
        action['context'] = {'default_todo_task_id': self.id}
        return action


    def write(self, vals):
        vals['updated_time'] = fields.Datetime.now()
        return super(TodoTask, self).write(vals)
    # this fn updates time automatic for now when user updates any record


class TodoTimesheet(models.Model):
    _name = "timesheet.line"


    timesheet_id = fields.Many2one('todo.task', string="Task", required=True)
    day = fields.Integer(string="Day")
    description = fields.Char(string="Description", required=True)
    hours = fields.Float(string="Hours")