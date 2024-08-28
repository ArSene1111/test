import json
import math
from itertools import combinations
from tqdm import tqdm



def load_game_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            game_data = json.load(file)
            return game_data
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 文件")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")










file_path = 'game_logs34.json'

# 加載遊戲數據
data = load_game_data(file_path)  # 將加載的數據賦值給 data 變數

# 假設 data 是包含所有遊戲資料的列表
games = data  # 如果 data 是列表，直接賦值給 games

errors = []
total_games = 0
matching_gameNos = []

for game in tqdm(data, desc="驗證中", colour="green"):
    total_games += 1
    log = game.get('log', {})
    data = log.get('data', {})
    bigdata = data.get('big_data', {})
    gameNo = bigdata.get('gameNo', None)

    pub1 = bigdata['data'][0]['pub1']
    if pub1:
        numbers = pub1.split(';')
        count_13 = 0
        found_pattern_1 = False
        found_pattern_2 = False

        for number in numbers:
            parts = number.split(':')
            if len(parts) > 1:
                values = parts[1].split(',')
                count_13 += values.count('13')
                
                # 檢查第一個數字是13，後面兩個數字是12或13
                if values[0] == '13' and all(v in ['12', '13'] for v in values[1:3]):
                    found_pattern_1 = True
                
                # 檢查第二個數字是12或與第一個數字相同，第三個數字是14
                if len(values) > 2 and (values[1] == '12' or values[1] == values[0]) and values[2] == '14':
                    found_pattern_2 = True

        if count_13 >= 1 and found_pattern_1 and found_pattern_2:
            matching_gameNos.append(gameNo)

print(f"驗證總局數: {total_games}")
print("符合條件的局號:")
for gameNo in matching_gameNos:
    print(gameNo)
