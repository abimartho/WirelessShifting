import subprocess
from pymemcache.client import base
import time

class Shifter():
    def __init__(self, address="00:A0:50:BD:38:21"):
        self.address = address

        self.command = ['screen', '-s', 'shifting', '-X', 'stuff']
        self.connect = self.command.copy()
        self.connect.append('connect^M')
        
        self.file = open('results.txt', 'r+')

        self.gear = base.Client(('localhost',11211))
        self.read_gear()
        self.max = 9
        self.min = 1

    def write_gear(self, offset):
        goal = int(self.gear.get('gear')) + offset
        if goal > self.max:
            print("Gear is too large")
            return
        if goal < self.min:
            print("Gear is too small")
            return
        print("Attempting to write gear ", goal)
        
        self.attempt_connect()
        to_write = format(goal, '02x')
        
        write = self.command.copy()
        write.append('char-write-req 0x0012 {}^M'.format(to_write))
        subprocess.run(write)
        
        self.gear.set('gear', goal)

    def read_gear(self):
        print("Reading Gear")
        self.attempt_connect()
         
        read = self.command.copy()
        read.append('char-read-hnd 0x0012^M')
        subprocess.run(read)
        time.sleep(1)
        
        msg = self.file.readlines()[-2]
        curr_gear = int(msg[-4:-2], 16)
        print("Current Gear:", curr_gear)
        
        self.gear.set('gear', curr_gear)

    def attempt_connect(self):
        msg = "Failed"
        while "Failed" in msg or "Error" in msg:
            subprocess.run(self.connect)
            time.sleep(1)
            msg = self.file.readlines()[-2]
