#!/bin/bash
source bin/activate
python3 systemrdl2jinjatemplate.py $1 $2 $3
source bin/deactivate
