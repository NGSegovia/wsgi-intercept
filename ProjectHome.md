# Notice #

There is a new version of wsgi-intercept now available which works with Python 2.6, 2.7 and 3.3 (and beyond). It can be found on [GitHub](https://github.com/cdent/python3-wsgi-intercept) and [PyPI](https://pypi.python.org/pypi/wsgi_intercept).

The below is left for historical reference.

# Introduction #

Testing a WSGI application normally involves starting a server at a local host and port, then pointing your test code to that address.  Instead, this library lets you intercept calls to any specific host/port combination and redirect them into a [WSGI application](http://www.python.org/peps/pep-0333.html) importable by your test program.  Thus, you can avoid spawning multiple processes or threads to test your Web app.

# How Does It Work? #

`wsgi_intercept` works by replacing `httplib.HTTPConnection` with a subclass, `wsgi_intercept.WSGI_HTTPConnection`.  This class then redirects specific server/port combinations into a WSGI application by emulating a socket.  If no intercept is registered for the host and port requested, those requests are passed on to the standard handler.

The functions `add_wsgi_intercept(host, port, app_create_fn, script_name='')` and `remove_wsgi_intercept(host,port)` specify which URLs should be redirect into what applications.  Note especially that `app_create_fn` is a **function object** returning a WSGI application; `script_name` becomes `SCRIPT_NAME` in the WSGI app's environment, if set.

# Install #

```
easy_install wsgi_intercept
```

(The `easy_install` command is bundled with the [setuptools](http://cheeseshop.python.org/pypi/setuptools/) module)

To use a [development version](http://wsgi-intercept.googlecode.com/svn/trunk/#egg=wsgi_intercept-dev) of wsgi\_intercept, run:

```
easy_install http://wsgi-intercept.googlecode.com/svn/trunk
```

# Packages Intercepted #

Unfortunately each of the Web testing frameworks uses its own specific mechanism for making HTTP call-outs, so individual implementations are needed.  Below are the packages supported and how to create an intercept.

## urllib2 ##

[urllib2](http://docs.python.org/lib/module-urllib2.html) is a standard Python module, and `urllib2.urlopen` is a pretty normal way to open URLs.

The following code will install the WSGI intercept stuff as a default urllib2 handler:

```
>>> from wsgi_intercept.urllib2_intercept import install_opener
>>> install_opener() #doctest: +ELLIPSIS
<urllib2.OpenerDirector instance at ...>
>>> import wsgi_intercept
>>> from wsgi_intercept.test_wsgi_app import create_fn
>>> wsgi_intercept.add_wsgi_intercept('some_host', 80, create_fn)
>>> import urllib2
>>> urllib2.urlopen('http://some_host:80/').read()
'WSGI intercept successful!\n'
```

The only tricky bit in there is that different handler classes need to be constructed for Python 2.3 and Python 2.4, because the httplib interface changed between those versions.

## httplib2 ##

[httplib2](http://code.google.com/p/httplib2/) is a 3rd party extension of the built-in `httplib`.  To intercept requests, it is similar to urllib2:

```
>>> from wsgi_intercept.httplib2_intercept import install
>>> install()
>>> import wsgi_intercept
>>> from wsgi_intercept.test_wsgi_app import create_fn
>>> wsgi_intercept.add_wsgi_intercept('some_host', 80, create_fn)
>>> import httplib2
>>> resp, content = httplib2.Http().request('http://some_host:80/', 'GET')
>>> content
'WSGI intercept successful!\n'
```

(Contributed by [David "Whit" Morris](http://public.xdi.org/=whit).)

## webtest ##

[webtest](http://www.cherrypy.org/file/trunk/cherrypy/test/webtest.py) is an extension to `unittest` that has some nice functions for testing Web sites.

To install the WSGI intercept handler, do

```
>>> import wsgi_intercept.webtest_intercept
>>> class WSGI_Test(wsgi_intercept.webtest_intercept.WebCase):
...     HTTP_CONN = wsgi_intercept.WSGI_HTTPConnection
...     HOST='localhost'
...     PORT=80
...
...     def setUp(self):
...         wsgi_intercept.add_wsgi_intercept(self.HOST, self.PORT, create_fn)
...
>>>
```

## webunit ##

[webunit](http://mechanicalcat.net/tech/webunit/) is another unittest-like framework that contains nice functions for Web testing.  ([funkload](http://funkload.nuxeo.org/) uses webunit, too.)

webunit needed to be patched to support different scheme handlers. The patched package is in webunit/wsgi\_webunit/, and the only file that was changed was webunittest.py; the original is in webunittest-orig.py.

To install the WSGI intercept handler, do

```
>>> from httplib import HTTP
>>> import wsgi_intercept.webunit_intercept
>>> class WSGI_HTTP(HTTP):
...     _connection_class = wsgi_intercept.WSGI_HTTPConnection
...
>>> class WSGI_WebTestCase(wsgi_intercept.webunit_intercept.WebTestCase):
...     scheme_handlers = dict(http=WSGI_HTTP)
...
...     def setUp(self):
...         wsgi_intercept.add_wsgi_intercept('127.0.0.1', 80, create_fn)
...
>>>
```

## mechanize ##

[mechanize](http://wwwsearch.sf.net/) is John J. Lee's port of Perl's WWW::Mechanize to Python. It mimics a browser.  (It's also what's behind [twill](http://www.idyll.org/~t/www-tools/twill.html).)

mechanize is just as easy as mechanoid:

```
>>> import wsgi_intercept.mechanize_intercept
>>> from wsgi_intercept.test_wsgi_app import create_fn
>>> wsgi_intercept.add_wsgi_intercept('some_host', 80, create_fn)
>>> b = wsgi_intercept.mechanize_intercept.Browser()
>>> response = b.open('http://some_host:80')
>>> response.read()
'WSGI intercept successful!\n'
```

## mechanoid ##

[mechanoid](http://www.python.org/pypi/mechanoid/) is a fork of [mechanize](http://wwwsearch.sf.net/).

```
>>> import wsgi_intercept.mechanoid_intercept
>>> from wsgi_intercept.test_wsgi_app import create_fn
>>> wsgi_intercept.add_wsgi_intercept('some_host', 80, create_fn)
>>> b = wsgi_intercept.mechanoid_intercept.Browser()
>>> response = b.open('http://some_host:80')
>>> response.read()
'WSGI intercept successful!\n'
```

## zope.testbrowser ##

[zope.testbrowser](http://www.python.org/pypi/zope.testbrowser) is a prettified interface to [mechanize](http://wwwsearch.sf.net/) that is used primarily for testing Zope applications.

zope.testbrowser is also pretty easy

```
>>> import wsgi_intercept.zope_testbrowser
>>> from wsgi_intercept.test_wsgi_app import create_fn
>>> wsgi_intercept.add_wsgi_intercept('some_host', 80, create_fn)
>>> b = wsgi_intercept.zope_testbrowser.WSGI_Browser('http://some_host:80/')
>>> b.contents
'WSGI intercept successful!\n'
```

# History #

Pursuant to Ian Bicking's ["best Web testing framework"](http://blog.ianbicking.org/best-of-the-web-app-test-frameworks.html) post, Titus Brown put together an [in-process HTTP-to-WSGI interception mechanism](http://www.advogato.org/person/titus/diary.html?start=119) for his own Web testing system, [twill](http://www.idyll.org/~t/www-tools/twill.html).  Because the mechanism is pretty generic -- it works at the httplib level -- Titus decided to try adding it into all of the **other** Python Web testing frameworks.

This is the result.

# Mocking your HTTP Server #

Marc Hedlund has gone one further, and written a full-blown mock HTTP server for wsgi\_intercept.  Combined with wsgi\_intercept itself, this lets you entirely replace client calls to a server with a mock setup that hits neither the network nor server code.  You can see his work in the file `mock_http.py`.  Run `mock_http.py` to see a test.

# Project Home #

If you aren't already there, this project lives on [Google Code](http://code.google.com/p/wsgi-intercept/).  Please submit all bugs, patches, failing tests, et cetera using the [Issue Tracker](http://code.google.com/p/wsgi-intercept/issues/list)
