{
    "name": "GE10-TEAM6",
    "summary": "Total Motorcycle Mileage",
    "description": """
Motorcycle Registry
====================
K'awiil Motors wants to be able to showcase both its motorcycle's reliability and popularity. They want to display the total miles all of their motorcycles have traveled. Since they already keep track of their motorcycle's mileage on their motorcycle registry, this should be fairly straightforward to implement on the backend. They're not sure where they want it to be shown, so they want it to be a website snippet/widget that they can drag/drop anywhere on the website. Bonus points for making an attractive odometer counter snippet
    """,    
    "version": "1.0",
    "category": "Kauil/Registry",
    "license": "OPL-1",
    "depends": ["motorcycle_registry"],
    "data": [
        "views/snippets/snippets.xml",
        "views/snippets/s_mileage.xml",
    ],
    "demo": [],
    "author": "kauil-motors",
    "website": "www.odoo.com",
    "application": False,
    "assets": {
        'website.assets_wysiwyg': [
            'GE10-TEAM6/static/src/snippets/s_mileage/options.js',
        ],
    }
}
