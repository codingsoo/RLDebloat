#!/bin/bash

NAME=basic2
SRC=$NAME.c
BIN=$NAME

clang -w -o $BIN $SRC >& /dev/null || exit 1
./$BIN >& /dev/null || exit 1
rm $BIN
