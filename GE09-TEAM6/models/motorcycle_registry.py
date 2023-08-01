from odoo import fields, models, api

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'
    count_orders = fields.Float(compute = '_compute_count_orders')
    
    repair_order_ids = fields.One2many(comodel_name="repair.order", string="Repair orders", inverse_name="registry_id")
    def action_report_repair_order(self):
        self.repair_order_ids
        action = self.env["ir.actions.actions"]._for_xml_id("repair.action_repair_order_tree")
        action["domain"] = [('registry_id', '=' ,self.id)]
        return action

    @api.depends('repair_order_ids')
    def _compute_count_orders(self):
        self.count_orders = len(self.repair_order_ids)
