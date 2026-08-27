# =============================================================================
# Import the required Odoo modules.
# - models: provides the base classes for defining Odoo models.
# - fields: provides all the field types available in Odoo (Char, Integer, etc.)
# =============================================================================
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


# =============================================================================
# Property Model
# =============================================================================
# This model represents a real estate property. It inherits from
# models.Model, which means it will be backed by a database table
# and will have full ORM capabilities (create, read, update, delete).
#
# The '_name' attribute defines the model's technical name used in the
# database and throughout the ORM. It must be unique and follow the
# "module.model_name" convention using dot notation (e.g., "estate.property").
#
# The '_description' attribute provides a human-readable name for the
# model, used in logs, warnings, and the Odoo backend interface.
# =============================================================================
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        definition="CHECK(expected_price > 0)",
        message="Expected price must be positive.",
    )

    _check_selling_price = models.Constraint(
        definition="CHECK(selling_price > 0)", message="Selling price must be positive."
    )

    # -------------------------------------------------------------------------
    # Basic Fields
    # -------------------------------------------------------------------------
    # These are the fundamental field types in Odoo:
    # - Char: short text (stored as VARCHAR in the database).
    # - Text: long text (stored as TEXT in the database).
    # - Float: decimal numbers (stored as DOUBLE PRECISION).
    # - Integer: whole numbers (stored as INTEGER).
    # - Boolean: true/false values (stored as BOOLEAN).
    # - Selection: a list of predefined choices (stored as VARCHAR).
    # - Date: a date value without time (stored as DATE).
    #
    # Common attributes for all fields:
    # - string: the label displayed in the UI.
    # - required: if True, the field must have a value (NOT NULL constraint).
    # - default: the default value when creating a new record.
    # - readonly: if True, the field cannot be edited in the UI.
    # - copy: if False, the field value is NOT copied when duplicating a record.
    # -------------------------------------------------------------------------

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")

    # Date field with a callable default.
    # The 'default' parameter accepts a callable (function or lambda) that
    # will be executed each time a new record is created. This ensures the
    # date is always computed relative to the current moment, instead of
    # being fixed at module load time.
    # 'copy=False' prevents the value from being copied when the record
    # is duplicated.
    # 'fields.Date.add()' is a static helper method provided by Odoo to
    # perform date arithmetic using relativedelta under the hood.
    date_availability = fields.Date(
        string="Available from",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float(string="Expected Price", required=True)

    # 'readonly=True' makes the field non-editable in the UI.
    # 'copy=False' ensures the selling price is not carried over
    # when duplicating a property record.
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    # Integer fields with default values.
    # The 'default' parameter can also be a static value (not a callable)
    # when the value does not depend on runtime context.
    bedrooms = fields.Integer(string="Bedrooms", default=2)

    living_area = fields.Integer(string="Living Area (sqm)", default=0)
    facades = fields.Integer(string="Facades")

    # Boolean fields represent simple true/false toggles.
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")

    # Garden-related fields (only relevant if garden=True).
    garden_area = fields.Integer(string="Garden Area (sqm)", default=0)

    # Selection fields present a dropdown of predefined options.
    # The 'selection' parameter is a list of tuples: (value, label).
    # - The first element is the value stored in the database.
    # - The second element is the label displayed in the UI.
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        copy=False,
    )

    # -------------------------------------------------------------------------
    # Reserved Fields
    # -------------------------------------------------------------------------
    # Odoo has a set of "reserved field names" that trigger special
    # behavior when defined on a model. The most common ones are:
    #
    # - 'active' (Boolean): controls the visibility of records.
    #   When active=False, the record is hidden from most searches
    #   and list views, but it still exists in the database.
    #   Odoo automatically provides two methods on models that
    #   define this field:
    #     * action_archive(): sets active to False.
    #     * action_unarchive(): sets active to True.
    #
    # - 'name' (Char): used as the default representation of records
    #   (_rec_name) in the UI (e.g., in Many2one dropdowns).
    #
    # - 'state' (Selection): used to define lifecycle stages of a record.
    #
    # - 'company_id' (Many2one to res.company): enables multi-company
    #   record rules.
    # -------------------------------------------------------------------------
    active = fields.Boolean(string="Active", default=True)

    # -------------------------------------------------------------------------
    # Lifecycle Status (reserved field 'state')
    # -------------------------------------------------------------------------
    # 'state' is a reserved field name in Odoo used to define the
    # lifecycle stages of a record. It is implemented as a Selection
    # field whose possible values represent where the property is in
    # its selling workflow.
    #
    # The workflow transitions are:
    #   new            -> Offer Received -> Offer Accepted -> Sold
    #                                            \-> Canceled
    #
    # - 'new': the property has just been created, no offers yet.
    # - 'offer_received': at least one offer has been received.
    # - 'offer_accepted': an offer has been accepted by the seller.
    # - 'sold': the sale has been completed.
    # - 'canceled': the sale process was aborted.
    #
    # Attributes used:
    # - string: the label shown in the UI.
    # - required: every property must always have a status.
    # - copy=False: the status must NOT be duplicated when copying a
    #   property; the new record starts fresh in its default stage.
    # - default='new': new properties always start in the 'new' stage.
    # -------------------------------------------------------------------------
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Type"
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Tags"
    )
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    total_area = fields.Float(compute="_total_area", default=0.0)

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_offer = fields.Float(compute="_best_offer", default=0.0, readonly=True)

    @api.depends("offer_ids.price")
    def _best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_state_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties can not be sold.")
            if record.date_availability >= fields.Date.today():
                raise UserError(
                    f"The property is available to be sold from {record.date_availability}"  # noqa: E501
                )
            record.state = "sold"
        return True

    def action_set_state_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties can not be cancelled.")
            record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_rounding=0.001)
                and float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_rounding=0.001,
                )
                == -1
            ):
                raise ValidationError(
                    "Selling price must be at least 90% of the expected price. "
                    "You must reduce expected price to accept this offer."
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("Only new or cancelled properties can be deleted.")
