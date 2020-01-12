#region Imports
from inspect import stack
from os import path
from yaml import safe_load # Dependencies: pip install pyyaml

from lib_io import *
import log
#endregion Imports


#region Functions
def loadConfig(fileName="config.yml"):
    """"""
    try:
        filePath = path.join(ROOT_PATH, fileName)
        return safe_load( open(filePath) )
    except Exception as ex:
        logging.error("Exception occurred!", exc_info=True)


def getConfigValues(config=None):
    """"""
    if not config :
        config = loadConfig()
        if not config :
            logger.warn("Input parameter [config] is empty!")
            return None

    # global DB_URL
    # if hasattr(config, "DB_URL"):
    #     DB_URL = config.DB_URL
    # else:
    #     DB_URL = None

    # SITE_URL
    # FILE_TO_BE_PROCESSED

    return config
#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
else:
    logger.info(f"This module is imported")
#endregion Startup