#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' shared utility functions '''
import subprocess
import os
import json
import time
from threading import Timer


def run_command_noret(command, timeout=None):
    ''' execute command with subprocess and capture output '''
    with open(os.devnull, 'wb') as devnull:
        process = subprocess.Popen(command,
                                   stdout=devnull,
                                   stderr=devnull,
                                   shell=True)

        try:
            if timeout is not None:
                timer = Timer(timeout, kill_process, args=(process, timeout))
                timer.start()

            process.communicate()
        except Exception:
            print 'process communicate error'
        finally:
            kill_process(process)
            if timeout is not None:
                timer.cancel()


def kill_process(process, timeout=None):
    ''' try to kill the subprocess.Popen() ed process '''
    pid = process.pid
    try:
        process.terminate()
    except Exception:
        pass

    # Check if the process has really terminated & force kill if not.
    time.sleep(1)
    try:
        os.kill(pid, 9)
        # process.kill()
    except OSError:
        pass
    if timeout is not None:
        print '''process terminated with timeout ({})'''.format(timeout)



def build_cmd(cmd_file, basedir=None):
    ''' parse command file and build execute command of binary '''

    cmd = []
    basedir = basedir if basedir is not None else os.path.dirname(cmd_file)

    with open(cmd_file, 'r') as f_cmd:
        cmd_dict = json.load(f_cmd)

    cmd_len = cmd_dict.get('cmd_len')

    for idx in range(cmd_len):
        detail = cmd_dict.get('pos_{}'.format(idx))
        if detail['type'] in ('opt', 'input'):
            cmd.append(detail['value'])
        else:
            target = '{}/{}/{}'.format(basedir, detail['type'], detail['target'])
            cmd.append(detail['value'].format(target))

    return cmd
