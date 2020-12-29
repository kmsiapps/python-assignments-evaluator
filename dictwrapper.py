class DictWrapper:
    '''
    Wrapper class to enable JS style dictonary access.
    '''
    def __init__(self, target):
        if not isinstance(target, dict):
            raise TypeError("Target should be dictionary")
        self.inner = self.convert(target)
    
    def convert(self, target):
        if isinstance(target, dict):
            for key, value in target.items():
                if isinstance(value, dict):
                    target[key] = DictWrapper(target[key])
        elif isinstance(target, (list, tuple)):
            for i, item in enumerate(target):
                if isinstance(item, dict):
                    target[i] = DictWrapper(item)
        return target
    
    def __getattr__(self, name):
        if name not in self.inner:
            raise NameError(f"{name} not in dictionary")
        return self.inner[name]
