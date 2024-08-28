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

    


def card_value(card):
    """
    将牌面名称转换为点数。
    
    :param card: 牌面名称
    :return: 点数
    """
    rank = card[2:]  # 获取牌面数字部分
    if rank == 'A':
        return 1
    elif rank in ['J', 'Q', 'K']:
        return 10
    else:
        return int(rank)

def card_number_to_name(card_number):
    """
    将牌的编号转换为牌面名称。
    
    :param card_number: 牌的编号
    :return: 牌面名称
    """
    suits = ['黑桃', '红心', '梅花', '方片']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    if 1 <= card_number <= 13:
        suit = suits[0]  # 黑桃
        rank = ranks[card_number - 1]
    elif 14 <= card_number <= 26:
        suit = suits[1]  # 红心
        rank = ranks[card_number - 14]
    elif 27 <= card_number <= 39:
        suit = suits[2]  # 梅花
        rank = ranks[card_number - 27]
    elif 40 <= card_number <= 52:
        suit = suits[3]  # 方片
        rank = ranks[card_number - 40]
    else:
        return None
    
    return f"{suit}{rank}"

def calculate_hand_type(cards):
    """
    计算手牌的牌型。
    
    :param cards: 手牌列表
    :return: 牌型名称
    """
    card_values = [card_value(card) for card in cards]

    def is_five_small_niu():
        return all(value < 5 for value in card_values) and sum(card_values) <= 10

    def is_four_of_a_kind():
        card_ranks = [card[2:] for card in cards]
        counts = {rank: card_ranks.count(rank) for rank in set(card_ranks)}
        return any(count == 4 for count in counts.values())

    def is_five_flower_niu():
        return all(card_value(card) == 10 for card in cards) and all(card[2:] in ['J', 'Q', 'K'] for card in cards)

    def is_four_flower_niu():
        card_ranks = [card[2:] for card in cards]
        flower_cards = [card for card in card_ranks if card in ['J', 'Q', 'K']]
        ten_cards = [card for card in card_ranks if card == '10']
    
        # 检查是否有 4 张 J、Q、K 和 1 张 10
        return len(flower_cards) == 4 and len(ten_cards) == 1
        # ten_cards = [card for card in cards if card[2:] == '10']
        # rank_counts = {rank: card_ranks.count(rank) for rank in ['J', 'Q', 'K']}
        
        # has_four_flower = all(rank_counts.get(rank, 0) >= 1 for rank in ['J', 'Q', 'K']) and len(ten_cards) == 1
        # return has_four_flower
        
    
   # 判断牌型顺序
    if is_five_small_niu():
        return "五小牛"
    if is_four_of_a_kind():
        return "四炸"
    if is_five_flower_niu():
        return "五花牛"
    if is_four_flower_niu():
        return "四花牛"
    
# 如果都不是，继续判断牛牛等其他类型
    for three_cards in combinations(card_values, 3):
        if sum(three_cards) % 10 == 0:
            remaining_cards = list(card_values)
            for card in three_cards:
                remaining_cards.remove(card)
            remaining_sum = sum(remaining_cards) % 10
            hand_types = {
                0: "牛牛", 9: "牛九", 8: "牛八", 7: "牛七",
                6: "牛六", 5: "牛五", 4: "牛四", 3: "牛三",
                2: "牛二", 1: "牛一"
            }
            return hand_types.get(remaining_sum, "没牛")

    return "没牛"

def compare_cards(cards1, cards2):
    """
    比较两手牌的大小。
    
    :param cards1: 第一手牌
    :param cards2: 第二手牌
    :return: 比较结果，1 表示第一手牌大，-1 表示第二手牌大，0 表示相同
    """
    hand_rankings = {
        "五小牛": 14, "四炸": 13, "五花牛": 12, "四花牛": 11, "牛牛": 10, 
        "牛九": 9, "牛八": 8, "牛七": 7, "牛六": 6, "牛五": 5, "牛四": 4, 
        "牛三": 3, "牛二": 2, "牛一": 1, "没牛": 0
    }

    hand_type1 = calculate_hand_type(cards1)
    hand_type2 = calculate_hand_type(cards2)

    # 比较牌型
    if hand_rankings[hand_type1] > hand_rankings[hand_type2]:
        return 1
    elif hand_rankings[hand_type1] < hand_rankings[hand_type2]:
        return -1
    else:
        # 牌型相同，比较最大单张
        def card_rank(card):
            rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1}
            return rank_order[card[2:]]
        
        def card_suit(card):
            suit_order = {'黑桃': 4, '红心': 3, '梅花': 2, '方片': 1}
            return suit_order[card[:2]]
        
        # Find the highest card in each hand
        highest_card1 = max(cards1, key=lambda card: (card_rank(card), card_suit(card)))
        highest_card2 = max(cards2, key=lambda card: (card_rank(card), card_suit(card)))

        if card_rank(highest_card1) > card_rank(highest_card2):
            return 1
        elif card_rank(highest_card1) < card_rank(highest_card2):
            return -1
        else:
            if card_suit(highest_card1) > card_suit(highest_card2):
                return 1
            elif card_suit(highest_card1) < card_suit(highest_card2):
                return -1

        return 0

