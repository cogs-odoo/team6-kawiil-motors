{
    'name' : 'GE04 TEAM6',
    'description': '''
                    Motorcycle Registry
                    ====================
                    This Module is used to keep track of the Motorcycle Registration and Ownership of each motorcycled of the brand.
                    ''',
    'autor' : 'jlma-odoo',
    'website' : 'https://github.com/jlma-odoo/custom-addons',
    'category' : 'Kawiil/custom',
    'application' : 'True',
    'depends' : ['stock','website','sale'],
    "license": "OPL-1",
    'data' : [
        'data/discount_data.xml',
        'views/sale_view_inherit.xml',
    ],
    'demo' : [
    ],
}
