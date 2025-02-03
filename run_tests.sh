#!/bin/bash
coverage run --source=phaseOne -m unittest discover
coverage report -m
coverage html
echo "Open htmlcov/index.html in a browser to view coverage details."
