from odoo import fields, models, api
from odoo.exceptions import ValidationError

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'
    lot_ids = fields.One2many(comodel_name="stock.lot", string="Lot", inverse_name="motorcycle_id")
    lot_id = fields.Many2one(comodel_name="stock.lot", compute='_compute_lot_id')

    vin = fields.Char(related = "lot_ids.name", required = False)
    sale_order_id = fields.Many2one('sale.order', ondelete="restrict")
    owner_id = fields.Many2one(comodel_name='res.partner', ondelete="restrict", related = "sale_order_id.partner_id")

    @api.constrains('lot_ids')
    def _constrain_lot_ids(self):
        for registry in self:
            if len(registry.lot_ids) > 1:
                raise ValidationError('Odoopsie!')
        return True

    @api.depends('lot_ids')
    def _compute_lot_id(self):
        if len(self.lot_ids) > 0:
            self.lot_id = self.lot_ids[0]
        else:
            self.lot_id = False
