class KeyFormater:
    """
    For creating a key for Redis storage
    """

    def __init__(self, template: str):
        self.template = template

    def build_key(self, **kwargs) -> str:
        return self.template.format(**kwargs)
