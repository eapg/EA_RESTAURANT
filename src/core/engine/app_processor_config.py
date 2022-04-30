class AppProcessorConfig:
    def __init__(
        self,
        id,
        interval,
        on_start=None,
        on_destroy=None,
        before_execute=None,
        after_execute=None,
    ):
        self.id = id
        self.interval = interval
        self.on_start = on_start
        self.on_destroy = on_destroy
        self.before_execute = before_execute
        self.after_execute = after_execute
