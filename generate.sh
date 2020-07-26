#!/bin/bash

set -e

cd "$(dirname "$0")"
PYTHONPATH=$PWD python ./mkdocs/ build

