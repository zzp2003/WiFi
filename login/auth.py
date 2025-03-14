import requests
import json
import time
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('login/auth.log'),
        logging.StreamHandler()
    ]
)

class CampusNetAuth:
    def __init__(self):
        self.config = self._load_config()
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36 Edg/133.0.0.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }

    def _load_config(self):
        try:
            config_path = Path('login/config.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logging.error(f'加载配置文件失败: {str(e)}')
            raise

    def check_login_status(self):
        try:
            # 检测网络连通性
            test_urls = [
                'https://www.baidu.com',  # 国内网站
                  
            ]
            
            network_status = False
            for url in test_urls:
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code == 200:
                        network_status = True
                        logging.info(f'网络连通性正常，可以访问 {url}')
                        break
                except Exception:
                    continue
            
            if not network_status:
                logging.error('网络连接异常，无法访问外部网站')
                return False
            
            # 从rad_user_info接口获取当前登录用户信息
            info_url = f"http://218.104.96.75/cgi-bin/rad_user_info?callback=jQuery&ip={self.config['wlanuserip']}"
            info_response = self.session.get(info_url, headers=self.headers, timeout=10)
            
            # 解析返回的数据
            data = info_response.text
            if 'user_name' in data:
                # 提取user_name值
                import re
                match = re.search('"user_name":"([^"]+)"', data)
                if match:
                    current_user = match.group(1)
                    logging.info(f'当前已登录，使用账号: {current_user}')
                    return True
            
            # 如果没有获取到用户信息，说明未登录
            logging.info('当前未登录')
            return False
        except Exception as e:
            logging.error(f'检查登录状态失败: {str(e)}')
            return False

    def login(self):
        try:
            # 构建登录请求
            login_data = {
                'username': self.config['username'],
                'password': self.config['password'],
                'ac_id': self.config['ac_id'],
                'ip': self.config['wlanuserip']
            }

            # 发送登录请求
            response = self.session.post(
                self.config['login_url'],
                data=login_data,
                headers=self.headers,
                timeout=10
            )

            # 检查登录是否成功
            success_indicators = ['success', 'success_mobile']
            if any(indicator in response.url.lower() for indicator in success_indicators):
                logging.info('登录成功')
                return True
            else:
                logging.error('登录失败')
                return False

        except Exception as e:
            logging.error(f'登录过程发生错误: {str(e)}')
            return False

    def maintain_login(self, check_interval=300):
        while True:
            try:
                if not self.check_login_status():
                    logging.info('检测到未登录状态，尝试重新登录')
                    self.login()
                else:
                    logging.info('登录状态正常')
                
                time.sleep(check_interval)

            except Exception as e:
                logging.error(f'保持登录状态时发生错误: {str(e)}')
                time.sleep(60)  # 发生错误时等待1分钟后重试

def main():
    auth = CampusNetAuth()
    auth.maintain_login()

if __name__ == '__main__':
    main()