from odoo import models

class RepairOrder(models.Model):
    _name = 'repair.order'
    _inherit = ['repair.order','portal.mixin']
    
    def _compute_access_url(self):
        super()._compute_access_url()
        for repair in self:
            repair.access_url = f'/my/repairs/{repair.id}'
