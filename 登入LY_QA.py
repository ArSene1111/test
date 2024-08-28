import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
import json
from tqdm import tqdm

# 定义登录API的URL
login_url = 'http://192.168.33.100:9100/api/login'

# 登录所需的账号和密码
login_payload = {
    'name': 'arsene',
    'password': '234a8fc1f934cc650484a771a83bb89d',
    'validateCode': '',
    'count': 0
}

# 创建一个会话对象
session = requests.Session()

# 发送POST请求进行登录
login_response = session.post(login_url, data=login_payload)

# 检查登录是否成功
if login_response.status_code == 200:
    print('登录成功')
    print('Cookies:', session.cookies)

    # 检查登录状态
    status_url = 'http://192.168.33.100:9100/api/2fa/status'
    status_response = session.post(status_url)

    if status_response.status_code == 200:
        print('登录状态检查成功')
        # 存储已获取的数据以去除重复
        all_data = []
        # 定义查找数据的API URL
        data_url = 'http://192.168.33.100:9100/api/winAndLoseReport/getGameRecord?'

        begin_time_str = '2024-08-23 09:00:00'
        end_time_str = '2024-08-23 10:20:00'

        if not begin_time_str:
            begin_time = datetime.now()
            begin_time_str = begin_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            begin_time = datetime.strptime(begin_time_str, '%Y-%m-%d %H:%M:%S')
        
        if not end_time_str:
            end_time = begin_time + timedelta(minutes=10)
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        
        response = session.get(data_url, params={'beginTime': begin_time_str, 'endTime': end_time_str, 'gameId': '8870', 'currency': 'CNY'})
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data["rows"])
        else:
            print(f"请求失败，状态码：{response.status_code}")

        begin_time = datetime.strptime(begin_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

        # 计算时间差
        time_difference = (end_time - begin_time).total_seconds() / 60.0

        if time_difference <= 10:
            # 如果时间差小于或等于10分钟，则只进行一次数据提取
            response = session.get(data_url, params={'beginTime': begin_time_str, 'endTime': end_time_str, 'gameId': '8870', 'currency': 'CNY'})
            if response.status_code == 200:
                data = response.json()
                all_data.extend(data["rows"])
            else:
                print(f"请求失败，状态码：{response.status_code}")
        else:
            # 如果时间差大于10分钟，则分批进行数据提取
            current_time = begin_time
            while current_time < end_time:
                next_time = min(current_time + timedelta(minutes=10), end_time)

                print(f"提取数据的时间范围: {current_time.strftime('%Y-%m-%d %H:%M:%S')} - {next_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                response = session.get(data_url, params={'beginTime': current_time.strftime('%Y-%m-%d %H:%M:%S'), 'endTime': next_time.strftime('%Y-%m-%d %H:%M:%S'), 'gameId': '8870', 'currency': 'CNY'})
                if response.status_code == 200:
                    data = response.json()
                    all_data.extend(data["rows"])
                else:
                    print(f"请求失败，状态码：{response.status_code}")
                

                

                # 构造获取数据时所需的参数
                data_payload = {
                    'gameId': '8870',
                    'roomId': '',
                    'roomType': '',
                    'currency': 'CNY',
                    'gameNo': '',
                    'account': '',
                    'pageSize': '20000',
                    'page': '1',
                    'beginTime': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'endTime': next_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                full_url = f"{data_url}{urlencode(data_payload)}"
                print('完整的URL:', full_url)
                current_time = next_time


                # 发送GET请求获取数据
                data_response = session.get(data_url, params=data_payload)

                # 检查获取数据的请求是否成功
                if data_response.status_code == 200:
                    print(f'获取数据成功: {current_time} - {next_time}')
                    try:
                        data = data_response.json()
                        # 打印每次获取的数据
                        print('当前响应数据:', data)
                        if 'rows' in data and isinstance(data['rows'], list):
                            all_data.extend(data['rows'])
                        else:
                            print('返回的数据格式不正确:', data)
                    except ValueError:
                        print('无法解析为JSON:', data_response.text)
                else:
                    print(f'获取数据失败: {current_time} - {next_time}')
                    print('Status Code:', data_response.status_code)
                    print('Response:', data_response.text)

                # 更新当前时间
                current_time = next_time

        # 去重
        unique_data = {entry['gameNo']: entry for entry in all_data}.values()

        # 打印去重前的数据
        print('去重前数据:')
        for entry in all_data:
            print(entry)

        # 打印去重前的数据总数
        print(f'去重前总共有 {len(all_data)} 条数据')

        # 打印去重后的数据
        print('去重后的数据:')
        for entry in unique_data:
            print(entry)

        # 打印去重后的数据总数
        print(f'去重后总共有 {len(unique_data)} 条数据')

        # 定义新API的URL
        log_api_url = 'http://192.168.33.100:9100/api/gameLog/log'

        # 存储新API返回的数据
        log_data = []

        # 对每个gameNo调用新API
        for entry in tqdm(unique_data, desc="获取游戏日志数据",colour = "green"):
            game_no = entry['gameNo']
            log_url = f"{log_api_url}?gameNo={game_no}"
            print('调用新API的URL:', log_url)

            # 发送GET请求获取游戏日志数据
            log_response = session.get(log_url)

            # 检查获取数据的请求是否成功
            if log_response.status_code == 200:
                print(f'获取游戏日志成功: {game_no}')
                try:
                    log_entry = log_response.json()
                    # 将返回的数据添加到log_data中
                    log_data.append({
                        'gameNo': game_no,
                        'log': log_entry
                    })
                except ValueError:
                    print(f'无法解析为JSON: {log_response.text} for gameNo {game_no}')
            else:
                print(f'获取游戏日志失败: {game_no}')
                print('Status Code:', log_response.status_code)
                print('Response:', log_response.text)

        # 保存日志数据到文件
        log_file_name = 'game_logs35.json'
        with open(log_file_name, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)

        print(f'日志数据已保存到 {log_file_name}')
    else:
        print('登录状态检查失败')
        print('Status Code:', status_response.status_code)
        print('Response:', status_response.text)
else:
    print('登录失败')
    print('Status Code:', login_response.status_code)
    print('Response:', login_response.text)