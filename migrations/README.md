# D1 数据库迁移指南

本目录包含 Cloudflare D1 数据库的迁移脚本。

## 前置要求

1. 安装 Wrangler CLI
```bash
npm install -g wrangler
```

2. 登录 Cloudflare 账户
```bash
wrangler login
```

## 创建 D1 数据库

如果你还没有创建 D1 数据库，运行以下命令：

```bash
wrangler d1 create tg-bot-db
```

命令执行后会返回数据库的 ID，类似：
```
✅ Successfully created DB 'tg-bot-db'!

[[d1_databases]]
binding = "DB"
database_name = "tg-bot-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**重要：** 将返回的 `database_id` 更新到 `wrangler.toml` 文件中！

## 执行数据库迁移

### 本地开发环境（可选）

```bash
wrangler d1 execute tg-bot-db --local --file=./migrations/schema.sql
```

### 生产环境

```bash
wrangler d1 execute tg-bot-db --remote --file=./migrations/schema.sql
```

**注意：** 使用 `--remote` 标志将更改应用到生产数据库。

## 验证数据库

查看数据库信息：

```bash
wrangler d1 info tg-bot-db
```

查询数据库表：

```bash
wrangler d1 execute tg-bot-db --remote --command="SELECT name FROM sqlite_master WHERE type='table'"
```

## 数据库表结构

- `users` - 用户信息表
- `orders` - 订单表
- `payments` - 支付记录表
- `transactions` - 交易记录表

详细的表结构和字段说明请查看 `schema.sql` 文件。

## 常用命令

### 备份数据（导出）

```bash
wrangler d1 export tg-bot-db --remote --output=backup.sql
```

### 清空所有表（谨慎使用）

```bash
wrangler d1 execute tg-bot-db --remote --command="DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS payments; DROP TABLE IF EXISTS transactions;"
```

### 重新创建表

```bash
wrangler d1 execute tg-bot-db --remote --file=./migrations/schema.sql
```

---

**作者**: @author seven  
**时间**: @since 2025-11-28

