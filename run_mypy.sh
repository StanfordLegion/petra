#!/bin/bash

strict_flags="--disallow-any-unimported --disallow-any-expr --disallow-any-decorated --disallow-any-explicit --disallow-any-generics --disallow-subclassing-any"

mypy petra
mypy examples $strict_flags
mypy tests $strict_flags
