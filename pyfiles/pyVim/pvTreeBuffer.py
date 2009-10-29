from pvWrap import pvBuffer , GenerateRandomName , PV_BUF_TYPE_READONLY
import re

PV_TREE_NODE_TYPE_BRANCH = 0x01
PV_TREE_NODE_TYPE_LEEF   = 0x02

class pvTreeNode(object):
    def __init__( self , type ):
        self.__type = type

    @property
    def type( self ):
        return self.__type

    def __iter__( self ):
        raise NotImplementedError("pvTreeNode::__iter__")

    def __str__( self ):
        raise NotImplementedError("pvTreeNode::__iter__")

class pvTreeNodeFactory( object ):
    def generateNode ( self , path ):
        raise NotImplementedError("pvTreeNodeFactory")

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
    __indent_string = '  '
    __format_string = "%(indent)s%(flag)1s%(name)s"
    __format_search_re = re.compile( """
                ^
                (?P<indent>\s*)
                (?P<flag>[-+ ])
                (?P<name>.*)
                $
                """ , re.VERBOSE )


    def __init__( self , node_factory ):
        pvBuffer.__init__( self , PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_TREEBUF_' ) )

        self.__node_factory = node_factory

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

    def OnUpdate( self , **kwdict ) :
        # nothing in the buffer , means the buffer not contain the root
        # children , and maybe the first time of opening the buffer ,
        # need update the root child to the buffer
        if len( self.buffer ) == 1 and len( self.buffer[0] ) == 0 :
            root_node = self.__node_factory.generateNode( [] )
            if root_node.type == PV_TREE_NODE_TYPE_BRANCH:
                show_list = []
                for child in root_node :
                    show_list.append( self.__format_string % {
                            'indent' : '' , 
                            'flag'   : '+' if child.type == PV_TREE_NODE_TYPE_BRANCH else ' ' ,
                            'name'   : str( child ) } )
                self.buffer[ 0 : len( show_list ) ] = show_list

        if not 'type' in kwdict :
            return

        type = kwdict['type']
        if type == PV_TREE_ACTION_TYPE_SWITCH:
            self.__switch( kwdict )
        elif type == PV_TREE_ACTION_TYPE_FOCUS:
            self.__focus( kwdict )
        elif type == PV_TREE_ACTION_TYPE_UPDATE:
            self.__update()
        
    def __switch( self , kwdict ):
        import vim
        #print >> open('D:\\here.txt','a+') , "UPDATE"
        line_no = self.__path2LineNo( kwdict['path'] ) \
                if 'path' in kwdict else \
                vim.current.window.cursor[0] - 1

        if line_no == -1 :
            return

        indent_level , flag , name = self.__getNodeInfo( self.buffer[line_no] )
        if flag == '+': # expand tree
            path = self.__lineNo2Path( line_no )
            node = self.__node_factory.generateNode( path )
            show_list = []
            for child in node :
                show_list.append( self.__format_string % {
                        'indent' : self.__indent_string * ( indent_level + 1 ), 
                        'flag'   : '+' if child.type == PV_TREE_NODE_TYPE_BRANCH else ' ' ,
                        'name'   : str( child ) } )
            #print >> open( 'E:\\log.txt' , 'a+' ) , show_list
            range = self.buffer.range( line_no + 1 , line_no + 1 )
            if show_list : range.append( show_list )
            range[0] = self.__format_string % {
                        'indent' : self.__indent_string * indent_level ,
                        'flag'   : '-' ,
                        'name'   : str( node ) }

    def __focus( self , kwdict ):
        pass

    def __update( self ):
        pass

    def __path2LineNo( self , path ):
        total_line = len( self.buffer )

        line_index = -1 
        for indent_level , path_item in enumerate( path ):
            while True: 
                line_index += 1
                # find all line , but can't find it
                if line_index >= total_line : return -1
                level , flag , name = self.__getNodeInfo( self.buffer[line_index] )

                if level == indent_level and name == path_item : # find it , break to find next level
                    break
                elif level < indent_level : # search begin at another branch , means can't find
                    return -1
                else :
                    # 1 . name not the same
                    # 2 . children level
                    # just continue to find
                    continue
        return line_index

    def __getNodeInfo( self , string ):
        search_result = self.__format_search_re.match( string )
        indent_level = len ( search_result.group('indent') ) / len( self.__indent_string )
        flag = search_result.group('flag')
        name = search_result.group('name')

        return ( indent_level , flag , name )

    def __lineNo2Path( self , line_no ):
        # result for the path list
        return_path = []

        # analyze the current line
        cur_indent_level , flag , name = self.__getNodeInfo( self.buffer[line_no] )
        return_path.insert( 0 , name )

        # search parent
        cur_indent_level -= 1
        while cur_indent_level >= 0 :
            line_no -= 1
            indent_level , flag , name = self.__getNodeInfo( self.buffer[line_no] )
            print >> open( 'E:\\log.txt' , 'a+' ) , indent_level , flag , name

            # children item , just pass
            if indent_level > cur_indent_level :
                continue

            # find the parent 
            if indent_level == cur_indent_level : # find the parent
                cur_indent_level -= 1
                return_path.insert( 0 , name )
                continue

            # if find a parent , before the find level , format error or
            # something else error , should not occured
            if indent_level < cur_indent_level :
                raise

        return return_path



        





