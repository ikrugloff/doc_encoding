# Is ASCII?
# Check if a document is encoded to ASCII is simple: test if the bit 7 of all bytes is unset (0b0xxxxxxx).


def isASCII(data):
    try:
        data.decode('ASCII')
    except UnicodeDecodeError:
        return False
    else:
        return True


# Check for BOM markers
# If the string begins with a BOM, the encoding can be extracted from the BOM. But there is a problem with UTF-16-BE
# and UTF-32-LE: UTF-32-LE BOM starts with the UTF-16-LE BOM.
# For the UTF-16-LE/UTF-32-LE BOM conflict: this function returns "UTF-32-LE" if the string begins
# with "\xFF\xFE\x00\x00", even if this string can be decoded from UTF-16-LE.

from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

BOMS = (
    (BOM_UTF8, "UTF-8"),
    (BOM_UTF32_BE, "UTF-32-BE"),
    (BOM_UTF32_LE, "UTF-32-LE"),
    (BOM_UTF16_BE, "UTF-16-BE"),
    (BOM_UTF16_LE, "UTF-16-LE"),
)


def check_bom(data):
    return [encoding for bom, encoding in BOMS if data.startswith(bom)]


# Is UTF-8?
# UTF-8 encoding adds markers to each bytes and so it’s possible to write a reliable algorithm to check if
# a byte string is encoded to UTF-8.

def isUTF8(data):
    try:
        data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    else:
        return True


"""
The codecs and encodings modules provide text encodings. They support a lot of encodings. Some examples: ASCII, 
ISO-8859-1, UTF-8, UTF-16-LE, ShiftJIS, Big5, cp037, cp950, EUC_JP, etc.

UTF-8, UTF-16-LE, UTF-16-BE, UTF-32-LE and UTF-32-BE don’t use BOM, whereas UTF-8-SIG, UTF-16 and UTF-32 use BOM. mbcs 
is only available on Windows: it is the ANSI code page.

Python provides also many error handlers used to specify how to handle undecodable byte sequences and unencodable 
characters:

strict (default): raise a UnicodeDecodeError or a UnicodeEncodeError
replace: replace undecodable bytes by � (U+FFFD) and unencodable characters by ? (U+003F)
ignore: ignore undecodable bytes and unencodable characters
backslashreplace (only encode): replace unencodable bytes by \xHH
Python 3 has three more error handlers:

surrogateescape: replace undecodable bytes (non-ASCII: 0x80—0xFF) by surrogate characters (in U+DC80—U+DCFF) on 
decoding, replace characters in range U+DC80—U+DCFF by bytes in 0x80—0xFF on encoding. Read the PEP 383 (Non-decodable 
Bytes in System Character Interfaces) for the details.
surrogatepass, specific to UTF-8 codec: allow encoding/decoding surrogate characters in UTF-8. It is required because 
UTF-8 decoder of Python 3 rejects surrogate characters by default.
backslashreplace (for decode): replace undecodable bytes by \xHH
"""