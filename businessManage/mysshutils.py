#coding=utf-8
'''
Created on 2014年12月9日
ssh工具类
@author: boring2
'''
#coding=utf-8
import paramiko
import os
from socket import error
import traceback

server_user = 'root'
server_passwd = 'coship'
server_port = 22
    
class Myssh:
    def __init__(self,server_ip):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.server_ip = server_ip
            self.ssh.connect(self.server_ip,server_port,server_user,server_passwd)
            #return self.ssh
        except error as err:
            f=open("log.txt",'a') 
            traceback.print_exc(file=f) 
            f.write("请求出错"+err)
            f.flush() 
            f.close()
            #print "请求出错" + err
        
    def getClient(self):
        self.client = paramiko.Transport((self.server_ip, server_port))
        
        
    def ssh_disconnect(self):
        self.client.close()

        
    def win_to_linux(self,localpath,remotepath):
        '''
        windows向linux服务器上传文件.
        localpath  为本地文件的绝对路径。如：D:  est.py
        remotepath 为服务器端存放上传文件的绝对路径,而不是一个目录。如：/tmp/my_file.txt
        '''
        if os.path.exists(localpath):
            if os.path.isfile(localpath):
                try:
                    filename = os.path.basename(localpath)
                    remotepath = os.path.split(remotepath)[0]
                    #print 'filename'+filename 
                    self.getClient()
                    self.client.connect(username = server_user, password = server_passwd)
                    sftp = paramiko.SFTPClient.from_transport(self.client)
                    if remotepath.endswith('/'):
                        remotepath = remotepath + filename
                    else:
                        remotepath = remotepath + '/' + filename
                    #print('remote',remotepath)
                    sftp.put(localpath,remotepath)
                except:
                    f=open("log.txt",'a') 
                    traceback.print_exc(file=f) 
                    f.write("上传出错")
                    f.flush() 
                    f.close()
                    
            else:
                return "不是文件"
                
