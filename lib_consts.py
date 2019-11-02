#region Imports
from pathlib import Path
#endregion Imports


#region MainCode
ROOT_PATH = Path().absolute()
INPUT_FOLDER_LST = [ROOT_PATH, "files", "input"]
OUTPUT_FOLDER_LST = [ROOT_PATH, "files", "output"]
#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup