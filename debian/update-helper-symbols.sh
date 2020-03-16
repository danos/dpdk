#!/bin/bash
if [ "$#" -lt 2 ]; then
    echo "Need at least two arguments"
    echo "Usage: $0 <newversion> <symbol-files>..."
fi

newv=${1}

for symbolf in ${@:2}
do
    echo "modifying ${symbolf}"
    perl -pi -e "s/\.so\.[0-9.]*/.so.${newv}/g" "${symbolf}"
    perl -pi -e "s/[0-9.]* #MINVER#/${newv} #MINVER#/g" "${symbolf}"
done
