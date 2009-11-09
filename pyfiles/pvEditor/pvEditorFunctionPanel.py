import os
import string

from pyVim.pvUtil import pvString
from pyVim.pvListBuffer import pvListBuffer
from pyVim.pvTreeBuffer import pvTreeBuffer , pvTreeNode , pvTreeNodeFactory , pvTreeObserver
from pyVim.pvTreeBuffer import PV_TREE_NODE_TYPE_BRANCH , PV_TREE_NODE_TYPE_LEEF

from pvEditorTabPanel import pvEditorTabPanelItem




class pvEditorPanel_ContextComplete( pvEditorTabPanelItem ):
    def __init__( self ):
        self.buffer = pvListBuffer()

    def getBuffer( self ):
        return self.buffer

    def DoName( self ):
        str = pvString()
        str.UnicodeString = u'Context Complete'
        return str


class pvEditorPanel_BufferExplorer( pvEditorTabPanelItem ):
    def __init__( self ):
        self.buffer = pvListBuffer()

    def getBuffer( self ):
        return self.buffer

    def DoName( self ):
        str = pvString()
        str.UnicodeString = u'Buffer Explorer'
        return str


class FENodeRoot( pvTreeNode ):
    def __init__( self ):
        super( FENodeRoot , self ).__init__( PV_TREE_NODE_TYPE_BRANCH )

    def __iter__( self ):
        for x in string.ascii_uppercase :
            driver_path = u'%s:\\' % x
            if os.path.isdir( driver_path ):
                yield FENodeDirectory( driver_path )

    def OnName( self ):
        return pvString()

class FENodeDirectory( pvTreeNode ):
    def __init__( self , path ):
        super( FENodeDirectory , self ).__init__( PV_TREE_NODE_TYPE_BRANCH )
        self.path = path

    def __iter__( self ):
        for x in os.listdir( self.path ):
            full_path = os.path.join( self.path , x )
            if os.path.isdir( full_path ):
                yield FENodeDirectory( full_path )
            else:
                yield FENodeFile( full_path )

    def OnName( self ):
        name = os.path.basename( self.path )

        ret = pvString()
        ret.UnicodeString = self.path if name == u'' else name
        return ret

class FENodeFile( pvTreeNode ):
    def __init__( self , path ):
        super( FENodeFile , self ).__init__( PV_TREE_NODE_TYPE_LEEF )
        self.path = path

    def OnName( self ):
        name = pvString()
        name.UnicodeString = os.path.basename( self.path)
        return name



class pvEditorFileExplorer_NodeFactory( pvTreeNodeFactory ):
    def generateNode( self , path ):
        if path == [] :
            return FENodeRoot()
        else:
            uni_path = [ x.UnicodeString for x in path ]
            full_path = os.path.join( *uni_path )
            if os.path.isdir( full_path ):
                return FENodeDirectory( full_path )
            elif os.path.isfile( full_path ):
                return FENodeFile( full_path )
            else :
                return None

class pvEditorDirectoryObserver( pvTreeObserver ):
    def OnUpdate( self , node , type ):
        print node , type


class pvEditorPanel_FileExplorer( pvEditorTabPanelItem ):
    def __init__( self ):
        self.buffer = pvTreeBuffer( pvEditorFileExplorer_NodeFactory() )
        self.buffer.registerObserver( pvEditorDirectoryObserver() )

    def getBuffer( self ):
        return self.buffer

    def DoName( self ):
        str = pvString()
        str.UnicodeString = u'File Explorer'
        return str

