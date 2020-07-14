import os
import logging
import json

logger = logging.getLogger(__name__)

__pluginViewsList = 'viewsList.json'
__pluginViewListFilePath = os.path.join(os.path.dirname(__file__), __pluginViewsList)

try:
    with open(__pluginViewListFilePath, 'r') as vlFile:
        __availableViews = json.load(vlFile)
except json.JSONDecodeError as e:
    __availableViews = {}
    logger.warning('No valid json format! - Exception: %s', e)
except IOError:
    __availableViews = {}
    logger.warning('No available view list found!')

def getContexts():
    return tuple(__availableViews.keys())

def getViews(context :str = 'default'):
    return tuple(__availableViews[context])

def getViewsDict():
    return __availableViews
