

class Story:
    _yaml_options = dict(default_style=False, default_flow_style=False)

    def __init__(self, base_call, calls=None):
        self.base_call = base_call
        self.calls = calls or []
