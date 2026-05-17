from odoo import http

class TestAPI(http.Controller):

    @http.route('/api/test', type='http', auth='public', methods=['GET'], csrf=False)
    def test_api(self, **kwargs):
        return "HELLO API"