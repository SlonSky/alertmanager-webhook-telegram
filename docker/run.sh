#!/bin/bash
/usr/bin/gunicorn -w 4 -b 0.0.0.0:9119 flaskAlert:app
