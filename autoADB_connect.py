from http import client
from sys import stderr, stdin, stdout
import paramiko



## DUT Creds
dutHost = ""
dutUser = ""
dutPass = ""

## Performance Host Creds
perfUser = ""
perfPass = ""
perfServer = ""

## Ports
port = 22

## Logs test user into DUT
def runAutoLogin():
    dutClient = paramiko.SSHClient()
    dutClient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    dutClient.connect(dutHost, port, dutUser, dutPass)
    ## Autologin Command
    autoLogin = "/usr/local/autotest/bin/autologin.py --arc --enable_default_apps"
    stdin, stdout, stderr = dutClient.exec_command(autoLogin)
    #stdout.channel.set_combine_stderr(True)
    for line in stdout.readlines():
        print(line)
    dutClient.close()

## Sends ADB connection from Perf host causing 'ADB Connect' popup
def connectADB():
    perfClient = paramiko.SSHClient()
    perfClient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    perfClient.connect(perfServer, port, perfUser, perfPass)
    ## adb connect command
    adbConn = "adb connect " + dutHost
    stdin, stdout, stderr = perfClient.exec_command(adbConn)
    for line in stdout.readlines():
        print(line)
    perfClient.close()

## Creates python script needed to accept ADB connection
def scriptADB():
    dutClient = paramiko.SSHClient()
    dutClient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    dutClient.connect(dutHost, port, dutUser, dutPass)

    ## File for python script
    touchFile = "touch /home/adbconnect.py; chmod 755 /home/adbconnect.py"
    dutClient.exec_command(touchFile)
    ## File contents
    adbConn = ['import uinput', 'import time',\
        'device = uinput.Device([uinput.KEY_ENTER, uinput.KEY_TAB, uinput.KEY_W, uinput.KEY_LEFTCTRL])', \
            'device.emit_click(uinput.KEY_TAB)', 'time.sleep(1)', 'device.emit_click(uinput.KEY_TAB)', 'time.sleep(1)',\
                'device.emit_click(uinput.KEY_TAB)', 'time.sleep(1)', 'device.emit_click(uinput.KEY_ENTER)',\
                   'time.sleep(1)', 'device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_W])' ]

    for cmd in adbConn:
            stdin, stdout, stderr = dutClient.exec_command("echo " + "'" + cmd + "'" + " >> /home/adbconnect.py" )
    for line in stderr.readlines():
        print(line)
    dutClient.close()

## Run python script to accept ADB connection
def acceptADB():
    dutClient = paramiko.SSHClient()
    dutClient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    dutClient.connect(dutHost, port, dutUser, dutPass)
    ## Accept ADB connection from popup
    clickAccept = "python /home/adbconnect.py"
    stdin, stdout, stderr = dutClient.exec_command(clickAccept)

    for line in stdout.readlines():
        print(line)

runAutoLogin()
connectADB()
scriptADB()
acceptADB()
