import logging
import os
import datetime
import wsgiref.handlers
from urllib import unquote

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

register = webapp.template.create_template_register()


# This filter handles capitalizing the first character of 
# a string, and lower-casing the rest of it.
@register.filter
def normalCasing(value):
  # logging.info( 'using filter "normalCasing" on: ' + value )
  lowered = value.capitalize()
  cleaned = lowered.replace('_',' ')
  return cleaned

# This filter handles capitalizing the first character of 
# a string, and lower-casing the rest of it.
@register.filter
def safeLength(value):
  #logging.info( 'using filter "safeLength" on: ' + value + '...length: ' + str(len(value)) )
  cleaned = normalCasing(value)
  if len(cleaned) > 10:
    chopped = cleaned[:10] + '...'
    # logging.info( 'chopped string filter' )
  else:
    chopped = cleaned
  return chopped  


# This filter handles getting a uid that can be
# used in HTML safely with data tags. The output
# is a string with characters turned into numbers
@register.filter
def getASCIIString(uid):
  safe = ''
  #loop through the characters and convert them
  for c in uid:
    csafe = ord(c)
    safe += str(csafe)
  return safe;


@register.filter
def slugstring(value):
  return value.replace(" ", "-")
    
@register.filter
def unquotestring(value):
  return unquote(value)
