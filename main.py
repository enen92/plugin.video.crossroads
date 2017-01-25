# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import urlresolver
import requests
import re
import re

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """

    resp = requests.get('https://www.crossroads.net/proxy/content/api/series')
    data = resp.json()['series']
    #for series in data:
        #print('{} {}'.format(series['id'], remove_non_ascii(series['title'])))
    return data

def show_main_menu():
    """
    Create the initial interface for past or live series.
    """
    #Live
    list_item_live = xbmcgui.ListItem(label='Live Streams')
    list_item_live.setInfo('video', {'title': 'Live Streams'})
    url_live = get_url(action='live')
    xbmcplugin.addDirectoryItem(_handle, url_live, list_item_live, True)

    #Historical
    list_item_past = xbmcgui.ListItem(label='Past Series')
    list_item_past.setInfo('video', {'title': 'Past Series'})
    url_past = get_url(action='historical')
    xbmcplugin.addDirectoryItem(_handle, url_past, list_item_past, True)
    xbmcplugin.endOfDirectory(_handle)

def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        #print(category)
        #print(category['image'])
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category['title'])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': category['image']['filename'],
                          'icon': category['image']['filename'],
                          'fanart': category['image']['filename']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video',
                          {'title': category['title'],
                           'trailer': category['trailerLink'],
                           'plot': cleanhtml(category['description']),
                           'dateadded': category['startDate'],
                           'year': category['startDate'][:4]})
        # Create a URL for a plugin recursive call.
        # Example:
        # plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category['messages'])
        # is_folder = True means that this item opens a sub-list of lower level
        # items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore
    # articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(messages):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    print messages
    # Iterate through videos.
    for message in messages:
        # Create a list item with a text label and a thumbnail image.
        print message
        list_item = xbmcgui.ListItem(label=message['title'])
        # Set additional info for the list item.
        list_item.setInfo(
            'video', {'title': message['title'], 'genre': 'message'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        #list_item.setArt({'thumb': video['thumb'], 'icon': video[
        #                 'thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example:
        # plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = get_url(action='play',
                      video="{}{}".format("https://www.youtube.com/watch?v=",
                                          message['messageVideo.serviceId']))
        #url = ''
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore
    # articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=urlresolver.resolve(path))
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        elif params['action'] == 'historical':
            list_categories()
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        show_main_menu()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call
    # paramstring
    router(sys.argv[2][1:])
