{
    'name': "To-Do App",
    'author': "Almoatasem",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'mail'
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'reports/todo_task_report.xml',
        'wizard/change_states_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': ['todo_management/static/src/css/task.css'],
        'web.report_assets_common': ['todo_management/static/src/css/font.css']
    },
    'application': True,
}