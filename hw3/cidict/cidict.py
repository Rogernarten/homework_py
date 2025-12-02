# write your CIDict here
class CIDict(dict):
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in dict(**kwargs).items():
            self[k] = v

    def __setitem__(self, key, value):
        key = key.lower() if isinstance(key,str) else key
        super().__setitem__(key,value)

    def __getitem__(self, item):
        item = item.lower() if isinstance(item, str) else item
        return super().__getitem__(item)

    def __delitem__(self, key):
        key = key.lower() if isinstance(key, str) else key
        super().__delitem__(key)

    def update_all(self, fun):
        for k, v in self.items():
            self[k] = fun(v)


