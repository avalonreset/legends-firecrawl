@echo off
setlocal
if defined PYTHONPATH (
  set "PYTHONPATH=%~dp0..\python;%PYTHONPATH%"
) else (
  set "PYTHONPATH=%~dp0..\python"
)
python -m legends_firecrawl.cli %*
