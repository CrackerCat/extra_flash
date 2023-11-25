@ECHO OFF
setlocal enabledelayedexpansion
color 3f
title MIO-KITCHEN 线刷脚本
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
ECHO.[1].保留全部数据刷入
ECHO.[2].格式化用户数据
ECHO.[3].格式化全部数据(有时候无效)
if not "!right_device!"=="" echo.注意:此ROM专为[!right_device!]制作，其他机型不可刷入！！！
ECHO.驱动程序 到 【879232506】 下载
set /p zyxz=请选择你要操作的项目：
if "!zyxz!" == "1" set xz=1&goto FLASH
if "!zyxz!" == "2" set xz=2&goto FLASH
if "!zyxz!" == "3" set xz=3&goto FLASH
goto HOME&pause
:FLASH
cls
ECHO.手机必须为Bootloader模式, 正在等待设备
for /f "tokens=2" %%a in ('!fastboot! getvar product 2^>^&1^|find "product"') do set DeviceCode=%%a
for /f "tokens=2" %%a in ('!fastboot! getvar slot-count 2^>^&1^|find "slot-count" ') do set fqlx=%%a
if "!fqlx!" == "2" (set fqlx=AB)  else (set fqlx=A)
ECHO.发现设备:[!DeviceCode!]
if not "!DeviceCode!"=="!right_device!" (
		color 4f
		echo "此ROM是为 !right_device! 制作，但你的设备是 !DeviceCode!"
		PAUSE
		GOTO :EOF
)
if "!fqlx!"=="A" (
for /f "delims=" %%b in ( 'dir /b images ^| findstr /v /i "super.img" ^| findstr /v /i "preloader_raw.img" ^| findstr /v /i "cust.img"' ) do (
echo 正在刷入%%~nb分区文件！
!fastboot! flash %%~nb images\%%~nxb %sg%
if "!errorlevel!"=="0" (echo 刷入 %%~nb 完成) else (echo 刷入 %%~nb 时出现错误-代码!errorlevel!)
)
) else (
for /f "delims=" %%b in ( 'dir /b images ^| findstr /v /i "super.img" ^| findstr /v /i "preloader_raw.img" ^| findstr /v /i "cust.img"' ) do (
echo 正在刷入%%~nb分区文件！
!fastboot! flash %%~nb_a images\%%~nxb %sg%
!fastboot! flash %%~nb_b images\%%~nxb %sg%
if "!errorlevel!"=="0" (echo 刷入 %%~nb 完成) else (
	!fastboot! flash %%~nb images\%%~nxb %sg%
	if not "!errorlevel!"=="0" (
	echo 刷入 %%~nb 时出现错误-代码!errorlevel!)
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
echo.正在转换 %%~na
!zstd! --rm -d images/%%~nxa -o images/%%~na
echo 开始刷入 %%~na
set name=%%~na
!fastboot! flash !name:~0,-4! images\%%~na
)
if "!xz!" == "1" echo 已保留全部数据,准备重启！
if "!xz!" == "2" (echo 正在格式化DATA
!fastboot! erase userdata
!fastboot! erase metadata)
if "!xz!" == "3" (
echo 正在格式化所有用户数据
!fastboot! -w)
if "!fqlx!"=="AB" (!fastboot! set_active a %sg%)
!fastboot! reboot
echo.刷机完毕 感谢使用MIO-KITCHEN工具
pause
exit