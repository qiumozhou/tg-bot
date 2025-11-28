# 安装指南

## 依赖安装问题解决

如果在安装依赖时遇到问题，特别是 Pillow 安装失败，请按照以下步骤操作：

### 方法 1: 使用国内镜像源（推荐）

使用清华大学镜像源安装，速度更快且更稳定：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或者使用阿里云镜像：

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 方法 2: 升级 pip 和构建工具

在安装前先升级 pip 和相关构建工具：

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 方法 3: 单独安装 Pillow

如果 Pillow 安装失败，可以尝试：

```bash
# 使用预编译的 wheel 文件
pip install Pillow --only-binary :all:

# 或者使用国内镜像
pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方法 4: Windows 用户特别说明

如果是在 Windows 上安装失败，可能需要安装 Visual C++ 构建工具：

1. 下载并安装 [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. 在安装时选择 "C++ 桌面开发" 组件
3. 重新尝试安装依赖

### 方法 5: 使用预编译包

如果以上方法都不行，可以尝试安装预编译的二进制包：

```bash
pip install --prefer-binary -r requirements.txt
```

## 完整安装步骤

1. **创建虚拟环境（推荐）**：
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

2. **升级 pip**：
```bash
python -m pip install --upgrade pip setuptools wheel
```

3. **安装依赖**：
```bash
# 使用国内镜像（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用默认源
pip install -r requirements.txt
```

4. **配置环境变量**：
```bash
# 创建 .env 文件
copy config.example.py .env

# 编辑 .env 文件，填入你的配置
```

5. **运行 Bot**：
```bash
python main.py
```

## 常见错误

### 错误: `KeyError: '__version__'` (Pillow 安装失败)

**解决方案**：
- 使用国内镜像源重新安装
- 升级 pip: `python -m pip install --upgrade pip`
- 使用预编译包: `pip install --prefer-binary Pillow`

### 错误: `Microsoft Visual C++ 14.0 is required`

**解决方案**：
- 安装 Visual C++ Build Tools（见方法 4）
- 或使用预编译的 wheel 文件

### 错误: 网络连接超时

**解决方案**：
- 使用国内镜像源
- 增加超时时间: `pip install -r requirements.txt --default-timeout=100`

## 验证安装

安装完成后，验证所有依赖是否正确安装：

```bash
pip list
```

应该能看到以下包：
- python-telegram-bot
- python-dotenv
- sqlalchemy
- aiosqlite
- aiohttp
- Pillow
- loguru

如果还有问题，请检查：
1. Python 版本（建议 Python 3.8+）
2. 网络连接
3. 系统是否有足够的权限

