# -*- coding: utf-8 -*-
from odoo import http

# class StockInspection(http.Controller):
#     @http.route('/stock_inspection/stock_inspection/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_inspection/stock_inspection/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_inspection.listing', {
#             'root': '/stock_inspection/stock_inspection',
#             'objects': http.request.env['stock_inspection.stock_inspection'].search([]),
#         })

#     @http.route('/stock_inspection/stock_inspection/objects/<model("stock_inspection.stock_inspection"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_inspection.object', {
#             'object': obj
#         })