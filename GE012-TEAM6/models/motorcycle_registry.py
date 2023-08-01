from odoo import fields, models, api
from odoo.exceptions import UserError

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'
    
    
    @api.model_create_multi
    def create(self, vals_list):
        
        res = super().create(vals_list)
        data =  res.env['res.users'].search([]).mapped('login')
        if res.owner_id.email not in data:
            user = res.env['res.users'].create({
                    'name': res.owner_id.name,
                    'login' : res.owner_id.email,
                    'email' : res.owner_id.email,
                })        
            self.action_grant_access(user)
            return res
    
    def action_grant_access(self,user):
        user.ensure_one()
        group_portal = self.env.ref('base.group_portal')
        group_user = self.env.ref('base.group_user')
        user_sudo = user.sudo()
        user_sudo.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_user.id)]})        
        user_sudo.partner_id.signup_prepare()
        self._send_email(user)
        return True

    def _send_email(self,user):
            user.ensure_one()
            template = self.env.ref('GE012-TEAM6.mail_template_data_motorcycle')
            if not template:
                raise UserError(('The template "Portal: new user" not found for sending email to the portal user.'))
            lang = user.sudo().lang
            partner = user.sudo().partner_id
            portal_url = partner.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[partner.id]
            partner.signup_prepare()
            template.with_context(dbname=self._cr.dbname, portal_url=portal_url, lang=lang).send_mail(user.id, force_send=True)
            return True
