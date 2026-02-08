# Ghana Real Estate Premium Website - Odoo Module

## 🏠 Premium Real Estate Website for Ghana

A comprehensive, elite-quality Odoo module for building a premium real estate website tailored for the Ghanaian market. This module includes everything you need to showcase properties, manage agents, and provide an exceptional user experience.

## ✨ Features

### Core Features
- **Property Management**: Complete property listing with detailed information
- **Agent Profiles**: Showcase your real estate agents with contact information
- **Property Types**: Houses, Apartments, Villas, Land, Commercial, Office
- **Location-based Search**: Browse by Ghana's regions and cities
- **Advanced Search**: Filter by price, bedrooms, bathrooms, and more
- **Featured Properties**: Highlight premium listings
- **Inquiry Forms**: Contact forms and schedule viewing requests
- **Property Comparison**: Compare up to 4 properties side by side
- **Favorites**: Save properties to your favorites list

### Website Sections
- **Premium Header**: Sticky navigation with dropdown menus
- **Hero Section**: Eye-catching hero with property search
- **Featured Properties**: Grid of premium property listings
- **Property Types**: Browse by category
- **Spotlight Section**: Exclusive properties carousel
- **Locations Grid**: Explore Ghana's regions
- **Featured Agents**: Team showcase
- **Why Choose Us**: Company advantages
- **Testimonials**: Client reviews carousel
- **Premium Footer**: Complete footer with contact info

## 🚀 Installation

### Prerequisites
- Odoo 16.0 or higher
- Python 3.8+
- PostgreSQL

### Installation Steps

1. **Copy Module**
   ```bash
   # Copy the ghana_real_estate module to your Odoo addons path
   cp -r ghana_real_estate /path/to/odoo/addons/
   ```

2. **Restart Odoo**
   ```bash
   # Restart your Odoo server
   systemctl restart odoo
   # Or manually restart
   ```

3. **Update Apps List**
   - Go to **Apps** → Click **Update Apps List**
   - Or navigate to: `http://localhost:8069/web?debug=1#menu_id=`

4. **Install Module**
   - Search for "Ghana Real Estate"
   - Click **Install**

5. **Load Demo Data**
   - After installation, click "Load Demo Data" to populate sample properties and agents

## 📁 Module Structure

```
ghana_real_estate/
├── __init__.py                    # Module initialization
├── __manifest__.py                # Module manifest
├── models/
│   ├── __init__.py
│   ├── property.py               # Property model (200+ lines)
│   ├── agent.py                  # Agent model (150+ lines)
│   └── property_type.py          # Property types and locations
├── controllers/
│   ├── __init__.py
│   ├── main.py                   # Main website controller
│   └── property_controller.py     # Property-specific actions
├── views/
│   ├── templates.xml             # Homepage and main templates
│   ├── property_views.xml       # Property detail and listing
│   └── agent_views.xml           # Agent pages
├── static/
│   ├── src/
│   │   ├── css/
│   │   │   └── premium_style.css # Premium styling (900+ lines)
│   │   ├── js/
│   │   │   └── premium_script.js  # Interactive functionality
│   │   └── xml/
│   │       └── website.xml        # QWeb templates
│   └── description/
│       └── icon.png              # Module icon
├── security/
│   └── ir.model.access.csv       # Access control lists
└── demo/
    ├── properties.xml            # Demo properties data
    └── agents.xml                # Demo agents data
```

## 🔧 Configuration

### Settings

After installation, configure the following in **Settings → Ghana Real Estate**:

1. **Company Information**
   - Company Name
   - Contact Email
   - Phone Number
   - Address

2. **Website Settings**
   - Default Currency: GHS (Ghana Cedi)
   - Properties per page: 12
   - Featured properties limit: 6

3. **Social Media Links**
   - Facebook
   - Twitter
   - Instagram
   - LinkedIn
   - YouTube

## 📝 Usage

### Adding Properties

1. Go to **Properties** menu
2. Click **Create**
3. Fill in property details:
   - Name and Description
   - Property Type (House, Apartment, etc.)
   - Transaction Type (Sale, Rent, Lease)
   - Location (Region, City, Address)
   - Pricing
   - Features (Bedrooms, Bathrooms, Size)
   - Images
   - Assign Agent
4. Click **Publish** to make visible on website

### Managing Agents

1. Go to **Agents** menu
2. Click **Create**
3. Fill in agent information:
   - Name and Photo
   - License Number
   - Contact Information
   - Bio and Specializations
   - Performance Metrics
4. Click **Publish** to show on website

### Customizing Website

#### Colors
Edit `static/src/css/premium_style.css`:
```css
:root {
    --primary-color: #1a5f2a;  /* Ghana Green */
    --secondary-color: #d4af37; /* Gold Accent */
}
```

#### Hero Image
Replace `static/src/images/hero-bg.jpg` with your own image

#### Logo
Update the brand text in `views/templates.xml`

## 🎨 Design Highlights

### Premium Color Scheme
- **Primary**: Ghana Green (#1a5f2a) - Represents growth and prosperity
- **Secondary**: Gold (#d4af37) - Adds premium elegance
- **Neutral**: Clean whites and grays for readability

### Typography
- **Headings**: Playfair Display - Sophisticated serif
- **Body**: Poppins - Clean, modern sans-serif

### Animations & Effects
- Smooth scroll animations
- Hover effects on cards
- Parallax scrolling
- Fade-in transitions
- Number counter animations

## 🔌 API Endpoints

### Public API
- `GET /api/properties/search` - Search properties
- `GET /api/property/<id>` - Get property details
- `GET /api/property-types` - List property types
- `GET /api/locations` - List regions
- `GET /api/featured-properties` - Get featured listings

### Example API Call
```javascript
// Search properties
const response = await fetch('/api/properties/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        transaction_type: 'sale',
        property_type: 'villa',
        location: 'Accra',
        min_price: 500000,
        bedrooms: 3
    })
});
```

## 📱 Responsive Design

The website is fully responsive and works perfectly on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🔒 Security Features

- CSRF protection on all forms
- Input validation and sanitization
- Secure file upload for images
- Role-based access control
- SQL injection prevention

## 📄 License

This module is licensed under the LGPL-3.0 license.

## 👨‍💻 Development

Created with ❤️ by Elite Development Team

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support, please contact:
- Email: support@ghanarealestate.com
- Phone: +233 30 123 4567

## 🙏 Acknowledgments

- Odoo Community
- Font Awesome for icons
- Owl Carousel for sliders
- Google Fonts for typography

---

**Made with ❤️ for Ghana's Real Estate Market**
