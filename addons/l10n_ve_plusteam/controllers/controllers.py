# -*- coding: utf-8 -*-
# from odoo import http


# class L10nVePlusteam(http.Controller):
#     @http.route('/l10n_ve_plusteam/l10n_ve_plusteam/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_ve_plusteam/l10n_ve_plusteam/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_ve_plusteam.listing', {
#             'root': '/l10n_ve_plusteam/l10n_ve_plusteam',
#             'objects': http.request.env['l10n_ve_plusteam.l10n_ve_plusteam'].search([]),
#         })

#     @http.route('/l10n_ve_plusteam/l10n_ve_plusteam/objects/<model("l10n_ve_plusteam.l10n_ve_plusteam"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_ve_plusteam.object', {
#             'object': obj
#         })
