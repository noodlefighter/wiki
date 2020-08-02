#!/bin/bash

cd "$(dirname "$0")"
PYTHONPATH=$PWD python ./mkdocs/ serve
