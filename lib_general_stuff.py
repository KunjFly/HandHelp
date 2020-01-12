#region Imports
from inspect import stack
import time

import log
#endregion Imports


#region MainCode
def getNowTS(): # Get now timestamp w/ milliseconds
    """"""
    return time.time() * 1000

def main_general_stuff(): # Test
    """"""
#endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main_general_stuff()
else:
    logger.info(f"This module is imported")
#endregion Startup