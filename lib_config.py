#region Imports
from inspect import stack
from os import path
from yaml import safe_load          # !!!!! pip install pyyaml

from lib_consts import *
from lib_io import *
#endregion Imports


#region MainCode
##############################
#	Config
##############################

def loadConfig(fileName="config.yml"):
    funcName = stack()[0][3]
    try:
        filePath = path.join(ROOT_PATH, fileName)
        return safe_load( open(filePath) )
    except Exception as ex:
        errF("Error in function [{}]. Exception: [{}].", funcName, ex)


def getConfigValues(config=None):
    funcName = stack()[0][3]

    if not config :
        config = loadConfig()
        if not config :
            warnF("Warning in function [{}]: Config is Empty", funcName)
            return None

    # global DB_URL
    # if hasattr(config, "DB_URL"):
    #     DB_URL = config.DB_URL
    # else:
    #     DB_URL = None

    # SITE_URL
    # FILE_TO_BE_PROCESSED

    return config
#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup