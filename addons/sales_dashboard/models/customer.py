from odoo import fields, models


class SdCustomer(models.Model):
    _name = 'sd.customer'
    _description = 'Dashboard Customer'

    name = fields.Char(required=True)
    city = fields.Char()