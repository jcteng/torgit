#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'
import os
from torgit.repomgr import BaseRepoManager
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