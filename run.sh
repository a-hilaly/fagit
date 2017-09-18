#!/bin/bash


_GIT_USER="ial-bot"
_GIT_PW="uehMLMRwIALBOT0"
_ORGANISATION="iallabs"
export _GIT_USER
export _GIT_PW
export _ORGANISATION

python3 bavtu-sos-packaging.py "$@"
