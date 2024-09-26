#!/home/flask/.pyenv/versions/3.12.6/bin/python3
# TODO: ↑書き換えが必要 --- (※1)
# -*- coding: utf-8 -*-
from wsgiref.handlers import CGIHandler
from app import app
from sys import path
import os

# スクリプトのディレクトリをパスに追加
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
path.insert(0, SCRIPT_DIR) 
# CGIで実行するためのプロキシを設定 --- (※2)
class ProxyFix(object):
  def __init__(self, app):
      self.app = app
  def __call__(self, environ, start_response):
      global env
      env = environ
      environ['SERVER_NAME'] = "flask.sakura.ne.jp" # TODO: 書き換えが必要 --- (※3)
      environ['SERVER_PORT'] = "80"
      environ['SCRIPT_NAME'] = ""
      environ['SERVER_PROTOCOL'] = "HTTP/1.1"
      return self.app(environ, start_response)
if __name__ == '__main__':
   app.wsgi_app = ProxyFix(app.wsgi_app)
   CGIHandler().run(app)

