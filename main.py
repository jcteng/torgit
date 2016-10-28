#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'
import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os

settings = {'debug' : True,'log':"DEBUG",'template_path':os.path.join(os.path.dirname(__file__), "templates")}



from torgit import  git_urls,torgit_init,handler
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',manager = torgit.handler.repo_manager,request=self.request)

import torgit.handler
import demo_repo_mgr
def make_app():
    #init must call before tornado started, the repo_mgr will stay in memory
    torgit_init(git_root=os.path.dirname(__file__),repo_class=demo_repo_mgr.DemoRepoManager)
    #create test repos,if the repo already existed simply drop it
    for prefix ,repos in torgit.handler.repo_manager.repo_dict.items():
        for repo  in repos:
            torgit.handler.repo_manager.create_repo(prefix,repo)


    return tornado.web.Application([
        (r"/", MainHandler),
    ]+git_urls,**settings)


if __name__ == "__main__":
    print "enter torgit"
    app = make_app()

    server = tornado.httpserver.HTTPServer(app, max_buffer_size=10485760000)  # 10G
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()