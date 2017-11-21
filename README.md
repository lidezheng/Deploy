# Deploy
# 这是一个用python写的代码发布脚本

#### 功能：按照指定的git标签来发布代码。
#### 实现：主要使用到的库是Fabric，可以将本脚本结合Jenkins来实现代码可视化发布。

命令：fab -f course_deploy.py local_pack:version=$tag deploy:version=$tag local_clean:version=$tag

*串行执行三个步骤：*
1. 本地打包
2. 多服务器并行上传、重启(此步骤并行执行)
3. 本地清理
