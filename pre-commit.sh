#!/bin/sh
# To use this as a pre-commit hook add a file "prec-commit" to .git/hooks with content
# (without '#' at the start of the lines):
#    #!/bin/sh
#
#    sh ./pre-commit.sh

#!/usr/bin/env bash

# If any command fails, exit immediately with that command's exit status
set -eo pipefail

make lint
make static-checks | grep "Error 1 (ignored)"
