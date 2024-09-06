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
        9001: "龙虎斗新手场",
        9002: "龙虎斗中級场",
        9003: "龙虎斗高級场",
        9004: "龙虎斗大師场"
    }
    return room_mapping.get(server_id, "未知房間")
# 各房間籌碼數值
def get_chip_values(room_name):
    chip_values_mapping = {
        "龙虎斗新手场": [200, 500, 1000, 2000, 5000, 10000],
        "龙虎斗中級场": [1000, 2000, 5000, 10000, 20000, 50000],
        "龙虎斗高級场": [5000, 10000, 20000, 50000, 100000, 250000],
        "龙虎斗大師场": [20000, 50000, 100000, 200000, 500000, 1000000]
    }
    return chip_values_mapping.get(room_name, [])
# pos代表點位
def get_bet_position_name(pos):
    position_names = {
        1: "龍",
        2: "虎",
        3: "和",
        4: "黑桃龍",
        5: "紅心龍",
        6: "梅花龍",
        7: "方塊龍",
        8: "黑桃虎",
        9: "紅心虎",
        10: "梅花虎",
        11: "方塊虎",
        12: "壓庄贏",
        13: "壓庄輸"   
    }
    return position_names.get(pos, "未知點位")
# 各房間點位限紅

bet_limits = {
    "9001": {
        "1": (200, 10000),
        "2": (200, 10000),
        "3": (200, 10000),
        "4": (200, 10000),
        "5": (200, 10000),
        "6": (200, 10000),
        "7": (200, 10000),
        "8": (200, 10000),
        "9": (200, 10000),
        "10": (200, 10000),
        "11": (200, 10000),
        "12": (200, 10000),
        "13": (200, 10000)
    },
    "9002": {
        "1": (1000, 50000),
        "2": (1000, 50000),
        "3": (1000, 50000),
        "4": (1000, 50000),
        "5": (1000, 50000),
        "6": (1000, 50000),
        "7": (1000, 50000),
        "8": (1000, 50000),
        "9": (1000, 50000),
        "10": (1000, 50000),
        "11": (1000, 50000),
        "12": (1000, 50000),
        "13": (1000, 50000)
        

        
    },
     "9003": {
        "1": (5000, 250000),
        "2": (5000, 250000),
        "3": (5000, 50000),
        "4": (5000, 250000),
        "5": (5000, 250000),
        "6": (5000, 250000),
        "7": (5000, 250000),
        "8": (5000, 250000),
        "9": (5000, 250000),
        "10": (5000, 250000),
        "11": (5000, 250000),
        "12": (5000, 250000),
        "13": (5000, 250000)


        
        
    },
    "9004": {
        "1": (20000, 1000000),
        "2": (20000, 1000000),
        "3": (20000, 50000),
        "4": (20000, 1000000),
        "5": (20000, 1000000),
        "6": (20000, 1000000),
        "7": (20000, 1000000),
        "8": (20000, 1000000),
        "9": (20000, 1000000),
        "10": (20000, 1000000),
        "11": (20000, 1000000),
        "12": (20000, 1000000),
        "13": (20000, 1000000)
        
       
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
    1: 2,
    2: 2,
    3: 30,
    4: 3.9,
    5: 3.9,
    6: 3.9,
    7: 3.9,
    8: 3.9,
    9: 3.9,
    10: 3.9,
    11: 3.9,
    12: 1.96,
    13: 1.96   
}

# 示例: 根據點位獲取賠率
def get_odds(pos):
    return odds_table.get(pos, None)

# 解析 info 字典的函數
def parse_info(info):
    long_bet = info.get('long', 0)
    hu_bet = info.get('hu', 0)
    return long_bet, hu_bet


def parse_pub1(pub1):
    if len(pub1) < 6:
        raise ValueError("pub1 的長度不足六位數")

    # 撲克牌花色和數字對應表
    suits = ['方塊', '梅花', '紅心', '黑桃']
    values = {
        '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13  # 10, J, Q, K 分別對應 10, 11, 12, 13
    }

    # 解析撲克牌
    dragon_suit = suits[int(pub1[0])]
    dragon_value = values[pub1[1]]
    tiger_suit = suits[int(pub1[2])]
    tiger_value = values[pub1[3]]

    dragon_card = f"{dragon_suit}{dragon_value}"
    tiger_card = f"{tiger_suit}{tiger_value}"

    # 解析後面的數字作為開獎點位
    winning_positions = []
    for i in range(4, len(pub1), 2):
        pos = int(pub1[i:i+2])
        winning_positions.append(pos)

    return (dragon_value, tiger_value, dragon_suit, tiger_suit, dragon_card, tiger_card, winning_positions)

  

# 撲克牌大小比較
suit_rank = {'方塊': 1, '梅花': 2, '紅心': 3, '黑桃': 4}

def compare_cards(dragon_suit, dragon_value, tiger_suit, tiger_value):
    if dragon_value > tiger_value:
        return '龍贏'
    elif dragon_value < tiger_value:
        return '虎贏'
    else:
        # 如果數字相同，則比較花色
        if suit_rank[dragon_suit] > suit_rank[tiger_suit]:
            return '龍贏'
        elif suit_rank[dragon_suit] < suit_rank[tiger_suit]:
            return '虎贏'
        else:
            return '平局'



# 根據比牌結果和下注金額來判定開獎點位
def determine_winning_positions(comparison_result, dragon_suit, tiger_suit, long_bet, hu_bet):
    positions = []

    if comparison_result == '龍贏':
        positions.append(1)
    elif comparison_result == '虎贏':
        positions.append(2)
    elif comparison_result == '平局':
        positions.append(3)

    if dragon_suit == '黑桃':
        positions.append(4)
    elif dragon_suit == '紅心':
        positions.append(5)
    elif dragon_suit == '梅花':
        positions.append(6)
    elif dragon_suit == '方塊':
        positions.append(7)

    if tiger_suit == '黑桃':
        positions.append(8)
    elif tiger_suit == '紅心':
        positions.append(9)
    elif tiger_suit == '梅花':
        positions.append(10)
    elif tiger_suit == '方塊':
        positions.append(11)

    if comparison_result in ['龍贏', '虎贏']:
        if (comparison_result == '龍贏' and long_bet < hu_bet) or (comparison_result == '虎贏' and hu_bet < long_bet):
            positions.append(12)
        elif (comparison_result == '龍贏' and long_bet > hu_bet) or (comparison_result == '虎贏' and hu_bet > long_bet):
            positions.append(13)

    return positions

def verify_winning_positions(pub1, long_bet, hu_bet, winning_positions1):
    winning_positions1 = []
    result = parse_pub1(pub1)
    if isinstance(result, tuple):
        # 拆解返回結果
        dragon_value = result[0]
        tiger_value = result[1]
        dragon_suit = result[2]
        tiger_suit = result[3]
        dragon_card = result[4]
        tiger_card = result[5]
        long_bet, hu_bet = parse_info(info)

        # # 拆解牌信息
        # dragon_suit = dragon_card[:-1]  # 提取花色
        # dragon_value = int(dragon_card[-1])  # 提取數字
        # tiger_suit = tiger_card[:-1]
        # tiger_value = int(tiger_card[-1])

        comparison_result = compare_cards(dragon_suit, dragon_value, tiger_suit, tiger_value)
        positions = determine_winning_positions(comparison_result, dragon_suit, tiger_suit, long_bet, hu_bet)
        
        # 將開獎點位加入 winning_positions 列表
        winning_positions1.extend(positions)
        return winning_positions1
    else:
        print("錯誤：result 不是元組")
        return []




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
file_path = 'game_logs38.json'

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
        winning_positions = parse_pub1(pub1)[6]
        # print(winning_positions)
    else:
        errors.append(f"局號 {game.get('gameNo', '未知')} 未找到 pub1 的數據")
    
    # 處理 big_data 中的 info
    info = bigdata.get('info', None)
    long_bet, hu_bet = parse_info(info)
    
    winning_positions1 = [] 
    if pub1:
        winning_positions1 = verify_winning_positions(pub1, long_bet, hu_bet, winning_positions1)
        # print(winning_positions1)
        
    if set(winning_positions).issubset(set(winning_positions1)):
        pass
    else:
        missing_positions = set(winning_positions) - set(winning_positions1)
        errors.append(f"錯誤: winning_positions1 缺少數字 {missing_positions}")

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
    bet_amount = 0

    for action in act:
        if action.get('ty') != 4:
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
    
    # print(bet_totals_per_position)
    valid_bet = total_all
    # print(valid_bet)
    #判斷對壓不計算有效投注
   
    if all(x in bet_totals_per_position for x in [1, 2]):
        valid_bet -=   bet_totals_per_position.get(1, 0) + bet_totals_per_position.get(2, 0)
        # print(valid_bet)
    if all(x in bet_totals_per_position for x in [12, 13]):
        valid_bet -=   bet_totals_per_position.get(12, 0) + bet_totals_per_position.get(13, 0)
        # print(valid_bet)
    if len([x for x in [4, 5, 6, 7] if x in bet_totals_per_position]) >= 3:
        valid_bet -=   sum(bet_totals_per_position.get(x, 0) for x in [4, 5, 6, 7])
        # print(valid_bet)
    if len([x for x in [8, 9, 10, 11] if x in bet_totals_per_position]) >= 3:
        valid_bet -=   sum(bet_totals_per_position.get(x, 0) for x in [8, 9, 10, 11])
        # print(valid_bet)
    

    #判斷和局時有效投注的計算方式
    if 3 in winning_positions :
        valid_bet = total_all
        if all(x in bet_totals_per_position for x in [1, 2]):
            valid_bet -=   bet_totals_per_position.get(1, 0) + bet_totals_per_position.get(2, 0)
        if any(x in bet_totals_per_position for x in [12, 13]):    
           valid_bet -= bet_totals_per_position.get(12, 0) + bet_totals_per_position.get(13, 0)
        if len([x for x in [4, 5, 6, 7] if x in bet_totals_per_position]) >= 3:
            valid_bet -=   sum(bet_totals_per_position.get(x, 0) for x in [4, 5, 6, 7])
        if len([x for x in [8, 9, 10, 11] if x in bet_totals_per_position]) >= 3:
            valid_bet -=   sum(bet_totals_per_position.get(x, 0) for x in [8, 9, 10, 11])   

    #判斷龍虎總下注額相等時，有效投注的計算方式
    if 3 in winning_positions and  long_bet == hu_bet:
        pass 
    elif long_bet == hu_bet:
        valid_bet = total_all
        # print(valid_bet)
        if any(x in bet_totals_per_position for x in [12, 13]):
            valid_bet -= bet_totals_per_position.get(12, 0) + bet_totals_per_position.get(13, 0)
            # print(valid_bet)
        if all(x in bet_totals_per_position for x in [1, 2]):    
           valid_bet -= bet_totals_per_position.get(1, 0) + bet_totals_per_position.get(2, 0)
            # print(valid_bet)
        if len([x for x in [4, 5, 6, 7] if x in bet_totals_per_position]) >= 3:
            valid_bet -=   sum(bet_totals_per_position.get(x, 0) for x in [4, 5, 6, 7])
            # print(valid_bet)
        if len([x for x in [8, 9, 10, 11] if x in bet_totals_per_position]) >= 3:
            valid_bet -=   sum(bet_totals_per_position.get(x, 0) for x in [8, 9, 10, 11]) 
            # print(valid_bet)     



    # print(valid_bet)

        
        
    # 打印全部點位的下注總和
    # print(f"全部點位的下注總和為 {total_all}") 
    
    winning_totals_per_position = {}
    final_win = 0
    winning_amount_total = 0
    # 計算每個點位的中奖金额
    for pos, total in bet_totals.items():
        position_names = get_bet_position_name(pos)
        if pos in winning_positions:
            odds = get_odds(pos)
            if odds is not None:
                winning_amount = total * odds
                winning_totals_per_position[pos] = winning_amount
                winning_amount_total += winning_amount
                # print(f"點位 {position_names} 的總下注金額 {total} 乘以賠率 {odds}，中奖金额為 {winning_amount}")
            else:
                errors.append(f"局號 {game_no}, 點位 {position_names} 沒有找到賠率")
    
    #計算盈利金額
    
    final_win = winning_amount_total
    # 當和局時退還押庄贏 押庄輸
    if 3 in winning_positions :
        final_win = winning_amount_total
        if any(x in bet_totals_per_position for x in [12, 13]): 
            final_win += bet_totals_per_position.get(12, 0) + bet_totals_per_position.get(13, 0) 
    
    # 當和局且龍虎總下注相等時 
    if 3 in winning_positions and  long_bet == hu_bet:
        pass 
    # 當龍虎總下注相等時
    elif long_bet == hu_bet:
        final_win = winning_amount_total
        if any(x in bet_totals_per_position for x in [12, 13]):    
            final_win += bet_totals_per_position.get(12, 0) + bet_totals_per_position.get(13, 0) 
            # print(final_win)
        


    
    finally_win = final_win - total_all
    final_value_bet = valid_bet
    info_value_bet = bigdata['att'][0]['validBet']
    info_changes = bigdata['att'][0]['changes']

    if finally_win != info_changes:
        errors.append(f"局號 {game_no} 盈利金額錯誤: finally_win = {finally_win}, info_changes = {info_changes}")
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

print(f"總共驗證了 龙虎斗 {total_games} 局遊戲。")