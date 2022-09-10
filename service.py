class Service():

    @staticmethod
    def get_filter(iter_object, value):
        return filter(lambda x: value in x, iter_object)

    @staticmethod
    def get_map(iter_object, value):
        return map(lambda x: x.split()[int(value)], iter_object)

    @staticmethod
    def get_unique(iter_object):
        return set(iter_object)

    @staticmethod
    def get_sort(iter_object, value):
        return sorted(iter_object, reverse=True if value == "desc" else False)

    @staticmethod
    def get_limit(iter_object, value):
        return list(iter_object)[:int(value)]
