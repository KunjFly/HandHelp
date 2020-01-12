# region Imports
import os
import yaml
import logging
import logging.config
import sys
# endregion Imports


##### Extend funcs .info(), .warn(), ...
#  Nice try 1. Workz only w/ placeholders like {} and {0}. But havn't ability to pass one argument
""" 
class BraceString(str):
    def __mod__(self, other):
        return self.format(*other)
    def __str__(self):
        return self


class StyleAdapter(logging.LoggerAdapter):

    def __init__(self, logger, extra=None):
        super(StyleAdapter, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        if kwargs.pop('style', "%") == "{":  # optional
            msg = BraceString(msg)
        return msg, kwargs
 """
# logger.info("knights:{0}", "ni", style="{")         # Example 2
# logger.info("knights:{}", "shrubbery", style="{")   # Example 2


#  Nice try 2 (not workz)
""" 
class MyLogger(logging.Logger):
    """"""
    def __init__(self, name, level = logging.NOTSET):
        return super(MyLogger, self).__init__(name, level)        

    def warning(self, msg, *args, **kwargs):
        return super(MyLogger, self).warning(msg, *args, **kwargs)
 """


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
            logging.error("Exception occurred!", exc_info=True)
            return None
    else:
        logging.basicConfig(level=default_level)
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
        logging.error("Exception occurred!", exc_info=True)
        return None


def init(name = None):
    """"""
    # logging.setLoggerClass(MyLogger)    # Set overrided Logger
    if not _setup():
        return None
    return _get(name)
#endregion Functions


# region MainCode
def main_log():
    """"""
    if not logger:
        return
    
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
# endregion MainCode


#region Startup
log = sys.modules[__name__]
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main_log()
else:
    logger.info(f"This module is imported")
#endregion Startup