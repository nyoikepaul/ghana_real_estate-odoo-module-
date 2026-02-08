# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class GhanaRealEstateAgent(models.Model):
    """Premium Agent Model for Ghana Real Estate Website"""
    
    _name = 'ghana_real_estate.agent'
    _description = 'Real Estate Agent'
    _inherit = ['website.seo.metadata', 'website.published.mixin']
    _order = 'sequence, name'
    _rec_name = 'name'

    # Basic Information
    name = fields.Char(
        string='Full Name',
        required=True,
        index=True
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        ondelete='set null',
        help='Link to system partner for complete contact info'
    )
    
    # Professional Information
    title = fields.Char(
        string='Professional Title',
        default='Real Estate Agent'
    )
    
    license_number = fields.Char(
        string='License Number',
        required=True,
        index=True
    )
    
    bio = fields.Html(
        string='Biography',
        sanitize_attributes=False
    )
    
    specializations = fields.Many2many(
        'ghana_real_estate.property.type',
        string='Specializations'
    )
    
    languages = fields.Many2many(
        'res.lang',
        string='Languages',
        help='Languages the agent speaks'
    )
    
    # Contact Information
    phone = fields.Char(
        string='Phone',
        required=True
    )
    
    mobile = fields.Char(
        string='Mobile Phone'
    )
    
    email = fields.Char(
        string='Email',
        required=True
    )
    
    website = fields.Char(
        string='Personal Website'
    )
    
    # Social Media
    facebook = fields.Char(
        string='Facebook URL'
    )
    
    twitter = fields.Char(
        string='Twitter URL'
    )
    
    linkedin = fields.Char(
        string='LinkedIn URL'
    )
    
    instagram = fields.Char(
        string='Instagram URL'
    )
    
    whatsapp = fields.Char(
        string='WhatsApp Number',
        help='Include country code'
    )
    
    # Office Information
    office_id = fields.Many2one(
        'ghana_real_estate.office',
        string='Office',
        ondelete='restrict'
    )
    
    # Media
    photo = fields.Binary(
        string='Photo',
        attachment=True
    )
    
    # Performance Metrics
    properties_sold = fields.Integer(
        string='Properties Sold',
        readonly=True,
        default=0
    )
    
    properties_rented = fields.Integer(
        string='Properties Rented',
        readonly=True,
        default=0
    )
    
    years_experience = fields.Integer(
        string='Years of Experience',
        default=0
    )
    
    client_rating = fields.Float(
        string='Client Rating',
        digits=(3, 2),
        readonly=True,
        default=0.0
    )
    
    review_count = fields.Integer(
        string='Number of Reviews',
        readonly=True,
        default=0
    )
    
    # Website Display
    website_published = fields.Boolean(
        string='Published on Website',
        default=False,
        copy=False
    )
    
    featured_agent = fields.Boolean(
        string='Featured Agent',
        default=False,
        help='Show on homepage as featured'
    )
    
    sequence = fields.Integer(
        string='Display Sequence',
        default=10
    )
    
    # Active Record
    active = fields.Boolean(
        string='Active',
        default=True,
        index=True
    )
    
    # Computed Fields
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
    full_contact_info = fields.Html(
        string='Full Contact Info',
        compute='_compute_full_contact_info'
    )
    
    properties_count = fields.Integer(
        string='Active Properties',
        compute='_compute_properties_count'
    )
    
    # Search Keywords
    search_tags = fields.Char(
        string='Search Tags'
    )
    
    # Constrains and Validation
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, record.email):
                    raise ValidationError(_('Invalid email format for %s') % record.name)
    
    @api.constrains('phone', 'mobile')
    def _check_phone(self):
        """Validate Ghana phone numbers"""
        for record in self:
            if record.phone:
                # Ghana phone format: +233 or 0 followed by 9 digits
                phone_pattern = r'^(\+233|0)\d{9}$'
                if not re.match(phone_pattern, record.phone.replace(' ', '')):
                    raise ValidationError(_('Invalid Ghana phone number format for %s') % record.name)
    
    @api.constrains('whatsapp')
    def _check_whatsapp(self):
        """Validate WhatsApp number"""
        for record in self:
            if record.whatsapp:
                phone_pattern = r'^(\+233|0)\d{9}$'
                if not re.match(phone_pattern, record.whatsapp.replace(' ', '')):
                    raise ValidationError(_('Invalid WhatsApp number format for %s') % record.name)
    
    # Compute Methods
    @api.depends('name', 'title')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.title}: {record.name}" if record.title else record.name
    
    def _compute_full_contact_info(self):
        for record in self:
            info = f"""
            <div class="agent-contact">
                <p><strong>Phone:</strong> {record.phone or ''}</p>
                <p><strong>Mobile:</strong> {record.mobile or ''}</p>
                <p><strong>Email:</strong> {record.email or ''}</p>
                <p><strong>License:</strong> {record.license_number or ''}</p>
            </div>
            """
            record.full_contact_info = info
    
    def _compute_properties_count(self):
        for record in self:
            record.properties_count = self.env['ghana_real_estate.property'].search_count([
                ('agent_id', '=', record.id),
                ('website_published', '=', True),
                ('state', 'in', ['available', 'draft'])
            ])
    
    # Action Methods
    def action_view_properties(self):
        """View all properties by this agent"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'res_model': 'ghana_real_estate.property',
            'view_mode': 'kanban,tree,form',
            'domain': [('agent_id', '=', self.id)],
            'context': {'default_agent_id': self.id}
        }
    
    def action_toggle_publish(self):
        """Toggle website publication status"""
        self.write({'website_published': not self.website_published})
    
    def action_send_email(self):
        """Send email to agent"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'mailto:{self.email}',
            'target': 'new'
        }
    
    def action_call(self):
        """Initiate call to agent"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'tel:{self.phone}',
            'target': 'new'
        }
    
    def action_whatsapp(self):
        """Open WhatsApp chat"""
        # Format number for WhatsApp
        number = self.whatsapp.replace('+', '').replace(' ', '')
        return {
            'type': 'ir.actions.act_url',
            'url': f'https://wa.me/{number}',
            'target': 'new'
        }
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_license', 'UNIQUE(license_number)', 'License number must be unique!'),
        ('unique_email', 'UNIQUE(email)', 'Email must be unique!'),
    ]


class GhanaRealEstateOffice(models.Model):
    """Office/Branch Model"""
    
    _name = 'ghana_real_estate.office'
    _description = 'Real Estate Office'
    _order = 'name'
    
    name = fields.Char(
        string='Office Name',
        required=True
    )
    
    address = fields.Text(
        string='Address',
        required=True
    )
    
    city = fields.Char(
        string='City',
        required=True
    )
    
    region = fields.Selection([
        ('greater_accra', 'Greater Accra'),
        ('ashanti', 'Ashanti'),
        ('central', 'Central'),
        ('eastern', 'Eastern'),
        ('northern', 'Northern'),
        ('upper_east', 'Upper East'),
        ('upper_west', 'Upper West'),
        ('volta', 'Volta'),
        ('western', 'Western'),
        ('western_north', 'Western North'),
        ('bono', 'Bono'),
        ('bono_east', 'Bono East'),
        ('ahafo', 'Ahafo'),
        ('oti', 'Oti'),
        ('savannah', 'Savannah'),
        ('north_east', 'North East'),
    ], string='Region',
       required=True
    )
    
    phone = fields.Char(
        string='Phone',
        required=True
    )
    
    email = fields.Char(
        string='Email',
        required=True
    )
    
    working_hours = fields.Char(
        string='Working Hours',
        default='Mon-Fri: 8:00 AM - 6:00 PM'
    )
    
    agent_ids = fields.One2many(
        'ghana_real_estate.agent',
        'office_id',
        string='Agents'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
