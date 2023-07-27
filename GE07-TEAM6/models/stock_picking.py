from odoo import fields, models, api, Command

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super()._action_done()

        # When? When destination is partner/customers address: if location_dest_id == self.env.ref("stock.stock_location_customers") ?
        # When? When sale is validated: Sale > S0000 > Transfers
        # Keep in mind: Cancel validation shouldn't create a registry

        if res:
            for line in self.move_line_ids:
                if line.product_id.product_tmpl_id.detailed_type == 'motorcycle' and self.location_dest_id == self.env.ref('stock.stock_location_customers'):
                    if self.origin:
                        records = self.env['sale.order'].search([('name', '=', self.origin)], limit = 1)
                        sale_order = records[0].id if len(records) > 0 else False
                    else:
                        sale_order = False
                    
                    self.env['motorcycle.registry'].create({
                        'lot_ids': [Command.link(line.lot_id.id)],
                        'sale_order_id': sale_order, 
                    })
            
        return res
