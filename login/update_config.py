import json
import os
import re

def get_sorted_user_files():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    user_files = [f for f in os.listdir(data_dir) if f.startswith('user_') and f.endswith('.json')]
    
    # 提取文件名中的数字并按数字大小排序
    user_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    return [os.path.join(data_dir, f) for f in user_files]

def get_next_username(current_username=None):
    user_files = get_sorted_user_files()
    if not user_files:
        raise ValueError('未找到用户数据文件')
    
    usernames = []
    for file_path in user_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
            usernames.append(data['user_name'])
    
    if not current_username or current_username not in usernames:
        return usernames[0]
    
    current_index = usernames.index(current_username)
    next_index = (current_index + 1) % len(usernames)
    return usernames[next_index]

def update_config():
    try:
        # 读取现有的config.json
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        # 读取当前配置
        current_username = None
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                current_username = config.get('username')
        else:
            config = {}
        
        # 获取下一个用户名
        username = get_next_username(current_username)
        
        # 更新配置
        config['username'] = username
        config['password'] = '123456'
        
        # 保存更新后的配置
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print('配置更新成功')
        
    except Exception as e:
        print(f'更新配置失败: {str(e)}')

if __name__ == '__main__':
    update_config()