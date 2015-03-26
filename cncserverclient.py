import logging
import json
import os
import requests

class CNCServerClient:
    """
    Connects to CNCServer and sends commands to the WaterColorBot for drawing purpouses
    """
    hasConnection = False

    def __init__(self, cncserver_address="http://localhost:4242", cncserver_args=""):
        # Create Logging instance
        self.logger = logging.getLogger('CNCClient')
        self.logger.debug('Client instance created!')
        self.cncserver_address = cncserver_address
        self.cncserver_args = cncserver_args

        # Attempt to connect to an already running CNCServer instance
        try:
            r = requests.get(self.cncserver_address+'/v1/settings/global',  timeout = 1)
            self.hasConnection = True
        except requests.exceptions.ConnectionError as er:
            # If we cannot connect, send an error message
            self.logger.critical('Could not create connection to external server!')
            self.hasConnection = False

            # And start our own internal CNCServer
            if self.launchCncServer():
                self.hasConnection = True

    def setPenPos(self,x,y):
        """
        Set the position of the robot's implement
        """
        if not self.hasConnection: return

        # Assemble packet and compress it into a JSON formatted string
        data = {'x':str(x),'y':str(y)}
        data_json = json.dumps(data)

        try:
            # Send the pen data to the server
            r = requests.put(self.cncserver_address+'/v1/pen/', data=data, timeout = 0.01)
        except requests.exceptions.ReadTimeout: pass
        except requests.exceptions.ConnectTimeout:
            # Ignore timeouts on the returned status
            pass

    def setPenHeight(self, height):
        """
        Set the position of the robot's implement
        """
        if not self.hasConnection: return

        # Assemble packet and compress it into a JSON formatted string
        data = {'state': str(height)}
        data_json = json.dumps(data)

        try:
            # Send the pen data to the server
            r = requests.put(self.cncserver_address+'/v1/pen/', data=data, timeout = 0.01)
        except requests.exceptions.ReadTimeout: pass
        except requests.exceptions.ConnectTimeout:
            # Ignore timeouts on the returned status
            pass

    def setPenSpeed(self, speed_drawing, speed_moving):
        """
        Set the speed of the robot
        """
        if not self.hasConnection: return

        # Assemble packet and compress it into a JSON formatted string
        data = {"speed:drawing": speed_drawing, "speed:moving": speed_moving}
        data_json = json.dumps(data)

        try:
            # Send the pen data to the server
            r = requests.put(self.cncserver_address+'/v1/settings/bot', data=data, timeout = 0.01)
        except requests.exceptions.ReadTimeout: pass
        except requests.exceptions.ConnectTimeout:
            # Ignore timeouts on the returned status
            pass


    def getPenStatus(self):
        try:
            # Send the pen data to the server
            r = requests.get(self.cncserver_address+'/v1/pen/', timeout = 0.01).text
        except requests.exceptions.ReadTimeout:
            r = "{}"
        except requests.exceptions.ConnectTimeout:
            # Ignore timeouts on the returned status
            r = "{}"
        return json.loads(r)


    def setPenPosScaled(self, pos, size):
        """
        Sets the pen position to 'pos', but scaling it as a percentage of 'size'
        """
        x = 100*(pos[0]/float(size[0]))
        y = 100*(pos[1]/float(size[1]))
        self.setPenPos(x,y)

    def setTool(self, toolname):
        try:
            # Send the pen data to the server
            r = requests.put(self.cncserver_address + '/v1/tools/' + toolname, timeout = 0.01)
        except requests.exceptions.ReadTimeout: pass
        except requests.exceptions.ConnectTimeout:
            # Ignore timeouts on the returned status
            pass

    def parkPen(self):
        try:
            # Send the request to the server
            r = requests.delete(self.cncserver_address + '/v1/pen/', timeout = 0.01)
        except requests.exceptions.ReadTimeout: pass
        except requests.exceptions.ConnectTimeout:
            # Ignore timeouts on the returned status
            pass

    def launchCncServer(self):
        """
        Looks for a built-in CNCServer instance at ../cncserver/ and launches it.
        """
        # Check if CNCserver actually exists first
        if os.path.exists("cncserver/cncserver.js"):
            self.logger.info('Built-In CNCServer exists!')

            # Start CNCServer as it's own process
            self.serverProcess = subprocess.Popen(['node', 'cncserver.js', self.cncserver_args],
                                                  stdout=subprocess.PIPE,
                                                  cwd = 'cncserver')
            # Create a new logging instance for CNCServer
            serverLog = logging.getLogger('CNCServer')

            # Start a thread to log the output from the thread
            self.loggigngThread = threading.Thread(target=self._outputHandlingThread,
                                                   args = (serverLog, self.serverProcess,))
            self.loggigngThread.start()
        else:
            self.logger.error('CNCServer not found at ../cncserver/cncserver.js')

    def _outputHandlingThread(self,logger, serverInstance):
        # Send output from the CNCServer thread to the log
        while True:
            # Read a line and strip the extra newline character. Blocking operation
            line = serverInstance.stdout.readline().replace('\n','')
            logger.info(line)

            # If the output from CNCServer indicates it's ready, then we can send commands to it
            if 'is ready to receive commands' in line: self.hasConnection = True
