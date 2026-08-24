from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    _check_name = models.Constraint("unique (name)", "Name must be unique.")

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer("Color", default=1)
