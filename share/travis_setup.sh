#!/bin/bash
set -evx

mkdir ~/.gentariumcore

# safety check
if [ ! -f ~/.gentariumcore/.gentarium.conf ]; then
  cp share/gentarium.conf.example ~/.gentariumcore/gentarium.conf
fi
