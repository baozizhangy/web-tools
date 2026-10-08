#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import paramiko
import os

class FTPClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.sftp = None

    def connect(self):
        """
        连接 SFTP 服务器
        """
        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def list_directory(self, directory='.'):
        """
        列出当前目录下的文件和目录
        """
        return self.sftp.listdir(directory)

    def upload_file(self, local_file, remote_file):
        """
        上传文件到 SFTP 服务器
        """
        print(f"Uploading: {local_file} to: {remote_file}")
        # 读取本地图片数据
        with open(local_file, 'rb') as file:
            image_data = file.read()
        # print(f"image_data: {image_data} to: {remote_file}")
        try:
            res = self.sftp.put(image_data, remote_file)
        except IOError:
            # 如果远程目录不存在,先创建目录
            remote_dir = os.path.dirname(remote_file)
            self.sftp.mkdir(remote_dir)
            res = self.sftp.put(image_data, remote_file)
        return res

    def upload_dir(self, local_dir, remote_dir):
        try:
            for root, dirs, files in os.walk(local_dir):
                for files_path in files:
                    local_file = os.path.join(root, files_path)
                    a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
                    remote_file = os.path.join(remote_dir, a)
                    try:
                        self.sftp.put(local_file, remote_file)
                    except Exception as e:
                        self.sftp.mkdir(os.path.split(remote_file)[0])
                        self.sftp.put(local_file, remote_file)
                for name in dirs:
                    local_path = os.path.join(root, name)
                    a = local_path.replace(local_dir, '').replace('\\', '')
                    remote_path = os.path.join(remote_dir, a)
                    try:
                        self.sftp.mkdir(remote_path)
                    except Exception as e:
                        print(55, e)
        except Exception as e:
            print(88, e)

    def download_file(self, remote_file, local_file):
        """
        从 SFTP 服务器下载文件
        """
        self.sftp.get(remote_file, local_file)

    def disconnect(self):
        """
        断开 SFTP 服务器连接
        """
        self.sftp.close()
        self.transport.close()


if __name__ == '__main__':
    ftp_client = FTPClient('106.14.56.109', 22, 'sftp_xurong', 'sdkfjksdjKJKf213')
    ftp_client.connect()
    print(f"ftp_client:{ftp_client}")
    # ftp_client.upload_file('/path/to/local/file.txt', '/path/to/remote/file.txt')
    # ftp_client.disconnect()
