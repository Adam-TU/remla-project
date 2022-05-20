#!/bin/sh
# To use this as a pre-commit hook add a file "prec-commit" to .git/hooks with content
# (without '#' at the start of the lines):
#    #!/bin/sh
#
#    sh ./pre-commit.sh


make lint
make static-checks