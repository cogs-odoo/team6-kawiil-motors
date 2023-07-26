from odoo import  fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    

    is_new_customer = fields.Boolean(compute = "_compute_is_new_customer")
  

    def _compute_is_new_customer(self):
        for registry in self:
            orders = registry.sale_order_ids.mapped('order_line')
            ids_productos = orders.mapped('product_id')
            if (False not in ids_productos.mapped('detailed_type') and 'motorcycle' in ids_productos.mapped('detailed_type')):
                registry.is_new_customer = False
            else:
                registry.is_new_customer = True
   