#!/usr/bin/env python3
"""
百度链接主动推送脚本
从 sitemap.xml 读取链接，批量提交到百度站长平台
"""
import requests
from xml.etree import ElementTree as ET
import sys
import time
import random

# 配置
SITEMAP_URL = "https://www.jumohub.com/sitemap.xml"
BAIDU_API_URL = "http://data.zz.baidu.com/urls?site=www.jumohub.com&token=dTxLYHaZsI2Sg4DO"
BATCH_SIZE = 10  # 缩小批次，降低单次失败概率
DELAY = 2  # 批次间延迟(秒)
MAX_RETRIES = 3  # 失败重试次数

def get_urls_from_sitemap(sitemap_url):
    """从 sitemap.xml 中提取所有 URL"""
    print(f"正在读取 sitemap: {sitemap_url} ...")
    try:
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall('.//sm:loc', ns)]
        
        print(f"✓ 从 sitemap 中提取了 {len(urls)} 个链接")
        return urls
    except Exception as e:
        print(f"✗ 读取 sitemap 失败: {e}")
        sys.exit(1)

def submit_batch(urls, api_url, batch_num, total_batches):
    """提交一批链接，包含重试"""
    data = "\n".join(urls)
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                api_url,
                data=data,
                headers={
                    "Content-Type": "text/plain",
                    "User-Agent": "Baiduspider"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                success = result.get('success', 0)
                remain = result.get('remain', '未知')
                error = result.get('error', '')
                error_msg = result.get('message', '')
                
                if error:
                    if error == 400 and 'over quota' in error_msg.lower():
                        print(f"  跳过第 {batch_num} 批（配额超限，建议明天重试或减少频率）")
                        return 'quota_exceeded'
                    else:
                        print(f"  第 {batch_num} 批: 失败 - {error}: {error_msg}")
                        if attempt < MAX_RETRIES - 1:
                            wait = (attempt + 1) * 3
                            print(f"  重试 {attempt + 1}/{MAX_RETRIES}，{wait} 秒后...")
                            time.sleep(wait)
                            continue
                        return 'failed'
                else:
                    print(f"  第 {batch_num} 批: 成功 - {success}/{len(urls)} 个链接已提交 (剩余配额: {remain})")
                    return 'success'
            else:
                print(f"  第 {batch_num} 批: HTTP {response.status_code}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)
                    continue
                return 'failed'
                
        except Exception as e:
            print(f"  第 {batch_num} 批: 异常 - {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return 'failed'
    
    return 'failed'

def submit_to_baidu(urls, api_url):
    """批量提交链接到百度"""
    total = len(urls)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\n开始提交到百度，共 {total} 个链接，分为 {total_batches} 批...\n")
    
    success_count = 0
    fail_count = 0
    quota_exceeded = False
    
    for i in range(0, total, BATCH_SIZE):
        batch_num = i // BATCH_SIZE + 1
        batch = urls[i:i+BATCH_SIZE]
        
        result = submit_batch(batch, api_url, batch_num, total_batches)
        
        if result == 'quota_exceeded':
            quota_exceeded = True
            print(f"\n⚠ 检测到配额超限，停止后续提交。")
            print(f"  建议: 登录百度站长平台确认每日配额，或改用JS自动推送+sitemap方式。")
            break
        elif result == 'success':
            success_count += len(batch)
        else:
            fail_count += len(batch)
        
        if not quota_exceeded and batch_num < total_batches:
            jitter = random.uniform(0, DELAY)
            time.sleep(jitter)
    
    print(f"\n{'='*50}")
    print(f"提交完成!")
    print(f"总链接数: {total}")
    print(f"成功提交: {success_count} 个")
    print(f"失败/跳过: {fail_count} 个")
    if quota_exceeded:
        print(f"\n提示: 百度主动推送配额已超，建议搭配sitemap+JS自动推送使用。")
    print(f"{'='*50}\n")

def main():
    print(f"百度链接主动推送工具")
    print(f"站点: www.jumohub.com")
    print(f"API: {BAIDU_API_URL}")
    print(f"{'='*50}\n")
    
    urls = get_urls_from_sitemap(SITEMAP_URL)
    if urls:
        submit_to_baidu(urls, BAIDU_API_URL)

if __name__ == "__main__":
    main()
