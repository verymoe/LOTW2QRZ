# LOTW2QRZ
Automatically sync LOTW to QRZ

# Run QRZ Sync Script

## English Version

### Purpose of the Script

This script automates the process of logging into QRZ.com and synchronizing Logbook of The World (LoTW) entries. It handles two-factor authentication using a TOTP secret and interacts with QRZ.com to retrieve a login ticket, authenticate, and perform the synchronization.

### How to Use

1. **Environment Variables Configuration:**
   - `USERNAME`: Your QRZ username.
   - `PASSWORD`: Your QRZ password.
   - `SECRET`: Your TOTP secret key for generating two-factor authentication codes.
   - `BID`: Your QRZ logbook ID.
   - `LOTW_PW`: Your LoTW password.

2. **Modify and Schedule the Script:**
   - The provided YAML configuration is for a GitHub Actions workflow, which schedules the script to run daily at midnight UTC.
   - To modify the schedule, change the cron expression in the YAML file. For example, to run it at a different time or more frequently.
   - To run the script manually, ensure the environment variables are set in your local environment or GitHub repository secrets, and execute the Python script.

**Note:** This script was created as a quick solution and has not been tested without two-factor authentication enabled. The functionality without 2FA is therefore not guaranteed.

## 中文版本

### 脚本用途

该脚本自动化了登录 QRZ.com 和同步世界日志册（LoTW）条目的过程。它使用 TOTP 秘钥处理双因素认证，并与 QRZ.com 交互以检索登录票证、认证和执行同步操作。

### 如何使用

1. **环境变量配置：**
   - `USERNAME`：您的 QRZ 用户名。
   - `PASSWORD`：您的 QRZ 密码。
   - `SECRET`：用于生成双因素认证代码的 TOTP 秘钥。
   - `BID`：您的 QRZ 日志册 ID。
   - `LOTW_PW`：您的 LoTW 密码。

2. **修改和计划脚本执行时间：**
   - 提供的 YAML 配置是用于 GitHub Actions 工作流程的，该工作流程将脚本设置为在 UTC 时间午夜每天运行一次。
   - 要修改计划，更改 YAML 文件中的 cron 表达式。例如，要在不同时间或更频繁地运行它。
   - 要手动运行脚本，请确保环境变量在您的本地环境或 GitHub 仓库秘密中设置，并执行 Python 脚本。

**注意：** 这个脚本是作为一个快速解决方案创建的，并且没有在未启用双因素认证的情况下进行测试。因此，不保证在没有 2FA 的情况下的功能。
