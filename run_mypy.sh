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
    # --no-incremental # IMPORANT: if you change the flags for MyPy, uncomment this line to flush the cache
)

set -x

mypy petra "${flags[@]}"
mypy examples "${flags[@]}"
mypy tests "${flags[@]}"
