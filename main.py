# File: main.py

from util import logger, Timer
from fsm import FSM

# Setup logger
def main():
    sys_logger = logger.setup_logger('CoffeeMachine')
    logger.setup_file_logger(sys_logger, 'CoffeeMachine')
    # Log some initial message
    sys_logger.info("Starting the coffee machine system")

    # Use timer
    timer = Timer()
    timer.start()
    # Some long-running task
    timer.wait(1)  # Pauses the execution for 2 seconds
    elapsed_time = timer.elapsed()
    sys_logger.info(f"Task completed in {elapsed_time:.2f} seconds")

    button_ctrlsys = FSM(sys_logger)
    button_ctrlsys.button_func()

if __name__ == "__main__":
    main()
