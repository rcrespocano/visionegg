import os
import ctypes

if os.name=='nt':
    QTMLClient = ctypes.CDLL(r'C:\Program Files\QuickTime\QTSystem\QTMLClient.dll')

# OSErr SInt16 MacTypes.h
# OSStatus SInt32 MacTypes.h
# ItemCount UInt32 MacTypes.h
# FourCharCode SInt32 MacTypes.h
# OSType FourCharCode MacTypes.h
# QTNewMoviePropertyElement struct Movies.h
# QTPropertyClass OSType Movies.h
# QTPropertyID OSType Movies.h
# ByteCount UInt32 MacTypes.h
# QTPropertyValuePtr void* Movies.h
# Movie

OSErr = ctypes.c_short
OSStatus = ctypes.c_int
ItemCount = ctypes.c_uint
FourCharCode = ctypes.c_int
OSType = FourCharCode
QTPropertyClass = OSType
QTPropertyID = OSType
ByteCount = ctypes.c_uint
QTPropertyValuePtr = ctypes.c_void_p
QTVisualContextRef = ctypes.c_void_p
class Rect(ctypes.Structure):
    _fields_ = [("top",   ctypes.c_short),
                ("left",  ctypes.c_short),
                ("bottom",ctypes.c_short),
                ("right", ctypes.c_short)]

Movie = ctypes.c_void_p # not done

class QTNewMoviePropertyElement(ctypes.Structure):
    _fields_ = [("propClass",QTPropertyClass),
                ("propID",QTPropertyID),
                ("propValueSize",ByteCount),
                ("propValueAddress",QTPropertyValuePtr),
                ("propStatus",OSStatus)]

def FOUR_CHAR_CODE(code):
    assert isinstance(code,str)
    assert len(code)==4
    val = 0
    for i in range(4):
        c = code[i]
        ordc = ord(c)
        addval = ordc << (3-i)*8
        #print '%d: %s %x %x'%(i,c,ordc,addval)
        val += addval
    #print '%x\n'%val
    return val

if 1:
    kQTPropertyClass_DataLocation = FOUR_CHAR_CODE('dloc')
    kQTDataLocationPropertyID_DataReference = FOUR_CHAR_CODE('dref') # DataReferenceRecord (for semantics of NewMovieFromDataRef)
    kQTDataLocationPropertyID_CFStringNativePath = FOUR_CHAR_CODE('cfnp')
    kQTDataLocationPropertyID_CFStringPosixPath = FOUR_CHAR_CODE('cfpp')
    kQTDataLocationPropertyID_CFStringHFSPath = FOUR_CHAR_CODE('cfhp')
    kQTDataLocationPropertyID_CFStringWindowsPath = FOUR_CHAR_CODE('cfwp')
    kQTDataLocationPropertyID_CFURL = FOUR_CHAR_CODE('cfur')
    kQTDataLocationPropertyID_QTDataHandler = FOUR_CHAR_CODE('qtdh') # for semantics of NewMovieFromStorageOffset
    kQTDataLocationPropertyID_Scrap = FOUR_CHAR_CODE('scrp')
    kQTDataLocationPropertyID_LegacyMovieResourceHandle = FOUR_CHAR_CODE('rezh') # QTNewMovieUserProcInfo * (for semantics of NewMovieFromHandle)
    kQTDataLocationPropertyID_MovieUserProc = FOUR_CHAR_CODE('uspr') # for semantics of NewMovieFromUserProc
    kQTDataLocationPropertyID_ResourceFork = FOUR_CHAR_CODE('rfrk') # for semantics of NewMovieFromFile
    kQTDataLocationPropertyID_DataFork = FOUR_CHAR_CODE('dfrk') # for semantics of NewMovieFromDataFork64
    kQTPropertyClass_Context      = FOUR_CHAR_CODE('ctxt') # Media Contexts
    kQTContextPropertyID_AudioContext = FOUR_CHAR_CODE('audi')
    kQTContextPropertyID_VisualContext = FOUR_CHAR_CODE('visu')
    kQTPropertyClass_MovieResourceLocator = FOUR_CHAR_CODE('rloc')
    kQTMovieResourceLocatorPropertyID_LegacyResID = FOUR_CHAR_CODE('rezi') # (input/result property)
    kQTMovieResourceLocatorPropertyID_LegacyResName = FOUR_CHAR_CODE('rezn') # (result property)
    kQTMovieResourceLocatorPropertyID_FileOffset = FOUR_CHAR_CODE('foff') # NewMovieFromDataFork[64]
    kQTMovieResourceLocatorPropertyID_Callback = FOUR_CHAR_CODE('calb') # NewMovieFromUserProc(getProcrefcon)
                                        # Uses kQTMovieDefaultDataRefPropertyID for default dataref
    kQTPropertyClass_MovieInstantiation = FOUR_CHAR_CODE('mins')
    kQTMovieInstantiationPropertyID_DontResolveDataRefs = FOUR_CHAR_CODE('rdrn')
    kQTMovieInstantiationPropertyID_DontAskUnresolvedDataRefs = FOUR_CHAR_CODE('aurn')
    kQTMovieInstantiationPropertyID_DontAutoAlternates = FOUR_CHAR_CODE('aaln')
    kQTMovieInstantiationPropertyID_DontUpdateForeBackPointers = FOUR_CHAR_CODE('fbpn')
    kQTMovieInstantiationPropertyID_AsyncOK = FOUR_CHAR_CODE('asok')
    kQTMovieInstantiationPropertyID_IdleImportOK = FOUR_CHAR_CODE('imok')
    kQTMovieInstantiationPropertyID_DontAutoUpdateClock = FOUR_CHAR_CODE('aucl')
    kQTMovieInstantiationPropertyID_ResultDataLocationChanged = FOUR_CHAR_CODE('dlch') # (result property)
    kQTPropertyClass_NewMovieProperty = FOUR_CHAR_CODE('mprp')
    kQTNewMoviePropertyID_DefaultDataRef = FOUR_CHAR_CODE('ddrf') # DataReferenceRecord
    kQTNewMoviePropertyID_Active  = FOUR_CHAR_CODE('actv')
    kQTNewMoviePropertyID_DontInteractWithUser = FOUR_CHAR_CODE('intn')
    
