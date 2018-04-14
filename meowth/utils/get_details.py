
def get_type(guild, pkmn_number):
    pkmn_number = int(pkmn_number) - 1
    types = type_list[pkmn_number]
    ret = []
    for type in types:
        ret.append(parse_emoji(guild, config['type_id_dict'][type.lower()]))
    return ret

def get_name(pkmn_number):
    pkmn_number = int(pkmn_number) - 1
    name = pkmn_info['pokemon_list'][pkmn_number].capitalize()
    return name

def get_number(pkm_name):
    number = pkmn_info['pokemon_list'].index(pkm_name) + 1
    return number

def get_level(pkmn):
    if str(pkmn).isdigit():
        pkmn_number = pkmn
    elif (not str(pkmn).isdigit()):
        pkmn_number = get_number(pkmn)
    for level in raid_info['raid_eggs']:
        for pokemon in raid_info['raid_eggs'][level]['pokemon']:
            if pokemon == pkmn_number:
                return level

def get_raidlist():
    raidlist = []
    for level in raid_info['raid_eggs']:
        for pokemon in raid_info['raid_eggs'][level]['pokemon']:
            raidlist.append(pokemon)
            raidlist.append(get_name(pokemon).lower())
    return raidlist

def get_weaknesses(species):
    """Returns a list of weaknesses for the specified pokemon"""
    # Get the Pokemon's number
    number = pkmn_info['pokemon_list'].index(species)
    # Look up its type
    pk_type = type_list[number]

    # Calculate sum of its weaknesses
    # and resistances.
    # -2 == immune
    # -1 == NVE
    #  0 == neutral
    #  1 == SE
    #  2 == double SE
    type_eff = {}
    for type in pk_type:
        for atk_type in type_chart[type]:
            if atk_type not in type_eff:
                type_eff[atk_type] = 0
            type_eff[atk_type] += type_chart[type][atk_type]
    ret = []
    for (type, effectiveness) in sorted(type_eff.items(), key=(lambda x: x[1]), reverse=True):
        if effectiveness == 1:
            ret.append(type.lower())
        elif effectiveness == 2:
            ret.append(type.lower() + 'x2')
    return ret

def weakness_to_str(guild, weak_list):
    """Return type IDs for a list of weaknesses"""
    ret = ''
    for weakness in weak_list:

        x2 = ''
        if weakness[(- 2):] == 'x2':
            weakness = weakness[:(- 2)]
            x2 = 'x2'
        # Append to string
        ret += (parse_emoji(guild,
                config['type_id_dict'][weakness]) + x2) + ' '
    return ret