def hand_multiplier(hand_type):
    """
    根据牌型返回倍数。
    
    :param hand_type: 牌型
    :return: 倍数
    """
    multipliers = {
        "没牛": 1, "牛一": 1, "牛二": 1, "牛三": 1, "牛四": 1, "牛五": 1, "牛六": 1,
        "牛七": 2, "牛八": 2, "牛九": 2, "牛牛": 3,
        "五小牛": 4, "四炸": 4, "五花牛": 4, "四花牛": 4
    }
    return multipliers.get(hand_type, 1)

def calculate_payout(bet, hand_type, banker_multiplier, player_multiplier):
    """
    根据牌型和倍数计算盈利金额。
    
    :param bet: 底注
    :param hand_type: 牌型
    :param banker_multiplier: 庄家倍数
    :param player_multiplier: 闲家倍数
    :param deduct: 抽水比例
    :return: 有效投注和盈利金额
    """    
    multiplier = hand_multiplier(hand_type)
    valid_bet = bet * multiplier * banker_multiplier * player_multiplier
    
    return valid_bet

def get_next_seat(seat, total_seats=5):
    return (seat % total_seats) + 1


error_log = []
def extract_blink_and_bets(data):
    total_games = len(data)
    for entry in tqdm(data, desc="驗證中",colour = "green"):
        game_id =  entry["log"]["data"]["roomData"].get("GameID")

        # if game_id == 830:
        #     # 进行验证逻辑
        #     print("GameID 是 830，开始进行验证。")
        #     # 在这里添加你的验证代码
        # else:
        #     print(f"GameID 不是 830，当前 GameID: {game_id}")  
            
        # Initialize game-specific variables
        used_cards = set()
        banker_valid_bet_total = 0
        banker_win_amount_total = 0
        player_loss_ratios = {}
        banker_deduct = 0  # Initialize banker_deduct
        f_valid_bet = 0
        f_final_win = 0
        f_deduct = 0
        f_valid_bets = {}
        f_final_wins = {}
        f_deducts = {}
        play_hand_type_ons = {}
       


        game_no = entry['gameNo']
        big_data = entry['log']['data']['big_data']
        
        
        # 提取底注
        blink = big_data.get('blink', None)
        if blink is None:
            print(f"GameNo: {game_no} 中未找到底注 (blink)")
            error_log.append((game_no,"中未找到底注 (blink)"))
            continue

        print(f"GameNo: {game_no}, 底注: {blink}")
        
        # 提取 act 中的下注数据
        act = big_data.get('act', [])
        bet_multiplier_bidding = {}
        bet_multiplier_player = {}
        
        for action in act:
            ty = action.get('ty')
            pos = action.get('pos')
            bet = action.get('bet')
            
            if ty == 2:  # 抢庄阶段
                bet_multiplier_bidding[pos] = bet
            elif ty == 4:  # 闲家下注阶段
                bet_multiplier_player[pos] = bet
        
        # 确定庄家
        all_seats = set(range(1, 6))  # 最多五个座位
        player_seats = set(bet_multiplier_player.keys())
        all_seats_with_bets = set(bet_multiplier_bidding.keys()) | player_seats
        banker_seats = all_seats - player_seats
        
        # 过滤掉没有下注数据的座位
        valid_banker_seats = banker_seats & all_seats_with_bets
        
        if len(valid_banker_seats) != 1:
            print(f"无法确定庄家: {valid_banker_seats}")
            error_log.append((game_no,f"无法确定庄家: {valid_banker_seats}"))
            continue
        
        banker_seat = list(valid_banker_seats)[0]
        banker_bet = bet_multiplier_bidding.get(banker_seat, None)
        if banker_bet == 0:
            banker_bet = 1
        
        print(f"庄家座位号: {banker_seat}, 抢庄倍数: {banker_bet}")
        
        for pos, bet in bet_multiplier_player.items():
            print(f"闲家座位号: {pos}, 下注倍数: {bet}")

        # 提取 att 中的数据
        att = big_data.get('att', [])
        player_info = {}
        card_info = {}

        for item in att:
            pos = item.get('pos')
            if pos is not None:
                player_info[pos] = {
                    'chip': item.get('chip'),
                    'deduct': item.get('deduct'),
                    'validBet': item.get('validBet'),
                    'changes': item.get('changes'),
                    'total': item.get('total'),
                    'cardType': item.get('cardType')
                }
                card_info[pos] = [card_number_to_name(card) for card in item.get('card', [])]
        
        # 验证牌是否重复    
        for pos, cards in card_info.items():
            for card in cards:
                if card in used_cards:
                    print(f"错误: GameNo {game_no}, 座位号 {pos} 的牌 {card} 已经出现过")
                    error_log.append((game_no,f"错误: GameNo {game_no}, 座位号 {pos} 的牌 {card} 已经出现过"))
                used_cards.add(card)
        
        for pos, info in player_info.items():
            cards = card_info.get(pos, [])
            hand_type = calculate_hand_type(cards)
            print(f"座位号: {pos}, 手牌: {', '.join(cards)}, 携带金额: {info['chip']}, 总投注: {info['total']}, 有效投注: {info['validBet']}, 盈利金额: {info['changes']}, 抽水: {info['deduct']}, 牌型编号: {info['cardType']}, 牌型: {hand_type}")
            
            
        # 打印每个座位的数据并验证牌型
        for pos, info in player_info.items():
            if pos != banker_seat:
                cards = card_info.get(pos, [])
                hand_type = calculate_hand_type(cards)
                player_cards = card_info[pos]
                banker_cards = card_info[banker_seat]
                compare_result = compare_cards(player_cards, banker_cards)
                player_bet = bet_multiplier_player[pos]
                player_hand_type = calculate_hand_type(player_cards)
                banker_hand_type = calculate_hand_type(banker_cards)
                
                
                handcard_rankings = {
                    "五小牛": 14, "四炸": 13, "五花牛": 12, "四花牛": 11, "牛牛": 10, 
                    "牛九": 9, "牛八": 8, "牛七": 7, "牛六": 6, "牛五": 5, "牛四": 4, 
                    "牛三": 3, "牛二": 2, "牛一": 1, "没牛": 0
                }
                
                player_hand_type_no = handcard_rankings[calculate_hand_type(player_cards)]
                banker_hand_type_no = handcard_rankings[calculate_hand_type(banker_cards)]   
                
                if compare_result == 1:  # 闲家赢
                    valid_bet = calculate_payout(blink, player_hand_type, banker_bet, player_bet)
                elif compare_result == -1:  # 庄家赢
                    valid_bet = calculate_payout(blink, banker_hand_type, banker_bet, player_bet)

                
                if valid_bet > info['chip']:
                    valid_bet = info['chip']
                
                if compare_result == 1:  # 闲家赢
                    # valid_bet = calculate_payout(blink, player_hand_type, banker_bet, player_bet)
                    win_amount = valid_bet
                    if win_amount > info['chip']:
                        win_amount = info['chip']
                    deduct = math.floor(win_amount * 0.05)  # Floor the deduct amount
                    final_amount = math.ceil(win_amount - deduct)  # Ceil the final amount
                    result = '赢'
                elif compare_result == -1:  # 庄家赢
                    # valid_bet = calculate_payout(blink, banker_hand_type, banker_bet, player_bet)
                    win_amount = valid_bet * -1
                    if abs(win_amount) > info['chip']:
                        win_amount = -info['chip']
                    final_amount = math.ceil(win_amount)  # Ceil the final amount
                    deduct = 0
                    result = '输'

                # print(f"座位号: {pos}, 闲家, 牌型: {player_hand_type}, 比较结果: {result}, 有效投注: {valid_bet}, 盈利金额: {final_amount}, 抽水: {deduct}")
                # f_valid_bet = valid_bet
                # f_final_win = final_amount
                # f_deduct = deduct
                # handcard_rankings = {
                #     "五小牛": 14, "四炸": 13, "五花牛": 12, "四花牛": 11, "牛牛": 10, 
                #     "牛九": 9, "牛八": 8, "牛七": 7, "牛六": 6, "牛五": 5, "牛四": 4, 
                #     "牛三": 3, "牛二": 2, "牛一": 1, "没牛": 0
                # }
                
                # player_hand_type_no = handcard_rankings[calculate_hand_type(player_cards)]
                # banker_hand_type_no = handcard_rankings[calculate_hand_type(banker_cards)]
                print(f"座位号: {pos}, 闲家, 牌型: {player_hand_type}, 牌型編號: {player_hand_type_no}, 比较结果: {result}, 有效投注: {valid_bet}, 盈利金额: {final_amount}, 抽水: {deduct}")
                banker_valid_bet_total += abs(valid_bet)
                banker_win_amount_total += win_amount
                player_loss_ratios[pos] = abs(valid_bet)
    
                f_valid_bets[pos] = valid_bet
                f_final_wins[pos]  = final_amount
                f_deducts[pos]  = deduct
                play_hand_type_ons[pos] = player_hand_type_no
               
            

                
        if banker_valid_bet_total <= player_info[banker_seat]['chip']:
                # 閒家
            for pos, info in player_info.items():
                if pos != banker_seat:
                    f_valid_bet = f_valid_bets[pos]
                    f_final_win = f_final_wins[pos]
                    f_deduct = f_deducts[pos]
                    player_hand_type_no = play_hand_type_ons[pos]
                    if f_valid_bet != info['validBet'] or f_final_win != info['changes'] or f_deduct != info['deduct'] or player_hand_type_no != info['cardType']:
                        if f_valid_bet != info['validBet']:
                            print(f"座位号: {pos} 的有效投注 (1f_valid_bet) 对比错误: 计算值 = {f_valid_bet}, 记录值 = {info['validBet']}")
                            error_log.append((game_no,f"座位号: {pos} 的有效投注 (1f_valid_bet) 对比错误: 计算值 = {f_valid_bet}, 记录值 = {info['validBet']}"))
                        if f_final_win != info['changes']:
                            print(f"座位号: {pos} 的盈利金额 (1f_final_win) 对比错误: 计算值 = {f_final_win}, 记录值 = {info['changes']}")
                            error_log.append((game_no,f"座位号: {pos} 的盈利金额 (1f_final_win) 对比错误: 计算值 = {f_final_win}, 记录值 = {info['changes']}"))
                        if f_deduct != info['deduct']:
                            print(f"座位号: {pos} 的抽水 (1f_deduct) 对比错误: 计算值 = {f_deduct}, 记录值 = {info['deduct']}")
                            error_log.append((game_no,f"座位号: {pos} 的抽水 (1f_deduct) 对比错误: 计算值 = {f_deduct}, 记录值 = {info['deduct']}"))
                        if player_hand_type_no != info['cardType']:
                            print(f"座位号: {pos} 的牌型編號 (player_hand_type_no) 对比错误: 计算值 = {player_hand_type_no}, 记录值 = {info['cardType']}")
                            error_log.append((game_no,f"座位号: {pos} 的牌型編號 (player_hand_type_no) 对比错误: 计算值 = {player_hand_type_no}, 记录值 = {info['cardType']}"))
                    else:
                        print("ok") 
            
        banker_chip = player_info[banker_seat]['chip']
        
        if  banker_valid_bet_total <= banker_chip :
            banker_win_amount_total = -banker_win_amount_total 
            if banker_win_amount_total > 0:
                banker_deduct = math.floor(banker_win_amount_total * 0.05)
                banker_win_amount_total = math.ceil(banker_win_amount_total * 0.95)
            else:
                banker_deduct = 0
            
            print(f"座位号: {banker_seat}, 庄家, 牌型: {banker_hand_type}, 牌型編號: {banker_hand_type_no}, 比较结果: {result}, 有效投注: {banker_valid_bet_total}, 盈利金额: {banker_win_amount_total}, 抽水: {banker_deduct}")
        # 庄家
        if banker_valid_bet_total <= player_info[banker_seat]['chip']:
            if (banker_valid_bet_total != player_info[banker_seat]['validBet'] or
                banker_win_amount_total != player_info[banker_seat]['changes'] or
                banker_deduct != player_info[banker_seat]['deduct'] or
                banker_hand_type_no != player_info[banker_seat]['cardType']):
                
                if banker_valid_bet_total != player_info[banker_seat]['validBet']:
                    print(f"座位号: {banker_seat} 的有效投注 (banker_valid_bet_total) 对比错误: 计算值 = {banker_valid_bet_total}, 记录值 = {player_info[banker_seat]['validBet']}")
                    error_log.append((game_no,f"座位号: {banker_seat} 的有效投注 (banker_valid_bet_total) 对比错误: 计算值 = {banker_valid_bet_total}, 记录值 = {player_info[banker_seat]['validBet']}"))
                if banker_win_amount_total != player_info[banker_seat]['changes']:
                    print(f"座位号: {banker_seat} 的盈利金额 (banker_win_amount_total) 对比错误: 计算值 = {banker_win_amount_total}, 记录值 = {player_info[banker_seat]['changes']}")
                    error_log.append((game_no,f"座位号: {banker_seat} 的盈利金额 (banker_win_amount_total) 对比错误: 计算值 = {banker_win_amount_total}, 记录值 = {player_info[banker_seat]['changes']}"))
                if banker_deduct != player_info[banker_seat]['deduct']:
                    print(f"座位号: {banker_seat} 的抽水 (banker_deduct) 对比错误: 计算值 = {banker_deduct}, 记录值 = {player_info[banker_seat]['deduct']}")
                    error_log.append((game_no,f"座位号: {banker_seat} 的抽水 (banker_deduct) 对比错误: 计算值 = {banker_deduct}, 记录值 = {player_info[banker_seat]['deduct']}"))
                if banker_hand_type_no != player_info[banker_seat]['cardType']:
                    print(f"座位号: {banker_seat} 的牌型編號 (banker_hand_type_no) 对比错误: 计算值 = {banker_hand_type_no}, 记录值 = {player_info[banker_seat]['cardType']}")
                    error_log.append((game_no,f"座位号: {banker_seat} 的牌型編號 (banker_hand_type_no) 对比错误: 计算值 = {banker_hand_type_no}, 记录值 = {player_info[banker_seat]['cardType']}"))
            else:
                print("okb")   
        # 计算庄家抽水后的盈利金额
        banker_chip = player_info[banker_seat]['chip']
        
        if banker_valid_bet_total > banker_chip:
            banker_valid_bet_total = banker_chip
            banker_win_amount_total = -banker_win_amount_total
            
            
            if banker_win_amount_total > 0:
                if banker_win_amount_total > banker_chip:
                    # 庄家盈利超过携带金额，按比例分配
                    remaining_banker_chip = banker_chip
                    total_loss = sum(player_loss_ratios.values())
                    player_loss = {}
                    
                  
                        


                    for pos, info in player_info.items():
                    
                        if pos != banker_seat:
                            player_cards = card_info[pos]
                            compare_result = compare_cards(player_cards, banker_cards)
                            if compare_result == -1:  # 庄家赢
                                win_amount = calculate_payout(blink, calculate_hand_type(player_cards), banker_bet, bet_multiplier_player[pos]) * -1
                                
                                if abs(win_amount) > info['chip']:
                                    win_amount = -info['chip']
                                player_loss[pos] = math.ceil(win_amount)  # Ceil the final amount
                                deduct = 0
                        
                    next_to_banker_seat = get_next_seat(banker_seat)
                    f_final_win_list = []
                    f_final_win_dict = {}
                    f_valid_bet_dict = {}
                    f_deduct_dict = {}
                    player_hand_type_no_dict = {}

                    num_players = len(player_loss_ratios) +1
                    # print(num_players)
                    for pos, loss in player_loss_ratios.items():
                        
                        
                        player_cards = card_info[pos]
                        banker_cards = card_info[banker_seat]
                        compare_result = compare_cards(player_cards, banker_cards)
                        player_bet = bet_multiplier_player[pos]
                        player_hand_type = calculate_hand_type(player_cards)
                        banker_hand_type = calculate_hand_type(banker_cards)
                        if compare_result == 1:  # 闲家赢
                            valid_bet = calculate_payout(blink, player_hand_type, banker_bet, player_bet)
                            if valid_bet > player_info[pos]['chip'] :
                                valid_bet = player_info[pos]['chip'] 
                        elif compare_result == -1:  # 庄家赢
                            valid_bet = calculate_payout(blink, banker_hand_type, banker_bet, player_bet)
                            if valid_bet > player_info[pos]['chip'] :
                                valid_bet = player_info[pos]['chip']
                               
                        proportionate_loss = loss / total_loss * remaining_banker_chip
                        if pos == next_to_banker_seat:
                            f_final_win = math.ceil(-proportionate_loss)
                        else:
                            f_final_win = math.ceil(-proportionate_loss)

                        handcard_rankings = {
                            "五小牛": 14, "四炸": 13, "五花牛": 12, "四花牛": 11, "牛牛": 10, 
                            "牛九": 9, "牛八": 8, "牛七": 7, "牛六": 6, "牛五": 5, "牛四": 4, 
                            "牛三": 3, "牛二": 2, "牛一": 1, "没牛": 0
                        }
                        player_hand_type_no = handcard_rankings[calculate_hand_type(player_cards)]


                        f_final_win_list.append(f_final_win)
                        player_hand_type_no_dict[pos] = player_hand_type_no
                        f_deduct_dict[pos] = deduct
                        f_valid_bet_dict[pos] = valid_bet
                        player_cards = card_info[pos]
                        f_final_win_dict[pos] = f_final_win
                        
                       

                     
                    
                    next_to_banker_seat = ((banker_seat - 1 + 1) % num_players) + 1
                    print(f"Initial next_to_banker_seat: {next_to_banker_seat}")
                    sum_f_final_win = sum(f_final_win_list)
                    difference = - remaining_banker_chip - sum_f_final_win
                    print(difference) 
                    for pos, loss in player_loss_ratios.items():
                        if difference != 0:
                            index = next_to_banker_seat
                            print(f"Starting adjustment from index {index}")
                            adjusted_players = set()
                            while difference != 0:
                                if index not in f_final_win_dict:
                                    print(f"Skipping index {index} as it is not in f_final_win_dict")
                                    index = (index + 1) % num_players
                                    continue
                                print(f"Adjusting index {index} with current difference {difference}")
                                if difference < 0:
                                    # 需要减少 f_final_win
                                    f_final_win_dict[index] -= 1
                                    print(f_final_win_dict)
                                    difference += 1
                                else:
                                    # 需要增加 f_final_win
                                    f_final_win_dict[index] += 1
                                    difference -= 1
                                    print(f_final_win_dict)
                                adjusted_players.add(index)    

                                index = ((index - 1 + 1) % num_players) + 1
                                # 確保不會無限迴圈
                                if len(adjusted_players) == num_players:
                                    # print(f"Adjusting index {index} with current difference {difference}")
                                    adjusted_players.clear()
                                # if index in adjusted_players:
                                #     # 如果所有玩家都已被调整过，则重置调整过的玩家集合
                                #     adjusted_players.clear()

                                # # 确保不调整到庄家
                                # if index == banker_seat:
                                #     index = (index + 1) % num_players
                    
                                # 打印结果
                                # print(f_final_win_dict)
                                # print(f_valid_bet_dict)
                                # print(sum(f_final_win_list))
                        


                    for pos in f_final_win_dict:
                        f_final_win = f_final_win_dict[pos]
                        f_valid_bet = f_valid_bet_dict[pos]  # 如果座位号不在字典中，默认为0
                        f_deduct = f_deduct_dict[pos]
                        player_hand_type_no = player_hand_type_no_dict[pos]
                        handcard_rankings = {
                        "五小牛": 14, "四炸": 13, "五花牛": 12, "四花牛": 11, "牛牛": 10, 
                        "牛九": 9, "牛八": 8, "牛七": 7, "牛六": 6, "牛五": 5, "牛四": 4, 
                        "牛三": 3, "牛二": 2, "牛一": 1, "没牛": 0
                    }
                    
                        
                        banker_hand_type_no = handcard_rankings[calculate_hand_type(banker_cards)]

                        print(f"座位号: {pos}, 最終有效投注: {f_valid_bet}, 最終输的金额: {f_final_win}, 最終抽水: {f_deduct}")
                        if (f_valid_bet != player_info[pos]['validBet'] or
                            f_final_win != player_info[pos]['changes'] or
                            f_deduct != player_info[pos]['deduct'] or
                            player_hand_type_no != player_info[pos]['cardType']):
                            
                            if f_valid_bet != player_info[pos]['validBet']:
                                print(f"座位号: {pos}, 的最終有效投注 对比错误: 计算值 = {f_valid_bet}, 记录值 = {player_info[pos]['validBet']}")
                                error_log.append((game_no,f"座位号: {pos}, 的最終有效投注 对比错误: 计算值 = {f_valid_bet}, 记录值 = {player_info[pos]['validBet']}"))
                            if f_final_win != player_info[pos]['changes']:
                                print(f"座位号: {pos}, 的最終赢的金额 对比错误: 计算值 = {f_final_win}, 记录值 = {player_info[pos]['changes']}")    
                                error_log.append((game_no,f"座位号: {pos}, 的最終赢的金额 对比错误: 计算值 = {f_final_win}, 记录值 = {player_info[pos]['changes']}") )
                            if f_deduct != player_info[pos]['deduct']:
                                print(f"座位号: {pos}, 的最終抽水 对比错误: 计算值 = {f_deduct}, 记录值 = {player_info[pos]['deduct']}")
                                error_log.append((game_no,f"座位号: {pos}, 的最終抽水 对比错误: 计算值 = {f_deduct}, 记录值 = {player_info[pos]['deduct']}"))
                            if player_hand_type_no != player_info[pos]['cardType']:
                                print(f"座位号: {pos}, 的牌型編號 对比错误: 计算值 = {player_hand_type_no}, 记录值 = {player_info[pos]['cardType']}")
                                error_log.append((game_no,f"座位号: {pos}, 的牌型編號 对比错误: 计算值 = {player_hand_type_no}, 记录值 = {player_info[pos]['cardType']}"))
                        else:
                            print("ok1")

                banker_win_amount_total = banker_chip
                banker_deduct = math.floor(banker_win_amount_total * 0.05)  # Floor the deduct amount
                banker_win_amount_total = math.ceil(banker_win_amount_total * 0.95)  # Ceil the win amount after deduct

                banker_cards = card_info[banker_seat]
                banker_hand_type = calculate_hand_type(banker_cards)
                # print(f"座位号Q: {banker_seat}, 庄家, 牌型: {banker_hand_type}, 比较结果: {'赢' if banker_win_amount_total > 0 else '输'}, 有效投注: {banker_valid_bet_total}, 盈利金额: {banker_win_amount_total}, 抽水: {banker_deduct}")
                bank_f_final_win = banker_win_amount_total
                bank_f_deduct = banker_deduct
                print(f"座位号: {banker_seat}, 庄家, 牌型: {banker_hand_type}, 牌型編號:{banker_hand_type_no}, 比较结果: {'赢' if banker_win_amount_total > 0 else '输'}, 最終有效投注: {banker_valid_bet_total}, 最終盈利金额: {bank_f_final_win}, 最終抽水: {bank_f_deduct}")            
                print(f"座位号: {banker_seat}, 最終有效投注: {banker_valid_bet_total}, 最終赢的金额: {bank_f_final_win}, 最終抽水: {bank_f_deduct}")
                if (banker_valid_bet_total != player_info[banker_seat]['validBet'] or
                    bank_f_final_win != player_info[banker_seat]['changes'] or
                    bank_f_deduct != player_info[banker_seat]['deduct'] or
                    banker_hand_type_no != player_info[banker_seat]['cardType']):

                    if banker_valid_bet_total != player_info[banker_seat]['validBet']:
                        print(f"座位号: {banker_seat}, 的最終有效投注 对比错误: 计算值 = {banker_valid_bet_total}, 记录值 = {player_info[banker_seat]['validBet']}")
                        error_log.append((game_no,f"座位号: {banker_seat}, 的最終有效投注 对比错误: 计算值 = {banker_valid_bet_total}, 记录值 = {player_info[banker_seat]['validBet']}"))
                    if bank_f_final_win != player_info[banker_seat]['changes']:
                        print(f"座位号: {banker_seat}, 的最終赢的金额 对比错误: 计算值 = {bank_f_final_win}, 记录值 = {player_info[banker_seat]['changes']}")    
                        error_log.append((game_no,f"座位号: {banker_seat}, 的最終赢的金额 对比错误: 计算值 = {bank_f_final_win}, 记录值 = {player_info[banker_seat]['changes']}"))
                    if bank_f_deduct != player_info[banker_seat]['deduct']:
                        print(f"座位号: {banker_seat}, 的最終抽水 对比错误: 计算值 = {bank_f_deduct}, 记录值 = {player_info[banker_seat]['deduct']}")
                        error_log.append((game_no,f"座位号: {banker_seat}, 的最終抽水 对比错误: 计算值 = {bank_f_deduct}, 记录值 = {player_info[banker_seat]['deduct']}"))
                    if banker_hand_type_no != player_info[banker_seat]['cardType']:
                        print(f"座位号: {banker_seat}, 的牌型編號 对比错误: 计算值 = {banker_hand_type_no}, 记录值 = {player_info[banker_seat]['cardType']}")
                        error_log.append((game_no,f"座位号: {banker_seat}, 的牌型編號 对比错误: 计算值 = {banker_hand_type_no}, 记录值 = {player_info[banker_seat]['cardType']}"))
                else:
                    print("ok2")

            else:
                if abs(banker_win_amount_total) > banker_chip:
                    # 庄家亏损超过携带金额，按比例分配
                    remaining_banker_chip = banker_chip
                    player_wins = {}
                    
                    for pos, info in player_info.items():
                        
                        if pos != banker_seat:
                            player_cards = card_info[pos]
                            compare_result = compare_cards(player_cards, banker_cards)
                            if compare_result == 1:  # 闲家赢，记录闲家盈利
                                win_amount = calculate_payout(blink, calculate_hand_type(player_cards), banker_bet, bet_multiplier_player[pos])
                                if win_amount > info['chip']:
                                    win_amount = info['chip']
                                player_wins[pos] = win_amount
                        
                    total_wins = sum(player_wins.values())
                    next_to_banker_seat = get_next_seat(banker_seat)
                    for pos, win in player_wins.items():
                        player_cards = card_info[pos]
                        banker_cards = card_info[banker_seat]
                        compare_result = compare_cards(player_cards, banker_cards)
                        player_bet = bet_multiplier_player[pos]
                        player_hand_type = calculate_hand_type(player_cards)
                        banker_hand_type = calculate_hand_type(banker_cards)
                        if compare_result == 1:  # 闲家赢
                            valid_bet = calculate_payout(blink, player_hand_type, banker_bet, player_bet)
                        elif compare_result == -1:  # 庄家赢
                            valid_bet = calculate_payout(blink, banker_hand_type, banker_bet, player_bet) 
                        proportionate_win = win / total_wins * remaining_banker_chip
                        deduct = math.floor(proportionate_win * 0.05)  # Floor the deduct amount
                        final_win = math.ceil(proportionate_win * 0.95)  # Ceil the final amount
                        if pos == next_to_banker_seat:
                            final_win = final_win + 1  # Ceil the final amount for the next to banker seat
                        else:
                            final_win = final_win  # Floor the final amount for other seats

                        f_final_win = final_win
                        f_deduct = deduct
                        f_valid_bet = valid_bet
                        player_cards = card_info[pos]
                        handcard_rankings = {
                        "五小牛": 14, "四炸": 13, "五花牛": 12, "四花牛": 11, "牛牛": 10, 
                        "牛九": 9, "牛八": 8, "牛七": 7, "牛六": 6, "牛五": 5, "牛四": 4, 
                        "牛三": 3, "牛二": 2, "牛一": 1, "没牛": 0
                    }
                    
                        player_hand_type_no = handcard_rankings[calculate_hand_type(player_cards)]
                        banker_hand_type_no = handcard_rankings[calculate_hand_type(banker_cards)]
                        print(f"座位号: {pos}, 最終有效投注: {f_valid_bet}, 最終赢的金额: {f_final_win}, 最終抽水: {f_deduct}")
                        if (f_valid_bet != player_info[pos]['validBet'] or
                            f_final_win != player_info[pos]['changes'] or
                            f_deduct != player_info[pos]['deduct'] or
                            player_hand_type_no != player_info[pos]['cardType']):
                            
                            if f_valid_bet != player_info[pos]['validBet']:
                                print(f"座位号: {pos}, 的最終有效投注 对比错误: 计算值 = {f_valid_bet}, 记录值 = {player_info[pos]['validBet']}")
                                error_log.append((game_no,f"座位号: {pos}, 的最終有效投注 对比错误: 计算值 = {f_valid_bet}, 记录值 = {player_info[pos]['validBet']}"))       
                            if f_final_win != player_info[pos]['changes']:
                                print(f"座位号: {pos}, 的最終赢的金额 对比错误: 计算值 = {f_final_win}, 记录值 = {player_info[pos]['changes']}")    
                                error_log.append((game_no,f"座位号: {pos}, 的最終赢的金额 对比错误: 计算值 = {f_final_win}, 记录值 = {player_info[pos]['changes']}"))         
                            if f_deduct != player_info[pos]['deduct']:
                                print(f"座位号: {pos}, 的最終抽水 对比错误: 计算值 = {f_deduct}, 记录值 = {player_info[pos]['deduct']}")
                                error_log.append((game_no,f"座位号: {pos}, 的最終抽水 对比错误: 计算值 = {f_deduct}, 记录值 = {player_info[pos]['deduct']}"))       
                            if player_hand_type_no != player_info[pos]['cardType']:
                                print(f"座位号: {pos}, 的牌型編號 对比错误: 计算值 = {player_hand_type_no}, 记录值 = {player_info[pos]['cardType']}")
                                error_log.append((game_no,f"座位号: {pos}, 的牌型編號 对比错误: 计算值 = {player_hand_type_no}, 记录值 = {player_info[pos]['cardType']}"))
                        else:
                            print("ok3")       

                    banker_win_amount_total = -banker_chip
                    banker_deduct = 0

                    banker_cards = card_info[banker_seat]
                    banker_hand_type = calculate_hand_type(banker_cards)
                    # print(f"座位号: {banker_seat}, 庄家, 牌型: {banker_hand_type}, 比较结果: {'赢' if banker_win_amount_total > 0 else '输'}, 有效投注: {banker_valid_bet_total}, 盈利金额: {banker_win_amount_total}, 抽水: {banker_deduct}")
                    bank_f_final_win = banker_win_amount_total
                    bank_f_deduct = banker_deduct
                    print(f"座位号: {banker_seat}, 庄家, 牌型: {banker_hand_type}, 牌型編號:{banker_hand_type_no}, 比较结果: {'赢' if banker_win_amount_total > 0 else '输'}, 最終有效投注: {banker_valid_bet_total}, 最終盈利金额: {bank_f_final_win}, 最終抽水: {bank_f_deduct}")            
                    print(f"座位号: {banker_seat}, 最終有效投注: {banker_valid_bet_total}, 最終輸的金额: {bank_f_final_win}, 最終抽水: {bank_f_deduct}")
                    if (banker_valid_bet_total != player_info[banker_seat]['validBet'] or
                        bank_f_final_win != player_info[banker_seat]['changes'] or
                        bank_f_deduct != player_info[banker_seat]['deduct'] or
                        banker_hand_type_no != player_info[banker_seat]['cardType']):

                        if banker_valid_bet_total != player_info[banker_seat]['validBet']:
                            print(f"座位号: {banker_seat}, 的最終有效投注 对比错误: 计算值 = {banker_valid_bet_total}, 记录值 = {player_info[banker_seat]['validBet']}")
                            error_log.append((game_no,f"座位号: {banker_seat}, 的最終有效投注 对比错误: 计算值 = {banker_valid_bet_total}, 记录值 = {player_info[banker_seat]['validBet']}"))
                        if bank_f_final_win != player_info[banker_seat]['changes']:
                            print(f"座位号: {banker_seat}, 的最終赢的金额 对比错误: 计算值 = {bank_f_final_win}, 记录值 = {player_info[banker_seat]['changes']}")    
                            error_log.append((game_no,f"座位号: {banker_seat}, 的最終赢的金额 对比错误: 计算值 = {bank_f_final_win}, 记录值 = {player_info[banker_seat]['changes']}"))
                        if bank_f_deduct != player_info[banker_seat]['deduct']:
                            print(f"座位号: {banker_seat}, 的最終抽水 对比错误: 计算值 = {bank_f_deduct}, 记录值 = {player_info[banker_seat]['deduct']}")
                            error_log.append((game_no,f"座位号: {banker_seat}, 的最終抽水 对比错误: 计算值 = {bank_f_deduct}, 记录值 = {player_info[banker_seat]['deduct']}"))
                        if banker_hand_type_no != player_info[banker_seat]['cardType']:
                            print(f"座位号: {banker_seat}, 的牌型編號 对比错误: 计算值 = {banker_hand_type_no}, 记录值 = {player_info[banker_seat]['cardType']}")
                            error_log.append((game_no,f"座位号: {banker_seat}, 的牌型編號 对比错误: 计算值 = {banker_hand_type_no}, 记录值 = {player_info[banker_seat]['cardType']}"))
                    else:
                        print("ok4")
    print(f"总共验证了 {total_games} 局游戏。")
    if error_log:
        print("验证过程中发现以下错误：")
        for game_no, error in error_log:
            print(f"游戏编号 {game_no}: {error}")
    else:
        print("所有游戏条目均验证通过。")

# 示例调用
file_path = 'C:/Users/arsene.lee/Desktop/test1/game_logs22.json'
game_data = load_game_data(file_path)

if game_data:
    extract_blink_and_bets(game_data)