from pvWrap import pvBuffer , GenerateRandomName

PV_TREE_NODE_TYPE_BRANCH = 0x01
PV_TREE_NODE_TYPE_LEEF   = 0x02

class pvTreeNode(object):
    def __init__( self , type ):
        self.__type = type

    @property
    def type( self ):
        return self.__type

    def __iter__( self ):
        return self

    def __len__( self ):
        raise NotImplementedError("pvTreeNode::__len__")

    def next( self ):
        raise NotImplementedError("pvTreeNode::next")

    def __str__( self ):
        raise NotImplementedError("pvTreeNode::__iter__")

class pvTreeObserver(object):
    def onBranchOpen( self , path ):
        pass

    def onBranchClose( self , path ):
        pass

    def onLeef( self , path ):
        pass


PV_TREE_ACTION_TYPE_SWITCH = 0x01
PV_TREE_ACTION_TYPE_FOCUS = 0x02
PV_TREE_ACTION_TYPE_UPDATE = 0x04

class pvTreeBuffer(pvBuffer):
    __level_indent = 2
    def __init__( self , root_node ):
        assert root_node
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_TREEBUF_' ) )

        self.__root = root_node
        self.__show_root = False

        self.registerCommand('setlocal nowrap')
        self.registerCommand('setlocal nonumber')
        self.registerCommand('setlocal foldcolumn=0')

        self.__observer_list = []


    def registerObserver( self , ob ):
        self.__observer_list.append( ob )

    def removeObserver( self , ob ):
        try : 
            self.__observer_list.remove( ob )
        except:
            pass

    def OnUpdate( **kwdict ) :
        try :
            action_type = kwdict['type']
        except:
            return

        buffer = kwdict['buffer'] # get vim buffer object
        _format_str = "%(indent)s%(flag)s %(name)s"

        # first open , need to expand the root item
        show_list = []
        if len( buffer ) == 1 && len( buffer[0] ) == 0 :
            for child in self.__root:
                show_list.append( _format_str % {
                        'indent' : '' , 
                        'flag'   : '+' if child.type == PV_TREE_NODE_TYPE_BRANCH else ' '
                        'name'   : str( child ) } )
            root_range = buffer.range(1,1)
            root_range.append( show_list )


