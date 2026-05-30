from odoo import http

class TestTheApi(http.Controller):

    @http.route("/api/testit", methods=["GET"],type="http", auth="none", csrf=False)
    def test_the_endpoint(self):
        print("inside test_the_endpoint method")