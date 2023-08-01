import binascii

from odoo import http
from collections import OrderedDict
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager

from odoo.osv.expression import OR

class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        MotorcycleRegistry = request.env['motorcycle.registry']
        if 'registry_count' in counters:
            values['registry_count'] = MotorcycleRegistry.search_count(self._prepare_motorcycle_domain(partner)) \
                if MotorcycleRegistry.check_access_rights('read', raise_exception=False) else 0

        return values
    
    def _prepare_motorcycle_domain(self, partner):
        return [
            '|',
            ('owner_id', '=', [partner.id]),
            ('public', '=', True)
        ]
    
    def _get_registry_searchbar_inputs(self):
        return {
            'all': {'input': 'all', 'label': ('Search in All')},
            'owner': {'input': 'owner', 'label': ('Search in Rider')},
            'state': {'input': 'state', 'label': ('Search in State')},
            'country': {'input': 'country', 'label': ('Search in Country')},
            'make': {'input': 'make', 'label': ('Search in Make')},
            'model': {'input': 'model', 'label': ('Search in Model')}
        }
    
    def _get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('owner', 'all'):
            search_domain = OR([search_domain, [('owner_id', 'ilike', search)]])
        if search_in in ('state', 'all'):
            search_domain = OR([search_domain, [('owner_id.state_id', 'ilike', search)]])
        if search_in in ('country', 'all'):
            search_domain = OR([search_domain, [('owner_id.country_id', 'ilike', search)]])
        if search_in in ('make', 'all'):
            search_domain = OR([search_domain, [('make', '=ilike', search)]])
        if search_in in ('model', 'all'):
            search_domain = OR([search_domain, [('model', '=ilike', search)]])
        return search_domain
    
    def _prepare_registries_portal_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, search_in="all", search=None, registries_page=False, **kwargs
    ):
        MotorcycleRegistry = request.env['motorcycle.registry']

        if not sortby:
            sortby = 'date'

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()

        if registries_page:
            url = "/my/registries"
            domain = self._prepare_motorcycle_domain(partner)

        searchbar_inputs = self._get_registry_searchbar_inputs()

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        pager_values = portal_pager(
            url=url,
            total=MotorcycleRegistry.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={'search_in': search_in, 'search': search},
        )
        registries = MotorcycleRegistry.search(domain, order=None, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'date': date_begin,
            'registries': registries.sudo() if registries_page else MotorcycleRegistry,
            'page_name': 'registry' if registries_page else 'registry',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': None,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'searchbar_inputs': searchbar_inputs,
        }) 

        return values

    @http.route(['/my/registries', '/my/registries/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_motorcycle_registries(self, **kwargs):
        values = self._prepare_registries_portal_rendering_values(registries_page=True, **kwargs)
        request.session['my_registries_history'] = values['registries'].ids[:100]
        return request.render("GE08-TEAM6.portal_my_motorcycle_registries", values)
    
    @http.route(['/my/registries/<int:registry_id>'], type='http', auth='user', website=True)
    def portal_registry_page(self, registry_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            registry_sudo= self._document_check_access('motorcycle.registry', registry_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        backend_url = f'/web#model={registry_sudo._name}'\
                      f'&id={registry_sudo.id}'\
                      f'&action={registry_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        
        values = {
            'motorcycle_registry': registry_sudo,
            'message': 'Registry view',
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': registry_sudo.owner_id,  # Used to display correct company logo
        }

        history_session_key = 'my_registries_history'

        values = self._get_page_view_values(
            registry_sudo, access_token, values, history_session_key, False)
        
        return request.render('GE08-TEAM6.portal_registry_page', values)
    
    @http.route(['/my/registries/<int:registry_id>/edit'], type='http', auth="public", methods=['POST'], website=True)
    def portal_edit_registry_page(self, registry_id, access_token=None, **kw):

        access_token = access_token or request.httprequest.args.get('access_token')

        try:
            registry_sudo = self._document_check_access('motorcycle.registry', registry_id, access_token)
        except (AccessError, MissingError):
            return {'error': ('Invalid registry.')}
        
        MotorcycleRegistry = request.env['motorcycle.registry'].search_read([('id', '=', registry_id)])
        is_public = MotorcycleRegistry[0].get('public', None)

        print(is_public)
        
        if 'public' in kw:
            print('in')
            is_public = not is_public

        print(is_public)
        
        try:
            if kw['license_plate']:
                registry_sudo.update({
                    'license_plate': kw['license_plate'],
                })
            if kw['current_mileage']:
                registry_sudo.update({
                    'current_mileage': kw['current_mileage'],
                })
            if 'public' in kw:
                registry_sudo.update({
                    'public': is_public
                })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': ('Invalid signature data.')}

        return request.redirect(registry_sudo.get_portal_url())
