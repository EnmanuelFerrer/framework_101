from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    _check_name = models.Constraint(
        definition="unique (name)", message="Name must be unique."
    )

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order types")
    property_ids = fields.One2many(
        string="Properties",
        comodel_name="estate.property",
        inverse_name="property_type_id",
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.constrains("name")
    def _check_name_case_insensitive(self):
        for record in self:
            domain = [("id", "!=", record.id), ("name", "ilike", record.name)]
            if self.search_count(domain) > 0:
                raise ValidationError(message="Name must be unique.")
