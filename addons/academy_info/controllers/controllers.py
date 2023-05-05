# -*- coding: utf-8 -*-
# from odoo import http


# class AcademyInfo(http.Controller):
#     @http.route('/academy_info/academy_info/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/academy_info/academy_info/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('academy_info.listing', {
#             'root': '/academy_info/academy_info',
#             'objects': http.request.env['academy_info.academy_info'].search([]),
#         })

#     @http.route('/academy_info/academy_info/objects/<model("academy_info.academy_info"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('academy_info.object', {
#             'object': obj
#         })
