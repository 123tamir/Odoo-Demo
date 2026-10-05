{
    'name': 'Sales Dashboard',
    'version': '17.0.1.0.0',
    'summary': 'Custom sales dashboard with KPI tiles and charts',
    'category': 'Sales',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/seed.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sales_dashboard/static/src/dashboard/dashboard.js',
            'sales_dashboard/static/src/dashboard/dashboard.xml',
            'sales_dashboard/static/src/dashboard/dashboard.scss',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}