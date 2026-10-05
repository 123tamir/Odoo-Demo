from odoo import api, fields, models


class SdProduct(models.Model):
    _name = 'sd.product'
    _description = 'Dashboard Product'

    name = fields.Char(required=True)
    category = fields.Selection([
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('stationery', 'Stationery'),
    ], default='electronics')
    unit_price = fields.Float(required=True)
    stock_qty = fields.Integer(string="In Stock")
    reorder_level = fields.Integer(default=10)
    is_low_stock = fields.Boolean(
        compute='_compute_is_low_stock', store=True, index=True)

    @api.depends('stock_qty', 'reorder_level')
    def _compute_is_low_stock(self):
        for product in self:
            product.is_low_stock = product.stock_qty <= product.reorder_level