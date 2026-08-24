from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    _check_name = models.Constraint("unique (name)", "Name must be unique.")

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer("Sequence", default=1, help="Used to order types")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
