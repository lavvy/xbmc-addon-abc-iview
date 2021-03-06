#
#  ABC iView XBMC Plugin
#  Copyright (C) 2012 Andy Botting
#
#  This plugin includes from from python-iview
#  Copyright (C) 2009-2012 by Jeremy Visser <jeremy@visser.name>
#
#  This plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this plugin. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import config
import utils
import comm

try:
    import xbmc, xbmcgui, xbmcplugin
except ImportError:
    pass # for PC debugging


def make_programs_list(url):

    try:
        params = utils.get_url(url)
        iview_config = comm.get_config()
        programs = comm.get_series_items(iview_config, params["series_id"])

        ok = True
        for p in programs:
            listitem = xbmcgui.ListItem(label=p.get_list_title(), iconImage=p.get_thumbnail(), thumbnailImage=p.get_thumbnail())
            listitem.setInfo('video', p.get_xbmc_list_item())

            if hasattr(listitem, 'addStreamInfo'):
                listitem.addStreamInfo('audio', p.get_xbmc_audio_stream_info())
                listitem.addStreamInfo('video', p.get_xbmc_video_stream_info())

            # Build the URL for the program, including the list_info
            url = "%s?play=true&%s" % (sys.argv[0], p.make_xbmc_url())

            # Add the program item to the list
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False, totalItems=len(programs))

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=ok)
        xbmcplugin.setContent(handle=int(sys.argv[1]), content='episodes')
    except:
        d = xbmcgui.Dialog()
        msg = utils.dialog_error("Unable to fetch listing")
        d.ok(*msg)
        utils.log_error();
