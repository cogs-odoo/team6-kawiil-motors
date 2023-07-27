from odoo import fields, models, api
from odoo.exceptions import ValidationError

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'
    lot_ids = fields.One2many(comodel_name="stock.lot", string="Lot", inverse_name="motorcycle_id")
    lot_id = fields.Many2One(compute='_compute_lot_id')

    vin = fields.Char(related = "lot_id.name")
    sale_order_id = fields.Many2one('sale.order', ondelete="restrict")
    owner_id = fields.Many2one(comodel_name='res.partner', ondelete="restrict", related = "sale_order_id.partner_id")

    @api.constrain('lot_ids')
    def _constrain_lot_ids(self):
        for registry in self:
            if len(registry.lot_ids) > 1:
                raise ValidationError('Odoopsie!')
        return True

    @api.depends('lot_ids')
    def _compute_lot_id(self):
        for registry in self:
            if registry.lot_ids != False:
                registry.lot_id = registry.lots_id[0]
            else:
                registry.lot_id = False
