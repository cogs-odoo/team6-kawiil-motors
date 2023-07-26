{
    "name": "GE07-TEAM6",
    "summary": "Motorcyle Registry Manufacturing Enhancements",
    "description": """
Motorcycle Registry
====================
K'awiil Motors wants to integrate their Motorcycle registry with the inventory app. They would like to create an entry in the motorcycle registry right when the final delivery order is validated. (So when the motorcycle is about to leave the dealership to go to the customer. K'awiil's flow currently creates a Delivery Order from the manufacturing plant to the dealership, and then a 2nd one from the dealership to the customer.
    """,
    "version": "1.0",
    "category": "Kauil/Registry",
    "license": "OPL-1",
    "depends": ["motorcycle_registry"],
    "data": [
        "views/ge07_stock_view_production_lot_tree_inherit.xml",
        "views/ge07_motorcycle_registry_view_list_inherit.xml"
    ],
    "demo": [],
    "author": "kauil-motors",
    "website": "www.odoo.com",
    "application": True,
}
