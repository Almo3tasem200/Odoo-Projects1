from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

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
    active = fields.Boolean(default=True)

    state = fields.Selection([
        ("new", "New"),
        ("in_progress", "In Progress ..."),
        ("completed", "Completed"),
        ('closed', 'Closed')
    ],default="new")

    def action_in_progress(self):
        for rec in self:
            rec.state = "in_progress"

    def action_completed(self):
        for rec in self:
            rec.state = "completed"

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



class TodoTimesheet(models.Model):
    _name = "timesheet.line"


    timesheet_id = fields.Many2one('todo.task', string="Task", required=True)
    day = fields.Integer(string="Day")
    description = fields.Char(string="Description", required=True)
    hours = fields.Float(string="Hours")