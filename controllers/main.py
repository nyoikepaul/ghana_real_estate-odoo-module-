# -*- coding: utf-8 -*-
from odoo import http, fields, _
from odoo.http import request, Response
from odoo.addons.website.controllers.main import Website
import json
import werkzeug.urls
import werkzeug.exceptions


class GhanaRealEstateWebsite(Website):
    """Premium Real Estate Website Controller for Ghana"""

    @http.route([
        '/',
        '/home',
        '/properties',
    ], type='http', auth='public', website=True, sitemap=True)
    def website_home(self, **kwargs):
        """Homepage with featured properties and search"""
        # Get featured properties
        featured_properties = request.env['ghana_real_estate.property'].search([
            ('website_published', '=', True),
            ('featured', '=', True),
            ('state', 'in', ['available', 'draft'])
        ], limit=6, order='sequence, create_date desc')
        
        # Get spotlight properties
        spotlight_properties = request.env['ghana_real_estate.property'].search([
            ('website_published', '=', True),
            ('spotlight', '=', True),
            ('state', 'in', ['available', 'draft'])
        ], limit=3, order='sequence, create_date desc')
        
        # Get property types
        property_types = request.env['ghana_real_estate.property.type'].search([
            ('website_published', '=', True),
            ('active', '=', True)
        ], limit=6, order='sequence')
        
        # Get locations
        locations = request.env['ghana_real_estate.location'].search([
            ('active', '=', True)
        ], limit=10, order='sequence')
        
        # Get featured agents
        featured_agents = request.env['ghana_real_estate.agent'].search([
            ('website_published', '=', True),
            ('featured_agent', '=', True),
            ('active', '=', True)
        ], limit=4, order='sequence')
        
        # Get statistics
        stats = {
            'properties_for_sale': request.env['ghana_real_estate.property'].search_count([
                ('website_published', '=', True),
                ('transaction_type', '=', 'sale'),
                ('state', 'in', ['available', 'draft'])
            ]),
            'properties_for_rent': request.env['ghana_real_estate.property'].search_count([
                ('website_published', '=', True),
                ('transaction_type', '=', 'rent'),
                ('state', 'in', ['available', 'draft'])
            ]),
            'happy_clients': 500,  # Can be made dynamic
            'years_experience': 10,
        }
        
        values = {
            'featured_properties': featured_properties,
            'spotlight_properties': spotlight_properties,
            'property_types': property_types,
            'locations': locations,
            'featured_agents': featured_agents,
            'stats': stats,
            'main_object': None,
        }
        
        return request.render('ghana_real_estate.premium_homepage', values)

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True, sitemap=True)
    def property_detail(self, property_id, **kwargs):
        """Property detail page"""
        property_obj = request.env['ghana_real_estate.property'].browse(property_id)
        
        if not property_obj.exists() or not property_obj.website_published:
            return request.render('website.404')
        
        # Get similar properties
        similar_properties = request.env['ghana_real_estate.property'].search([
            ('website_published', '=', True),
            ('property_type_id', '=', property_obj.property_type_id.id),
            ('id', '!=', property_id),
            ('state', 'in', ['available', 'draft'])
        ], limit=4, order='create_date desc')
        
        # Get property images
        images = request.env['ghana_real_estate.property.image'].search([
            ('property_id', '=', property_id)
        ], order='sequence')
        
        values = {
            'property': property_obj,
            'similar_properties': similar_properties,
            'images': images,
            'main_object': property_obj,
        }
        
        return request.render('ghana_real_estate.property_detail', values)

    @http.route('/properties/for-sale', type='http', auth='public', website=True, sitemap=True)
    def properties_for_sale(self, **kwargs):
        """Properties for sale listing"""
        return self._render_properties(transaction_type='sale', **kwargs)

    @http.route('/properties/for-rent', type='http', auth='public', website=True, sitemap=True)
    def properties_for_rent(self, **kwargs):
        """Properties for rent listing"""
        return self._render_properties(transaction_type='rent', **kwargs)

    @http.route('/properties/type/<string:property_type>', type='http', auth='public', website=True, sitemap=True)
    def properties_by_type(self, property_type, **kwargs):
        """Properties by type"""
        type_obj = request.env['ghana_real_estate.property.type'].search([
            ('code', '=', property_type),
            ('active', '=', True)
        ], limit=1)
        
        if not type_obj:
            return request.render('website.404')
        
        return self._render_properties(property_type_id=type_obj.id, **kwargs)

    @http.route('/properties/location/<string:location_code>', type='http', auth='public', website=True, sitemap=True)
    def properties_by_location(self, location_code, **kwargs):
        """Properties by location"""
        location_obj = request.env['ghana_real_estate.location'].search([
            ('code', '=', location_code),
            ('active', '=', True)
        ], limit=1)
        
        if not location_obj:
            return request.render('website.404')
        
        return self._render_properties(location_code=location_code, **kwargs)

    def _render_properties(self, transaction_type=None, property_type_id=None, location_code=None, **kwargs):
        """Common method to render properties listing"""
        # Build domain
        domain = [
            ('website_published', '=', True),
            ('state', 'in', ['available', 'draft'])
        ]
        
        if transaction_type:
            domain.append(('transaction_type', '=', transaction_type))
        
        if property_type_id:
            domain.append(('property_type_id', '=', property_type_id))
        
        if location_code:
            domain.append(('location_id.code', '=', location_code))
        
        # Search
        search_term = kwargs.get('search', '')
        if search_term:
            domain.append('|')
            domain.append('|')
            domain.append('|')
            domain.append(('name', 'ilike', search_term))
            domain.append(('city', 'ilike', search_term))
            domain.append(('address', 'ilike', search_term))
            domain.append(('description', 'ilike', search_term))
        
        # Price range
        min_price = kwargs.get('min_price')
        max_price = kwargs.get('max_price')
        if min_price:
            domain.append(('price', '>=', float(min_price)))
        if max_price:
            domain.append(('price', '<=', float(max_price)))
        
        # Bedrooms
        bedrooms = kwargs.get('bedrooms')
        if bedrooms and bedrooms != 'any':
            domain.append(('bedrooms', '>=', int(bedrooms)))
        
        # Bathrooms
        bathrooms = kwargs.get('bathrooms')
        if bathrooms and bathrooms != 'any':
            domain.append(('bathrooms', '>=', int(bathrooms)))
        
        # Sorting
        order = kwargs.get('sort', 'create_date desc')
        allowed_orders = ['create_date desc', 'price asc', 'price desc', 'name asc']
        if order not in allowed_orders:
            order = 'create_date desc'
        
        # Pagination
        page = int(kwargs.get('page', 1))
        per_page = 12
        offset = (page - 1) * per_page
        
        # Get properties
        properties = request.env['ghana_real_estate.property'].search(
            domain, 
            limit=per_page, 
            offset=offset, 
            order=order
        )
        
        # Get total count
        total_count = request.env['ghana_real_estate.property'].search_count(domain)
        
        # Get filters for sidebar
        property_types = request.env['ghana_real_estate.property.type'].search([
            ('active', '=', True)
        ])
        
        locations = request.env['ghana_real_estate.location'].search([
            ('active', '=', True)
        ])
        
        # Prepare pager
        pager = request.website.pager(
            url='/properties',
            total=total_count,
            page=page,
            step=per_page,
            scope=5,
        )
        
        values = {
            'properties': properties,
            'property_types': property_types,
            'locations': locations,
            'pager': pager,
            'transaction_type': transaction_type,
            'main_object': None,
        }
        
        return request.render('ghana_real_estate.property_listing', values)

    @http.route('/agents', type='http', auth='public', website=True, sitemap=True)
    def agents(self, **kwargs):
        """Agents listing page"""
        agents = request.env['ghana_real_estate.agent'].search([
            ('website_published', '=', True),
            ('active', '=', True)
        ], order='sequence, name')
        
        values = {
            'agents': agents,
            'main_object': None,
        }
        
        return request.render('ghana_real_estate.agents_listing', values)

    @http.route('/agent/<int:agent_id>', type='http', auth='public', website=True, sitemap=True)
    def agent_detail(self, agent_id, **kwargs):
        """Agent detail page"""
        agent_obj = request.env['ghana_real_estate.agent'].browse(agent_id)
        
        if not agent_obj.exists() or not agent_obj.website_published:
            return request.render('website.404')
        
        # Get agent's properties
        properties = request.env['ghana_real_estate.property'].search([
            ('agent_id', '=', agent_id),
            ('website_published', '=', True),
            ('state', 'in', ['available', 'draft'])
        ], limit=6, order='create_date desc')
        
        values = {
            'agent': agent_obj,
            'properties': properties,
            'main_object': agent_obj,
        }
        
        return request.render('ghana_real_estate.agent_detail', values)

    @http.route('/contact', type='http', auth='public', website=True, sitemap=True)
    def contact(self, **kwargs):
        """Contact page"""
        values = {
            'main_object': None,
        }
        return request.render('ghana_real_estate.contact_page', values)

    @http.route('/about', type='http', auth='public', website=True, sitemap=True)
    def about(self, **kwargs):
        """About page"""
        values = {
            'main_object': None,
        }
        return request.render('ghana_real_estate.about_page', values)

    # API Endpoints for AJAX calls
    @http.route('/api/properties/search', type='json', auth='public', website=True)
    def api_search_properties(self, **kwargs):
        """API endpoint for property search"""
        domain = [
            ('website_published', '=', True),
            ('state', 'in', ['available', 'draft'])
        ]
        
        # Apply filters from kwargs
        if kwargs.get('transaction_type'):
            domain.append(('transaction_type', '=', kwargs['transaction_type']))
        
        if kwargs.get('property_type'):
            domain.append(('property_type_id.code', '=', kwargs['property_type']))
        
        if kwargs.get('location'):
            domain.append('|')
            domain.append(('city', 'ilike', kwargs['location']))
            domain.append(('location_id.name', 'ilike', kwargs['location']))
        
        if kwargs.get('min_price'):
            domain.append(('price', '>=', float(kwargs['min_price'])))
        
        if kwargs.get('max_price'):
            domain.append(('price', '<=', float(kwargs['max_price'])))
        
        if kwargs.get('bedrooms'):
            domain.append(('bedrooms', '>=', int(kwargs['bedrooms'])))
        
        # Limit results
        limit = int(kwargs.get('limit', 10))
        offset = int(kwargs.get('offset', 0))
        
        properties = request.env['ghana_real_estate.property'].search(
            domain, 
            limit=limit, 
            offset=offset,
            order='create_date desc'
        )
        
        return {
            'count': len(properties),
            'properties': [{
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'display_price': p.display_price,
                'city': p.city,
                'bedrooms': p.bedrooms,
                'bathrooms': p.bathrooms,
                'image_url': p.image_ids[0].image if p.image_ids else False,
                'url': f'/property/{p.id}',
            } for p in properties]
        }

    @http.route('/api/locations', type='json', auth='public', website=True)
    def api_locations(self, **kwargs):
        """API endpoint to get locations"""
        locations = request.env['ghana_real_estate.location'].search([
            ('active', '=', True)
        ])
        
        return {
            'locations': [{
                'id': l.id,
                'name': l.name,
                'code': l.code,
            } for l in locations]
        }

    @http.route('/api/property-types', type='json', auth='public', website=True)
    def api_property_types(self, **kwargs):
        """API endpoint to get property types"""
        types = request.env['ghana_real_estate.property.type'].search([
            ('active', '=', True)
        ])
        
        return {
            'types': [{
                'id': t.id,
                'name': t.name,
                'code': t.code,
                'icon': t.icon,
            } for t in types]
        }

    @http.route('/api/featured-properties', type='json', auth='public', website=True)
    def api_featured_properties(self, **kwargs):
        """API endpoint to get featured properties"""
        limit = int(kwargs.get('limit', 6))
        
        properties = request.env['ghana_real_estate.property'].search([
            ('website_published', '=', True),
            ('featured', '=', True),
            ('state', 'in', ['available', 'draft'])
        ], limit=limit, order='sequence, create_date desc')
        
        return {
            'properties': [{
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'display_price': p.display_price,
                'city': p.city,
                'bedrooms': p.bedrooms,
                'bathrooms': p.bathrooms,
                'image_url': p.image_ids[0].image if p.image_ids else False,
                'url': f'/property/{p.id}',
            } for p in properties]
        }
