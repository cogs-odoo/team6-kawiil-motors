{
    'name' : 'GE02 TEAM6',
    'description': '''
Motorcycle Registry
====================
Addition of a map views that allows K'awiil Motors to view the locations of their registered motorcycles on a map.
''',
    'autor' : 'cogs-odoo',
    'website' : 'https://github.com/cogs-odoo/team6-kawiil-motors',
    'category' : 'Kawiil/custom',
    'application' : 'True',
    'depends' : [
        'motorcycle_registry',
        'web_map'
        ],
    'data' : [
        'views/motorcycle_map_view_inherit.xml',
    ],
    'demo' : [],
    "application": False,
    "license": "OPL-1",
}
