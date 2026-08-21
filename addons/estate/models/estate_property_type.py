from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    _check_name = models.Constraint("unique (name)", "Name must be unique.")

    name = fields.Char(string="Name", required=True)
