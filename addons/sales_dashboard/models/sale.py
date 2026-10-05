import random
from datetime import timedelta

from odoo import api, fields, models


class SdSale(models.Model):
    _name = 'sd.sale'
    _description = 'Dashboard Sale'
    _order = 'date desc, id desc'

    name = fields.Char(compute='_compute_name', store=True)
    date = fields.Date(required=True, index=True, default=fields.Date.today)
    customer_id = fields.Many2one('sd.customer', required=True, index=True)
    product_id = fields.Many2one('sd.product', required=True, index=True)
    quantity = fields.Integer(default=1)
    amount = fields.Float(compute='_compute_amount', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed')],
        default='draft', index=True)

    @api.depends('customer_id.name', 'product_id.name')
    def _compute_name(self):
        for sale in self:
            sale.name = f"{sale.customer_id.name or ''} - {sale.product_id.name or ''}"

    @api.depends('quantity', 'product_id.unit_price')
    def _compute_amount(self):
        for sale in self:
            sale.amount = sale.quantity * sale.product_id.unit_price

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    # ---------- Dashboard data (called from the OWL component) ----------
    @api.model
    def get_dashboard_data(self, date_from, date_to):
        domain = [
            ('state', '=', 'confirmed'),
            ('date', '>=', date_from),
            ('date', '<=', date_to),
        ]
        # One SQL aggregate query instead of looping over records
        totals = self.read_group(domain, ['amount:sum'], [])
        total_sales = (totals[0].get('amount') or 0.0) if totals else 0.0
        order_count = totals[0]['__count'] if totals else 0

        by_product = self.read_group(
            domain, ['amount:sum'], ['product_id'],
            orderby='amount desc', limit=5)
        by_month = self.read_group(
            domain, ['amount:sum'], ['date:month'], orderby='date:month')

        low_stock = self.env['sd.product'].search_read(
            [('is_low_stock', '=', True)],
            ['name', 'stock_qty', 'reorder_level'], order='stock_qty')

        return {
            'total_sales': total_sales,
            'order_count': order_count,
            'avg_order': total_sales / order_count if order_count else 0.0,
            'low_stock_count': len(low_stock),
            'low_stock': low_stock,
            'top_products': [
                {'name': r['product_id'][1], 'amount': r['amount']}
                for r in by_product],
            'monthly': [
                {'label': r['date:month'], 'amount': r['amount']}
                for r in by_month],
        }

    # ---------- Our own sample data (runs once on install) ----------
    @api.model
    def _seed_data(self):
        if self.search_count([]):
            return
        rnd = random.Random(42)
        customers = self.env['sd.customer'].create([
            {'name': n, 'city': c} for n, c in [
                ('Aarav Traders', 'Mumbai'), ('Kiran Stores', 'Pune'),
                ('Meera Enterprises', 'Delhi'), ('Rohan & Co', 'Bengaluru'),
                ('Sana Retail', 'Hyderabad'), ('Vikram Supplies', 'Chennai'),
            ]])
        products = self.env['sd.product'].create([
            {'name': 'Laptop', 'category': 'electronics', 'unit_price': 55000, 'stock_qty': 8, 'reorder_level': 10},
            {'name': 'Monitor', 'category': 'electronics', 'unit_price': 12000, 'stock_qty': 40, 'reorder_level': 10},
            {'name': 'Keyboard', 'category': 'electronics', 'unit_price': 1500, 'stock_qty': 120, 'reorder_level': 20},
            {'name': 'Office Chair', 'category': 'furniture', 'unit_price': 7500, 'stock_qty': 5, 'reorder_level': 8},
            {'name': 'Standing Desk', 'category': 'furniture', 'unit_price': 18000, 'stock_qty': 22, 'reorder_level': 5},
            {'name': 'Notebook Pack', 'category': 'stationery', 'unit_price': 300, 'stock_qty': 3, 'reorder_level': 50},
            {'name': 'Pen Box', 'category': 'stationery', 'unit_price': 150, 'stock_qty': 300, 'reorder_level': 50},
        ])
        today = fields.Date.today()
        self.create([{
            'date': today - timedelta(days=rnd.randint(0, 180)),
            'customer_id': rnd.choice(customers).id,
            'product_id': rnd.choice(products).id,
            'quantity': rnd.randint(1, 10),
            'state': rnd.choices(['confirmed', 'draft'], [85, 15])[0],
        } for _ in range(400)])