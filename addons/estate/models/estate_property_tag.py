from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    _check_name = models.Constraint(
        definition="unique (name)", message="Name must be unique."
    )

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color", default=1)

    @api.constrains("name")
    def _check_name_case_insensitive(self):
        for record in self:
            domain = [("id", "!=", record.id), ("name", "ilike", record.name)]
            if self.search_count(domain) > 0:
                raise ValidationError(message="Name must be unique.")
