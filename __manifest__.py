# -*- coding: utf-8 -*-
{
    'name': 'Ghana Real Estate Premium Website',
    'description': 'Premium Real Estate Website for Ghana - Elite Development',
    'author': 'Elite Development Team',
    'website': 'https://www.ghanarealestate.com',
    'version': '1.0.0',
    'category': 'Website',
    'depends': [
        'website',
        'sale',
        'account',
        'base_setup',
    ],
    'data': [
        'views/templates.xml',
        'views/property_views.xml',
        'views/agent_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/properties.xml',
        'demo/agents.xml',
    ],
    'qweb': [
        'static/src/xml/website.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ghana_real_estate/static/src/css/premium_style.css',
            'ghana_real_estate/static/src/js/premium_script.js',
        ],
    },
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'GHS',
}
