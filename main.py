import os
import requests
from datetime import datetime
from google import genai
from google.genai import types

# --- 配置区域 ---
API_KEY = os.environ.get("API_KEY") 
PUSH_TOKEN = os.environ.get("PUSH_TOKEN")

# 配置 Gemini
if not API_KEY:
    print("❌ 错误：未找到 API_KEY (Gemini)。请在 GitHub Secrets 中配置1。")
    exit(1)

# 初始化新版客户端
client = genai.Client(api_key=API_KEY)

# 模型名称
MODEL_NAME = "gemini-2.5-flash"

def generate_aml_report():
    print(f"🤖 正在调用 {MODEL_NAME} 并使用 Google 搜索...")
    
    current_date = datetime.now().strftime("%Y年%m月%d日")
    
    # 提示词
    # 读取提示词模板
    try:
        with open("prompt_template.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print("❌ 错误：未找到 prompt_template.txt 文件")
        return None

    # 填充日期
    prompt = prompt_template.format(date=current_date)

    try:
        # 使用新版 SDK 调用
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())], # 新版工具配置写法
            )
        )
        
        # 获取回复文本
        return response.text
        
    except Exception as e:
        return f"❌ Gemini API 调用出错: {e}"

def push_wechat(content):
    if not PUSH_TOKEN:
        print("🔕 未配置 PUSH_TOKEN，跳过推送。")
        print("--- 生成的内容如下 ---")
        print(content)
        return
        
    print("🚀 正在推送到微信...")
    url = "http://www.pushplus.plus/send"
    
    data = {
        "token": PUSH_TOKEN,
        "title": "今日反洗钱简报",
        "content": content,
        "template": "markdown"
    }
    try:
        res = requests.post(url, json=data).json()
        if res.get('code') == 200:
            print("✅ 推送成功！")
        else:
            print(f"❌ 推送失败: {res}")
    except Exception as e:
        print(f"❌ 推送请求异常: {e}")

if __name__ == "__main__":
    
    print("🕒 开始执行每日反洗钱简报任务...")
    
    report = generate_aml_report()
    
    if report:
        if "无重大反洗钱监管动态" not in report:
            push_wechat(report)
        else:
            print("⚠️ AI 判断今日无重要内容，部分推送或跳过。")
            push_wechat(report) 
    else:
        print("❌ 生成失败，无内容。")