#region Imports
from inspect import stack
import time

import log
#endregion Imports


#region Functions
def getNowTS(): # Get now timestamp w/ milliseconds
    """"""
    return time.time() * 1000
#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
else:
    logger.info(f"This module is imported")
#endregion Startup