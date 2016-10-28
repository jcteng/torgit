#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'


from handler import git_urls,repo_manager
from settings import GIT_REPO_ROOT,REPO_CLASS

import importlib
def get_kls_from_string(kls_name):
    print "get_kls_from_string"
    module_name, class_name = kls_name.rsplit(".",1)
    somemodule = importlib.import_module(module_name)
    return getattr(somemodule, class_name)

def torgit_init(git_root=GIT_REPO_ROOT,repo_class = REPO_CLASS):
    import handler
    if isinstance(repo_class,str):
        handler.repo_manager = get_kls_from_string(repo_class)(git_root)
    else:
        handler.repo_manager  = repo_class(git_root)