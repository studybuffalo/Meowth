import os
import pickle
import logging
import gettext
import json

import utils.spelling as spelling


logger = logging.getLogger("meowth")

def _get_prefix(bot, message):
    guild = message.guild

    try:
        set_prefix = bot.guild_dict[guild.id]['prefix']
    except (KeyError, AttributeError):
        set_prefix = None
    default_prefix = bot.config['default_prefix']

    return set_prefix or default_prefix

def retrieve_server_dict():
    server_dict = {}

    try:
        with open(os.path.join('data', 'serverdict'), 'rb') as fd:
             server_dict = pickle.load(fd)

        logger.info('Serverdict Loaded Successfully')
    except OSError:
        logger.info('Serverdict Not Found - Looking for Backup')

        try:
            with open(os.path.join('data', 'serverdict_backup'), 'rb') as fd:
                server_dict = pickle.load(fd)

            logger.info('Serverdict Backup Loaded Successfully')
        except OSError:
            logger.info('Serverdict Backup Not Found - Creating New Serverdict')

            with open(os.path.join('data', 'serverdict'), 'wb') as fd:
                pickle.dump(server_dict, fd, (- 1))

            logger.info('Serverdict Created')

    return server_dict

def load_config():
    config = {}
    pkmn_info = {}
    type_chart = {}
    type_list = []
    raid_info = {}

    # Load configuration
    with open('config.json', 'r') as fd:
        config = json.load(fd)

    # Set up message catalog access
    language = gettext.translation(
        'meowth', localedir='locale', languages=[config['bot-language']]
    )
    language.install()

    pokemon_language = [config['pokemon-language']]
    pokemon_path_source = os.path.join(
        'locale', '{0}', 'pkmn.json'
    ).format(config['pokemon-language'])

    # Load Pokemon list
    with open(pokemon_path_source, 'r') as fd:
        pkmn_info = json.load(fd)

    # Load Raid Info
    with open(os.path.join('data', 'raid_info.json'), 'r') as fd:
        raid_info = json.load(fd)

    # Load type information
    with open(os.path.join('data', 'type_chart.json'), 'r') as fd:
        type_chart = json.load(fd)

    with open(os.path.join('data', 'type_list.json'), 'r') as fd:
        type_list = json.load(fd)

    # Set spelling dictionary to our list of Pokemon
    spelling.set_dictionary(pkmn_info['pokemon_list'])

    return {
        "config": config,
        "pkmn_info": pkmn_info,
        "type_chart": type_chart,
        "type_list": type_list,
        "raid_info": raid_info,
    }