#!/bin/sh

pandoc report.pandoc --from=markdown --listings --citeproc -o report.pdf
