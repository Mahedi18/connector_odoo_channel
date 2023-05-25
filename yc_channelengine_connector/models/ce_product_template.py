from odoo import api, fields, models


class CEProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"

    name = fields.Char(string="Brand")


class CEProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product template information"

    product_brand_id = fields.Many2one('product.brand', string="Product Brand")
    merchant_product_no = fields.Char(string="Merchant Product Number")
