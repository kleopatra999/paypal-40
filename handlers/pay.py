#!/usr/bin/env python
# encoding: utf-8

"""Lin Pay Handlers"""


__author__ = 'Lin Zhong (lzhong@applause.com)',


import cgi
import json
import logging
import re
import urllib
import urllib2
import webapp2
import sys
import traceback
import datetime


from google.appengine.api import logservice
logservice.AUTOFLUSH_EVERY_SECONDS = None
logservice.AUTOFLUSH_EVERY_BYTES = None
logservice.AUTOFLUSH_EVERY_LINES = 1


from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template



from handlers import base_handler

template.register_template_library('handlers.string_filters')


class LinHandler(base_handler.BaseHandler):
  def __init__(self, request=None, response=None):
    try:
      logging.info("Trying to get some cookie action")
      cookie = request.cookies.get('applause_v2', '')
      logging.info("Trying to get some user action")
      # TBD: ad cookie usage later
      #self.CurrentUser = v2_user.GetUser(cookie=cookie)
      logging.info("CurrentUser set to %s", self.CurrentUser.email)
    except:
      self.CurrentUser = None

    logging.info("Current user is %s", self.CurrentUser)
    self.initialize(request, response)


  def setLoggedIn(self, user):
      self.CurrentUser = user
      self.response.headers.add_header('Set-Cookie', str('applause_v2=%s;path=/' % user.auth_cookie))
      

  def setLoggedOut(self):
      self.response.headers.add_header('Set-Cookie', str('applause_v2=;path=/'))
      self.CurrentUser = None

  def isLoggedIn(self):
    logging.info("CHECKING CURRENT HEADERS TO SET:")
    logging.info("Outgoing Headers: %s", self.response.headers)
    logging.info("CHECKING IS LOGGED IN:")
    if self.CurrentUser and self.CurrentUser.email:
      logging.info("User is: %s, %s", self.CurrentUser, (self.CurrentUser.email or None) )
      return True
    else:
      logging.info("USER IS NONE")
      return False

  def redirectToIndex(self, view="welcome"):
    self.redirect('/%s', view)

  def redirectToWelcome(self):
    self.redirect('/welcome')

  def redirectToExpiredAccount(self):
    self.redirect('/expired')

  def redirectToSignup(self, app_id):
    if not app_id:
      self.redirect('/signup')
      return
    else:
      self.redirect(('/signup?q=%s') % app_id)
      return

  # persist_url ensures that return_url is sent along to login so we get back to the same page.
  def redirectToLogin(self, persist_url = True):
    login_url = '/login'
    if persist_url:
      return_url = urllib.quote(self.request.path, '')
      login_url = login_url + '?return=' + return_url
    self.redirect(login_url)


#### BEGIN GLOBAL FUNCTIONS
def ResponseJson(data, success):
  return json.dumps({'data': data, 'success':success})


def SanitizeHtml(s):
  s = re.sub('[^0-9a-zA-Z\s\-\_@.\']+', '', s)
  return s


def CallApi(api_url):
    try:
      app_json = urlfetch.fetch(api_url).content
      app_info = json.loads(app_json)
      if app_info[u'success'] == True:
        app_info = app_info[u'data']
        return app_info
      else: return {}
    except:
      return {}
    

def ErrorConvertException():
  exc_type, exc_msg, tb = sys.exc_info()
  return u'%s\nCall Stack:\n%s' % (
      u''.join(traceback.format_exception(exc_type, exc_msg, tb)),
      u''.join(traceback.format_stack()))
#### END GLOBAL FUNCTIONS
  

class Pay(base_handler.BaseHandler):  
  def post(self):
    return  

   
  def get(self):
    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.render_template('pay/start.html', {})

class PayThankYou(base_handler.BaseHandler):   
  def get(self):
    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.render_template('pay/thankyou.html', {})

app = webapp2.WSGIApplication([
  # UX
  ('/pay/test', Pay),
  ('/pay/cancel', PayThankYou),
  ('/pay/complete', PayThankYou),
], debug=True)
