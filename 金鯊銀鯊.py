import json
import math
from itertools import combinations
from tqdm import tqdm
from itertools import combinations_with_replacement

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
# 判定房間名稱
def get_room_name(server_id):
    room_mapping = {
        86301: "金鲨银鲨新手场",
        86302: "金鲨银鲨中級场",
        86303: "金鲨银鲨高級场",
        86304: "金鲨银鲨大師场"
    }
    return room_mapping.get(server_id, "未知房間")
# 各房間籌碼數值
def get_chip_values(room_name):
    chip_values_mapping = {
        "金鲨银鲨新手场": [200, 1000, 5000, 15000, 30000],
        "金鲨银鲨中級场": [1000, 5000, 10000, 20000, 50000],
        "金鲨银鲨高級场": [5000, 10000, 20000, 50000, 100000],
        "金鲨银鲨大師场": [20000, 50000, 100000, 200000, 3000000]
    }
    return chip_values_mapping.get(room_name, [])
# pos代表點位
def get_bet_position_name(pos):
    position_names = {
        1: "燕子",
        2: "鸽子",
        3: "孔雀",
        4: "鹰",
        5: "兔子",
        6: "猴子",
        7: "熊猫",
        8: "狮子",
        9: "银鲨",
        10: "金鲨",
        11: "飞禽",
        12: "走兽",   
    }
    return position_names.get(pos, "未知點位")
# 各房間點位限紅

bet_limits = {
    "86301": {
        "1": (200, 60000),
        "2": (200, 60000),
        "3": (200, 60000),
        "4": (200, 60000),
        "5": (200, 60000),
        "6": (200, 60000),
        "7": (200, 60000),
        "8": (200, 60000),
        "9": (200, 30000),
        "10": (200, 15000),
        "11": (200, 90000),
        "12": (200, 90000)
    },
    "86302": {
        "1": (1000, 100000),
        "2": (1000, 100000),
        "3": (1000, 100000),
        "4": (1000, 100000),
        "5": (1000, 100000),
        "6": (1000, 100000),
        "7": (1000, 100000),
        "8": (1000, 100000),
        "9": (1000, 50000),
        "10": (1000, 25000),
        "11": (1000, 150000),
        "12": (1000, 150000)     
    },
     "86303": {
        "1": (5000, 200000),
        "2": (5000, 200000),
        "3": (5000, 200000),
        "4": (5000, 200000),
        "5": (5000, 200000),
        "6": (5000, 200000),
        "7": (5000, 200000),
        "8": (5000, 200000),
        "9": (5000, 100000),
        "10": (5000, 50000),
        "11": (5000, 300000),
        "12": (5000, 300000)
        
    },
    "86304": {
        "1": (20000, 400000),
        "2": (20000, 400000),
        "3": (20000, 400000),
        "4": (20000, 400000),
        "5": (20000, 400000),
        "6": (20000, 400000),
        "7": (20000, 400000),
        "8": (20000, 400000),
        "9": (20000, 200000),
        "10": (20000, 100000),
        "11": (20000, 600000),
        "12": (20000, 600000)
       
    }
}
    
def get_bet_limits(server_id, pos):
    server_id = str(server_id)  # 确保 server_id 是字符串类型
    pos = str(pos)  # 确保 pos 是字符串类型
    
    if server_id in bet_limits:
        if pos in bet_limits[server_id]:
            return bet_limits[server_id][pos]
    return (None, None)

# 定義賠率表
odds_table = {
    1: 6,
    2: 8,
    3: 9,
    4: 12,
    5: 6,
    6: 8,
    7: 9,
    8: 12,
    9: 25,
    10: 50,
    11: 2,
    12: 2
}

# 示例: 根據點位獲取賠率
def get_odds(pos):
    return odds_table.get(pos, None)


# 解析 pub1 獲取開獎點位
def get_odds(pos):
    return odds_table.get(pos, None)


# 解析 pub1 獲取開獎點位
def parse_pub1(pub1):
    if len(pub1) < 4:
        raise ValueError("pub1 的長度不足四位數")
    
    # 解析前兩位數字作為開獎點位
    pos = int(pub1[:2])
    
    # 解析後兩位數字作為賠率
    rate = int(pub1[2:])
    # 根據開獎點位添加額外的點位
    winning_positions = []
    additional_pos = None
    if pos in [1, 2, 3, 4]:
        additional_pos = 11
    elif pos in [5, 6, 7, 8]:
        additional_pos = 12

     # 存入開獎點位和額外點位
    winning_positions = [pos]
    if additional_pos:
        winning_positions.append(additional_pos)    
    
    return pos, rate, winning_positions

# # 測試範例
# pub1 = "0309"
# pos, rate, winning_positions = parse_pub1(pub1)
# print(f"點位: {pos}, 賠率: {rate}倍")
# print(f"開獎點位: {winning_positions}")



# 判斷下注金額是否符合籌碼數值

def can_combine_bet(chip_values, bet_amount):
    if bet_amount is None:
        return False
    for r in range(1, len(chip_values) + 1):
        for combo in combinations_with_replacement(chip_values, r):
            if sum(combo) == bet_amount:
                return True
    return False




# 指定文件名稱
file_path = 'game_logs33.json'

# 加載遊戲數據
data = load_game_data(file_path)  # 將加載的數據賦值給 data 變數

# 假設 data 是包含所有遊戲資料的列表
games = data  # 如果 data 是列表，直接賦值給 games

errors = []
total_games = 0

