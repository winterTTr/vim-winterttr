from pvWrap import pvBuffer , GenerateRandomName , PV_BUF_TYPE_READONLY
from pvUtil import pvString
import re

# type of the node on the tree :
##  branch : for the node can open and close
PV_TREE_NODE_TYPE_BRANCH = 0x01
##  leef   : for the node just a leef for the tree
PV_TREE_NODE_TYPE_LEEF   = 0x02

# type of the action for the OnUpdate
PV_TREE_UPDATE_SELECT = 0x01
PV_TREE_UPDATE_TARGET = 0x02

# type of the action for observer
PV_TREE_OBSERVER_BRANCH_OPEN = 0x01
PV_TREE_OBSERVER_BRANCH_CLOSE = 0x02
PV_TREE_OBSERVER_LEEF_SELECT = 0x03


class pvTreeNode(object):
    def __init__( self , type ):
        self.__type = type

    @property
    def type( self ):
        return self.__type

    @property
    def name( self ):
        return self.OnName()

    def __iter__( self ):
        raise NotImplementedError("pvTreeNode::__iter__")

    def OnName( self ):
        raise NotImplementedError("pvTreeNode::OnName")

class pvTreeNodeFactory( object ):
    def generateNode ( self , path ):
        raise NotImplementedError("pvTreeNodeFactory")

class pvTreeObserver(object):
    def OnUpdate( self , node , action_type ):
        pass


class pvTreeBuffer(pvBuffer):
    __indent_string = '  '
    __format_string = "%(indent)s%(flag)1s %(name)s"
    __format_search_re = re.compile( """
                ^
                (?P<indent>\s*)
                (?P<flag>[-+ ])
                [ ]
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
                            'name'   :  child.name.MultibyteString } )
                self.buffer[ 0 : len( show_list ) ] = show_list

        if not 'type' in kwdict : return

        # run funciton for the type
        { 
                PV_TREE_UPDATE_SELECT : self.__select ,
                PV_TREE_UPDATE_TARGET : self.__target 
        }[ kwdict['type'] ]( kwdict )
          
        
    def __select( self , kwdict ):
        import vim
        line_no = self.__path2LineNo( kwdict['path'] ) \
                if 'path' in kwdict else \
                vim.current.window.cursor[0] - 1

        if line_no == -1 : return

        indent_level , flag , name = self.__getNodeInfo( self.buffer[line_no] )

        # make pvString for the factory
        mbstr_path = self.__lineNo2Path( line_no )
        uni_path = [ pvString() for x in xrange( len( mbstr_path ) ) ]
        for x in xrange( len( mbstr_path ) ):
            uni_path[x].MultibyteString = mbstr_path[x]
        node = self.__node_factory.generateNode( uni_path )


        # open the branch
        if flag == '+': 
            ## 1. fetch the children node
            show_list = []
            for child in node :
                show_list.append( self.__format_string % {
                        'indent' : self.__indent_string * ( indent_level + 1 ), 
                        'flag'   : '+' if child.type == PV_TREE_NODE_TYPE_BRANCH else ' ' ,
                        'name'   :  child.name.MultibyteString } )

            ## 2. make the range object
            range = self.buffer.range( line_no + 1 , line_no + 1 )

            ## 3. append the child
            if show_list : range.append( show_list )

            ## 4. update flag to '-'
            range[0] = self.__format_string % {
                        'indent' : self.__indent_string * indent_level ,
                        'flag'   : '-' ,
                        'name'   :  node.name.MultibyteString } 

            self.__notifyObserver( node , PV_TREE_OBSERVER_BRANCH_OPEN )

        # close the branch
        elif flag == '-': 
            range_start = line_no 
            range_end = line_no
            ## 1. search children range
            total_line_count = len( self.buffer )
            for index in xrange( line_no + 1 , total_line_count ):
                line_info = self.__getNodeInfo( self.buffer[index] )
                if line_info[0] > indent_level :
                    range_end += 1
                    continue
                else:
                    break
            ## 2. make the range object
            vim_range = self.buffer.range( range_start + 1 , range_end + 1 )

            ## 3. delete the child item
            if  range_end - range_start > 0 : del vim_range[1:]

            ## 4. update the flag to '+'
            vim_range[0] = self.__format_string % {
                        'indent' : self.__indent_string * indent_level ,
                        'flag'   : '+' ,
                        'name'   :  node.name.MultibyteString } 

            self.__notifyObserver( node , PV_TREE_OBSERVER_BRANCH_CLOSE )

        # select a leef node
        else:
            self.__notifyObserver( node , PV_TREE_OBSERVER_LEEF_SELECT )

    def __target( self , kwdict ):
        pass

    def __notifyObserver( self , node , observer_type ):
        for ob in self.__observer_list :
            ob.OnUpdate( node , observer_type )

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



        





