#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'

#git url
# base_url/prefix/repo_name.git

from tornado.web import RequestHandler,stream_request_body,HTTPError
from gitcmd import smart_http_ref_info,blob_transfer_chunk_open
from settings import URL_BASE

repo_manager =None


def package_line(string_in):
    outstr = "%04x" % (len(string_in) + 4) + string_in
    return outstr
def package_end():
    return "0000"

#TODO:Tornado bug - on chunk mode ,receive-pack will hange while HTTPServer max_buffer_size default value is None
#reproduce env:windows




@stream_request_body
class GitServiceHandler(RequestHandler):

    process = None
    send_chunk_size = 1024*512

    def post(self,prefix,repo,service,*args, **kwargs):
        if not self.process.stdout.closed:
            while True:
                buf = self.process.stdout.read(self.send_chunk_size)
                self.write(buf)
                if len(buf)<self.send_chunk_size:
                    break
        self.finish()


    def prepare(self):
        repo_manager.basic_auth(self,**self.path_kwargs)
        repo = self.path_kwargs.get('repo')
        prefix = self.path_kwargs.get('prefix')
        service = self.path_kwargs.get('service')
        repo_dir =repo_manager.get_abs_dir(prefix,repo)

        if self.process==None:
            self.set_header("Content-Type","application/x-git-%s-request" % service)
            self.process  = blob_transfer_chunk_open(service,repo_dir)

    def data_received(self, chunk):
        self.process.stdin.write(chunk)





#no args :return file directly
# => GET $GIT_URL/info/refs?service=git-upload-pack
# 001e# service=git-upload-pack
# 000000e7ca82a6dff817ec66f44342007202690a93763949 HEADmulti_ack thin-pack \
# 	side-band side-band-64k ofs-delta shallow no-progress include-tag \
# 	multi_ack_detailed no-done symref=HEAD:refs/heads/master \
# 	agent=git/2:2.1.1+github-607-gfba4028
# 003fca82a6dff817ec66f44342007202690a93763949 refs/heads/master
# 0000
class GitInfoHandler(RequestHandler):

    def prepare(self):
        service = self.get_argument("service",default="git-upload-pack")
        service = service.replace("git-","")
        self.service = service
        repo_manager.basic_auth(self,service=service,**self.path_kwargs)

    def get(self,prefix,repo,*args, **kwargs):

        repo_dir =repo_manager.get_abs_dir(prefix,repo)
        steam,err =smart_http_ref_info(self.service,repo_dir)

        self.set_header("Content-Type","application/x-git-%s-advertisement" % self.service)

        if err==None or err=="":
            self.write(package_line("# service=git-" + self.service + "\n"))
            self.write(package_end())
            return self.write(steam)
        else:
            #make error string in single line
            err = err.replace("\r","").replace("\n","")
            raise HTTPError(500,reason=err)


git_urls = [
            (r"%s/(?P<prefix>[\w_-]+)/(?P<repo>[\w_-]+).git/git-(?P<service>[\w-]+)$"%URL_BASE, GitServiceHandler),
            (r"%s/(?P<prefix>[\w_-]+)/(?P<repo>[\w_-]+).git/info/refs$"%URL_BASE,GitInfoHandler)
            ]
