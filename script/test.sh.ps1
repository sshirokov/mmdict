#!/bin/bash
echo --% >/dev/null ; : ' #| Out-Null
<#'

python -m unittest discover -s tests

exit $? #>


#
# powershell part
#
python -m unittest discover -s tests
