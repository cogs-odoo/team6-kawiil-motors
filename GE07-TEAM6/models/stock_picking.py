from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super(self)._action_done()
            
        return res
