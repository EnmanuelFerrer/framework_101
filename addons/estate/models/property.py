from odoo import fields, models


class Property(models.Model):
    _name = "property"
    _description = "Property"

    name = fields.Char(string="Name of the property", required=True)
    description = fields.Text(string="Property description")
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(
        string="Availability date",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Amount of bedroom", default=2)
    living_area = fields.Integer(string="Amount of livings")
    facades = fields.Integer(string="Amount of facades")
    garage = fields.Boolean(string="Have garage?")
    garden = fields.Boolean(string="Have garden?")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(
        string="Cardinal orientation of the garden",
        selection=[
            ("North", "north"),
            ("South", "south"),
            ("East", "east"),
            ("West", "west"),
        ],
    )

    active = fields.Boolean("Active", default=True)
