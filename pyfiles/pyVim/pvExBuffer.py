import vim
import types
from pvWrap import pvBuffer
from pvWrap import GenerateRandomName
from pvWrap import PV_BUF_TYPE_READONLY , PV_BUF_TYPE_NORMAL

class pvListBufferItem(object):
    def __str__( self ):
        raise NotImplementedError("pvListBufferItem::__str__")

    def __eq__( self , other ):
        return str( self ) == str( other )

class pvListBuffer(pvBuffer):
    def __init__( self ):
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_LISTBUF_' ) )
        self.item = []
        self.selection = 0
        self.resize = False
        self.format = "%-20s"
        self.hilight = 'Search'

        self.registerCommand('setlocal nowrap')
        self.registerCommand('setlocal nonumber')
        self.registerCommand('setlocal foldcolumn=0')

    def getItemList( self ):
        return self.item

    def getSelection( self ):
        return self.selection

    def OnUpdate( self , ** kwdict ):
        """
        @brief update the list buffer content according to the member data [self.data]
        @param kwdict 
                      - selection : set the current selection item
                      - resize    : set if resize the window height
                      - format    : use to format the string to show
                      - hilight   : the group name for the hilight
        """

        # get selection and resize
        try:
            self.selection = kwdict['selection']
        except:
            selection = self.selection 

        try:
            self.resize = kwdict['resize']
        except:
            resize = self.resize

        try:
            self.format = kwdict['format']
        except:
            format = self.format

        try:
            self.hilight = kwdict['hilight']
        except:
            hilight = self.hilight

        if self.selection >= len( self.item ):
            self.selection = 0

        # clear the screen
        self.buffer[:] = None

        # deal with internal data
        show_data = []
        for index in xrange( len( self.item ) ):
            show_data.append( format % str( self.item[index] ) )

        # hilight the item
        if len( show_data ) != 0 :
            self.registerCommand('match %s /\V%s/' % ( hilight ,  show_data[self.selection] ) )

        # redraw the content
        self.buffer[0:len(show_data) -1 ] = show_data

        # resize window
        if self.resize : self.registerCommand('resize %d' % len( self.item ) )


PV_TREE_NODE_TYPE_BRANCH = 0x01
PV_TREE_NODE_TYPE_LEEF   = 0x02

class pvTreeNode(object):
    def __init__( self , type ):
        self.__type = type

    @property
    def type( self ):
        return self.__type

    def isOpen( self ):
        raise NotImplementedError("pvTreeNode::isOpen")

    def hasChildren(self):
        raise NotImplementedError("pvTreeNode::hasChildren")

    def expand( self ):
        raise NotImplementedError("pvTreeNode::expand")

    def getChildrenList( self ):
        raise NotImplementedError("pvTreeNode::__iter__")

    def __str__( self ):
        raise NotImplementedError("pvTreeNode::__iter__")

        
class pvTreeBuffer(pvBuffer):
    __level_indent = 2
    def __init__( self ):
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_TREEBUF_' ) )

        self.__root = None
        self.__show_root = False

        self.registerCommand('setlocal nowrap')
        self.registerCommand('setlocal nonumber')
        self.registerCommand('setlocal foldcolumn=0')

    def OnUpdate( **kwdict ) :
        buffer = kwdict['buffer'] # get vim buffer object

        _format_str = "%(indent)s%(flag)1s %(name)s"

        #try :
        #    target = kwdict['target']
        #    assert type(target) == types.ListType
        #except:
        #    return 

        self.__root.expand()
        children_list = self.__root.getChildrenList()
        show_list = []
        for x in children_list:
            if x.hasChildren():
                show_list.append( str(x) )





        


