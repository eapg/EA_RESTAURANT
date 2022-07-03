import time
from abc import abstractmethod
from datetime import datetime
from threading import Thread


class AbstractProcessor(Thread):
    def __init__(self, app_processor_config, app_context=None):
        Thread.__init__(self)
        self.app_processor_config = app_processor_config
        self.app_context = app_context
        self.paused = False
        self.destroyed = False
        self.last_execution_time = datetime.now().timestamp()

    @abstractmethod
    def process(self, delta_time):
        pass

    def run(self):
        if self.app_processor_config.on_start:
            self.app_processor_config.on_start(
                self.app_processor_config, self.app_context
            )

        while not self.destroyed:
            if not self.paused:
                if self.app_processor_config.before_execute:
                    self.app_processor_config.before_execute(
                        self.app_processor_config, self.app_context
                    )

                current_time = datetime.now().timestamp()
                delta_time = current_time - self.last_execution_time

                self.process(delta_time)

                self.last_execution_time = current_time

                if self.app_processor_config.after_execute:
                    self.app_processor_config.after_execute(
                        self.app_processor_config, self.app_context
                    )

                time.sleep(self.app_processor_config.interval)

        if self.app_processor_config.on_destroy:
            self.app_processor_config.on_destroy(
                self.app_processor_config, self.app_context
            )
