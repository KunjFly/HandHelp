# region Imports
import os
import yaml
import logging
import logging.config
import sys
# endregion Imports


#region Functions
def _setup( default_path='logging.yml',
            default_level=logging.INFO,
            env_key='LOG_CFG'
            ):
    """
        Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        try:
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        except Exception as ex:
            logger.error("Exception occurred!", exc_info=True)
            return None
    else:
        logger.basicConfig(level=default_level)
    return True


def _get(name = None):
    """"""
    try:
        if name:
            return logging.getLogger(name)
            # logger = logging.getLogger(name)
            # return StyleAdapter(logger)
        return logging.getLogger()
        # logger = logging.getLogger()
        # return StyleAdapter(logger)
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return None


def init(name = None):
    """"""
    # logging.setLoggerClass(MyLogger)    # Set overrided Logger
    if not _setup():
        return None
    return _get(name)
# endregion Functions


#region Startup
log = sys.modules[__name__]
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
else:
    logger.info(f"This module is imported")
#endregion Startup