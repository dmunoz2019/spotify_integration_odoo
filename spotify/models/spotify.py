# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
# logs 
import logging
_logger = logging.getLogger(__name__)
import base64


class SpotifyAPI(models.AbstractModel):
    _name = 'spotify.api'
    _description = 'Spotify API Integration'

    # Método para obtener el token de la API de Spotify
    def get_spotify_token(self):
        client_id = self.env['ir.config_parameter'].sudo().get_param('spotify.client_id')
        client_secret = self.env['ir.config_parameter'].sudo().get_param('spotify.client_secret')
        _logger.info('Estamos en el modelo abstracto')
        _logger.info(client_id)
        _logger.info(client_secret)
        # Asegúrate de utilizar el ID de cliente y el secreto de cliente correctos
        if not client_id or not client_secret:
            return UserWarning(_('Please configure Spotify Client ID and Client Secret.'))
    
        # Asegúrate de utilizar la URL correcta para obtener el token de Spotify
        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'client_credentials'
        }
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
        }

        # lets do a try catch to see if we get the token from spotify.api

        try:
            response = requests.post(token_url, data=data, headers=headers)
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                return _logger.info(response.status_code)
        except Exception as e:
            _logger.info(e)
            return None

     
    # # Método para hacer consultas a la API de Spotify
    def query_spotify(self, endpoint, params=None, method='GET'):
        base_url = 'https://api.spotify.com/v1/'
        token = self.get_spotify_token()
        if not token:


            return None

        headers = {
            'Authorization': f'Bearer {token}'
        }

        url = base_url + endpoint

        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        else:
            # Añadir otros métodos según sea necesario (POST, PUT, DELETE)
            response = None

        if response and response.status_code == 200:
            return response.json()
        else:
            # Manejar errores o excepciones según sea necesario
            return None
    

class SpotifyRecommendation(models.Model):
    _name = 'spotify.recommendation'
    _description = 'Spotify Recommendation'

    # this model is going to be used to store the recommendations that we get from spotify.api all the fields are going to be readonly it should be computed once the partner select the musical genre

    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    artist = fields.Char(string='Artist', readonly=True)
    track = fields.Char(string='Track', readonly=True)
    album = fields.Char(string='Album', readonly=True)
    url = fields.Char(string='URL', readonly=True)

    # lets create a method that depends on the musical_genre field of the partner model and that is going to be used to get the recommendations from spotify.api

    # @api.depends('partner_id.musical_genre')
    # def get_recommendations(self):

class SpotifyGenre(models.Model):
    _name = 'spotify.genre'
    _description = 'Spotify Genre'
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    # this model is going to be used to store the musical genres that we are going to use to get the recommendations from spotify.api
    name = fields.Char(string='Name', readonly=True)
    # lets init the model with the musical genres that we are going to use to get the recommendations from spotify.api
    # using spotify.api
    
    # inicializamos con generos musicale obtenidos de spotify.api solo una vez
    @api.model
    def init(self):
        # lets log get_spotify_token result to see if it works from spotify.api
        token = self.env['spotify.api'].get_spotify_token()
        _logger.info('Este es el token')
        _logger.info(token)
        # lets get the musical genres from spotify.api
        genres = self.env['spotify.api'].query_spotify('recommendations/available-genre-seeds')
        _logger.info('Estos son los generos')
        _logger.info(genres)
        # lets create the musical genres in the model
        for genre in genres['genres']:
            self.env['spotify.genre'].create({
                'name': genre
            })

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # lets add a new field to the res.partner model that has the musical genre of the partner that we are going to use to get recommendations from spotify.api

    genre_ids = fields.One2many('spotify.genre','partner_id', string='Genres')

    # lets add a field to get the recommendations from spotify.api based on the genre of the partner when the field musical_genre is changed it should work on a one2many field

    recommendations = fields.One2many('spotify.recommendation', 'partner_id', string='Recommendations')

    @api.onchange('genre_ids')
    def get_recommendations(self):
        # lets log get_spotify_token result to see if it works from spotify.api
        token = self.env['spotify.api'].get_spotify_token()
        _logger.info('Este es el token')
        _logger.info(token)
       