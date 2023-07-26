from odoo import api, fields, models

class StockLot (models.Model):
    _inherit = "stock.lot"

    name = fields.Char (compute = "_format_serial_number")

    # product_id = fields.Many2one(
    #     'product.product', 'Product', index=True,
    #     domain=lambda self: self._domain_product_id(), required=True, check_company=True)
    
    # product_tmpl_id = fields.Many2one(related = "product_id.product_tmpl_id")
    # detailed_type = fields.Selection(related = "product_tmpl_id.detailed_type")

    @api.model
    def _get_next_serial(self, company, product):
        """Return the next serial number to be attributed to the product."""
        if product.tracking != "none":
            last_serial = self.env['stock.lot'].search(
                [('company_id', '=', company.id), ('product_id', '=', product.id)],
                limit=1, order='id DESC')
            if last_serial:
                if last_serial.product_id.product_tmpl_id.detailed_type == 'motorcycle':
                    s_vin = last_serial.product_id.product_tmpl_id.make + last_serial.product_id.product_tmpl_id.model + str(last_serial.product_id.product_tmpl_id.year) + last_serial.product_id.product_tmpl_id.battery_capacity
                    return s_vin + self.env['stock.lot'].generate_lot_names(last_serial.name, 2)[1] ######
                else:
                    super()._get_next_serial(self, company, product)
        return False
