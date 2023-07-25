from odoo import models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('user_id', 'company_id', 'partner_shipping_id')
    def _compute_warehouse_id(self):
        sf = ['Alaska', 'California', 'Colorado', 'Hawaii', 'Idaho', 'Montana', 'Nevada', 'Oregon', 'Utah', 'Washington', 
              'Wyoming', 'Arizona', 'New Mexico', 'Texas', 'Oklahoma', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 
              'Michigan', 'Minnesota', 'Nebraska', 'South Dakota', 'North Dakota', 'Ohio', 'Wisconsin']
        bf = ['Alabama', 'Arkansas', 'Florida', 'Georgia', 'Kentucky', 'Louisiana',  'Missouri', 'Mississippi',
              'South Carolina', 'North Carolina', 'Tennesse', 'Virginia', 'West Virigina', 'Delaware', 'Maryland',
              'New Jersey', 'Pennsylvania', 'New York', 'Connecticut', 'Maine', 'Massachusetss', 'Vermont', 
              'New Hampshire', 'Rhode Island']

        for order in self:
            if order.state in ['draft', 'sent'] or not order.ids:
                if order.partner_shipping_id.state_id.name in sf:
                    order.warehouse_id = 4
                elif order.partner_shipping_id.state_id.name in bf:
                    order.warehouse_id = 3
                else: 
                    super()._compute_warehouse_id()
