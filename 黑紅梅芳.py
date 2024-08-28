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
        86601: "黑红梅芳新手场",
        86602: "黑红梅芳中級场",
        86603: "黑红梅芳高級场",
        86604: "黑红梅芳大師场"
    }
    return room_mapping.get(server_id, "未知房間")
# 各房間籌碼數值
def get_chip_values(room_name):
    chip_values_mapping = {
        "黑红梅芳新手场": [200, 500, 1000, 2000, 5000, 10000],
        "黑红梅芳中級场": [2000, 5000, 10000, 20000, 50000, 100000],
        "黑红梅芳高級场": [20000, 50000, 100000, 200000, 500000, 1000000],
        "黑红梅芳大師场": [50000, 100000, 200000, 500000, 1000000, 1500000]
    }
    return chip_values_mapping.get(room_name, [])
# pos代表點位
def get_bet_position_name(pos):
    position_names = {
        1: "黑",
        2: "紅",
        3: "梅",
        4: "芳",
        5: "大",
        6: "小",
        7: "單",
        8: "雙",
        9: "7"   
    }
    return position_names.get(pos, "未知點位")
# 各房間點位限紅

bet_limits = {
    "86601": {
        "1": (200, 10000),
        "2": (200, 10000),
        "3": (200, 10000),
        "4": (200, 10000),
        "5": (200, 10000),
        "6": (200, 10000),
        "7": (200, 10000),
        "8": (200, 10000),
        "9": (200, 10000)
    },
    "86602": {
        "1": (2000, 100000),
        "2": (2000, 100000),
        "3": (2000, 100000),
        "4": (2000, 100000),
        "5": (2000, 100000),
        "6": (2000, 100000),
        "7": (2000, 100000),
        "8": (2000, 100000),
        "9": (2000, 100000)

        
    },
     "86603": {
        "1": (20000, 1000000),
        "2": (20000, 1000000),
        "3": (20000, 1000000),
        "4": (20000, 1000000),
        "5": (20000, 1000000),
        "6": (20000, 1000000),
        "7": (20000, 1000000),
        "8": (20000, 1000000),
        "9": (20000, 1000000)
        
    },
    "86604": {
        "1": (50000, 1500000),
        "2": (50000, 1500000),
        "3": (50000, 1500000),
        "4": (50000, 1500000),
        "5": (50000, 1500000),
        "6": (50000, 1500000),
        "7": (50000, 1500000),
        "8": (50000, 1500000),
        "9": (50000, 1500000)
       
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
    1: 4,
    2: 4,
    3: 4,
    4: 4,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 13,
}

# 示例: 根據點位獲取賠率
def get_odds(pos):
    return odds_table.get(pos, None)


# 解析 pub1 獲取開獎點位
def parse_pub1(pub1):
    if len(pub1) < 3:
        raise ValueError("pub1 的長度不足三位數")
    
    
    # 解析後面的數字作為開獎點位
    winning_positions = []
    for i in range(2, len(pub1), 2):
        pos = int(pub1[i:i+2])
        winning_positions.append(pos)
    
    return winning_positions



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
file_path = 'game_logs37.json'

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
        winning_positions = parse_pub1(pub1)
        
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
        if action.get('ty') != 3:
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
    bet_totals_per_position = {}
    total_all = 0
    valid_bet = 0
    # 檢查是否有點位 9
    has_position_9 = 9 in winning_positions
    # 打印每個下注點位的總下注金額並與限紅比較
    for pos, total in bet_totals.items():
        # 累加每個點位的下注金額到 total_all
        total_all += total
        
        # 累加每個點位的投注金額到 bet_totals_per_position
        if pos not in bet_totals_per_position:
            bet_totals_per_position[pos] = 0
        bet_totals_per_position[pos] += total
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
         
        # 打印每個點位的投注金額
        if has_position_9:
            if pos in [1, 2, 3, 4, 9]:
                valid_bet = sum(bet_totals.get(p, 0) for p in [1, 2, 3, 4, 9])
                # print(f"點位 {pos}: {bet_totals_per_position[pos]} 投注金額")
                
        else:
            valid_bet = total_all
            # print(f"點位 {pos}: {bet_totals_per_position[pos]} 投注金額")
        
    # 打印全部點位的下注總和
    # print(f"全部點位的下注總和為 {total_all}") 
    
    total_all_1 = 0
    # 計算每個點位的中奖金额
    for pos, total in bet_totals.items():
        position_names = get_bet_position_name(pos)
        if pos in winning_positions:
            odds = get_odds(pos)
            if odds is not None:
                winning_amount = total * odds
                winning_amount_total += winning_amount
                total_all_1 += total
                # print(f"點位 {position_names} 的總下注金額 {total} 乘以賠率 {odds}，中奖金额為 {winning_amount}")
            else:
                errors.append(f"局號 {game_no}, 點位 {position_names} 沒有找到賠率")
        
    # print(f"總中奖金额為 {winning_amount_total}")            
    # print(total_all_1)
    final_win = (winning_amount_total - total_all_1)*0.95 - (valid_bet - total_all_1)
    
    final_value_bet = valid_bet
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

print(f"總共驗證了 黑紅梅方 {total_games} 局遊戲。")