from fabric import Connection, Config, SerialGroup
import os
from pathlib import PureWindowsPath

class RemoteConnect():
    def __init__(self, hosts, username, password):
        config = Config(overrides={'user': username, 'sudo': {'password': password}, 'connect_kwargs': {'password': password}})

        self.username = username
        for h in hosts:
            if os.system("ping /n 1 " + h) != 0:
                hosts.remove(h)
        
        if len(hosts) == 0:
            print('Hosts are unreachable, please verify that hosts are online')
        else:
            self.c = SerialGroup(*hosts, config=config)
            

    def file_transfer(self, paths, destination):
        for path in paths:
            self.c.put(path, remote=destination)

    def execute(self, command):
        self.c.run(command)
    
    def sudo_execute(self, command):
        self.c.sudo(command)

    def send_and_unzip(self, path):
        destination = f'/home/{self.username}/Desktop'
        file = PureWindowsPath(path)
        self.c.put(path, destination)
        self.c.run(f'tar -C {destination} -xzvf {destination}/{file.name}')

    def update_all(self):
        self.c.sudo('apt-get update')
    


def remote_connect(host, username, password):
    config = Config(overrides={'user': username, 'sudo': {'password': password}, 'connect_kwargs': {'password': password}})

    c = Connection(host=host, config=config)
    c.sudo("apt-get update")





