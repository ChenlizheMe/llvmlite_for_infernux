from ctypes import c_void_p, c_char_p, c_bool, POINTER
import sys

from llvmlite.binding import ffi
from llvmlite.binding.common import _encode_string


def address_of_symbol(name):
    """
    Get the in-process address of symbol named *name*.
    An integer is returned, or None if the symbol isn't found.
    """
    return ffi.lib.LLVMPY_SearchAddressOfSymbol(_encode_string(name))


def add_symbol(name, address):
    """
    Register the *address* of global symbol *name*.  This will make
    it usable (e.g. callable) from LLVM-compiled functions.
    """
    ffi.lib.LLVMPY_AddSymbol(_encode_string(name), c_void_p(address))


def load_library_permanently(filename):
    """
    Load an external library
    """
    with ffi.OutputString() as outerr:
        if ffi.lib.LLVMPY_LoadLibraryPermanently(
                _encode_string(filename), outerr):
            if sys.platform == 'win32':
                # LLVM 22's DLOpen prefixes the UTF-8 filename to MakeErrMsg's
                # ASCII context + FormatMessageA text (Windows ANSI codepage).
                # Do not decode the filename itself as ANSI or guess encodings.
                suffix = outerr.bytes[len(_encode_string(filename)):]
                raise RuntimeError(filename + suffix.decode('mbcs'))
            raise RuntimeError(str(outerr))

# ============================================================================
# FFI


ffi.lib.LLVMPY_AddSymbol.argtypes = [
    c_char_p,
    c_void_p,
]

ffi.lib.LLVMPY_SearchAddressOfSymbol.argtypes = [c_char_p]
ffi.lib.LLVMPY_SearchAddressOfSymbol.restype = c_void_p

ffi.lib.LLVMPY_LoadLibraryPermanently.argtypes = [c_char_p, POINTER(c_char_p)]
ffi.lib.LLVMPY_LoadLibraryPermanently.restype = c_bool
