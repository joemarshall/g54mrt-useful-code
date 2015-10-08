
""" Reads NFC tags from the Grove NFC module, connected to RPISER on a grove shield

    example usage:

     # wait for up to 5 seconds and display the ID of an NFC tag that is 
     # put in front of the reader
     print grovenfcreader.waitForTag(5)


"""


import nfc
import time
import nfc.ndef
import nfc.tag
import nfc.clf

_cardFrontend=nfc.ContactlessFrontend('tty:AMA0:pn532')
_nextTimeout=0

def _on_connect(tag):
  return 



def waitForTag(timeout):
  """ Wait for an NFC tag (e.g. a university card) and return the
      ID of the tag.

     Args: 
        timeout:
           Time in seconds to wait for a tag
     
     Returns:
        List containing each byte of the tag ID, or None if no tag found 
  """
  global _nextTimeout
  _nextTimeout=time.time()+timeout
  tagObj=_cardFrontend.connect(rdwr={'on-connect':_on_connect},terminate=isTimeOut)
  if tagObj is None:
    return None
  id=[]
  for c in tagObj.identifier:
    id.append(ord(c))
  return id
  

def isTimeOut():
  global _nextTimeout
  if time.time()>_nextTimeout:
    return True
  return False

if __name__=="__main__":
  waitForTag(5)


