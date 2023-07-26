from odoo import api, fields, models

class StockLot (models.Model):
    _inherit = "stock.lot"

    name = fields.Char (compute = "_format_serial_number", store = True)

    @api.depends ('product_id')
    def _format_serial_number (self):
        for lot in self:
            template = lot.product_id.product_tmpl_id

            if template.detailed_type == 'motorcycle' and lot.product_id.tracking != 'None':
                make = template.make if template.make else 'XX'
                model = template.model if template.make else 'XX'
                year = template.year if template.make else '00'
                battery = template.battery_capacity if template.make else 'XX'
                serial = self.env['ir.sequence'].next_by_code('motorcycle.serial.number.auto')

                lot.name = make + model + str(year) + battery + serial
            else:
                lot.name = self.env['ir.sequence'].next_by_code('stock.lot.serial')
