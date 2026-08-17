from odoo import fields, models


class Property(models.Model):
    _name = "property"
    _description = "Propiedad"

    name = fields.Char(string="Nombre de la propiedad", required=True)
    description = fields.Text(string="Descripcion de la propiedad", required=False)
    postcode = fields.Char(
        string="Codigo postal", required=True, description="Codigo postal"
    )
    date_availability = fields.Date(string="Fecha de disponibilidad")
    expected_price = fields.Float(string="Precio", required=True)
    selling_price = fields.Float(string="Precio de venta")
    bedrooms = fields.Integer(string="Cantidad de habitaciones")
    living_area = fields.Integer(string="Cantidad de livings")
    facades = fields.Integer(string="Cantidad de fachadas")
    garage = fields.Boolean(string="Tiene garage")
    garden = fields.Boolean(string="Tiene jardin")
    garden_area = fields.Integer(string="Tamanio del jardin")
    garden_orientation = fields.Selection(
        string="Orientacion cardinal del jardin",
        selection=[
            ("Norte", "north"),
            ("Sur", "south"),
            ("Este", "east"),
            ("Oeste", "West"),
        ],
    )
