from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    _check_price = models.Constraint("CHECK(price > 0)", "Price must be positive.")

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

    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property type",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date_from = (
                record.create_date.date() if record.create_date else fields.Date.today()
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

    # set the offer status to Accepted, then set selling price
    def action_set_status_accepted(self):
        for offer in self:
            if (
                offer.property_id.state == "cancelled"
                or offer.property_id.state == "sold"
            ):
                raise UserError("Cancelled or sold properties cannot accept offers.")

            if offer.status == "refused":
                raise UserError("Refused offers cannot be accepted.")

            accepted_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            if accepted_offers:
                raise UserError("Only one offer can be accepted.")

            offer.status = "accepted"

            # offer.property_id.write(
            #     {
            #         "buyer_id": offer.buyer_id.id,
            #         "selling_price": offer.price,
            #         "state": "offer_accepted",
            #     }
            # )

            offer.property_id.buyer_id = offer.buyer_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"
        return True

    def action_set_status_refused(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("Accepted offers cannot be cancelled.")

            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "property_id" in vals and "price" in vals:
                # if ("property_id", "amount") in vals:
                property_record = self.env["estate.property"].browse(
                    vals["property_id"]
                )

                existing_prices = property_record.offer_ids.mapped("price")
                if existing_prices and vals["price"] < max(existing_prices):
                    raise UserError(
                        "The offer amount cannot be lower than an existing offer."
                    )

                property_record.state = "offer_received"
        return super(EstatePropertyOffer, self).create(vals_list)
