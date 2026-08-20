from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    buyer_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date_from = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = date_from + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date_from = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            # Set validity if the user modifies the date_deadline.
            if record.date_deadline:
                record.validity = (record.date_deadline - date_from).days
