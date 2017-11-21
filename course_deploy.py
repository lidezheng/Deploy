#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2017/3/30 下午10:23

from __future__ import with_statement
from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm


# 服务名称
SERVER = 'server_name'
SUPERVISOR_NAME = 'server'

# 部署路径
DEPLOY_PATH = '/home/user/packages/'
LINK_PATH = '/home/user'

# 主机列表
env.hosts = [
    'user@ip:port',
]
env.passwords = {
    'user@ip:port':     'passwd',
}


# 只运行一次
@runs_once
def local_pack(version=None):
    """本地打包程序"""
    if not version:
        return
    global SERVER
    folder_name = SERVER + '.' + version
    local('rm -rf {}'.format(folder_name))
    local('rm -rf *.tar.gz')
    # 拉取git代码
    command = 'git clone git@ip:v2-online-server/{}.git -b {} {}'.format(SERVER, version, folder_name)
    local(command)
    local('tar -czf {}.tar.gz {}'.format(folder_name, folder_name))
    print(green('pack success!!'))


# 只运行一次
@runs_once
def local_clean(version=None):
    """清理本地工作"""
    if not version:
        print(red('请输入版本号！'))
        return

    global SERVER
    folder_name = SERVER + '.' + version
    local('rm -rf {}'.format(folder_name))
    local('rm -rf *.tar.gz *.pyc')
    print(green('clean success......'))


def upload(version=None):
    """包上传"""
    if not version:
        return
    global SERVER
    folder_name = SERVER + '.' + version
    remote_tmp_tar = '/tmp/{}.tar.gz'.format(folder_name)
    run('rm -rf {}'.format(remote_tmp_tar))
    put('{}.tar.gz'.format(folder_name), remote_tmp_tar)
    print(green('upload file success!!'))


def remote_unpack(version=None):
    """远程解压"""
    if not version:
        return
    global SERVER
    global DEPLOY_PATH
    folder_name = SERVER + '.' + version
    # 检查文件夹路径
    run('mkdir -p {}'.format(DEPLOY_PATH))
    run('rm -rf {}'.format(DEPLOY_PATH + folder_name))
    source_file = '/tmp/{}.tar.gz'.format(folder_name)
    run('tar -zxf {} -C {}'.format(source_file, DEPLOY_PATH))
    # 建立软链接
    run('ln -snf {} {}'.format(DEPLOY_PATH + folder_name, LINK_PATH + SERVER))

    # 清理远程文件
    run('rm -rf /tmp/{}.tar.gz'.format(folder_name))
    print(green("unpack file success!!"))


def restart_server():
    """重启服务"""
    run('supervisorctl restart {}:*'.format(SUPERVISOR_NAME))
    print(green("restart server success!!"))


def rollback():
    """回滚动作"""
    pass


# 并行执行任务
@parallel
def deploy(version=None):
    """部署"""
    if not version:
        print(red('请输入版本号！'))
        return
    # 上传
    upload(version)
    # 解压
    remote_unpack(version)
    # 重启服务
    restart_server()

    print(green('all success......'))


# 启动命令(每个shell命令之间用&&隔开。说明：若前面的命令执行成功，才会去执行后面的命令)
# cd /home/work/deploy
# && fab -f course_deploy.py local_pack:version=$tag
# && fab -f course_deploy.py deploy:version=$tag
# && fab -f course_deploy.py local_clean:version=$tag;

# 或者: fab -f course_deploy.py local_pack:version=$tag deploy:version=$tag local_clean:version=$tag
