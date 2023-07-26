from odoo import api, fields, models

class StockLot (models.Model):
    _inherit = "stock.lot"
    motorcycle_id = fields.Many2one(comodel_name='motorcycle.registry', ondelete='restrict')
