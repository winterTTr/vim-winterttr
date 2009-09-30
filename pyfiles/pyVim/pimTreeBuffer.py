from pimWrap import *


class pimBufferException(Exception):
    pass
    
class pimBufferW(pimBuffer):
    def __init__( self , type , name , baseWin ):
        pimBuffer.__init__( self , type , name )
        self._basewin = baseWin
        
    def showBuffer( self ):
        pimBuffer.showBuffer( self , self._basewin )

PTNT_BRANCH     = 0 
PTNT_LEEF       = 1 

class pimTreeNode:
    def __init__( self , nodeType , id , parentNode = None ):
        self._nodeType = nodeType
        self._id = id
        self._parentNode = parentNode
        self._indentLevel = 0

        if nodeType == PTNT_BRANCH:
            self._child = []
            self.addChildNode = self._addChildNode
            self.searchNode = self._searchNode
            self.deleteNode = self._deleteNode

    def getNodeType( self ):
        return self._nodeType

    def getID(self):
        return self._id

    def _addChildNode(self , node ):
        if self.searchNode( node.getID() )[0] != -1:
            return False
        self._child.append( node )
        node._parentNode = self
        return True

    def _searchNode( self , nodeID ):
        for index , child in enumerate( self._child ):
            if child._id == nodeID:
                return index , child
        return -1 , None

    def _deleteNode( self , nodeID ):
        index , removechild = self.searchNode( nodeID )
        if index == -1 :
            return None
        del self._child[index]
        return removechild


    def getParentNode( self ):
        return self._parentNode


PTB_ADD_FIRST = 0
PTB_ADD_LAST  = 1
PTB_ADD_ALPHA = 2

class pimTreeBuffer(pimBuffer):
    def __init__( self , name = None ):
        if name == None :
            name = CreateRandomName( 'PIM.TREE.BUF' )

        # pimBufferW.__init__( self , PIM_BUF_TYPE_READONLY , name , basewin)
        pimBuffer.__init__( self , PIM_BUF_TYPE_READONLY , name )
        self._headerIndex = -1 
        self._data = []

        NoneDec = lambda x:x
        import os
        self._nodeDec = NoneDec
        self._nodeUnDec = NoneDec
        self._leafDecorator = NoneDec
        self._leafUnDecorator = NoneDec

        self._pathSplitter = os.path.split

    def addNode( self  , basepath , node , pos ):
        if basepath == None or basepath == "":
            if len(self._data) == 0 :
                self._data.append( node )
                node._indentLevel = 0 
                return True
        else:
            index = self.searchNode( basepath )
            if index == -1 :
                return False
            self._addChild( index , node , pos )
            return True

    def _addChild( self , parentIndex , node , pos ):
        if pos == PTB_ADD_FIRST:
            self._data = None


    def searchNode( self , path ):
        if path == None or path == "":
            return -1

        if path[-1] == '/':
            fullpath = path[:-1]
        else:
            fullpath = path

        lineIndex = self._headerIndex + 1
        indentLevel = 0

        while True :
            basepath , fullpath = self.splitFromBegin( fullpath )
            while True:
                if lineIndex > len( self._data ) - 1:
                    return -1

                curLine = self._data[lineIndex]
                if curLine._indentLevel > indentLevel :
                    # next level , just jump
                    lineIndex += 1
                    continue
                elif curLine._indentLevel < indentLevel:
                    # can not find
                    return -1

                if curLine._id == basepath:
                    if fullpath == "":
                        return index
                    else:
                        indentLevel += 1
                        lineIndex += 1
                        break
                else:
                    lineIndex += 1
                    continue


    def splitFromBegin( self , path ):
        pos =  path.find('/')
        if pos == -1:
            return path , ""
        else:
            return path[:pos] , path[pos+1:]


        
    #def nodeDecorator( self , nodeName ):
    #    return '['+nodeName+']'

    #def nodeUnDecorator( self , nodeName ):
    #    import re
    #    matchRet = re.match('\[(?P<name>.*)\]' , nodeName )
    #    if matchRet == None:
    #        raise pimBufferException('invalid node name')
    #    return matchRet.group('name')

    def addNode( self ):
        pass


class pimTabBuffer( pimBuffer ):

    def __init__( self , name = None ):
        if name == None :
            name = CreateRandomName( 'PIM.TAB.BUF' )
            
        pimBuffer.__init__( self , PIM_BUF_TYPE_READONLY , name )
    
    def OnUpdate(self , ** kwdict ):
            
        if not kwdict.has_key('namelist') or not kwdict.has_key('selected'):
            return
            
        import types
        if type(kwdict['namelist']) != types.ListType :
            return False
        
        formatSel = [ "<%s> " , "|%s| " ]
        showStr = ""
        for index , name in enumerate( kwdict['namelist'] ): 
            showStr += formatSel[ int( index == kwdict['selected'] ) ] % name
            
        self._buffer[:] = None
        self._buffer[0] = showStr

