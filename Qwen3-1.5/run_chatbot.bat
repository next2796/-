@echo off

:: 激活 w2v 虚拟环境
call "e:\annaconda\Scripts\activate.bat" w2v

:: 切换到项目目录
cd /d "e:\shi yan dai ma er\Qwen1.5-0.5B-Chat\Qwen3-1.5"

:: 运行集成版 ChatBot
echo 正在启动 Qwen1.5-0.5B ChatBot...
python chatbot.py

:: 暂停以查看输出
pause