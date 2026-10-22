#!/bin/sh
set -eu
exec socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/app/overflow,stderr
