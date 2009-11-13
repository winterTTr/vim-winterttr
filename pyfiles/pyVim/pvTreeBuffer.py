from pvWrap import pvBuffer , GenerateRandomName , PV_BUF_TYPE_READONLY
from pvUtil import pvString

from pvKeyMap import pvKeyMapManager , pvKeyMapEvent , pvKeyMapObserver
from pvKeyMap import PV_KM_MODE_NORMAL

import re
import vim

# type of the node on the tree :
##  branch : for the node can open and close
PV_TREE_NODE_TYPE_BRANCH = 0x01
##  leef   : for the node just a leef for the tree
PV_TREE_NODE_TYPE_LEEF   = 0x02

# type of the action for the OnUpdate
PV_TREE_UPDATE_SELECT = 0x01
PV_TREE_UPDATE_TARGET = 0x02


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
    def OnBranchOpen( self , node ):
        raise NotImplementedError("pvTreeObserver::OnBranchOpen")

    def OnBranchClose( self , node ):
        raise NotImplementedError("pvTreeObserver::OnBranchClose")

    def OnLeefSelect( self , node ):
        raise NotImplementedError("pvTreeObserver::OnLeefSelect")


class pvTreeBuffer(pvBuffer , pvKeyMapObserver):
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
        super( pvTreeBuffer , self ).__init__( PV_BUF_TYPE_READONLY , GenerateRandomName( 'PV_TREEBUF_' ) )

        self.__node_factory = node_factory

        self.registerCommand('setlocal nowrap')
        self.registerCommand('setlocal nonumber')
        self.registerCommand('setlocal foldcolumn=0')

        # double click
        db_click_event = pvKeyMapEvent( '<2-LeftMouse>' , PV_KM_MODE_NORMAL , self )
        pvKeyMapManager.registerObserver( db_click_event , self )
        # enter 
        enter_event = pvKeyMapEvent( '<Enter>' , PV_KM_MODE_NORMAL , self )
        pvKeyMapManager.registerObserver( enter_event , self )

        self.__observer_list = []


    def registerObserver( self , ob ):
        self.__observer_list.append( ob )

    def removeObserver( self , ob ):
        try : 
            self.__observer_list.remove( ob )
        except:
            pass

    def OnHandleKeyEvent( self , **kwdict ):
        # key : <2-LeftMouse> OR <Enter>
        self.updateBuffer( type = PV_TREE_UPDATE_SELECT )

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
        # retrieve the line_no for the path
        if 'target' in kwdict:
            path = [ x.MultibyteString for x in kwdict['path'] ]
            line_no = self.__path2LineNo( path )
        else:
            line_no = vim.current.window.cursor[0] - 1
        if line_no == -1 : return

        node_indent , node_flag , node_name = self.__getNodeInfo( line_no )
        {
                '+' : self.__openItem ,
                '-' : self.__closeItem ,
                ' ' : self.__openItem
        } [ node_flag ]( line_no )


    def __target( self , kwdict ):
        # check the target path should exist
        if not 'target' in kwdict : return

        # check for the min exist path
        open_path = [ x.MultibyteString for x in kwdict['target'] ]
        close_path = []
        line_no = -1

        while True:
            # nothing to find
            if open_path == [] : break

            # find the line
            line_no = self.__path2LineNo( open_path )

            if line_no == -1 : # not find
                close_path.insert( 0 , open_path.pop() )
            else: 
                break

        # not find event on the root path, must be something wrong
        if line_no == -1 : return

        line_no = self.__path2LineNo( open_path )
        self.__openItem( line_no )
        while close_path :
            open_path.append( close_path.pop(0) )
            line_no = self.__path2LineNo( open_path )
            if line_no == -1 : return
            self.__openItem( line_no )

    def __openItem( self , line_no ):
        node_indent , node_flag , node_name = self.__getNodeInfo( line_no )
        # make pvString for the factory
        node = self.__node_factory.generateNode( 
                [ pvString( MultibyteString = x ) for x in self.__lineNo2Path( line_no ) ] )

        if node_flag == '+':
            ## 1. fetch the children node
            show_list = []
            for child in node :
                show_list.append( self.__format_string % {
                        'indent' : self.__indent_string * ( node_indent + 1 ), 
                        'flag'   : '+' if child.type == PV_TREE_NODE_TYPE_BRANCH else ' ' ,
                        'name'   :  child.name.MultibyteString } )

            ## 2. make the range object
            range = self.buffer.range( line_no + 1 , line_no + 1 )

            ## 3. append the child
            if show_list : range.append( show_list )

            ## 4. update flag to '-'
            range[0] = self.__format_string % {
                        'indent' : self.__indent_string * node_indent ,
                        'flag'   : '-' ,
                        'name'   :  node.name.MultibyteString } 


            # notify observer
            for ob in self.__observer_list:
                ob.OnBranchOpen( node )
        elif node_flag == '-':
            return
        else : # leef node
            # notify observer
            for ob in self.__observer_list:
                ob.OnLeefSelect( node )

        # focus to the line
        self.__hilightItem( line_no )


    def __closeItem( self , line_no ):
        node_indent , node_flag , node_name = self.__getNodeInfo( line_no )
        # make pvString for the factory
        node = self.__node_factory.generateNode( 
                [ pvString( MultibyteString = x ) for x in self.__lineNo2Path( line_no ) ] )

        if node_flag == '+' or node_flag == ' ':
            return

        range_start = line_no + 1
        range_end = line_no + 1
        ## 1. search children range
        for index in xrange( line_no + 1 , len( self.buffer ) ):
            line_info = self.__getNodeInfo( index )
            # index > node_indent , means child node 
            if line_info[0] > node_indent : 
                range_end += 1
                continue
            else:
                break
        ## 2. make the range object
        vim_range = self.buffer.range( range_start , range_end )

        ## 3. delete the child item
        if  range_end - range_start > 0 : del vim_range[1:]

        ## 4. update the flag to '+'
        vim_range[0] = self.__format_string % {
                    'indent' : self.__indent_string * node_indent ,
                    'flag'   : '+' ,
                    'name'   :  node.name.MultibyteString } 

        # notify observer
        for ob in self.__observer_list:
            ob.OnBranchClose( node )

        # focus to the line
        self.__hilightItem( line_no )

    def __path2LineNo( self , path ):
        total_line = len( self.buffer )

        line_index = -1 
        for indent_level , path_item in enumerate( path ):
            while True: 
                line_index += 1
                # find all line , but can't find it
                if line_index >= total_line : return -1
                level , flag , name = self.__getNodeInfo( line_index )

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

    def __getNodeInfo( self , line_no ):
        search_result = self.__format_search_re.match( self.buffer[line_no] )
        indent_level = len ( search_result.group('indent') ) / len( self.__indent_string )
        flag = search_result.group('flag')
        name = search_result.group('name')

        return ( indent_level , flag , name )

    def __lineNo2Path( self , line_no ):
        # result for the path list
        return_path = []

        # analyze the current line
        cur_indent_level , flag , name = self.__getNodeInfo( line_no )
        return_path.insert( 0 , name )

        # search parent
        cur_indent_level -= 1
        while cur_indent_level >= 0 :
            line_no -= 1
            indent_level , flag , name = self.__getNodeInfo( line_no )

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

    def __hilightItem( self , line_no ):
        vim.current.window.cursor = ( line_no + 1 , 0 )
        line = self.buffer[line_no].replace('/','\/')
        line = line.replace( '\\' , '\\\\' )
        self.registerCommand('match %s /\V%s/' % ( 'Search' ,  line ) , True)



        





