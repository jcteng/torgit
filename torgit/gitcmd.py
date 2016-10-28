#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'

import subprocess


def git_exec(c_args,data=None,*args,**kwargs):
    p = subprocess.Popen(c_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    if data==None:
        out, err = p.communicate()
    else:
        out, err = p.communicate(input=data)
    return out, err



def blob_transfer_chunk_open(service,repo_dir,binpath="git",*args,**kwargs):
    accepts = ["upload-pack",
               "receive-pack"]
    if service in accepts:
        c_args = [binpath,service,"--stateless-rpc",repo_dir]
        p = subprocess.Popen(c_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        return p

    return None

def create_repo(repo_dir,binpath="git"):
     c_args = [binpath,"init","--bare",repo_dir]
     return git_exec(c_args)

def smart_http_ref_info(service,repo_dir,binpath="git",*args,**kwargs):
    accepts = ["upload-pack",
               "receive-pack"]
    if service in accepts:
        c_args = [binpath,service,"--stateless-rpc","--advertise-refs",repo_dir]
        return git_exec(c_args)
    else:
        return None,"Not Supported Parameters"

