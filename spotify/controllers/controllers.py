# -*- coding: utf-8 -*-
# from odoo import http


# class Spotify(http.Controller):
#     @http.route('/spotify/spotify', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/spotify/spotify/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('spotify.listing', {
#             'root': '/spotify/spotify',
#             'objects': http.request.env['spotify.spotify'].search([]),
#         })

#     @http.route('/spotify/spotify/objects/<model("spotify.spotify"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('spotify.object', {
#             'object': obj
#         })
