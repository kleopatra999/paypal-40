#!/usr/bin/env python
# encoding: utf-8
"""
base_handler.py

Copyright (c) 2012 uTest.com
All rights reserved.
"""

import os
import webapp2

from google.appengine.ext import ereporter
from google.appengine.ext.webapp import template

import settings
import urlparse


ereporter.register_logger()


class BaseHandler(webapp2.RequestHandler):
  def get_rendered_template(self,filename,template_args):
    path = os.path.join(settings.ROOT_FOLDER, 'templates', filename)
    rendered_template = template.render(path, template_args)
    return rendered_template

  def render_template(self, filename, template_args):
    path = os.path.join(settings.ROOT_FOLDER, 'templates', filename)
    rendered_template = template.render(path, template_args)
    self.response.write(rendered_template)
    return rendered_template

  def GetBaseUrl(self):
    """Returns 'http://foo.com' from 'http://foo.com/bar/baz?foobar'.
    """
    split = urlparse.urlsplit(self.request.url)
    return '%s://%s' % (split.scheme, split.netloc)
