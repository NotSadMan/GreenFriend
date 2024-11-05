import configparser


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    return {'bot': config['bot_data'],
            'db': config['db']}

