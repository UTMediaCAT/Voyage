#!/bin/bash
set -e

dir=`pwd`
sed 's#projectdir:.*$#projectdir: '"${dir}"'#' config.yaml > tmp.yaml
mv tmp.yaml config.yaml
mkdir -p log
