@echo off

setlocal
:PROMPT
SET /P PROMPT=Do you want to run the scripts before accessing your venv (y/n)? 
IF /I "%PROMPT%" NEQ "y" GOTO END

echo Running package cleanup...
cmd /k "cd /d venv\Scripts & activate & cd /d ..\..\scripts & python _RUN_ALL.py & exit"
echo.

:END
endlocal

setlocal
:PROMPT
SET /P PROMPT=Do you want to run Facile (y/n)? 
IF /I "%PROMPT%" NEQ "y" GOTO END

echo Running Facile...
cmd /k "cd /d venv\Scripts & activate & cd /d ..\..\src & python facile.py & exit"
echo.

:END
endlocal

setlocal
:PROMPT
SET /P PROMPT=Do you want to build a Facile executable (y/n)? 
IF /I "%PROMPT%" NEQ "y" GOTO END

cmd /k "cd /d venv\Scripts & activate & cd /d ..\..\scripts & python build_exe.py & exit"
echo.

:END
endlocal

echo.
echo Virtual environment activated.
cmd /k venv\Scripts\activate