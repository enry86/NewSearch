#!/bin/sh

latex report.tex
bibtex report.aux
latex report.tex
latex report.tex
dvipdf report.dvi report.pdf
