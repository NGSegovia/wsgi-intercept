
from nose.tools import with_setup, raises
from urllib2 import URLError
from wsgi_intercept.zope_testbrowser.wsgi_testbrowser import WSGI_Browser
import wsgi_intercept
from wsgi_intercept import test_wsgi_app

_saved_debuglevel = None
    
def add_intercept():
    # _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', 80, test_wsgi_app.create_fn)

def remove_intercept():
    wsgi_intercept.remove_wsgi_intercept('some_hopefully_nonexistant_domain', 80)
    # wsgi_intercept.debuglevel = _saved_debuglevel

@with_setup(add_intercept, remove_intercept)
def test_intercepted():
    b = WSGI_Browser()
    b.open('http://some_hopefully_nonexistant_domain:80/')
    assert test_wsgi_app.success()

@with_setup(add_intercept)
@raises(URLError)
def test_intercept_removed():
    remove_intercept()
    b = WSGI_Browser()
    b.open('http://some_hopefully_nonexistant_domain:80/')