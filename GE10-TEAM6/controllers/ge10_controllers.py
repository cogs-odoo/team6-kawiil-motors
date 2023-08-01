from odoo import http

class Academy(http.Controller):
    @http.route('/mileage', type='json', auth = 'public')
    def get_mileage(self):
        mileage_count = 0
        registries = http.request.env['motorcycle.registry'].search([])

        for registry in registries:
            mileage_count = mileage_count + registry.current_mileage

        return mileage_count
    