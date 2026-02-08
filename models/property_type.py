# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class GhanaRealEstatePropertyType(models.Model):
    """Property Type Model"""
    
    _name = 'ghana_real_estate.property.type'
    _description = 'Property Type'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Property Type Name',
        required=True,
        translate=True,
        index=True
    )
    
    code = fields.Char(
        string='Code',
        required=True,
        index=True,
        help='Short code for URL and reference'
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    icon = fields.Char(
        string='Icon Class',
        default='fa-home',
        help='Font Awesome icon class'
    )
    
    image = fields.Binary(
        string='Category Image',
        attachment=True
    )
    
    sequence = fields.Integer(
        string='Display Sequence',
        default=10
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Computed Fields
    property_count = fields.Integer(
        string='Number of Properties',
        compute='_compute_property_count'
    )
    
    # For website display
    website_published = fields.Boolean(
        string='Show on Website',
        default=True
    )
    
    # Child categories
    parent_id = fields.Many2one(
        'ghana_real_estate.property.type',
        string='Parent Category'
    )
    
    child_ids = fields.One2many(
        'ghana_real_estate.property.type',
        'parent_id',
        string='Sub Categories'
    )
    
    # SEO Fields
    meta_title = fields.Char(
        string='Meta Title',
        translate=True
    )
    
    meta_description = fields.Text(
        string='Meta Description',
        translate=True
    )
    
    @api.depends('code')
    def _compute_property_count(self):
        for record in self:
            record.property_count = self.env['ghana_real_estate.property'].search_count([
                ('property_type_id', '=', record.id),
                ('website_published', '=', True),
                ('state', 'in', ['available', 'draft'])
            ])
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Property type code must be unique!'),
    ]


class GhanaRealEstateLocation(models.Model):
    """Location/Region Model for Ghana"""
    
    _name = 'ghana_real_estate.location'
    _description = 'Location/Region'
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='Region Name',
        required=True,
        index=True
    )
    
    code = fields.Char(
        string='Code',
        required=True,
        index=True
    )
    
    # Geographic Information
    capital = fields.Char(
        string='Capital City'
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    # For website
    image = fields.Binary(
        string='Region Image',
        attachment=True
    )
    
    sequence = fields.Integer(
        string='Display Sequence',
        default=10
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Computed Fields
    property_count = fields.Integer(
        string='Number of Properties',
        compute='_compute_property_count'
    )
    
    # Related cities
    city_ids = fields.One2many(
        'ghana_real_estate.city',
        'region_id',
        string='Cities'
    )
    
    @api.depends('code')
    def _compute_property_count(self):
        for record in self:
            record.property_count = self.env['ghana_real_estate.property'].search_count([
                ('location_id.code', '=', record.code),
                ('website_published', '=', True),
                ('state', 'in', ['available', 'draft'])
            ])
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Location code must be unique!'),
    ]


class GhanaRealEstateCity(models.Model):
    """City Model"""
    
    _name = 'ghana_real_estate.city'
    _description = 'City'
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='City Name',
        required=True,
        index=True
    )
    
    region_id = fields.Many2one(
        'ghana_real_estate.location',
        string='Region',
        required=True,
        ondelete='restrict'
    )
    
    # For website
    image = fields.Binary(
        string='City Image',
        attachment=True
    )
    
    description = fields.Text(
        string='Description'
    )
    
    sequence = fields.Integer(
        string='Display Sequence',
        default=10
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Computed Fields
    property_count = fields.Integer(
        string='Number of Properties',
        compute='_compute_property_count'
    )
    
    @api.depends('name', 'region_id')
    def _compute_property_count(self):
        for record in self:
            record.property_count = self.env['ghana_real_estate.property'].search_count([
                ('city', '=', record.name),
                ('location_id', '=', record.region_id.id),
                ('website_published', '=', True),
                ('state', 'in', ['available', 'draft'])
            ])
