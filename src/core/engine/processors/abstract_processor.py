
import time
from abc import abstractmethod
from datetime import datetime
from threading import Thread


class AbstractProcessor(Thread):
    def __init__(self, app_processor_config=None, app_context=None):
        Thread.__init__(self)
        self.app_processor_config = app_processor_config
        self.app_context = app_context
        self.pause = False
        self.destroy = False
        self.last_execution_time = datetime.now()
        self.delta_time = 0

    @abstractmethod
    def process(self, delta_time):
        pass

    def run(self):
        if self.app_processor_config.on_start:
            self.app_processor_config.on_start()

        while not self.destroy:
            if not self.pause:
                if self.app_processor_config.on_execute:
                    self.app_processor_config.on_execute()

                self.delta_time = datetime.now() - self.last_execution_time

                self.process(self.delta_time)

                self.last_execution_time = datetime.now()

                time.sleep(self.app_processor_config.interval)

        if self.app_processor_config.on_destroy:
            self.app_processor_config.on_destroy()
