# sys import
import sys
import vim
import os
import subprocess
from xml.etree import ElementTree as ET
# pyfiles import 
from ATVimFuncWrapper import VimConfirm
# AT import
from ATBase import ATTypeBase


class ATTypeCPP( ATTypeBase ):

    def __init__( self ):
        ATTypeBase.__init__( self )


    def GetUserInput( self , info , prompt , keynavi , type ):
        if info == "":
            showprompt = "%-40s\\\" %s\nAutotags ==> " % ( prompt , keynavi )
        else:
            showprompt = "    %s\n%-40s\\\" %s\nAutotags ==> " % ( info , prompt , keynavi )
        return vim.eval('input("%s","","%s")' % ( showprompt , type ) )


    def LoadXML( self , basepath = None ):
        if basepath :
            config_base_path = basepath
        else:
            config_base_path = vim.eval(' expand("%:p:h") ' )

        # check config file
        config_file_path = os.path.join( config_base_path , '.at' , self.GetTypeID() + '.xml' )
        if not os.path.isfile( config_file_path ):
            raise

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
        sourcepath = self.GetUserInput( 
                        "" , 
                        "Give the <Source Path>:" , 
                        "<ESC> CANCEL" , 
                        "dir" )
        while True :
            if sourcepath == None :
                return None
    
            if not os.path.isdir( sourcepath ):
                srcbase = self.GetUserInput( 
                        "[%s] is not valid dir path" % sourcepath , 
                        "Give the <Source Path>:" , 
                        "<ESC> CANCEL" , 
                        "dir" )
                continue
            break
        # get where to gen the tags
        tagspath = self.GetUserInput( 
                "Source Path -> %s" % sourcepath ,
                "Give the <Tags Path> where to gen the tags:" , 
                "<ESC> CANCEL" , 
                "dir" )
        while True :
            if tagspath == None :
                return None

            if not os.path.isdir( tagspath ):
                tagsbase = self.GetUserInput( 
                        "[%s] is not valid dir path" % tagspath , 
                        "Give the <Tags Path> where to gen the tags:" , 
                        "<ESC> CANCEL" , 
                        "dir" )
                continue
            break
        
        # get systags list
        systagslist = []
        systags = self.GetUserInput(
                "Tags Path -> %s" % tagspath ,
                "Add <System Tags> :",
                "[Empty] enter next step | <Esc> CANCEL" ,
                "file" )
        while True:
            if systags == None:
                return None
            elif systags == "":
                break;

            if os.path.isfile( systags ) and ( not systags in systagslist ):
                systagslist.append( systags )
                systags = self.GetUserInput(
                        "Added to <System Tags> -> %s" % systags,
                        "Add system tag files:",
                        "[Empty] enter next step | <Esc> CANCEL" ,
                        "file" )
            else:
                systags = self.GetUserInput(
                        "[%s] is not valid file path" % systags ,
                        "Add system tag files:",
                        "[Empty] enter next step | <Esc> CANCEL" ,
                        "file" )


        confirmText  = "typeid : \n"
        confirmText += "    cpp\n"
        confirmText += "Source Path :\n"
        confirmText += "    %s\n" % sourcepath
        confirmText += "Tags Path :\n"
        confirmText += "    %s\n" % tagspath
        confirmText += "System Tags :\n"
        for x in systagslist:
            confirmText += "    %s\n" % x
        selection = VimConfirm( confirmText , ['Continue' , 'Cancel' ] )
        if selection != 'Continue' :
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
        return ["cpp","c","h"]

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

        for root , dirs , files in os.walk( config_dict['sourcepath'] , topdown = False ):
            for dir in dirs :
                self.GenATOneFolder( os.path.join( root , dir ) , et )
        self.GenATOneFolder( config_dict['sourcepath'] , et )


    def RemoveRepository( self ):
        # get source dir
        sourcepath = self.GetUserInput( 
                        "" , 
                        "Give the <Source Path>:" , 
                        "<ESC> CANCEL" , 
                        "dir" )
        while True :
            if sourcepath == None :
                return None
    
            if not os.path.isdir( sourcepath ):
                srcbase = self.GetUserInput( 
                        "[%s] is not valid dir path" % sourcepath , 
                        "Give the <Source Path>:" , 
                        "<ESC> CANCEL" , 
                        "dir" )
                continue
            break

        try:
            config_dict = self.LoadXML( sourcepath )
        except:
            sys.stderr.write("Autotags ==> Load config Error at[%s]" % sourcepath )
            return

        confirmText = "source path:\n"
        confirmText+= "    %s" % config_dict['sourcepath']
        selection = VimConfirm( confirmText , ['Continue' , 'Cancel' ] )

        if selection != 'Continue':
            print "Autotags ==> User cancel action!"
            return

        import shutil
        for root , dirs , files in os.walk( config_dict['sourcepath'] , topdown = False ):
            if '.at' in dirs :
                shutil.rmtree( os.path.join( root , '.at' ) )
        try:
            shutil.rmtree( os.path.join( config_dict['sourcepath'] , '.at' ) )
        except:
            pass





