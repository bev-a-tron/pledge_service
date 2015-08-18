"""General utilities."""

import urlparse
import logging

def ConstantTimeIsEqual(a, b):
  """Securely compare two strings without leaking timing information."""
  if len(a) != len(b):
    return False
  acc = 0
  for x, y in zip(a, b):
    acc |= ord(x) ^ ord(y)
  return acc == 0


# TODO(hjfreyer): Pull into some kind of middleware?
def EnableCors(handler):
  """Inside a request, set the headers to allow being called cross-domain."""
  if 'Origin' in handler.request.headers:
    origin = handler.request.headers['Origin']
    _, netloc, _, _, _, _ = urlparse.urlparse(origin)
    if not (handler.app.config['env'].app_name == 'local' or
            netloc == 'mayone.us' or netloc.endswith('.mayone.us') or
            netloc == 'mayday.us' or netloc.endswith('.mayday.us') or 
            netloc == 'localhost' or netloc.endswith('localhost') or
            netloc == 'test-dot-mayday-pac-teams.appspot.com' or 
            netloc == 'lessig-trust.appspot.com' or 
            netloc.endswith('lessigforpresident.com') or
            '104.131.9.3' in netloc):
      logging.warning('Invalid origin: ' + origin + ' Netloc was: ' + netloc )
      handler.error(403)
      return

    handler.response.headers.add_header('Access-Control-Allow-Origin', origin)
    handler.response.headers.add_header('Access-Control-Allow-Methods',
                                        'GET, POST')
    handler.response.headers.add_header('Access-Control-Allow-Headers',
                                        'content-type, origin')

