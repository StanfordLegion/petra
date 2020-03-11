#!/bin/bash

export MYPYPATH=$PWD/stubs

strict_flags="--disallow-any-unimported --disallow-any-expr --disallow-any-decorated --disallow-any-explicit --disallow-any-generics --disallow-subclassing-any"

mypy petra --disallow-any-unimported --disallow-any-decorated --disallow-any-explicit --disallow-any-generics --disallow-subclassing-any # --disallow-any-expr
mypy examples $strict_flags
mypy tests $strict_flags
