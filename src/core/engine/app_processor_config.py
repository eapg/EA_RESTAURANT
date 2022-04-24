class AppProcessorConfig:
    def __init__(
        self, id=None, interval=None, on_start=None, on_destroy=None, on_execute=None
    ):
        self.id = id
        self.interval = interval
        self.on_start = on_start
        self.on_destroy = on_destroy
        self.on_execute = on_execute
