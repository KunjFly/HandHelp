#region Imports
from pathlib import Path

import log
#endregion Imports


#region Functions
ROOT_PATH = Path().absolute()
INPUT_FOLDER_LST = [ROOT_PATH, "files", "input"]
OUTPUT_FOLDER_LST = [ROOT_PATH, "files", "output"]
#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
	if logger:
		logger.info(f"This module is executing")
else:
	logger.info(f"This module is imported")
#endregion Startup