commands = {}


def command(name, aliases=[]):
    def decorator(func):
        commands[name] = func
        if len(aliases) > 0:
            for a in aliases:
                commands[a] = func
        return func


    return decorator
