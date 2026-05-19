from odoo import fields, models

class ChangeStates(models.TransientModel):
    _name = 'change.states'

    todo_task_id = fields.Many2one('todo.task')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In_Progress'),
    ],default='new')
    reason = fields.Char('Reason')

    def action_conf(self):
        if self.todo_task_id.state == 'closed':
            self.todo_task_id.state = self.state
