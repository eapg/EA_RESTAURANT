# Kitchen Simulator impl
"""
    This file will be use to implement a kitchen simulator to work will the different orders, that will be manages
    for the differences chef in kitchen, they will manage the orders status while they are working with them. Also
    the implementation of threads will be used to work at the same time with the kitchen an new orders in real time.
"""
from time import sleep
from src.core.ioc import get_ioc_instance
from threading import Thread


class KitchenSimulatorSetup:
    def __init__(self):
        self.instance_ioc_kitchen = get_ioc_instance()


class KitchenSimulator:
    def __init__(self):
        self.kitchen_setup = KitchenSimulatorSetup()

    def kitchen_process(self):
        counter = 0
        while True:

            if counter == 5:
                print("kitchen waiting for orders every 5seg")
                counter = 0

            sleep(1)
            counter += 1


if __name__ == "__main__":

    kitchen_simulator_instance = KitchenSimulator()
    kitchen_thread = Thread(target=kitchen_simulator_instance.kitchen_process)
    kitchen_thread.start()


