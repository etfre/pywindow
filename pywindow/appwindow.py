class ApplicationWindow:

    def __init__(self, implementation):
        self._implementation = implementation

    @property
    def title(self):
        return self._implementation.title

    def minimize(self):
        self._implementation.minimize()