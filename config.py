from configparser import ConfigParser


# Возвращает словарь с данными для подключения к БД
def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    database = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            database[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))
    return database
