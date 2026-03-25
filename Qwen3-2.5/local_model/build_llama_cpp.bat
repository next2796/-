@echo off
chcp 65001
setlocal EnableDelayedExpansion

echo ==========================================
echo Building llama.cpp for Windows
echo ==========================================

:: Check for Visual Studio Build Tools
set "VS_PATH="
for /f "delims=" %%i in ('"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -property installationPath 2^>nul') do set "VS_PATH=%%i"

if not defined VS_PATH (
    echo Visual Studio Build Tools not found!
    echo Please install Visual Studio Build Tools from:
    echo https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
    pause
    exit /b 1
)

echo Found Visual Studio at: %VS_PATH%

:: Setup environment
set "VSCMD_START_DIR=%CD%"
call "%VS_PATH%\VC\Auxiliary\Build\vcvarsall.bat" x64

if errorlevel 1 (
    echo Failed to setup Visual Studio environment
    pause
    exit /b 1
)

:: Check for CMake
where cmake >nul 2>nul
if errorlevel 1 (
    echo CMake not found in PATH!
    echo Please install CMake from: https://cmake.org/download/
    pause
    exit /b 1
)

echo.
echo CMake version:
cmake --version

echo.
echo ==========================================
echo Configuring build...
echo ==========================================

cd llama.cpp

if exist build (
    echo Cleaning old build directory...
    rmdir /s /q build
)

cmake -B build -G "Visual Studio 17 2022" -A x64 -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=ON -DLLAMA_BUILD_SERVER=ON

if errorlevel 1 (
    echo CMake configuration failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Building llama.cpp (Release mode)...
echo ==========================================

cmake --build build --config Release --parallel

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Build completed successfully!
echo ==========================================
echo.
echo Binaries are located at: llama.cpp\build\bin\Release\
echo.
echo To run llama-server:
echo   llama.cpp\build\bin\Release\llama-server.exe -m ..\qwen2.5-0.5b-instruct-q5_0.gguf -c 2048
echo.

pause
