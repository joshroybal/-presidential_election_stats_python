#!/bin/sh
set -v
./report.py csv
./report.py flat
./report.py html
