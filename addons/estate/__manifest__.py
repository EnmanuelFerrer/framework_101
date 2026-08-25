{
    "name": "Estate Property",
    "version": "19.0.1.0.0",
    "category": "Prueba tecnica",
    "author": "Enmanuel Ferrer",
    "contributor": [
        "https://github.com/EnmanuelFerrer",
    ],
    "description": "Framework 101",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",

        # Views
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_property_menus.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
