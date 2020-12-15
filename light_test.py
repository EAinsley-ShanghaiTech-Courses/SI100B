#!/usr/bin/env python3
from light_controller.controller import BaseController
import sys
controller = BaseController()
controller.work_once(sys.argv[1])