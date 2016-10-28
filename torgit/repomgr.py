#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'


import os
import base64


class BaseRepoManager(object):
    def __init__(self, base_path=None,**kwargs):
        if base_path == None:
            self.base_path = os.path.dirname(__file__)
        else:
            self.base_path = base_path
    def get_url(self, prefix, repo_name):
        import settings

        return settings.URL_BASE+"/"+prefix+"/"+repo_name+".git"

    def get_abs_dir(self, prefix, repo_name):
        raise Exception("Implement Project Logic")
        return "ABS_PATH_OF_REPO"

    def makesure_path(self, filename):
        fpath = os.path.dirname(filename)
        if os.path.isdir(fpath):
            pass
        else:
            os.makedirs(fpath)

    def create_repo(self, prefix, repo_name):

        abs_path = self.get_abs_dir(prefix, repo_name)
        self.makesure_path(abs_path)
        # import pygit2
        # pygit2.init_repository(abs_path,
        #                        bare=True)
        import gitcmd
        gitcmd.create_repo(abs_path)

    def create_auth_header(self, handler, realm='Restricted'):
        handler.set_status(401)
        handler.set_header('WWW-Authenticate', 'Basic realm=%s' % realm)
        handler._transforms = []
        handler.finish()

    def basic_auth(self, handler, **kwargs):

        if not self.is_repo_existed(handler=handler,**kwargs):
            handler.set_status(404)
            handler._transforms = []
            handler.finish()
            return

        auth_header = handler.request.headers.get('Authorization')
        try:
            auth_decoded = base64.decodestring(auth_header[6:])
            user, pwd = auth_decoded.split(':', 2)
        except:
            user = ""
            pwd = ""

        if not self.auth_with_repo(handler, user, pwd, **kwargs):
            self.create_auth_header(handler)

    def auth(self, user, pwd):
        raise Exception("Implement Project Logic")
        return False


    def repo_anonymous_permission(self, repo, prefix, service):
        # "receive-pack" - w
        # "upload-pack" - r
        raise Exception("Implement Project Logic")
        return False


    def repo_user_permission(self, repo, prefix, service, user):
        # "receive-pack" - w
        # "upload-pack" - r
        raise Exception("Implement Project Logic")
        return False

    def is_repo_existed(self,handler,repo, prefix,**kwargs):

        raise Exception("Implement Project Logic")
        return False

    def auth_with_repo(self, handler, user, pwd, **kwargs):
        if self.repo_anonymous_permission(**kwargs):
            return True
        else:
            if self.auth(user, pwd):
                return self.repo_user_permission(user=user, **kwargs)
            else:
                return False


class DemoRepoManager(BaseRepoManager):

    auth_dict= {}
    repo_dict ={}

    def __init__(self,base_path=None,**kwargs):
        super(DemoRepoManager,self).__init__(base_path,**kwargs)

        import  os,json
        f = file(os.path.join(base_path, "users.json"))
        self.auth_dict = json.load(f)
        f.close()
        f = file(os.path.join(base_path, "repo.json"))
        self.repo_dict = json.load(f)
        f.close()

    def get_abs_dir(self, prefix, repo_name):
        return os.path.join(self.base_path,
                            prefix,
                            repo_name).replace("\\", "/")


    def auth(self, user, pwd):
        return pwd==self.auth_dict.get(user,None)

    def repo_anonymous_permission(self, repo, prefix, service):
        # "receive-pack" - w
        # "upload-pack" - r
        perm_dict = self.repo_dict[prefix][repo]
        if service=="receive-pack":
            return perm_dict["anonymous_write"]
        elif service=="upload-pack":
            return perm_dict["anonymous_read"]

        return False

    def is_repo_existed(self,handler,repo, prefix,**kwargs):
        return self.repo_dict.has_key(prefix) and self.repo_dict[prefix].has_key(repo)

    def repo_user_permission(self, repo, prefix, service, user):
        # "receive-pack" - w
        # "upload-pack" - r
        perm_dict = self.repo_dict[prefix][repo]
        if service == "receive-pack":
            return user in perm_dict["write_users"]
        elif service == "upload-pack":
            return user in perm_dict["read_users"]
