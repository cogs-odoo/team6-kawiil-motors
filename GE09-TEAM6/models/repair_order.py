from odoo import fields, models, api

class RepairOrder(models.Model):
    _inherit = 'repair.order'
    vin = fields.Char(string='VIN', required = True)
    mileage = fields.Float(string='Mileage')
    registry_id = fields.Many2one("motorcycle.registry", compute='_compute_registry_id_from_vin', store=True)
    partner_id = fields.Many2one(related='registry_id.owner_id')
    sale_order_id = fields.Many2one(related='registry_id.sale_order_id')
    product_id = fields.Many2one(related='registry_id.lot_id.product_id')

    lot_id = fields.Many2one(related="registry_id.lot_id")

    @api.depends('vin')
    def _compute_registry_id_from_vin(self):
        for registry in self:
            if registry.vin:
                registry.registry_id = self.env['motorcycle.registry'].search([('vin', '=', registry.vin)], limit = 1)
            else:
                registry.registry_id = False
