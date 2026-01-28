# 中国反洗钱 (AML) 合规监测日报

这是一个自动化的反洗钱合规信息聚合工具。它能够每日自动监测中国人民银行、国家金融监督管理总局等官方渠道，汇总当天的反洗钱政策、罚单及监管动态，并通过微信推送简报。

## 核心功能

- **🌏 全网监测**: 自动扫描央行、金管局、证监会等官方网站及权威财经媒体。
- **🧹 智能聚合**: 自动清洗无关信息，提取核心的政策要点与处罚事实。
- **📱 微信推送**: 每日定时将合规简报推送到您的微信。

## 💡 技术原理：为什么选择这种架构？

本项目摒弃了传统的“爬虫脚本 + 规则解析”模式，而是采用 **GitHub Actions + LLM Search Grounding** 的新型 Serverless 架构，彻底解决了爬虫维护难的痛点。

### 1. 动态检索 (AI as a Browser)
传统爬虫需要针对每个网站编写特定的解析规则（CSS/XPath），一旦官网改版即失效。
本系统利用数据引擎的 **Search Grounding（搜索落地）** 能力，像人类一样通过自然语言指令（如“查找今日央行反洗钱公告”）调用 Google 搜索接口。这意味着**无论源网站如何改版，只要它能被搜索引擎收录，本系统就能监测到**。

### 2. 语义清洗 (AI as a Filter)
搜索搜回的内容往往包含大量噪音（广告、无关新闻、过往旧闻）。本系统利用大模型的语义理解能力，充当一名“合规分析师”，严格依据 `prompt_template` 的标准进行筛选，**只提取实质性的监管动作**，自动过滤营销软文。

### 3. Zero Ops (零运维成本)
- **无服务器**：完全托管在 GitHub Actions 云端运行。
- **无数据库**：即时计算，即时推送。
- **零费用**：依赖 GitHub 免费额度和 API 免费层级，适合个人或小团队持续运行。

## 🚀 部署指南 (GitHub Actions)

本项目基于 GitHub Actions 实现全自动运行，无需自备服务器。

### 1. 建立文件夹结构

如果您是手动上传文件，请务必保证仓库中包含以下目录结构（这对自动化运行至关重要）：

```text
您的仓库名称/
├── .github/
│   └── workflows/
│       └── daily.yml      <-- 必须放在此处，用于定时任务
├── scripts/
│   └── daily-task.js      <-- (如有) 辅助脚本路径
├── main.py                <-- 主程序
├── prompt_template.txt    <-- 模板文件
└── requirements.txt
```

### 2. 配置密钥 (Secrets)

进入仓库的 **Settings (设置)** -> **Secrets and variables** -> **Actions**，点击 **New repository secret** 添加以下变量：

| 变量名 | 描述 | 获取方式 |
| :--- | :--- | :--- |
| `API_KEY` | **数据处理引擎密钥**<br>用于驱动底层的分析与汇总能力 (Google GenAI SDK)。 | [获取 Google API Key](https://aistudio.google.com/app/apikey) |
| `PUSH_TOKEN` | **微信推送 Token** (可选)<br>用于将结果推送到微信。 | [PushPlus 官网](http://www.pushplus.plus/) |

### 3. 验证运行

配置完成后，点击仓库上方的 **Actions** 标签页。
- 您应该能看到名为 "Daily AML Report" 的工作流。
- 它可以配置为每天自动运行（默认北京时间早晨），也可以点击 "Run workflow" 手动触发测试。

---

## 本地运行

1. 克隆仓库:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```
3. 设置环境变量并运行:
   ```bash
   # Windows Powershell
   $env:API_KEY="您的密钥"
   python main.py
   ```
