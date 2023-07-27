from odoo import api, fields, models

class StockPicking (models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super()._action_done()

        # When? When destination is partner/customers address: if location_dest_id == self.env.ref("stock.stock_location_customers") ?
        # When? When sale is validated: Sale > S0000 > Transfers
        # Keep in mind: Cancel validation shouldn't create a registry

        for line in self.move_line_ids:

            motorcycle_registry = self.env['motorcycle.registry'].create({
                'vin':self.move_lines_ids.lot_id.name
            })

        return res