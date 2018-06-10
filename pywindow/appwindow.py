class ApplicationWindow:

    def __init__(self, implementation):
        self._implementation = implementation

    def __getattr__(self, name):
        if name.startswith('_'):
            return getattr(super(), name)
        else:
            return getattr(self._implementation, name)

    def __dir__(self):
        return dir(self._implementation)