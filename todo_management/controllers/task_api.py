import json
from odoo import http
from odoo.http import request

class TaskApi(http.Controller):

    @http.route("/v1/todo.task", methods=["POST"], type="http", auth="none", csrf=False)
    def post_task(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("name"):
            return request.make_json_response({
                "message": "Name is required"
            }, status=400)
        try:
            res = request.env['todo.task'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "Task created successfully",
                    "id": res.id,
                    "name": res.name
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error
            }, status=400)




    @http.route("/v1/todo.task/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_task_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['todo.task'].sudo().create(vals)
        print(vals)
        if res:
            return {
                "message": "Task created successfully"
            }

    @http.route("/v1/todo.task/<int:task_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_task(self, task_id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id', '=', task_id)])
            if not task_id:
                return request.make_json_response({
                    "message": "Task does not exist!"
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            task_id.write(vals)
            return request.make_json_response({
                "message": "Task updated successfully",
                "id": task_id.id,
                "name": task_id.name

            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)