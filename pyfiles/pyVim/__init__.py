#from pvWrap import *
#from pvFrameBase import *
#from pvExBuffer import *
#from pvExFrame import *
#from pvFramework import *
#
#__all__ = [
#        # pvWrap
#        "pvBuffer",
#        "pvWindow",
#        "pvWinSplitter",
#        "pv_BUF_TYPE_READONLY",
#        "pv_BUF_TYPE_NORMAL",
#        "pv_SPLIT_TYPE_MOST_TOP",
#        "pv_SPLIT_TYPE_MOST_BOTTOM",
#        "pv_SPLIT_TYPE_MOST_RIGHT",
#        "pv_SPLIT_TYPE_MOST_LEFT",
#        "pv_SPLIT_TYPE_CUR_TOP",
#        "pv_SPLIT_TYPE_CUR_BOTTOM",
#        "pv_SPLIT_TYPE_CUR_LEFT",
#        "pv_SPLIT_TYPE_CUR_RIGHT",
#        # pvFrameBase
#        "pvFrame",
#        "pvChildWindow",
#        "pv_FRAME_TYPE_TOP",
#        "pv_FRAME_TYPE_BOTTOM",
#        "pv_FRAME_TYPE_LEFT",
#        "pv_FRAME_TYPE_RIGHT",
#        "pv_FRAME_TYPE_FIXSIZE",
#        "pv_CHILDWIN_TYPE_TOP",
#        "pv_CHILDWIN_TYPE_BOTTOM",
#        "pv_CHILDWIN_TYPE_LEFT",
#        "pv_CHILDWIN_TYPE_RIGHT",
#        # pvExBuffer
#        "pvBufferException",
#        "PTNT_BRANCH",
#        "PTNT_LEEF",
#        "pvTreeNode",
#        "PTB_ADD_FIRST",
#        "PTB_ADD_LAST",
#        "PTB_ADD_ALPHA",
#        "pvTreeBuffer",
#        "pvTabBuffer",
#        # pvExFrame
#        "pvTabFrame",
#        # pvFramework
#        "pvFramework"
#    ]
#
#
import vim
import logging

LOG_FILENAME = 'D:\\log.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


def pvLogDec( func ):
    def ret_func( *argv , **kwdict ):
        logging.debug(argv)
        return func( *argv , **kwdict )
    return ret_func


vim.command = pvLogDec( vim.command )
vim.eval = pvLogDec( vim.eval )

