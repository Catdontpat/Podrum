"""
*  ____           _
* |  _ \ ___   __| |_ __ _   _ _ __ ___
* | |_) / _ \ / _` | '__| | | | '_ ` _ \
* |  __/ (_) | (_| | |  | |_| | | | | | |
* |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
"""

import time
import os

from podrum.lang.Base import Base
from podrum.utils.Logger import Logger
from podrum.utils.ServerFS import ServerFS
from podrum.utils.Utils import Utils
from podrum.wizard.Wizard import Wizard

from pyraklib.server.PyRakLibServer import PyRakLibServer
from pyraklib.server.ServerHandler import ServerHandler


class Server:

    path = None
    withWizard = None
    port = 19132
    podrumLogo = """
            ____           _                      
           |  _ \ ___   __| |_ __ _   _ _ __ ___  
           | |_) / _ \ / _` | '__| | | | '_ ` _ \ 
           |  __/ (_) | (_| | |  | |_| | | | | | |
           |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
    """

    def __init__(self, path, withWizard, isTravisBuild = False):
        super().__init__()
        self.path = path
        self.withWizard = withWizard
        if(withWizard):
            ServerFS.checkAllFiles(path)
        else:
            Wizard.skipWizard(path)
        port = self.port
        print(str(self.podrumLogo))
        Wizard.isInWizard = False
        Logger.log('info',  str(Base.get("startingServer")).replace("{ip}", str(Utils.getPrivateIpAddress())).replace("{port}", str(port)))
        Logger.log('info', str(Base.get("extIpMsg")).replace("{ipPublic}", str(Utils.getPublicIpAddress())))
        Logger.log('info', str(Base.get("license")))
        server = PyRakLibServer(port=19132)
        handler = ServerHandler(server, None)
        handler.sendOption("name", "MCPE;Podrum powered server;390;1.14.60;0;0;0;PodrumPoweredServer;0")
        if (isTravisBuild):
            print("Build success.")
            os._exit(0)
        else:
            while Wizard.isInWizard == False:
                cmd = input('> ')
                Server.command(cmd, True)
                cmd = None
            ticking = True
            while ticking:
                time.sleep(0.002)

    def command(string, fromConsole):
        if string.lower() == 'stop':
            Logger.log('info', 'Stopping server...')
            Utils.killServer()
        elif string.lower() == '':
            pass
        elif string.lower() == 'help':
            Logger.log('info', '/stop: Stops the server')
        else:
            Logger.log('error', str(Base.get("invalidCommand")))