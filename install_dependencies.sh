#!/bin/bash
# 依赖安装脚本 (Linux/Mac)
# 使用国内镜像源安装依赖，避免网络问题和构建错误

echo "========================================"
echo "Telegram Bot 依赖安装脚本"
echo "========================================"
echo ""

# 升级 pip
echo "[1/3] 升级 pip 和构建工具..."
python3 -m pip install --upgrade pip setuptools wheel -i https://pypi.tuna.tsinghua.edu.cn/simple

# 先安装 Pillow（使用预编译包）
echo ""
echo "[2/3] 安装 Pillow（使用预编译包）..."
python3 -m pip install Pillow --only-binary :all: -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装其他依赖
echo ""
echo "[3/3] 安装其他依赖..."
python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo ""
echo "========================================"
echo "安装完成！"
echo "========================================"

