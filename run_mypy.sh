#!/bin/bash

set -e

export MYPYPATH=$PWD/stubs

flags=(
    --disallow-any-unimported
    # --disallow-any-expr
    --disallow-any-decorated
    --disallow-any-explicit
    --disallow-any-generics
    --disallow-subclassing-any
    --disallow-untyped-calls
    --disallow-untyped-defs
    --disallow-incomplete-defs
    --disallow-untyped-decorators
)

set -x

mypy petra "${flags[@]}"
mypy examples "${flags[@]}"
mypy tests "${flags[@]}"
