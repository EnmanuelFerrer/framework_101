# =============================================================================
# Import the required Odoo modules.
# - models: provides the base classes for defining Odoo models.
# - fields: provides all the field types available in Odoo (Char, Integer, etc.)
# =============================================================================
from odoo import fields, models


# =============================================================================
# Property Model
# =============================================================================
# This model represents a real estate property. It inherits from
# models.Model, which means it will be backed by a database table
# and will have full ORM capabilities (create, read, update, delete).
#
# The '_name' attribute defines the model's technical name used in the
# database and throughout the ORM. It must be unique and follow the
# "module.model_name" convention (here we omit the module prefix for
# simplicity).
#
# The '_description' attribute provides a human-readable name for the
# model, used in logs, warnings, and the Odoo backend interface.
# =============================================================================
class Property(models.Model):
    _name = "property"
    _description = "Property"

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

    name = fields.Char(string="Name of the property", required=True)
    description = fields.Text(string="Property description")
    postcode = fields.Char(string="Postal code")

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
        string="Availability date",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float(string="Expected price", required=True)

    # 'readonly=True' makes the field non-editable in the UI.
    # 'copy=False' ensures the selling price is not carried over
    # when duplicating a property record.
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)

    # Integer fields with default values.
    # The 'default' parameter can also be a static value (not a callable)
    # when the value does not depend on runtime context.
    bedrooms = fields.Integer(string="Amount of bedrooms", default=2)

    living_area = fields.Integer(string="Amount of livings")
    facades = fields.Integer(string="Amount of facades")

    # Boolean fields represent simple true/false toggles.
    garage = fields.Boolean(string="Have garage?")
    garden = fields.Boolean(string="Have garden?")

    # Garden-related fields (only relevant if garden=True).
    garden_area = fields.Integer(string="Garden area")

    # Selection fields present a dropdown of predefined options.
    # The 'selection' parameter is a list of tuples: (value, label).
    # - The first element is the value stored in the database.
    # - The second element is the label displayed in the UI.
    garden_orientation = fields.Selection(
        string="Cardinal orientation of the garden",
        selection=[
            ("North", "north"),
            ("South", "south"),
            ("East", "east"),
            ("West", "west"),
        ],
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
    active = fields.Boolean("Active", default=True)
