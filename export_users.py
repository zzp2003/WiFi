import json
import os
import pandas as pd

def main():
    # 指定数据目录
    data_dir = 'data'

    # 存储所有用户数据的列表
    users_data = []

    # 遍历data目录下的所有json文件
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                users_data.append({
                    '用户名': data['user_name'],
                    'IP后缀': data['ip_suffix'],
                    'IP地址': data['ip_address']
                })

    # 创建DataFrame并按用户名排序
    df = pd.DataFrame(users_data)
    df['用户名'] = df['用户名'].astype(str)
    df = df.sort_values(by='用户名')

    # 获取最新的文件序号
    def get_next_file_number():
        max_num = 0
        for filename in os.listdir('.'):
            if filename.startswith('users_data') and filename.endswith('.xlsx'):
                try:
                    num = int(filename.replace('users_data', '').replace('.xlsx', '') or 0)
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        return max_num + 1

    # 导出为Excel文件
    file_number = get_next_file_number()
    output_file = f'users_data{file_number}.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f'数据已成功导出到 {output_file}')

if __name__ == '__main__':
    main()