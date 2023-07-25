from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    name = fields.Char(compute = "_compute_name", readonly= False, store = True)

    @api.depends('year', 'make','model')
    def _compute_name(self):
         for registry in self:
            #
            if registry.detailed_type == 'motorcycle' and not False in (registry.make, registry.model, registry.year):
               registry.name = str(registry.year) +registry.make +registry.model
            else: 
               registry.name = registry.name


