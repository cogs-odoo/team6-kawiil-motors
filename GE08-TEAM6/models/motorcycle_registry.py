from odoo import models, fields

class MotorcycleRegistry(models.Model):
    _name = "motorcycle.registry"
    _inherit = ['portal.mixin', 'motorcycle.registry']

    registry_count = fields.Integer('Registry Count', compute='_compute_registry_count', compute_sudo = True)
    public = fields.Boolean(string="Public", default=False, store=True)

    make = fields.Char(search = 'search_make')
    model = fields.Char(search = 'search_model')

    def _compute_registry_count(self):
        registry_data = self._read_group([
            ('registry_number', 'in', self.ids)],
            ['registry_number'], ['registry_number'])
        data_map = {datum['registry_number'][0]: datum['registry_number_count'] for datum in registry_data}
        for registry in self:
            registry.registry_count = data_map.get(registry.id, 0)

    def _compute_access_url(self):
        super()._compute_access_url()
        for registry in self:
            registry.access_url = f'/my/registries/{registry.id}'

    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('GE08-TEAM6.portal_my_motorcycle_registries')
    
    def search_make(self, operator, value):
        domain = []

        if len(value) < 3:
            domain = [('vin', operator, f'{value}%')]

        return domain

    def search_model(self, operator, value):
        domain = []

        if len(value) < 3:
            domain = [('vin', operator, f'__{value}%')]

        return domain
