from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_state_sold(self):
        return super().action_set_state_sold()