for game in tqdm(data, desc="驗證中",colour = "green"):
# for game in games:
    total_games += 1
    log = game.get('log', {})
    data = log.get('data', {})
    bigdata = data.get('big_data', {})
    # 處理 roomdata
    roomdata = data.get('roomData', {})
    game_id = roomdata.get('GameID', None)
    if not isinstance(bigdata, dict):
        errors.append(f"局號 {game.get('gameNo', '未知')} 中的 bigdata 不是字典")
        continue

    if not bigdata:
        errors.append(f"局號 {game.get('gameNo', '未知')} 中的 bigdata 為空")
        continue

    # 處理 big_data 中的 pub1
    pub1 = bigdata.get('pub1', None)
    if pub1:
        pos, rate, winning_positions = parse_pub1(pub1)
        # print(winning_positions)
    else:
        errors.append(f"局號 {game.get('gameNo', '未知')} 未找到 pub1 的數據")

    # 處理 gameNo 和 bets
    game_no = game.get('gameNo', None)
    if not game_no:
        errors.append("未找到 gameNo，跳過此遊戲數據")
        continue

    room_name = game.get('roomName', '未知')
     
    # print(f"處理局號: {game_no}")
    

    att = bigdata.get('att', [])
    if not att:
        errors.append(f"局號 {game_no} 中沒有找到有效的 bets")
        continue

    for bet in att:
        act = bet.get('act', [])
    if not act:
        errors.append(f"局號 {game_no}, 點位 {bet.get('pos')} 中沒有找到有效的 act")
        continue

    # 重置變數
    bet_totals = {}
    total_all = 0
    winning_amount_total = 0

    for action in act:
        if action.get('ty') != 2:
            continue

        pos = action.get('pos')
        bet_amount = action.get('bet')
        if bet_amount is None:
            errors.append(f"局號 {game_no}, 點位 {pos} 的下注金額為 None，跳過此下注")
            continue

        # 累加每個下注點位的總下注金額
        if pos in bet_totals:
            bet_totals[pos] += bet_amount
        else:
            bet_totals[pos] = bet_amount

        server_id = roomdata.get('ServerID', None)
        if server_id:
            room_name = get_room_name(server_id)
            chip_values = get_chip_values(room_name)
           
            
            if can_combine_bet(chip_values, bet_amount):
                # print(f"局號 {game_no}, 點位 {get_bet_position_name(pos)}, 下注金額 {bet_amount} 符合 {room_name} 的籌碼數值")
                pass
            else:
                errors.append(f"局號 {game_no}, 點位 {get_bet_position_name(pos)}, 下注金額 {bet_amount} 不符合 {room_name} 的籌碼數值")
        else:
            errors.append(f"局號 {game_no} 中沒有找到 ServerID")

    # 初始化全部點位的下注總和
    total_all = 0
    # 打印每個下注點位的總下注金額並與限紅比較
    for pos, total in bet_totals.items():
        # 累加每個點位的下注金額到 total_all
        total_all += total
        
        # 獲取限紅
        server_id = roomdata.get('ServerID', None)
        # print(server_id, pos)
        limits = get_bet_limits(server_id, pos)
        # print(limits)
        # print(f"檢查 server_id: {server_id}, pos: {pos}: {limits}") 
        # print(limits)
        
        min_limit, max_limit = limits 
        # print(min_limit, max_limit)
        # print(total)
        if max_limit is not None:
            if total > max_limit:
                errors.append(f"局號 {game_no}, 點位 {pos} 的總下注金額 {total} 超出限紅 {max_limit}")
            else:
                # print(f"點位 {pos} 的總下注金額 {total} 在限紅 {max_limit} 內")
                pass
        else:
            errors.append(f"局號 {game_no}, 點位 {pos} 沒有找到限紅")
# 計算 valid_bet
real_valid_bet = 0
bet_11 = bet_totals.get(11, 0)
bet_12 = bet_totals.get(12, 0)
real_valid_bet = abs(bet_11 - bet_12)
# print(real_valid_bet)
# 加上其他點位的下注金額
for pos, total in bet_totals.items():
    if pos not in [11, 12]:
        real_valid_bet += total
        # print(real_valid_bet)

    # 計算每個點位的中奖金额
for pos in winning_positions:
    total = bet_totals.get(pos, 0)
    position_names = get_bet_position_name(pos)
    odds = get_odds(pos)
    if odds is not None:
        winning_amount = total * odds
        winning_amount_total += winning_amount
        # print(f"點位 {position_names} 的總下注金額 {total} 乘以賠率 {odds}，中奖金额為 {winning_amount}")
    else:
        errors.append(f"局號 {game_no}, 點位 {position_names} 沒有找到賠率")
    # print(f"總中奖金额為 {winning_amount_total}")            

final_win = winning_amount_total - total_all
# print(winning_amount_total)
# print(total_all)
# if final_win > 0:
#     final_win *= 0.95
final_value_bet = real_valid_bet
info_value_bet = bigdata['att'][0]['validBet']
info_changes = bigdata['att'][0]['changes']

if final_win != info_changes:
    errors.append(f"局號 {game_no} 盈利金額錯誤: final_win = {final_win}, info_changes = {info_changes}")
else:
    # print(f"盈利金額正確:  {final_win}")
    pass
# 檢查 final_value_bet 和 info_value_bet 是否相等
if final_value_bet != info_value_bet:
    errors.append(f"局號 {game_no} 有效錯誤: final_value_bet = {final_value_bet}, info_value_bet = {info_value_bet}")
else:
    # print(f"有效下注金額正確: {final_value_bet}")
    pass

# 最後打印所有錯誤
if errors:
    print("以下局號有錯誤:")
    for error in errors:
        print(error)
else:
    print("所有局數都通過")

print(f"總共驗證了 金鲨银鲨 {total_games} 局遊戲。")




