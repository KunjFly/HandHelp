# region Startup
if __name__ == "__main__":
    print("Module executed as main")
else:
    print("Module [{0}] imported".format(__name__))
# endregion Startup


# region Imports
import lib
# endregion Imports


# region MainCode
def main():

    lib.log("[Start script]")
    
    lib.deleteContentOfFolder(lib.OUTPUT_FOLDER_LST)

    fileName = "test-10-chunks.html"

    # read file
    linesLst = lib.readFileAsLinesLst(fileName)

    # get chunks
    chunksLst = lib.linesLstToChunksLst(linesLst)

    # write chunks to file
    lib.writeToFiles(chunksLst, filePath=lib.OUTPUT_FOLDER_LST)

    lib.log("[End script]")


main()
# endregion MainCode
