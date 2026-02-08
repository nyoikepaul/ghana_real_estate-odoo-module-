# -*- coding: utf-8 -*-
from odoo import http, fields, _


class GhanaRealEstatePropertyController(http.Controller):
    """Property-specific controller actions"""

    @http.route('/property/inquiry', type='http', auth='public', website=True, methods=['POST'])
    def submit_inquiry(self, **post):
        """Submit property inquiry form"""
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'property_id']
        for field in required_fields:
            if not post.get(field):
                return request.render('website.http_error', {
                    'error_code': 400,
                    'error_message': f'Field {field} is required'
                })
        
        # Create inquiry
        inquiry = request.env['crm.lead'].create({
            'name': f'Property Inquiry: {post.get("property_id")}',
            'contact_name': post.get('name'),
            'email_from': post.get('email'),
            'phone': post.get('phone'),
            'description': post.get('message', ''),
            'source_id': request.env.ref('ghana_real_estate.source_property_inquiry').id,
        })
        
        return request.render('ghana_real_estate.inquiry_thank_you')

    @http.route('/property/schedule-viewing', type='http', auth='public', website=True, methods=['POST'])
    def schedule_viewing(self, **post):
        """Schedule a property viewing"""
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'property_id', 'preferred_date']
        for field in required_fields:
            if not post.get(field):
                return request.render('website.http_error', {
                    'error_code': 400,
                    'error_message': f'Field {field} is required'
                })
        
        # Create lead with viewing request
        lead = request.env['crm.lead'].create({
            'name': f'Viewing Request: {post.get("property_id")}',
            'contact_name': post.get('name'),
            'email_from': post.get('email'),
            'phone': post.get('phone'),
            'description': f'Preferred Viewing Date: {post.get("preferred_date")}\n\nMessage: {post.get("message", "")}',
            'source_id': request.env.ref('ghana_real_estate.source_viewing_request').id,
        })
        
        return request.render('ghana_real_estate.viewing_scheduled')

    @http.route('/property/request-callback', type='http', auth='public', website=True, methods=['POST'])
    def request_callback(self, **post):
        """Request a callback"""
        # Validate required fields
        required_fields = ['name', 'phone']
        for field in required_fields:
            if not post.get(field):
                return request.render('website.http_error', {
                    'error_code': 400,
                    'error_message': f'Field {field} is required'
                })
        
        # Create lead
        lead = request.env['crm.lead'].create({
            'name': f'Callback Request',
            'contact_name': post.get('name'),
            'phone': post.get('phone'),
            'email_from': post.get('email', ''),
            'description': f'Preferred callback time: {post.get("preferred_time", "Any time")}',
            'source_id': request.env.ref('ghana_real_estate.source_callback').id,
        })
        
        return request.render('ghana_real_estate.callback_confirmed')

    @http.route('/property/compare', type='http', auth='public', website=True)
    def compare_properties(self, **kwargs):
        """Compare selected properties"""
        property_ids = kwargs.get('ids', '').split(',')
        property_ids = [int(pid) for pid in property_ids if pid.isdigit()]
        
        if len(property_ids) < 2:
            return request.redirect('/properties')
        
        properties = request.env['ghana_real_estate.property'].browse(property_ids)
        
        values = {
            'properties': properties,
            'main_object': None,
        }
        
        return request.render('ghana_real_estate.property_compare', values)

    @http.route('/property/save-search', type='json', auth='public', website=True)
    def save_search(self, **kwargs):
        """Save a property search for later"""
        if not request.session.get('uid'):
            return {'success': False, 'message': 'Please login to save searches'}
        
        # Create saved search
        saved_search = request.env['website.property.search'].create({
            'user_id': request.uid,
            'name': kwargs.get('name', 'My Search'),
            'filters': json.dumps(kwargs),
        })
        
        return {'success': True, 'saved_search_id': saved_search.id}

    @http.route('/api/property/<int:property_id>', type='json', auth='public', website=True)
    def get_property_details(self, property_id):
        """Get property details via API"""
        property_obj = request.env['ghana_real_estate.property'].browse(property_id)
        
        if not property_obj.exists() or not property_obj.website_published:
            return {'error': 'Property not found'}
        
        return {
            'id': property_obj.id,
            'name': property_obj.name,
            'description': property_obj.description,
            'price': property_obj.price,
            'display_price': property_obj.display_price,
            'city': property_obj.city,
            'address': property_obj.address,
            'bedrooms': property_obj.bedrooms,
            'bathrooms': property_obj.bathrooms,
            'land_size': property_obj.land_size,
            'building_size': property_obj.building_size,
            'property_type': property_obj.property_type_id.name,
            'state': property_obj.state,
            'transaction_type': property_obj.transaction_type,
            'features': [f.name for f in property_obj.feature_ids],
            'images': [{
                'id': img.id,
                'image': img.image,
            } for img in property_obj.image_ids],
            'agent': {
                'name': property_obj.agent_id.name,
                'phone': property_obj.agent_id.phone,
                'email': property_obj.agent_id.email,
                'photo': property_obj.agent_id.photo,
            }
        }
