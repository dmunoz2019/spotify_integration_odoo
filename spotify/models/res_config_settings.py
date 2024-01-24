from odoo import api, exceptions, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    #  el parametro config_parameter es el nombre del parametro que se va a guardar en la base de datos
    #  y que se va a usar para recuperar el valor de la configuracion
    spotify_client_id = fields.Char(string='Client ID', config_parameter='spotify.client_id')
    spotify_client_secret = fields.Char(string='Client Secret', config_parameter='spotify.client_secret')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            spotify_client_id=self.env['ir.config_parameter'].sudo().get_param('spotify.client_id'),
            spotify_client_secret=self.env['ir.config_parameter'].sudo().get_param('spotify.client_secret'),
        )
        return res