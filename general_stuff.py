#region Imports
from inspect import stack
import time
import re

import log
#endregion Imports


#region Functions
def getNowTS(): # Get now timestamp w/ milliseconds
	""""""
	return time.time() * 1000


# Remove all HTML tags
# https://stackoverflow.com/questions/822452/strip-html-from-text-javascript
def removeHtmlTags(str_in, regExpStr=r"<[^>]*>?", flags=None):
	""""""
	result	= ""
	if flags is None:
		result = re.sub(regExpStr, "", str_in)
	else:
		result = re.sub(regExpStr, "", str_in, flags=flags)

	if result == '':
		return str_in
	return result
	
#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
	if logger:
		logger.info(f"This module is executing")
else:
	logger.info(f"This module is imported")
#endregion Startup