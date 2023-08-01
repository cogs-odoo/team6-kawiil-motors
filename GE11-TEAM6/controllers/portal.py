from odoo import fields, http
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request

from odoo.osv.expression import OR

class CustomerPortal(portal.CustomerPortal):

    @http.route(['/my/repairs/new'], type='http', auth='user', methods=['GET'], website=True)
    def portal_new_repair_page (self, **kwargs):
        return request.render("GE11-TEAM6.repair_order_portal_new")

    @http.route(['/my/repairs/create_new'], type='http', auth='user', methods=['POST'], website=True)
    def portal_new_repair (self, access_token=None, **kwargs):

        vin = kwargs['input_vin']
        qty = kwargs['input_qty']

        RepairOrder = request.env['repair.order'].create({
            'vin': vin,
            'product_uom': qty,
        })

        return self.portal_my_orders ()
    
    @http.route(['/my/repairs', '/my/repairs/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_orders(self, **kwargs):
        values = self._prepare_repair_portal_rendering_values(repair_page=False, **kwargs)
        request.session['my_repairs_history'] = values['repairs'].ids[:100]
        return request.render("GE11-TEAM6.portal_my_repairs", values)
    
    @http.route(['/my/repairs/<int:repair_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, repair_id, report_type=None, access_token=None, sortby=None, search_in="all", search=None, message=False, download=False, **kw):
        try:
            repair_sudo = self._document_check_access('repair.order', repair_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=repair_sudo, report_type=report_type, report_ref='repair.action_report_repair_order', download=download)

        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_repair_%s' % repair_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_repair_%s' % repair_sudo.id] = today

        backend_url = f'/web#model={repair_sudo._name}'\
                      f'&id={repair_sudo.id}'\
                      f'&view_type=form'

        print ("URL: ", backend_url)    
    
        values = {
            'repair_order': repair_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': repair_sudo.company_id,  # Used to display correct company logo
            'landing_route': repair_sudo.get_portal_url(),
        }
            
        history_session_key = 'my_repairs_history'

        values = self._get_page_view_values(
            repair_sudo, access_token, values, history_session_key, False)

        return request.render('GE11-TEAM6.repair_order_portal_template', values)
    
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        RepairOrder = request.env['repair.order']
        if 'repair_count' in counters:
            values['repair_count'] = RepairOrder.search_count(self._prepare_repairs_domain(partner)) \
                if RepairOrder.check_access_rights('read', raise_exception=False) else 0

        return values
    
    def _get_repair_searchbar_inputs(self):
        return {
            'all': {'input': 'all', 'label': ('Search in All')},
            'ticket': {'input': 'ticket', 'label': ('Search in Ticket')},
            'vin': {'input': 'vin', 'label': ('Search in VIN')},
        }
    
    def _get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('ticket', 'all'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('vin', 'all'):
            search_domain = OR([search_domain, [('vin', 'ilike', search)]])
        return search_domain

    def _prepare_repair_portal_rendering_values (self, page = 1, date_begin = None, sortby = None, search_in="all", search=None, repair_page = False, **kwargs):
        
        RepairOrder = request.env['repair.order']
        
        if not sortby:
            sortby = 'date'

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values ()

        domain = self._prepare_repairs_domain(partner)

        searchbar_inputs = self._get_repair_searchbar_inputs()

        url = "/my/repairs"

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        pager_values = portal_pager (
            url = url,
            total = RepairOrder.search_count(domain),
            page = page,
            step = self._items_per_page,
            url_args={'search_in': search_in, 'search': search},
        )

        repairs = RepairOrder.search(domain, limit = self._items_per_page, offset = pager_values ['offset'])

        values.update ({
            'date': date_begin,
            'repairs': repairs,
            'page_name': 'repair',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': None,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'searchbar_inputs': searchbar_inputs,
        })

        return values
    
    def _prepare_repairs_domain(self, partner):
        return [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ]
