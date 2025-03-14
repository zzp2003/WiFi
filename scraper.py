import requests
import os
import time
import json
from concurrent.futures import ThreadPoolExecutor

base_url = 'http://218.104.96.75/cgi-bin/rad_user_info'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'http://218.104.96.75/srun_portal_success_mobile'
}

def scrape_data(ip_suffix):
    try:
        callback = f'jQuery{int(time.time()*1000)}_{int(time.time()*1000)}'
        params = {
            'callback': callback,
            'ip': f'100.83.28.{ip_suffix}',
            '_': int(time.time()*1000)
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 处理JSONP响应
        json_str = response.text[len(callback)+1:-1]  # 移除JSONP回调函数
        data = json.loads(json_str)
        
        if data.get('error') == 'ok' and data.get('user_name'):
            user_data = {
                'user_name': data['user_name'],
                'ip_suffix': ip_suffix,
                'ip_address': f'100.83.28.{ip_suffix}'
            }
            
            # 保存用户数据
            os.makedirs('./data', exist_ok=True)
            with open(f'./data/user_{ip_suffix}.json', 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)
            
            print(f'IP后缀 {ip_suffix} 数据抓取完成：{data["user_name"]}')
    except Exception as e:
        print(f'IP后缀 {ip_suffix} 数据抓取失败：{str(e)}')

def main():
    # 创建数据存储目录
    os.makedirs('./data', exist_ok=True)
    
    # 设置IP地址段范围
    ip_ranges = [
        range(1, 51),    # 1-50
        range(51, 101),  # 51-100
        range(101, 151), # 101-150
        range(151, 201), # 151-200
        range(201, 255)  # 201-254
    ]
    
    # 使用线程池并发处理多个IP段
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip_range in ip_ranges:
            executor.map(scrape_data, ip_range)
            time.sleep(2)  # 在处理不同IP段之间添加短暂延迟
    
    # 数据抓取完成后，自动执行数据导出
    print('\n数据抓取完成，开始导出到Excel...')
    from export_users import main as export_main
    export_main()

if __name__ == '__main__':
    main()