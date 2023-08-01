from odoo import  fields, models, api

class SaleOrder(models.Model):
    _inherit = ['sale.order']

    is_new_customer = fields.Boolean(related='partner_id.is_new_customer')

    
    def execute_pricelist_id(self):
        for order in self:
            if order.is_new_customer:
                order.pricelist_id = self.env.ref('GE04-TEAM6.new_customer_discount').id
                self.action_update_prices()
        return        



