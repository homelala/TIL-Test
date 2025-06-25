def indexing(seq, key, value=None):
    def _get_value(item):
        return item if value is None else value(item)

    return {key(item): _get_value(item) for item in seq}