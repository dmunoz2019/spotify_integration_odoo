# -*- coding: utf-8 -*-
{
    'name': "spotify",

    'summary': """
        """,

    'description': """
    """,

    'author': "Diego Munoz",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml'
        ,
        'views/spotify.xml',
        'views/res_partner.xml',
    ],
}
