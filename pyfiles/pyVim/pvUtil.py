import vim
import types


class pvString:
    def __init__( self ):
        self.unistring = u""

    @property
    def UnicodeString( self ):
        return self.unistring

    @UnicodeString.setter
    def unicodeStringSet( self , unicode ):
        if type( unicode ) == types.UnicodeType :
            self.unistring = unicode
        else:
            raise RuntimeError("pvString::unicodeSet not a unicode string")

    @property
    def MultibyteString( self ):
        vim_encode = vim.eval("&encoding")
        mbstr = self.unistring.encode( vim_encode )
        return mbstr

    @MultibyteString.setter
    def multibyteStringSetter( self , mbstr ):
        vim_encode = vim.eval("&encoding")
        if type( mbstr ) == type.StringType :
            self.unistring = mbstr.decode( vim_encode )
        else:
            raise RuntimeError("pvString::multibyteStringSetter not a multibyte string")

