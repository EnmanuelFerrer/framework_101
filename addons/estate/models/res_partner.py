from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="buyer_id",
        string="Properties",
        domain=[
            ("state", "=", "sold"),
        ],
    )
