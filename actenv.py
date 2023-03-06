import os
import sys

# os.system('cmd "/K" C:\ProgramData\Anaconda3\Scripts\\activate.bat C:\ProgramData\Anaconda3')

# os.system('cmd "/K" C:\ProgramData\Anaconda3\Scripts\\activate.bat C:\\Users\ADITYA\\.conda\envs\pycoin')


def activate_module(module):
    os.system('cmd "/K" C:\ProgramData\Anaconda3\Scripts\\activate.bat C:\\Users\ADITYA\\.conda\envs\{}'.format(module))

activate_module(sys.argv[1])
