{
    'name' : 'GE01 TEAM6',
    'description': '''
                    Motorcycle Registry
                    ====================
                    This Module is used to keep track of the Motorcycle Registration and Ownership of each motorcycled of the brand.
                    ''',
    'autor' : 'jlma-odoo',
    'website' : 'https://github.com/jlma-odoo/custom-addons',
    'category' : 'Kawiil/custom',
    'application' : 'True',
    'depends' : ['base','stock','website','sale'],
    'data' : [
        'views/product_template_inherit.xml',

    ],
    'demo' : [
        'demo/demo_data.xml',
    ],
}