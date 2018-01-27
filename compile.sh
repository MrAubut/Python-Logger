#!/bin/bash -e

pyinstaller --onefile loggingService/LoggingService.py --paths=loggingService/
