@ECHO OFF
setlocal enabledelayedexpansion
color 3f
title MIO-KITCHEN ��ˢ�ű�
mode con cols=50 lines=20
set fastboot=%cd%\bin\fastboot
set zstd=%cd%\bin\zstd
set sg=1^>nul 2^>nul
if exist bin\right_device (
	set /p right_device=<bin\right_device
)
:HOME
cls
ECHO.    Mio-MIUI
ECHO.[1].����ȫ������ˢ��
ECHO.[2].��ʽ���û�����
ECHO.[3].��ʽ��ȫ������(��ʱ����Ч)
if not "!right_device!"=="" echo.ע��:��ROMרΪ[!right_device!]�������������Ͳ���ˢ�룡����
ECHO.�������� �� ��879232506�� ����
set /p zyxz=��ѡ����Ҫ��������Ŀ��
if "!zyxz!" == "1" set xz=1&goto FLASH
if "!zyxz!" == "2" set xz=2&goto FLASH
if "!zyxz!" == "3" set xz=3&goto FLASH
goto HOME&pause
:FLASH
cls
ECHO.�ֻ�����ΪBootloaderģʽ, ���ڵȴ��豸
for /f "tokens=2" %%a in ('!fastboot! getvar product 2^>^&1^|find "product"') do set DeviceCode=%%a
for /f "tokens=2" %%a in ('!fastboot! getvar slot-count 2^>^&1^|find "slot-count" ') do set fqlx=%%a
if "!fqlx!" == "2" (set fqlx=AB)  else (set fqlx=A)
ECHO.�����豸:[!DeviceCode!]
if not "!DeviceCode!"=="!right_device!" (
		color 4f
		echo "��ROM��Ϊ !right_device! ������������豸�� !DeviceCode!"
		PAUSE
		GOTO :EOF
)
if "!fqlx!"=="A" (
for /f "delims=" %%b in ( 'dir /b images ^| findstr /v /i "super.img" ^| findstr /v /i "preloader_raw.img" ^| findstr /v /i "cust.img"' ) do (
echo ����ˢ��%%~nb�����ļ���
!fastboot! flash %%~nb images\%%~nxb %sg%
if "!errorlevel!"=="0" (echo ˢ�� %%~nb ���) else (echo ˢ�� %%~nb ʱ���ִ���-����!errorlevel!)
)
) else (
for /f "delims=" %%b in ( 'dir /b images ^| findstr /v /i "super.img" ^| findstr /v /i "preloader_raw.img" ^| findstr /v /i "cust.img"' ) do (
echo ����ˢ��%%~nb�����ļ���
!fastboot! flash %%~nb_a images\%%~nxb %sg%
!fastboot! flash %%~nb_b images\%%~nxb %sg%
if "!errorlevel!"=="0" (echo ˢ�� %%~nb ���) else (
	!fastboot! flash %%~nb images\%%~nxb %sg%
	if not "!errorlevel!"=="0" (
	echo ˢ�� %%~nb ʱ���ִ���-����!errorlevel!)
)
))
if exist images\cust.img !fastboot! flash cust images\cust.img
if exist images\preloader_raw.img (
!fastboot! flash preloader_a images\preloader_raw.img !sg!
!fastboot! flash preloader_b images\preloader_raw.img !sg!
!fastboot! flash preloader1 images\preloader_raw.img !sg!
!fastboot! flash preloader2 images\preloader_raw.img !sg!
)
for /f "delims=" %%a in ('dir /b "images\*.zst"')do (
echo.����ת�� %%~na
!zstd! --rm -d images/%%~nxa -o images/%%~na
echo ��ʼˢ�� %%~na
set name=%%~na
!fastboot! flash !name:~0,-4! images\%%~na
)
if "!xz!" == "1" echo �ѱ���ȫ������,׼��������
if "!xz!" == "2" (echo ���ڸ�ʽ��DATA
!fastboot! erase userdata
!fastboot! erase metadata)
if "!xz!" == "3" (
echo ���ڸ�ʽ�������û�����
!fastboot! -w)
if "!fqlx!"=="AB" (!fastboot! set_active a %sg%)
!fastboot! reboot
echo.ˢ����� ��лʹ��MIO-KITCHEN����
pause
exit