#!/bin/bash

set -e

export MYPYPATH=$PWD/stubs

flags=(
    --disallow-any-unimported
    --disallow-any-expr
    --disallow-any-decorated
    --disallow-any-explicit
    --disallow-any-generics
    --disallow-subclassing-any
    --disallow-untyped-calls
    --disallow-untyped-defs
    --disallow-incomplete-defs
    --disallow-untyped-decorators
    --warn-redundant-casts
    --warn-unused-ignores
    --warn-return-any # redundant with --disallow-any-expr, but less strict
    --warn-unreachable
     --no-incremental # IMPORANT: incremental mode seems to be buggy, at least as of version 0.770
)

set -x

mypy petra "${flags[@]}"
mypy examples "${flags[@]}"
mypy tests "${flags[@]}"
