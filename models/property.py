# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re

class GhanaRealEstateProperty(models.Model):
    """Premium Property Model for Ghana Real Estate Website"""
    
    _name = 'ghana_real_estate.property'
    _description = 'Ghana Real Estate Property'
    _inherit = ['website.seo.metadata', 'website.published.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    # Basic Information
    name = fields.Char(
        string='Property Name',
        required=True,
        translate=True,
        index=True
    )
    
    property_code = fields.Char(
        string='Property Code',
        readonly=True,
        copy=False,
        index=True,
        default=lambda self: self._generate_property_code()
    )
    
    description = fields.Html(
        string='Description',
        translate=True,
        sanitize_attributes=False
    )
    
    property_type_id = fields.Many2one(
        'ghana_real_estate.property.type',
        string='Property Type',
        required=True,
        ondelete='restrict',
        index=True
    )
    
    # Status Fields
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('off_plan', 'Off Plan'),
    ], string='Status',
       required=True,
       default='draft',
       index=True,
       tracking=True
    )
    
    transaction_type = fields.Selection([
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    ], string='Transaction Type',
       required=True,
       default='sale',
       index=True
    )
    
    # Location Information
    location_id = fields.Many2one(
        'ghana_real_estate.location',
        string='Region/Location',
        required=True,
        ondelete='restrict',
        index=True
    )
    
    city = fields.Char(
        string='City',
        required=True,
        index=True
    )
    
    address = fields.Text(
        string='Full Address',
        required=True
    )
    
    latitude = fields.Float(
        string='Latitude',
        digits=(10, 7)
    )
    
    longitude = fields.Float(
        string='Longitude',
        digits=(10, 7)
    )
    
    # Pricing Information
    price = fields.Monetary(
        string='Price',
        required=True,
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.GHS'),
        required=True
    )
    
    price_per_sqft = fields.Float(
        string='Price per Sq Ft',
        compute='_compute_price_per_sqft',
        store=True,
        digits=(10, 2)
    )
    
    # Property Details
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=0
    )
    
    bathrooms = fields.Integer(
        string='Bathrooms',
        default=0
    )
    
    floors = fields.Integer(
        string='Floors',
        default=1
    )
    
    living_rooms = fields.Integer(
        string='Living Rooms',
        default=1
    )
    
    kitchen = fields.Boolean(
        string='Kitchen',
        default=True
    )
    
    garage = fields.Boolean(
        string='Garage',
        default=False
    )
    
    parking_spaces = fields.Integer(
        string='Parking Spaces',
        default=0
    )
    
    # Size Information
    land_size = fields.Float(
        string='Land Size (Sq Ft)',
        digits=(10, 2)
    )
    
    building_size = fields.Float(
        string='Building Size (Sq Ft)',
        digits=(10, 2)
    )
    
    # Features and Amenities
    feature_ids = fields.Many2many(
        'ghana_real_estate.property.feature',
        string='Features & Amenities'
    )
    
    # Media
    image_ids = fields.One2many(
        'ghana_real_estate.property.image',
        'property_id',
        string='Images'
    )
    
    video_url = fields.Char(
        string='Video URL',
        help='YouTube or Vimeo URL'
    )
    
    virtual_tour_url = fields.Char(
        string='Virtual Tour URL'
    )
    
    # Agent Information
    agent_id = fields.Many2one(
        'ghana_real_estate.agent',
        string='Agent',
        required=True,
        ondelete='restrict',
        index=True
    )
    
    # Website Display
    website_published = fields.Boolean(
        string='Published on Website',
        default=False,
        copy=False
    )
    
    featured = fields.Boolean(
        string='Featured Property',
        default=False,
        index=True
    )
    
    spotlight = fields.Boolean(
        string='Spotlight Property',
        default=False,
        help='Shows in spotlight section'
    )
    
    sequence = fields.Integer(
        string='Display Sequence',
        default=10
    )
    
    # Dates
    availability_date = fields.Date(
        string='Available From',
        default=fields.Date.today
    )
    
    sold_date = fields.Date(
        string='Date Sold',
        readonly=True,
        copy=False
    )
    
    # Computed Fields
    main_image = fields.Binary(
        string='Main Image',
        related='image_ids.image',
        readonly=True
    )
    
    image_count = fields.Integer(
        string='Image Count',
        compute='_compute_image_count'
    )
    
    is_available = fields.Boolean(
        string='Is Available',
        compute='_compute_is_available',
        search='_search_is_available'
    )
    
    display_price = fields.Char(
        string='Display Price',
        compute='_compute_display_price',
        store=True
    )
    
    # Search Keywords
    search_tags = fields.Char(
        string='Search Tags',
        help='Keywords for search optimization'
    )
    
    # Year Built
    year_built = fields.Integer(
        string='Year Built'
    )
    
    # Condition
    condition = fields.Selection([
        ('new', 'Brand New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('renovated', 'Renovated'),
    ], string='Condition',
       default='good'
    )
    
    # Furnishing
    furnished = fields.Boolean(
        string='Furnished',
        default=False
    )
    
    # Pet Policy
    pets_allowed = fields.Boolean(
        string='Pets Allowed',
        default=False
    )
    
    # Active Record
    active = fields.Boolean(
        string='Active',
        default=True,
        index=True
    )
    
    # Comments/Notes
    internal_notes = fields.Text(
        string='Internal Notes'
    )
    
    # Compute Methods
    @api.depends('price', 'building_size')
    def _compute_price_per_sqft(self):
        for record in self:
            if record.building_size and record.building_size > 0:
                record.price_per_sqft = record.price / record.building_size
            else:
                record.price_per_sqft = 0.0
    
    def _compute_image_count(self):
        for record in self:
            record.image_count = len(record.image_ids)
    
    @api.depends('state')
    def _compute_is_available(self):
        for record in self:
            record.is_available = record.state in ['available', 'draft']
    
    def _search_is_available(self, operator, value):
        return [('state', 'in', ['available', 'draft'])]
    
    @api.depends('price', 'currency_id')
    def _compute_display_price(self):
        for record in self:
            if record.currency_id:
                # Format price with GHS symbol
                price_str = f"{record.price:,.0f}"
                record.display_price = f"₵{price_str}"
            else:
                record.display_price = str(record.price)
    
    def _generate_property_code(self):
        """Generate unique property code"""
        sequence = self.env['ir.sequence'].next_by_code('ghana_real_estate.property')
        return f"GRE-{sequence}"
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError(_('Price must be greater than zero.'))
    
    @api.constrains('bedrooms', 'bathrooms')
    def _check_rooms(self):
        for record in self:
            if record.bedrooms < 0:
                raise ValidationError(_('Number of bedrooms cannot be negative.'))
            if record.bathrooms < 0:
                raise ValidationError(_('Number of bathrooms cannot be negative.'))
    
    # Action Methods
    def action_publish(self):
        """Publish property on website"""
        self.write({'website_published': True, 'state': 'available'})
    
    def action_unpublish(self):
        """Unpublish property from website"""
        self.write({'website_published': False})
    
    def action_mark_as_sold(self):
        """Mark property as sold"""
        self.write({'state': 'sold', 'sold_date': fields.Date.today()})
    
    def action_mark_as_pending(self):
        """Mark property as pending"""
        self.write({'state': 'pending'})
    
    def action_reset_to_available(self):
        """Reset property to available"""
        self.write({'state': 'available'})
    
    def get_absolute_url(self):
        """Get absolute URL for website"""
        return f"/property/{self.id}"
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_property_code', 'UNIQUE(property_code)', 'Property code must be unique!'),
        ('positive_price', 'CHECK(price > 0)', 'Price must be greater than zero!'),
    ]
    
    # Cron Jobs
    def update_property_availability(self):
        """Update property availability status"""
        # This method can be called by a cron job
        pass
    
    # Website URL
    def website_url(self):
        """Generate website URL"""
        return f"/properties/{self.id}"
    
    @api.returns('self', lambda value: value.id)
    def website_publish_button(self):
        """Button to publish from website"""
        return self


