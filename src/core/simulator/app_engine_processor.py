# thread manager
from time import sleep
from threading import Thread
from src.core.simulator.kitchen_simulator import KitchenSimulator

global datetime


class AppEngineProcessThread(Thread):
    def __init__(self, target, target_config):
        super().__init__()
        self.thread_flag = True
        self.target = target
        self.target_config = target_config

    def run(self):

        while self.thread_flag:
            self.target()
            sleep(self.target_config.interval)
            if self.thread_flag is False:
                break


class AppEngineProcessor:
    def __init__(self):
        self.kitchen_simulator = KitchenSimulator()
        self.kitchen_Engine_process_config = AppEngineProcessConfig(5)
        self.kitchen_process = AppEngineProcessThread(
            self.kitchen_simulator.kitchen_process, self.kitchen_Engine_process_config
        )
        self.app_context = AppContext([self.kitchen_process])

    # method to Start thread process
    def start(self):
        self.kitchen_process.start()


class AppEngineProcessConfig:
    def __init__(self, interval):
        self.interval = interval  # Interval Time - This time will determinate How often does the thread run.


class AppContext:
    def __init__(self, *args):
        self.thread_array = args


# function to run the simulation of the AppEngineProcessor()
def app_engine_processor_start():

    app_engine_processor = AppEngineProcessor()
    app_engine_processor.start()


if __name__ == "__main__":
    app_engine_processor_start()
