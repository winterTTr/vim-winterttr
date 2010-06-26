# sys import
import sys
import vim
import os
import subprocess
from xml.etree import ElementTree as ET
# AT import
from ATBase import ATTypeBase


class ATTypeCPP( ATTypeBase ):

    def __init__( self ):
        ATTypeBase.__init__( self )


    def GetUserInput( self , prompt , type = None , check_func = None , allow_empty = False ):
        if type == None :
            cmdFirst = 'input( "%s: " , "" )' %  prompt  
            cmdRetry = 'input( "Invalid , retry: " , "" )'
        else:
            cmdFirst = 'input( "%s: " , "" , "%s" )' %  ( prompt  , type )
            cmdRetry = 'input( "Invalid , retry: " , "" )'

        input = vim.eval( cmdFirst )
        if check_func == None :
            return input
        else:
            while True :
                if input == None :
                    return None
                if allow_empty and input == "":
                    return ""
                if not check_func( input ):
                    input = vim.eval( cmdRetry )
                    continue
                break
            return input

    #def GetUserInput( self , info , prompt , keynavi , type = None ):
    #    if info == "":
    #        showprompt = "%-40s\\\" %s\nAutotags ==> " % ( prompt , keynavi )
    #    else:
    #        showprompt = "    %s\n%-40s\\\" %s\nAutotags ==> " % ( info , prompt , keynavi )

    #    if type == None :
    #        return vim.eval('input("%s","")' % showprompt )
    #    else:
    #        return vim.eval('input("%s","","%s")' % ( showprompt , type ) )

    def SearchConfig( self , basepath = None ):
        if basepath :
            search_base_path = basepath
        else:
            search_base_path = vim.eval(' expand("%:p:h") ' )

        # search config_base_path
        retryDepth = 8 
        while retryDepth :
            retryDepth -= 1

            config_file_path = os.path.join ( search_base_path , '.at' , self.GetTypeID() + '.xml' )
            if os.path.isfile( config_file_path ):
                return config_file_path

            next_search = os.path.dirname( search_base_path )
            if next_search == search_base_path :
                raise RuntimeError('not find .at config path')
            search_base_path = next_search

    def LoadXML( self , basepath = None ):
        # check config file
        config_file_path = self.SearchConfig( basepath )

        # <typeid>cpp</typeid>
        # <soucepath>D:</sourcepath>
        # <tagspath>E:</tagspath>
        # <systags>
        #     <item>D:/SymbianSDK/taglist/SDK/tags</item>
        # </systags>
        config_dict = {}
        et = ET.ElementTree( file = config_file_path )
        config_dict['typeid'] = et.find('typeid').text
        if config_dict['typeid'] != self.GetTypeID(): raise
        config_dict['systags'] = [ x.text for x in et.find('systags').findall('item') ]
        config_dict['sourcepath'] = et.find('sourcepath').text
        config_dict['tagspath'] = et.find('tagspath').text
        return config_dict

    def GetConfigFromUser( self ):
        # get source dir
        sourcepath = self.GetUserInput( "Give the <Source Path>" , 'dir' , os.path.isdir )
        if sourcepath == None : return None

        # get where to gen the tags
        tagspath = self.GetUserInput( "Give the <Tag path> where to gen the tags" , "dir" , os.path.isdir )
        if tagspath == None : return None
        
        # get systags list
        systagslist = []
        systags = self.GetUserInput( "Add <System Tags> , Empty for next Step" , 'file' , os.path.isfile )
        while True:
            if systags == None:
                return None
            elif systags == "":
                break;

            if not systags in systagslist :
                systagslist.append( systags )
            systags = self.GetUserInput("Add one more , Empty for next step" , 'file' , os.path.isfile , True )


        confirmText  = "\n" + "=" * 30 + "\n"
        confirmText += "typeid : \n"
        confirmText += "    cpp\n"
        confirmText += "Source Path :\n"
        confirmText += "    %s\n" % sourcepath
        confirmText += "Tags Path :\n"
        confirmText += "    %s\n" % tagspath
        confirmText += "System Tags :\n"
        for x in systagslist:
            confirmText += "    %s\n" % x
        confirmText += "=" * 30 + "\n"
        selection = self.GetUserInput( confirmText + 'Continue? (Enter to continue , ESC for CANCEL)' )

        if selection != "":
            return None

        config_dict = {}
        config_dict['typeid'] = self.GetTypeID()
        config_dict['sourcepath'] = sourcepath
        config_dict['tagspath'] = tagspath
        config_dict['systags'] = systagslist
        return config_dict

    def GenXML( self , config_dict ):
        # <typeid>cpp</typeid>
        # <sourcepath>D:</sourcepath>
        # <tagspath>E:</tagspath>
        # <systags>
        #     <item>D:/SymbianSDK/taglist/SDK/tags</item>
        # </systags>
        et = ET.Element( 'config' )
        ET.SubElement( et , 'typeid' ).text = self.GetTypeID() 
        ET.SubElement( et , 'sourcepath' ).text = config_dict['sourcepath']
        ET.SubElement( et , 'tagspath' ).text = config_dict['tagspath']
        systags = ET.SubElement( et , 'systags' )
        for x in config_dict['systags']:
            ET.SubElement( systags , 'item' ).text = x

        return ET.ElementTree( element = et )

    def GenATOneFolder( self , path , et ):
        atdir = os.path.join( path , '.at' )
        os.mkdir( atdir )
        if not os.path.isdir( atdir ):
            sys.stderr.write("Autotags ==> Gen [%s] dir error!" % atdir )
            return
        filename = os.path.join( atdir , self.GetTypeID() + '.xml' )
        et.write( filename , 'UTF-8' )

    # implement the base function
    def GetTagsCommand( self ):
        return "ctags.exe --c++-kinds=+p --fields=+iaS --extra=+q -o %(dst)s %(src)s"


    def GetTypeID( self ):
        return "cpp"

    def GetFilePattern( self ):
        return ["cpp","c","h","hrh"]

    def LoadConfig( self ):
        # load config
        try :
            config_dict = self.LoadXML()
        except:
            return

        tags_file_list = config_dict['systags'][:]
        for filename in os.listdir( config_dict['tagspath'] ):
            file_full_path = os.path.join( config_dict['tagspath'] , filename )
            if filename.endswith('.tags') and os.path.isfile( file_full_path ):
                tags_file_list.append( file_full_path )

        vim.command('set tags=%s' % ','.join(tags_file_list) )

    def ResetConfig( self ):
        # load config
        try :
            config_dict = self.LoadXML()
        except:
            return
        vim.command('set tags=%s' % ','.join( config_dict['systags'] ) )

    def UpdateTags( self ):
        # load config
        try :
            config_dict = self.LoadXML()
        except:
            return
        filename = vim.eval('expand("%:p:t")')
        full_path = vim.eval('expand("%:p")')
        self.GenTags( full_path , os.path.join( config_dict['tagspath'] , filename + '.tags')  )

    def CreateRepository( self ):
        config_dict = self.GetConfigFromUser()
        if config_dict == None :
            return 
        et = self.GenXML( config_dict );

        atdir = os.path.join( config_dict['sourcepath'] , '.at' )
        os.mkdir( atdir )
        if not os.path.isdir( atdir ):
            sys.stderr.write("Autotags ==> Gen [%s] dir error!" % atdir )
            return
        filename = os.path.join( atdir , self.GetTypeID() + '.xml' )
        et.write( filename , 'UTF-8' )


    def RemoveRepository( self ):
        # get source dir
        sourcepath = self.GetUserInput( "Give the <Source Path>:" , "dir" , os.path.isdir )
        if sourcepath == None : return
    
        try:
            config_dict = self.LoadXML( sourcepath )
        except:
            sys.stderr.write("Autotags ==> Load config Error at[%s]" % sourcepath )
            return

        confirmText = "source path:\n"
        confirmText+= "    %s" % config_dict['sourcepath']
        selection = self.GetUserInput( confirmText + '\nContinue? ( Enter to continue , ESC for CANCEL)' )

        if selection != '' :
            return

        import shutil
        shutil.rmtree( os.path.join( config_dict['sourcepath'] , '.at' ) )





