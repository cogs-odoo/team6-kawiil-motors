from odoo import fields, models

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'

    lot_id = fields.One2many(comodel_name="stock.lot", string="Lot", inverse_name="motorcycle_id")