class VEQTError(RuntimeError):
    pass

noErr = 0
paramErr = -50
movieToolboxUninitialized = -2020
def GetErrorString(value):
    if value == paramErr:
        return 'paramErr'
    elif value == movieToolboxUninitialized:
        return 'movieToolboxUninitialized'
    elif value != noErr:
        return 'error value: %d'%value
    else:
        return 'noErr'
    
def CheckOSStatus(value):
    if value != noErr:
        raise VEQTError(GetErrorString(value))
    return value

NewMovieFromFile = QTMLClient.NewMovieFromFile

NewMovieFromProperties = QTMLClient.NewMovieFromProperties
#NewMovieFromProperties.restype = OSStatus
NewMovieFromProperties.restype = CheckOSStatus
NewMovieFromProperties.argtypes = [ItemCount,
                                   ctypes.POINTER(QTNewMoviePropertyElement),
                                   ItemCount,
                                   ctypes.POINTER(QTNewMoviePropertyElement),
                                   ctypes.POINTER(Movie)]

InitializeQTML = QTMLClient.InitializeQTML
EnterMovies = QTMLClient.EnterMovies

QTGetCFConstant = QTMLClient.QTGetCFConstant

GetMovieBox = QTMLClient.GetMovieBox
GetMovieBox.argtypes = [Movie,
                        ctypes.POINTER(Rect)]
SetMovieBox = QTMLClient.SetMovieBox
SetMovieBox.argtypes = [Movie,
                        ctypes.POINTER(Rect)]

FSSpec = ctypes.c_void_p
CFStringRef = ctypes.c_void_p
CFStringEncoding = ctypes.c_uint
if 1:
    CFStringCreateWithCharacters = QTMLClient.CFStringCreateWithCharacters
    
    CFStringCreateWithCString = QTMLClient.CFStringCreateWithCString
    CFStringCreateWithCString.restype = CFStringRef
    CFStringCreateWithCString.argtypes = [ctypes.c_void_p,
                                          ctypes.c_char_p,
                                          ctypes.c_int]

    CFStringGetCString = QTMLClient.CFStringGetCString
    CFStringGetCStringPtr = QTMLClient.CFStringGetCStringPtr
    CFStringGetCStringPtr.restype = ctypes.c_char_p

    NativePathNameToFSSpec = QTMLClient.NativePathNameToFSSpec
    NativePathNameToFSSpec.restype = OSErr
    NativePathNameToFSSpec.argtypes = [ctypes.c_char_p,
                                       ctypes.POINTER(FSSpec),
                                       ctypes.c_long]

    OpenMovieFile = QTMLClient.OpenMovieFile
    
if 1:
    kCFAllocatorDefault = QTGetCFConstant("kCFAllocatorDefault")
    kCFStringEncodingMacRoman = 0 # CoreFoundation/CFString.h
