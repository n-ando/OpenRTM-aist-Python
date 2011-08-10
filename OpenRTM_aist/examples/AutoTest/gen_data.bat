for /L %%i in (0,1,15) do (
	echo %%i>>original-data-win
	echo %RANDOM% %RANDOM% %RANDOM% %RANDOM% %RANDOM%>>original-data-win
	echo message%%i>>original-data-win
	echo.>>original-data-win
)
