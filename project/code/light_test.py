#!/usr/bin/env python3
from light_controller.controller import BaseController
import sys
from time import sleep
controller = BaseController()
controller.work_once(int(sys.argv[1]))
sleep(2)