class GhanaRealEstatePropertyImage(models.Model):
    """Property Images Model"""
    
    _name = 'ghana_real_estate.property.image'
    _description = 'Property Image'
    _order = 'sequence, id'
    
    property_id = fields.Many2one(
        'ghana_real_estate.property',
        string='Property',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    image = fields.Binary(
        string='Image',
        required=True
    )
    
    name = fields.Char(
        string='Image Name',
        translate=True
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    is_main = fields.Boolean(
        string='Main Image',
        default=False
    )
    
    description = fields.Text(
        string='Description'
    )
    
    @api.constrains('is_main')
    def _check_single_main_image(self):
        """Ensure only one main image per property"""
        for record in self:
            if record.is_main:
                existing = self.search([
                    ('property_id', '=', record.property_id.id),
                    ('is_main', '=', True),
                    ('id', '!=', record.id)
                ])
                if existing:
                    existing.write({'is_main': False})


class GhanaRealEstatePropertyFeature(models.Model):
    """Property Features and Amenities Model"""
    
    _name = 'ghana_real_estate.property.feature'
    _description = 'Property Feature'
    _order = 'name'
    
    name = fields.Char(
        string='Feature Name',
        required=True,
        translate=True,
        index=True
    )
    
    icon = fields.Char(
        string='Icon Class',
        help='Font Awesome icon class',
        default='fa-check'
    )
    
    description = fields.Text(
        string='Description'
    )
    
    category = fields.Selection([
        ('outdoor', 'Outdoor'),
        ('indoor', 'Indoor'),
        ('security', 'Security'),
        ('eco', 'Eco-Friendly'),
        ('tech', 'Smart Home'),
        ('other', 'Other'),
    ], string='Category',
       default='other'
    )
    
    property_ids = fields.Many2many(
        'ghana_real_estate.property',
        string='Properties'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
