from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_new_customer = fields.Boolean(compute = "_compute_is_new_customer", store = True)
    
    
    def _compute_is_new_customer(self):
        for registry in self:
            ordenes = registry.sale_order_ids.mapped('order_line')
            ids_productos = ordenes.mapped('product_id')
            if 'motorcycle' in ids_productos.detailed_type:
                registry.is_new_customer = False
            else:
                registry.is_new_customer = True
    
       