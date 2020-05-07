#!/bin/bash

arch=$(dpkg --print-architecture)
case $arch in
    amd64|arm64|i386|ppc64el)
        echo "Architecture ${arch} supported, go on with test"
        ;;
    *)
        echo "Architecture ${arch} not supported, SKIP test"
        exit 77
        ;;
esac
