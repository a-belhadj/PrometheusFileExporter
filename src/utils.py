from drivers import *  # DO NOT DELETE !


def open_yaml(path):
    from yaml import safe_load, YAMLError
    with open(path, 'r') as stream:
        try:
            yaml_config = safe_load(stream)
        except YAMLError:
            raise YAMLError(f"Error while parsing {path}.")
    return yaml_config


def str_to_class(class_name):
    from sys import modules
    try:
        return getattr(modules[__name__], class_name)
    except AttributeError:
        raise NotImplementedError(f'Error in your config file, "{class_name}" is not a valid driver name.')
