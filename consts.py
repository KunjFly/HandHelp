#region Imports
from pathlib import Path
import log
#endregion Imports


#region MainCode
ROOT_PATH = Path().absolute()
INPUT_FOLDER_LST = [ROOT_PATH, "files", "input"]
OUTPUT_FOLDER_LST = [ROOT_PATH, "files", "output"]

def main_consts(): # Test
    """"""
#endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main_consts()
else:
    logger.info(f"This module is imported")
#endregion Startup