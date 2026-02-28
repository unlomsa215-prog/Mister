import telebot
from telebot import types
import random
import time
import json
import os
from threading import Timer, Lock, RLock
from datetime import datetime, timedelta
import string
import hashlib
import sys
import signal

# ====================== КОНФИГУРАЦИЯ ======================
TOKEN = os.getenv('BOT_TOKEN', '8019174987:AAFd_qG434htnd94mnCOZfd2ejD0hgTGUJk')
ADMIN_PASSWORD_HASH = hashlib.sha256('Kyniksvs1832'.encode()).hexdigest()

OWNER_USERNAME = '@kyniks'
CHANNEL_USERNAME = '@werdoxz_wiinere'
CHAT_LINK = 'https://t.me/+B7u5OmPsako4MTAy'

# Файлы для хранения данных
DATA_FILE = 'bot_data.json'
USERNAME_CACHE_FILE = 'username_cache.json'
PROMO_FILE = 'promocodes.json'
BUSINESS_FILE = 'business_data.json'
CLAN_FILE = 'clan_data.json'
ACHIEVEMENTS_FILE = 'achievements.json'
QUESTS_FILE = 'quests_data.json'
EVENT_FILE = 'event_data.json'
CASES_FILE = 'cases_data.json'
ORDERS_FILE = 'orders.json'
CHEQUES_FILE = 'cheques.json'
MICE_FILE = 'mice_data.json'
PETS_FILE = 'pets_data.json'
BANK_FILE = 'bank_data.json'
PHONE_FILE = 'phone_data.json'
BONUS_FILE = 'bonus_data.json'
DUEL_FILE = 'duel_data.json'
TOURNAMENT_FILE = 'tournament_data.json'
STATS_FILE = 'stats_data.json'
DAILY_QUESTS_FILE = 'daily_quests.json'

MAX_BET = 100000000
GAME_TIMEOUT = 300

# Константы для игр
TOWER_MULTIPLIERS = {1: 1.0, 2: 1.5, 3: 2.5, 4: 4.0, 5: 6.0}
FOOTBALL_MULTIPLIER = 2.0
BASKETBALL_MULTIPLIER = 2.0
PYRAMID_CELLS = 10
PYRAMID_MULTIPLIER = 5.0
DARTS_MULTIPLIERS = {1: 1.5, 2: 2.0, 3: 3.0, 4: 5.0, 5: 10.0}
POKER_MULTIPLIER = 2.0
MINES_MULTIPLIERS = {
    1: {1: 1.1, 2: 1.2, 3: 1.3, 4: 1.4, 5: 1.5, 6: 1.6, 7: 1.7, 8: 1.8, 9: 1.9, 10: 2.0},
    2: {1: 1.2, 2: 1.4, 3: 1.6, 4: 1.8, 5: 2.0, 6: 2.2, 7: 2.4, 8: 2.6, 9: 2.8, 10: 3.0},
    3: {1: 1.3, 2: 1.6, 3: 2.0, 4: 2.4, 5: 2.8, 6: 3.2, 7: 3.6, 8: 4.0, 9: 4.5, 10: 5.0},
    4: {1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0, 7: 4.5, 8: 5.0, 9: 5.5, 10: 6.0},
    5: {1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: 9.0, 9: 10.0, 10: 12.0}
}
BLACKJACK_MULTIPLIER = 2.0
SLOTS_SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
SLOTS_PAYOUTS = {
    ('7️⃣', '7️⃣', '7️⃣'): 10.0,
    ('💎', '💎', '💎'): 5.0,
    ('🍇', '🍇', '🍇'): 3.0,
    ('🍊', '🍊', '🍊'): 2.0,
    ('🍋', '🍋', '🍋'): 1.5,
    ('🍒', '🍒', '🍒'): 1.2
}
HILO_MULT = 2.0
HILO_WIN_CHANCE = 0.5
ROULETTE_NUMBERS = list(range(37))
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
ROULETTE_MULTIPLIERS = {
    'straight': 36,
    'red': 2,
    'black': 2,
    'even': 2,
    'odd': 2,
    '1-18': 2,
    '19-36': 2,
    'dozen': 3
}

# Ивент
RELEASE_EVENT = {
    'active': True,
    'multiplier': 2.0,
    'end_time': time.time() + 7 * 86400
}

# ====================== VIP СИСТЕМА ======================
VIP_LEVELS = {
    'bronze': {
        'name': '🥉 Бронзовый',
        'price': 50000,
        'duration': 30 * 86400,
        'bonus_mult': 1.1,
        'daily_bonus_mult': 1.2,
        'work_mult': 1.5,
        'max_bet_mult': 1.5,
        'quest_slots': 3,
        'krds_weekly': 5,
        'color': '🟫',
        'perks': [
            '🎁 +10% к выигрышам',
            '💰 +20% к ежедневному бонусу',
            '💼 x1.5 на работе',
            '🎰 +50% к макс ставке',
            '💎 +5 KRDS в неделю',
            '📋 3 ежедневных квеста'
        ]
    },
    'silver': {
        'name': '🥈 Серебряный',
        'price': 150000,
        'duration': 30 * 86400,
        'bonus_mult': 1.2,
        'daily_bonus_mult': 1.5,
        'work_mult': 2,
        'max_bet_mult': 2,
        'quest_slots': 4,
        'krds_weekly': 15,
        'color': '⚪️',
        'perks': [
            '🎁 +20% к выигрышам',
            '💰 +50% к ежедневному бонусу',
            '💼 x2 на работе',
            '🎰 x2 к макс ставке',
            '💎 +15 KRDS в неделю',
            '📋 4 ежедневных квеста'
        ]
    },
    'gold': {
        'name': '🥇 Золотой',
        'price': 500000,
        'duration': 30 * 86400,
        'bonus_mult': 1.5,
        'daily_bonus_mult': 2,
        'work_mult': 3,
        'max_bet_mult': 3,
        'quest_slots': 5,
        'krds_weekly': 30,
        'color': '🌟',
        'perks': [
            '🎁 +50% к выигрышам',
            '💰 x2 к ежедневному бонусу',
            '💼 x3 на работе',
            '🎰 x3 к макс ставке',
            '💎 +30 KRDS в неделю',
            '📋 5 ежедневных квестов'
        ]
    },
    'platinum': {
        'name': '💎 Платиновый',
        'price': 1000000,
        'duration': 30 * 86400,
        'bonus_mult': 2,
        'daily_bonus_mult': 3,
        'work_mult': 5,
        'max_bet_mult': 5,
        'quest_slots': 6,
        'krds_weekly': 50,
        'color': '💫',
        'perks': [
            '🎁 x2 к выигрышам',
            '💰 x3 к ежедневному бонусу',
            '💼 x5 на работе',
            '🎰 x5 к макс ставке',
            '💎 +50 KRDS в неделю',
            '📋 6 ежедневных квестов'
        ]
    }
}

# ====================== ЕЖЕДНЕВНЫЕ КВЕСТЫ ======================
DAILY_QUESTS = {
    'play_games': {
        'name': '🎮 Игроман',
        'desc': 'Сыграть {target} игр',
        'rewards': {1: 500, 3: 2000, 5: 5000, 10: 15000},
        'icon': '🎮',
        'type': 'games_played'
    },
    'win_games': {
        'name': '🏆 Победитель',
        'desc': 'Выиграть {target} игр',
        'rewards': {1: 1000, 3: 3000, 5: 7500, 10: 20000},
        'icon': '🏆',
        'type': 'wins'
    },
    'work': {
        'name': '💼 Трудяга',
        'desc': 'Поработать {target} раз',
        'rewards': {1: 500, 3: 1500, 5: 3000, 10: 8000},
        'icon': '💼',
        'type': 'works'
    },
    'referrals': {
        'name': '🤝 Реферал',
        'desc': 'Пригласить {target} друзей',
        'rewards': {1: 5000, 3: 15000, 5: 30000},
        'icon': '🤝',
        'type': 'referrals'
    },
    'games_big_win': {
        'name': '🎰 Крупный выигрыш',
        'desc': 'Выиграть {target} кредиксов за одну игру',
        'rewards': {10000: 2000, 50000: 10000, 100000: 25000, 500000: 100000},
        'icon': '🎰',
        'type': 'biggest_win'
    }
}

# ====================== ТУРНИРЫ ======================
TOURNAMENT_TYPES = {
    'daily': {
        'name': '📅 Ежедневный',
        'duration': 86400,
        'prize_pool': 100000,
        'entry_fee': 1000
    },
    'weekly': {
        'name': '📆 Еженедельный',
        'duration': 604800,
        'prize_pool': 500000,
        'entry_fee': 5000
    },
    'monthly': {
        'name': '📅 Месячный',
        'duration': 2592000,
        'prize_pool': 2000000,
        'entry_fee': 20000
    }
}

# ====================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ======================
users = {}
username_cache = {}
game_timers = {}
crash_update_timers = {}
crash_locks = {}
admin_users = set()
promocodes = {}
orders = {}
next_order_id = 1
cheques = {}
user_cases = {}
user_achievements = {}
user_quests = {}
duels = {}
clans = {}
businesses = {}
event_data = {'active': True, 'participants': {}, 'leaderboard': [], 'last_update': time.time()}
jackpot = {'total': 0, 'last_winner': None, 'last_win_time': None, 'history': []}
daily_reward = {}
daily_quests_data = {}
tournaments = {}

bank_data = {
    'loans': {},
    'deposits': {},
    'transfers': [],
    'total_deposits': 0,
    'interest_rate': 0.05
}

phone_data = {
    'contacts': {},
    'calls': {},
    'messages': {},
    'phone_numbers': {}
}

bonus_data = {
    'daily': {},
    'weekly': {},
    'monthly': {},
    'referral_bonus': 5000
}

pets_data = {}
clans_data = {}
businesses_data = {}
stats_data = {}

data_lock = RLock()
user_locks = {}

MICE_DATA = {
    'standard': {
        'name': '💖 Мышка - стандарт 💖',
        'price': 100000,
        'total': 100,
        'sold': 0,
        'rarity': 'обычная',
        'description': '👻 Для украшения аккаунта',
        'signature': 'kyn k.y 🌟',
        'version': 'стандарт',
        'income': 500,
        'income_interval': 3600,
        'icon': '🐭'
    },
    'china': {
        'name': '🤩 Мышка - чуньхаохаокакао 🤩',
        'price': 500000,
        'total': 100,
        'sold': 0,
        'rarity': 'средняя',
        'description': '💖 Китайская коллекционная мышка',
        'signature': 'chinalals k.y 💖',
        'version': 'china',
        'income': 1000,
        'income_interval': 3600,
        'icon': '🐹'
    },
    'world': {
        'name': '🌍 Мышка - мира 🌍',
        'price': 1000000,
        'total': 100,
        'sold': 0,
        'rarity': 'Lux',
        'description': '🍦 Эксклюзивная мышка мира',
        'signature': 'lux k.y 🖊️',
        'version': 'maximum',
        'income': 5000,
        'income_interval': 3600,
        'icon': '🐼'
    }
}

PETS_DATA = {
    'dog': {
        'name': '🐕 Пёс',
        'price': 5000,
        'food_cost': 10,
        'happiness': 100,
        'income': 50,
        'rarity': 'обычный',
        'description': 'Верный друг, приносит небольшой доход'
    },
    'cat': {
        'name': '🐈 Кот',
        'price': 7500,
        'food_cost': 8,
        'happiness': 100,
        'income': 70,
        'rarity': 'обычный',
        'description': 'Независимый, но прибыльный'
    },
    'parrot': {
        'name': '🦜 Попугай',
        'price': 12000,
        'food_cost': 5,
        'happiness': 100,
        'income': 100,
        'rarity': 'редкий',
        'description': 'Говорящий, приносит хороший доход'
    },
    'hamster': {
        'name': '🐹 Хомяк',
        'price': 3000,
        'food_cost': 3,
        'happiness': 100,
        'income': 30,
        'rarity': 'обычный',
        'description': 'Маленький, но трудолюбивый'
    },
    'dragon': {
        'name': '🐲 Дракон',
        'price': 100000,
        'food_cost': 50,
        'happiness': 100,
        'income': 1000,
        'rarity': 'легендарный',
        'description': 'Мифическое существо, огромный доход'
    }
}

BUSINESS_DATA = {
    'kiosk': {
        'name': '🏪 Ларёк',
        'price': 10000,
        'income': 500,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 5000,
        'icon': '🏪',
        'description': 'Маленький, но стабильный доход'
    },
    'shop': {
        'name': '🏬 Магазин',
        'price': 50000,
        'income': 2000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 25000,
        'icon': '🏬',
        'description': 'Серьёзный бизнес'
    },
    'restaurant': {
        'name': '🍽️ Ресторан',
        'price': 200000,
        'income': 10000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 100000,
        'icon': '🍽️',
        'description': 'Премиум сегмент'
    },
    'factory': {
        'name': '🏭 Завод',
        'price': 1000000,
        'income': 50000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 500000,
        'icon': '🏭',
        'description': 'Промышленный масштаб'
    },
    'corporation': {
        'name': '🏢 Корпорация',
        'price': 10000000,
        'income': 500000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 5000000,
        'icon': '🏢',
        'description': 'Мировой уровень'
    }
}

CLAN_DATA = {
    'create_cost': 100000,
    'max_members': 50,
    'war_cost': 50000,
    'bonus_per_member': 1000
}

CASES = {
    'case1': {'name': '😁 лол 😁', 'price': 3000, 'min_win': 1000, 'max_win': 5000, 'icon': '📦'},
    'case2': {'name': '🎮 лотус 🎮', 'price': 10000, 'min_win': 7500, 'max_win': 15000, 'icon': '🎮'},
    'case3': {'name': '💫 люкс кейс 💫', 'price': 50000, 'min_win': 35000, 'max_win': 65000, 'icon': '💫'},
    'case4': {'name': '💎 Платинум 💍', 'price': 200000, 'min_win': 175000, 'max_win': 250000, 'icon': '💎'},
    'case5': {'name': '💫 специальный кейс 👾', 'price': 1000000, 'min_win': 750000, 'max_win': 1250000, 'icon': '👾'},
    'case6': {'name': '🎉 ивентовый 🎊', 'price': 0, 'min_win': 12500, 'max_win': 75000, 'icon': '🎉'}
}

achievements = {
    'first_game': {'name': '🎮 Первый шаг', 'desc': 'Сыграть первую игру', 'reward': 1000},
    'millionaire': {'name': '💰 Миллионер', 'desc': 'Накопить 1,000,000 кредиксов', 'reward': 50000},
    'referral_master': {'name': '🤝 Реферал', 'desc': 'Пригласить 10 друзей', 'reward': 100000},
    'mice_collector': {'name': '🐭 Мышиный король', 'desc': 'Собрать всех видов мышек', 'reward': 150000},
    'pet_collector': {'name': '🐾 Зоофил', 'desc': 'Собрать всех питомцев', 'reward': 100000},
    'clan_leader': {'name': '👑 Лидер клана', 'desc': 'Создать клан', 'reward': 50000},
    'banker': {'name': '💳 Банкир', 'desc': 'Положить 1,000,000 в банк', 'reward': 75000},
    'businessman': {'name': '💼 Бизнесмен', 'desc': 'Купить 5 бизнесов', 'reward': 100000},
    'phone_addict': {'name': '📱 Телефономан', 'desc': 'Сделать 100 звонков', 'reward': 25000},
    'bonus_hunter': {'name': '🎁 Охотник за бонусами', 'desc': 'Забрать 30 ежедневных бонусов', 'reward': 50000},
    'tournament_winner': {'name': '🏆 Чемпион', 'desc': 'Выиграть турнир', 'reward': 100000},
    'quest_master': {'name': '✨ Мастер квестов', 'desc': 'Выполнить 100 квестов', 'reward': 75000}
}

# ====================== ИНИЦИАЛИЗАЦИЯ БОТА ======================
bot = telebot.TeleBot(TOKEN)

# ====================== ФУНКЦИИ ЗАГРУЗКИ/СОХРАНЕНИЯ ======================
def safe_json_load(file_path, default_value=None):
    if default_value is None:
        default_value = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return default_value
        except Exception as e:
            print(f"Ошибка загрузки {file_path}: {e}")
            return default_value
    return default_value

def load_data():
    global users, username_cache, promocodes, user_achievements, user_quests, event_data
    global user_cases, orders, next_order_id, cheques, jackpot, duels, clans, businesses
    global bank_data, phone_data, bonus_data, pets_data, clans_data, businesses_data
    global stats_data, daily_quests_data, tournaments

    with data_lock:
        users_data = safe_json_load(DATA_FILE, {})
        if users_data:
            users = {str(k): v for k, v in users_data.items()}
            for uid in users:
                if 'balance' not in users[uid]:
                    users[uid]['balance'] = 1000
                if 'krds_balance' not in users[uid]:
                    users[uid]['krds_balance'] = 0
                if 'mice' not in users[uid]:
                    users[uid]['mice'] = {}
                if 'mice_last_collect' not in users[uid]:
                    users[uid]['mice_last_collect'] = {}
                if 'pets' not in users[uid]:
                    users[uid]['pets'] = {}
                if 'pets_last_feed' not in users[uid]:
                    users[uid]['pets_last_feed'] = {}
                if 'businesses' not in users[uid]:
                    users[uid]['businesses'] = {}
                if 'businesses_last_collect' not in users[uid]:
                    users[uid]['businesses_last_collect'] = {}
                if 'clan' not in users[uid]:
                    users[uid]['clan'] = None
                if 'phone_number' not in users[uid]:
                    users[uid]['phone_number'] = None
                if 'phone_contacts' not in users[uid]:
                    users[uid]['phone_contacts'] = []
                if 'daily_bonus' not in users[uid]:
                    users[uid]['daily_bonus'] = {'last_claim': 0, 'streak': 0}
                if 'weekly_bonus' not in users[uid]:
                    users[uid]['weekly_bonus'] = {'last_claim': 0, 'streak': 0}
                if 'bank_deposit' not in users[uid]:
                    users[uid]['bank_deposit'] = {'amount': 0, 'time': 0}
                if 'bank_loan' not in users[uid]:
                    users[uid]['bank_loan'] = {'amount': 0, 'time': 0}
                if 'work_count' not in users[uid]:
                    users[uid]['work_count'] = 0
                if 'referrals' not in users[uid]:
                    users[uid]['referrals'] = 0
                if 'used_promos' not in users[uid]:
                    users[uid]['used_promos'] = []
                if 'game_history' not in users[uid]:
                    users[uid]['game_history'] = []
                if 'game' not in users[uid]:
                    users[uid]['game'] = None
                if 'banned' not in users[uid]:
                    users[uid]['banned'] = False
                if 'vip_level' not in users[uid]:
                    users[uid]['vip_level'] = None
                if 'vip_expires' not in users[uid]:
                    users[uid]['vip_expires'] = 0
                if 'vip_last_krds_claim' not in users[uid]:
                    users[uid]['vip_last_krds_claim'] = 0
                if 'daily_quests' not in users[uid]:
                    users[uid]['daily_quests'] = {}
                if 'quest_stats' not in users[uid]:
                    users[uid]['quest_stats'] = {
                        'games_played': 0,
                        'wins': 0,
                        'mice_collects': 0,
                        'business_collects': 0,
                        'works': 0,
                        'deposit_amount': 0,
                        'biggest_win': 0
                    }
                if 'tournament_points' not in users[uid]:
                    users[uid]['tournament_points'] = 0
                if 'current_tournament' not in users[uid]:
                    users[uid]['current_tournament'] = None

        username_cache = safe_json_load(USERNAME_CACHE_FILE, {})
        promocodes = safe_json_load(PROMO_FILE, {})
        
        mice_data = safe_json_load(MICE_FILE, {})
        if mice_data and 'mice_sold' in mice_data:
            for mouse_id, data in mice_data['mice_sold'].items():
                if mouse_id in MICE_DATA:
                    MICE_DATA[mouse_id]['sold'] = data

        orders_data = safe_json_load(ORDERS_FILE, {})
        if orders_data:
            orders = orders_data.get('orders', {})
            next_order_id = orders_data.get('next_id', 1)

        cheques = safe_json_load(CHEQUES_FILE, {})
        user_achievements = safe_json_load(ACHIEVEMENTS_FILE, {})
        user_quests = safe_json_load(QUESTS_FILE, {})
        user_cases = safe_json_load(CASES_FILE, {})
        duels = safe_json_load(DUEL_FILE, {})
        clans = safe_json_load(CLAN_FILE, {})
        businesses = safe_json_load(BUSINESS_FILE, {})

        bank_data = safe_json_load(BANK_FILE, {
            'loans': {},
            'deposits': {},
            'transfers': [],
            'total_deposits': 0,
            'interest_rate': 0.05
        })
        
        phone_data = safe_json_load(PHONE_FILE, {
            'contacts': {},
            'calls': {},
            'messages': {},
            'phone_numbers': {}
        })
        
        bonus_data = safe_json_load(BONUS_FILE, {
            'daily': {},
            'weekly': {},
            'monthly': {},
            'referral_bonus': 5000
        })
        
        pets_data = safe_json_load(PETS_FILE, {})
        clans_data = safe_json_load(CLAN_FILE, {})
        businesses_data = safe_json_load(BUSINESS_FILE, {})
        stats_data = safe_json_load(STATS_FILE, {})
        daily_quests_data = safe_json_load(DAILY_QUESTS_FILE, {})
        tournaments = safe_json_load(TOURNAMENT_FILE, {})

        jackpot_data = safe_json_load('jackpot.json', {'total': 0})
        if jackpot_data:
            jackpot.update(jackpot_data)

        event_data = safe_json_load(EVENT_FILE, {
            'active': RELEASE_EVENT['active'],
            'participants': {},
            'leaderboard': [],
            'last_update': time.time()
        })

def save_data():
    with data_lock:
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            with open(USERNAME_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(username_cache, f, ensure_ascii=False, indent=2)
            with open(PROMO_FILE, 'w', encoding='utf-8') as f:
                json.dump(promocodes, f, ensure_ascii=False, indent=2)
            with open(ACHIEVEMENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_achievements, f, ensure_ascii=False, indent=2)
            with open(QUESTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_quests, f, ensure_ascii=False, indent=2)
            with open(CASES_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_cases, f, ensure_ascii=False, indent=2)
            with open(DUEL_FILE, 'w', encoding='utf-8') as f:
                json.dump(duels, f, ensure_ascii=False, indent=2)
            with open(CLAN_FILE, 'w', encoding='utf-8') as f:
                json.dump(clans, f, ensure_ascii=False, indent=2)
            with open(BUSINESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(businesses, f, ensure_ascii=False, indent=2)
            with open('jackpot.json', 'w', encoding='utf-8') as f:
                json.dump(jackpot, f, ensure_ascii=False, indent=2)
            with open(EVENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(event_data, f, ensure_ascii=False, indent=2)
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)
            with open(DAILY_QUESTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(daily_quests_data, f, ensure_ascii=False, indent=2)
            with open(TOURNAMENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(tournaments, f, ensure_ascii=False, indent=2)
            
            with open(BANK_FILE, 'w', encoding='utf-8') as f:
                json.dump(bank_data, f, ensure_ascii=False, indent=2)
            with open(PHONE_FILE, 'w', encoding='utf-8') as f:
                json.dump(phone_data, f, ensure_ascii=False, indent=2)
            with open(BONUS_FILE, 'w', encoding='utf-8') as f:
                json.dump(bonus_data, f, ensure_ascii=False, indent=2)
            with open(PETS_FILE, 'w', encoding='utf-8') as f:
                json.dump(pets_data, f, ensure_ascii=False, indent=2)
            
            mice_data = {'mice_sold': {mid: MICE_DATA[mid]['sold'] for mid in MICE_DATA}}
            with open(MICE_FILE, 'w', encoding='utf-8') as f:
                json.dump(mice_data, f, ensure_ascii=False, indent=2)
            
            orders_data = {'orders': orders, 'next_id': next_order_id}
            with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            
            with open(CHEQUES_FILE, 'w', encoding='utf-8') as f:
                json.dump(cheques, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

def get_user_lock(user_id):
    if user_id not in user_locks:
        user_locks[user_id] = RLock()
    return user_locks[user_id]

def get_user(user_id):
    user_id = str(user_id)
    with get_user_lock(user_id):
        if user_id not in users:
            users[user_id] = {
                'balance': 1000,
                'krds_balance': 0,
                'game': None,
                'referrals': 0,
                'referrer': None,
                'banned': False,
                'bank': {'balance': 0, 'last_interest': time.time(), 'history': []},
                'used_promos': [],
                'clan': None,
                'total_wins': 0,
                'total_losses': 0,
                'games_played': 0,
                'win_streak': 0,
                'max_win_streak': 0,
                'total_lost': 0,
                'quests_completed': 0,
                'event_points': 0,
                'game_history': [],
                'daily_last_claim': 0,
                'daily_streak': 0,
                'last_case6_open': 0,
                'mice': {},
                'mice_last_collect': {},
                'pets': {},
                'pets_last_feed': {},
                'businesses': {},
                'businesses_last_collect': {},
                'phone_number': None,
                'phone_contacts': [],
                'daily_bonus': {'last_claim': 0, 'streak': 0},
                'weekly_bonus': {'last_claim': 0, 'streak': 0},
                'bank_deposit': {'amount': 0, 'time': 0},
                'bank_loan': {'amount': 0, 'time': 0},
                'work_count': 0,
                'vip_level': None,
                'vip_expires': 0,
                'vip_last_krds_claim': 0,
                'daily_quests': {},
                'quest_stats': {
                    'games_played': 0,
                    'wins': 0,
                    'mice_collects': 0,
                    'business_collects': 0,
                    'works': 0,
                    'deposit_amount': 0,
                    'biggest_win': 0
                },
                'tournament_points': 0,
                'current_tournament': None
            }
            save_data()
        return users[user_id]

def is_banned(user_id):
    user = get_user(user_id)
    return user.get('banned', False)

def is_admin(user_id):
    return str(user_id) in admin_users

def update_username_cache(user_id, username):
    if username:
        with data_lock:
            username_cache[username.lower()] = str(user_id)
            save_data()

def parse_bet(bet_str):
    try:
        bet_str = bet_str.lower().strip()
        if 'кк' in bet_str or 'ку' in bet_str:
            bet_str = bet_str.replace('кк', '').replace('ку', '')
            if bet_str == '':
                bet_str = '1'
            return int(float(bet_str) * 1000000)
        elif 'к' in bet_str:
            bet_str = bet_str.replace('к', '')
            if bet_str == '':
                bet_str = '1'
            return int(float(bet_str) * 1000)
        else:
            return int(bet_str)
    except:
        return None

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}М"
    elif num >= 1000:
        return f"{num/1000:.1f}К"
    return str(num)

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} сек"
    elif seconds < 3600:
        return f"{int(seconds/60)} мин"
    elif seconds < 86400:
        return f"{int(seconds/3600)} ч"
    else:
        return f"{int(seconds/86400)} д"

def get_event_multiplier():
    if RELEASE_EVENT['active'] and time.time() < RELEASE_EVENT['end_time']:
        return RELEASE_EVENT['multiplier']
    return 1.0

def get_vip_multiplier(user_id, multiplier_type='bonus_mult'):
    user = get_user(user_id)
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        return VIP_LEVELS[user['vip_level']].get(multiplier_type, 1.0)
    return 1.0

def unlock_achievement(user_id, achievement_id):
    if achievement_id not in achievements:
        return
    with data_lock:
        if user_id not in user_achievements:
            user_achievements[user_id] = {}
        if achievement_id in user_achievements[user_id]:
            return
        achievement = achievements[achievement_id]
        user_achievements[user_id][achievement_id] = time.time()
        
        user = get_user(user_id)
        user['balance'] += achievement['reward']
        save_data()
    
    try:
        bot.send_message(int(user_id), 
            f"🏆 ** ДОСТИЖЕНИЕ РАЗБЛОКИРОВАНО! ** 🏆\n\n"
            f"{achievement['name']}\n"
            f"{achievement['desc']}\n"
            f"💰 Награда: +{format_number(achievement['reward'])} кредиксов")
    except:
        pass

def update_quest_progress(user_id, quest_type, value=1):
    user = get_user(user_id)
    
    if quest_type in user['quest_stats']:
        if quest_type == 'deposit_amount':
            user['quest_stats'][quest_type] += value
        elif quest_type == 'biggest_win':
            if value > user['quest_stats']['biggest_win']:
                user['quest_stats']['biggest_win'] = value
        else:
            user['quest_stats'][quest_type] += value
    
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in user['daily_quests']:
        generate_daily_quests(user_id)
    
    completed = []
    for qid, qdata in user['daily_quests'].get(today, {}).items():
        if qdata['completed']:
            continue
        
        quest = DAILY_QUESTS.get(qid)
        if not quest:
            continue
        
        current_value = user['quest_stats'].get(quest['type'], 0)
        
        target = None
        reward = 0
        for t, r in quest['rewards'].items():
            if current_value >= t:
                target = t
                reward = r
        
        if target:
            qdata['completed'] = True
            qdata['reward'] = reward
            
            vip_mult = get_vip_multiplier(user_id, 'daily_bonus_mult')
            final_reward = int(reward * vip_mult)
            
            user['balance'] += final_reward
            user['quests_completed'] = user.get('quests_completed', 0) + 1
            completed.append(f"{quest['icon']} {quest['name']} +{format_number(final_reward)}")
            
            if user['quests_completed'] >= 100:
                unlock_achievement(user_id, 'quest_master')
    
    if completed:
        try:
            bot.send_message(int(user_id),
                f"✅ ** КВЕСТЫ ВЫПОЛНЕНЫ! ** ✅\n\n" +
                "\n".join(completed) +
                f"\n\n💰 Баланс: {format_number(user['balance'])}")
        except:
            pass
    
    save_data()

def generate_daily_quests(user_id):
    user = get_user(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    base_slots = 3
    vip_slots = 0
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        vip_slots = VIP_LEVELS[user['vip_level']].get('quest_slots', 0) - base_slots
    
    total_slots = base_slots + max(0, vip_slots)
    
    quest_ids = list(DAILY_QUESTS.keys())
    selected = random.sample(quest_ids, min(total_slots, len(quest_ids)))
    
    quests = {}
    for qid in selected:
        quest = DAILY_QUESTS[qid]
        targets = list(quest['rewards'].keys())
        target = random.choice(targets)
        
        quests[qid] = {
            'target': target,
            'completed': False,
            'reward': quest['rewards'][target]
        }
    
    if today not in user['daily_quests']:
        user['daily_quests'][today] = {}
    
    user['daily_quests'][today] = quests
    save_data()

def update_game_stats(user_id, won, bet, win_amount=0):
    user = get_user(user_id)
    with get_user_lock(user_id):
        user['games_played'] = user.get('games_played', 0) + 1
        
        if won:
            user['total_wins'] = user.get('total_wins', 0) + 1
            user['win_streak'] = user.get('win_streak', 0) + 1
            if user['win_streak'] > user.get('max_win_streak', 0):
                user['max_win_streak'] = user['win_streak']
            if 'game_history' not in user:
                user['game_history'] = []
            user['game_history'].append({
                'time': time.time(),
                'game': 'game',
                'bet': bet,
                'result': 'win',
                'profit': win_amount - bet
            })
            
            update_quest_progress(user_id, 'games_played')
            update_quest_progress(user_id, 'wins')
            update_quest_progress(user_id, 'biggest_win', win_amount)
        else:
            user['total_losses'] = user.get('total_losses', 0) + 1
            user['win_streak'] = 0
            user['total_lost'] = user.get('total_lost', 0) + bet
            if 'game_history' not in user:
                user['game_history'] = []
            user['game_history'].append({
                'time': time.time(),
                'game': 'game',
                'bet': bet,
                'result': 'loss',
                'profit': -bet
            })
            
            update_quest_progress(user_id, 'games_played')
        
        save_data()
    
    if user['games_played'] == 1:
        unlock_achievement(user_id, 'first_game')
    
    if user['balance'] >= 1000000:
        unlock_achievement(user_id, 'millionaire')
    
    if len(user.get('mice', {})) >= 3:
        unlock_achievement(user_id, 'mice_collector')
    
    if len(user.get('pets', {})) >= 5:
        unlock_achievement(user_id, 'pet_collector')
    
    if len(user.get('businesses', {})) >= 5:
        unlock_achievement(user_id, 'businessman')
    
    if user.get('clan') is not None:
        unlock_achievement(user_id, 'clan_leader')
    
    if user.get('bank_deposit', {}).get('amount', 0) >= 1000000:
        unlock_achievement(user_id, 'banker')
    
    if len(user.get('phone_contacts', [])) >= 100:
        unlock_achievement(user_id, 'phone_addict')
    
    if user.get('daily_bonus', {}).get('streak', 0) >= 30:
        unlock_achievement(user_id, 'bonus_hunter')

def cancel_user_game(user_id):
    with get_user_lock(user_id):
        if user_id in crash_update_timers:
            try:
                crash_update_timers[user_id].cancel()
            except:
                pass
            del crash_update_timers[user_id]
        
        if user_id in game_timers:
            try:
                game_timers[user_id].cancel()
            except:
                pass
            del game_timers[user_id]
        
        user = get_user(user_id)
        if user.get('game') is not None:
            if user['game'].get('stage') == 'waiting_bet' and 'bet' in user['game']:
                user['balance'] += user['game']['bet']
            user['game'] = None
            save_data()
            return True
    return False

def cleanup_all_timers():
    with data_lock:
        for user_id in list(crash_update_timers.keys()):
            try:
                crash_update_timers[user_id].cancel()
            except:
                pass
        for user_id in list(game_timers.keys()):
            try:
                game_timers[user_id].cancel()
            except:
                pass
        crash_update_timers.clear()
        game_timers.clear()

# ====================== ТУРНИРЫ ======================
def init_tournaments():
    for t_type, t_data in TOURNAMENT_TYPES.items():
        if t_type not in tournaments:
            tournaments[t_type] = {
                'active': True,
                'start_time': time.time(),
                'end_time': time.time() + t_data['duration'],
                'participants': {},
                'prize_pool': t_data['prize_pool'],
                'entry_fee': t_data['entry_fee']
            }
    save_data()

@bot.message_handler(commands=['турнир', 'турниры'])
def tournament_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    text = "🏆 ** ТУРНИРЫ ** 🏆\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for t_type, t_data in tournaments.items():
        if not t_data['active']:
            continue
        
        time_left = t_data['end_time'] - time.time()
        if time_left <= 0:
            continue
        
        tourn_info = TOURNAMENT_TYPES[t_type]
        
        is_participant = user_id in t_data['participants']
        user_points = t_data['participants'].get(user_id, 0) if is_participant else 0
        
        text += (
            f"{tourn_info['name']}\n"
            f"   ⏳ Осталось: {format_time(time_left)}\n"
            f"   💰 Призовой фонд: {format_number(t_data['prize_pool'])}\n"
            f"   💸 Взнос: {format_number(t_data['entry_fee'])}\n"
        )
        
        if is_participant:
            text += f"   📊 Твои очки: {user_points}\n"
            text += f"   🚫 /турнир_покинуть {t_type}\n\n"
        else:
            text += f"   ✅ /турнир_вступить {t_type}\n\n"
    
    for t_type, t_data in tournaments.items():
        if not t_data['active']:
            continue
        
        sorted_parts = sorted(t_data['participants'].items(), key=lambda x: x[1], reverse=True)[:5]
        if sorted_parts:
            text += f"\n📊 **ТОП {TOURNAMENT_TYPES[t_type]['name']}:**\n"
            for i, (uid, points) in enumerate(sorted_parts, 1):
                try:
                    u = bot.get_chat(int(uid))
                    name = f"@{u.username}" if u.username else u.first_name
                except:
                    name = f"ID {uid}"
                text += f"{i}. {name} - {points} очков\n"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['турнир_вступить'])
def tournament_join(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /турнир_вступить [тип]\nТипы: daily, weekly, monthly")
        return
    
    t_type = args[1]
    if t_type not in tournaments:
        bot.send_message(message.chat.id, "❌ Турнир не найден!")
        return
    
    t_data = tournaments[t_type]
    if not t_data['active']:
        bot.send_message(message.chat.id, "❌ Турнир не активен!")
        return
    
    if t_data['end_time'] <= time.time():
        bot.send_message(message.chat.id, "❌ Турнир уже закончился!")
        return
    
    user = get_user(user_id)
    if user_id in t_data['participants']:
        bot.send_message(message.chat.id, "❌ Ты уже участвуешь в турнире!")
        return
    
    entry_fee = t_data['entry_fee']
    if user['balance'] < entry_fee:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {format_number(entry_fee)}")
        return
    
    with data_lock, get_user_lock(user_id):
        user['balance'] -= entry_fee
        t_data['prize_pool'] += entry_fee // 2
        t_data['participants'][user_id] = 0
        user['current_tournament'] = t_type
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты вступил в турнир! Взнос: {format_number(entry_fee)}")

@bot.message_handler(commands=['турнир_покинуть'])
def tournament_leave(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /турнир_покинуть [тип]")
        return
    
    t_type = args[1]
    if t_type not in tournaments:
        bot.send_message(message.chat.id, "❌ Турнир не найден!")
        return
    
    t_data = tournaments[t_type]
    if user_id not in t_data['participants']:
        bot.send_message(message.chat.id, "❌ Ты не участвуешь в этом турнире!")
        return
    
    with data_lock:
        del t_data['participants'][user_id]
        save_data()
    
    bot.send_message(message.chat.id, "✅ Ты покинул турнир!")

def add_tournament_points(user_id, game_type, bet, win_amount):
    user = get_user(user_id)
    if not user.get('current_tournament'):
        return
    
    t_type = user['current_tournament']
    if t_type not in tournaments:
        return
    
    t_data = tournaments[t_type]
    if not t_data['active'] or t_data['end_time'] <= time.time():
        return
    
    points = 0
    if win_amount > bet:
        points = int((win_amount - bet) / 1000)
    elif win_amount == 0:
        points = max(1, bet // 10000)
    
    with data_lock:
        if user_id in t_data['participants']:
            t_data['participants'][user_id] = t_data['participants'].get(user_id, 0) + points
            save_data()

def check_tournament_ends():
    with data_lock:
        for t_type, t_data in tournaments.items():
            if not t_data['active']:
                continue
            
            if t_data['end_time'] <= time.time():
                t_data['active'] = False
                
                sorted_parts = sorted(t_data['participants'].items(), key=lambda x: x[1], reverse=True)
                
                if sorted_parts:
                    prize_pool = t_data['prize_pool']
                    
                    if len(sorted_parts) >= 1:
                        winner_id = sorted_parts[0][0]
                        prize = int(prize_pool * 0.5)
                        winner = get_user(winner_id)
                        winner['balance'] += prize
                        unlock_achievement(winner_id, 'tournament_winner')
                        try:
                            bot.send_message(int(winner_id), f"🏆 Ты выиграл турнир! Приз: {format_number(prize)}")
                        except:
                            pass
                    
                    if len(sorted_parts) >= 2:
                        winner_id = sorted_parts[1][0]
                        prize = int(prize_pool * 0.3)
                        get_user(winner_id)['balance'] += prize
                        try:
                            bot.send_message(int(winner_id), f"🥈 Ты занял 2 место в турнире! Приз: {format_number(prize)}")
                        except:
                            pass
                    
                    if len(sorted_parts) >= 3:
                        winner_id = sorted_parts[2][0]
                        prize = int(prize_pool * 0.2)
                        get_user(winner_id)['balance'] += prize
                        try:
                            bot.send_message(int(winner_id), f"🥉 Ты занял 3 место в турнире! Приз: {format_number(prize)}")
                        except:
                            pass
                
                tourn_info = TOURNAMENT_TYPES[t_type]
                tournaments[t_type] = {
                    'active': True,
                    'start_time': time.time(),
                    'end_time': time.time() + tourn_info['duration'],
                    'participants': {},
                    'prize_pool': tourn_info['prize_pool'],
                    'entry_fee': tourn_info['entry_fee']
                }
        
        save_data()

def start_tournament_checker():
    def check():
        while True:
            time.sleep(60)
            check_tournament_ends()
    
    import threading
    thread = threading.Thread(target=check, daemon=True)
    thread.start()

# ====================== ИГРЫ ======================
@bot.message_handler(commands=['дартс', 'Дартс'])
def darts_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ Использование: дартс [ставка]\nПример: дартс 1к, дартс 1000")
        return
    
    bet = parse_bet(parts[1])
    if bet is None:
        bot.send_message(message.chat.id, "❌ Неверный формат ставки.")
        return
    
    max_bet = MAX_BET
    vip_mult = get_vip_multiplier(user_id, 'max_bet_mult')
    max_bet = int(max_bet * vip_mult)
    
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)} кредиксов!")
        return
    
    if bet > user.get('balance', 0):
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Твой баланс: {format_number(user.get('balance', 0))}")
        return
    
    if bet <= 0:
        bot.send_message(message.chat.id, "❌ Ставка должна быть положительной!")
        return
    
    if user.get('game') is not None:
        bot.send_message(message.chat.id, "❌ У тебя уже есть активная игра! Закончи её или отмени (отмена)")
        return
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        
        score = random.randint(1, 100)
        
        if score <= 50:
            update_game_stats(user_id, False, bet)
            text = (
                f"🎯 ** ДАРТС ** 🎯\n\n"
                f"Твой бросок: {score} очков\n"
                f"❌ ПРОМАХ! Ты проиграл {format_number(bet)} кредиксов\n"
                f"💰 Баланс: {format_number(user['balance'])}"
            )
        elif score <= 80:
            multiplier = 1.5
            win_amount = int(bet * multiplier)
            vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
            win_amount = int(win_amount * vip_mult)
            win_amount = int(win_amount * get_event_multiplier())
            
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'дартс', bet, win_amount)
            
            text = (
                f"🎯 ** ДАРТС ** 🎯\n\n"
                f"Твой бросок: {score} очков\n"
                f"✅ ПОПАДАНИЕ! x{multiplier}\n"
                f"💰 Выигрыш: +{format_number(win_amount)} кредиксов\n"
                f"💸 Баланс: {format_number(user['balance'])}"
            )
        else:
            multiplier = random.choice([2.0, 3.0, 5.0, 10.0])
            win_amount = int(bet * multiplier)
            vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
            win_amount = int(win_amount * vip_mult)
            win_amount = int(win_amount * get_event_multiplier())
            
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'дартс', bet, win_amount)
            
            text = (
                f"🎯 ** ДАРТС ** 🎯\n\n"
                f"Твой бросок: {score} очков\n"
                f"🎉 ТОЧНО В ЦЕЛЬ! x{multiplier}\n"
                f"💰 Выигрыш: +{format_number(win_amount)} кредиксов\n"
                f"💸 Баланс: {format_number(user['balance'])}"
            )
        
        save_data()
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['покер', 'Покер'])
def poker_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ Использование: покер [ставка]\nПример: покер 1к, покер 1000")
        return
    
    bet = parse_bet(parts[1])
    if bet is None:
        bot.send_message(message.chat.id, "❌ Неверный формат ставки.")
        return
    
    max_bet = MAX_BET
    vip_mult = get_vip_multiplier(user_id, 'max_bet_mult')
    max_bet = int(max_bet * vip_mult)
    
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)} кредиксов!")
        return
    
    if bet > user.get('balance', 0):
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Твой баланс: {format_number(user.get('balance', 0))}")
        return
    
    if bet <= 0:
        bot.send_message(message.chat.id, "❌ Ставка должна быть положительной!")
        return
    
    if user.get('game') is not None:
        bot.send_message(message.chat.id, "❌ У тебя уже есть активная игра! Закончи её или отмени (отмена)")
        return
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        random.shuffle(cards)
        
        player_hand = [cards.pop(), cards.pop()]
        bot_hand = [cards.pop(), cards.pop()]
        
        def evaluate_hand(hand):
            values = []
            for card in hand:
                if card == 'J':
                    values.append(11)
                elif card == 'Q':
                    values.append(12)
                elif card == 'K':
                    values.append(13)
                elif card == 'A':
                    values.append(14)
                else:
                    values.append(int(card))
            
            values.sort()
            
            if values[0] == values[1]:
                return 2 + values[0] / 100
            else:
                return max(values)
        
        player_score = evaluate_hand(player_hand)
        bot_score = evaluate_hand(bot_hand)
        
        won = player_score > bot_score
        
        if won:
            multiplier = POKER_MULTIPLIER
            win_amount = int(bet * multiplier)
            vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
            win_amount = int(win_amount * vip_mult)
            win_amount = int(win_amount * get_event_multiplier())
            
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'покер', bet, win_amount)
            
            result_text = "ТЫ ВЫИГРАЛ! ✅"
        else:
            update_game_stats(user_id, False, bet)
            win_amount = 0
            result_text = "ТЫ ПРОИГРАЛ... ❌"
        
        text = (
            f"🃏 ** ПОКЕР ** 🃏\n\n"
            f"Твои карты: {player_hand[0]} {player_hand[1]}\n"
            f"Карты бота: {bot_hand[0]} {bot_hand[1]}\n\n"
            f"{result_text}\n\n"
        )
        
        if won:
            text += f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
        else:
            text += f"❌ Проигрыш: -{format_number(bet)} кредиксов\n"
        
        text += f"💰 Баланс: {format_number(user['balance'])}"
        
        save_data()
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['мины', 'Мины'])
def mines_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ Использование: мины [ставка]\nПример: мины 1к, мины 1000")
        return
    
    bet = parse_bet(parts[1])
    if bet is None:
        bot.send_message(message.chat.id, "❌ Неверный формат ставки.")
        return
    
    max_bet = MAX_BET
    vip_mult = get_vip_multiplier(user_id, 'max_bet_mult')
    max_bet = int(max_bet * vip_mult)
    
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)} кредиксов!")
        return
    
    if bet > user.get('balance', 0):
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Твой баланс: {format_number(user.get('balance', 0))}")
        return
    
    if bet <= 0:
        bot.send_message(message.chat.id, "❌ Ставка должна быть положительной!")
        return
    
    if user.get('game') is not None:
        bot.send_message(message.chat.id, "❌ У тебя уже есть активная игра! Закончи её или отмени (отмена)")
        return
    
    with get_user_lock(user_id):
        num_mines = random.randint(1, 5)
        field = ['💎'] * (25 - num_mines) + ['💣'] * num_mines
        random.shuffle(field)
        
        user['game'] = {
            'type': 'mines',
            'bet': bet,
            'stage': 'playing',
            'field': field,
            'opened': [False] * 25,
            'mines': num_mines,
            'steps': 0
        }
        save_data()
    
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(25):
        buttons.append(types.InlineKeyboardButton("⬜", callback_data=f"mines_{i}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="mines_take"))
    
    bot.send_message(
        message.chat.id,
        f"💣 ** МИНЫ ** 💣\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Мин на поле: {num_mines}\n\n"
        f"Открывай ячейки, но берегись мин!\n"
        f"Если найдешь мину - ставка сгорает!",
        reply_markup=markup
    )

# ====================== VIP СИСТЕМА ======================
@bot.message_handler(commands=['вип', 'vip'])
def vip_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    current_vip = None
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        current_vip = VIP_LEVELS[user['vip_level']]
        days_left = int((user['vip_expires'] - time.time()) / 86400)
        
        last_claim = user.get('vip_last_krds_claim', 0)
        if time.time() - last_claim > 7 * 86400:
            can_claim_krds = True
        else:
            next_claim = int((7 * 86400) - (time.time() - last_claim))
            next_claim_days = next_claim / 86400
            can_claim_krds = False
    
    text = f"👑 ** VIP СИСТЕМА ** 👑\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if current_vip:
        text += (
            f"✅ Твой статус: {current_vip['color']} {current_vip['name']}\n"
            f"⏳ Осталось: {days_left} дней\n\n"
            f"**Твои бонусы:**\n"
        )
        for perk in current_vip['perks']:
            text += f"• {perk}\n"
        
        if can_claim_krds:
            text += f"\n💎 **Доступно KRDS:** +{current_vip['krds_weekly']} (напиши /вип_крдс)\n"
        else:
            if 'next_claim_days' in locals():
                text += f"\n⏳ **Следующие KRDS:** через {next_claim_days:.1f} дней\n"
        
        text += f"\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    else:
        text += "❌ У тебя нет активного VIP\n\n"
    
    text += "**Доступные VIP уровни:**\n\n"
    
    for level_id, vip in VIP_LEVELS.items():
        text += (
            f"{vip['color']} {vip['name']}\n"
            f"   💰 Цена: {format_number(vip['price'])} кредиксов\n"
            f"   💎 KRDS/неделя: +{vip['krds_weekly']}\n"
            f"   ⏳ 30 дней\n"
            f"   **Бонусы:**\n"
        )
        for perk in vip['perks'][:3]:
            text += f"      • {perk}\n"
        text += f"   /купить_вип {level_id}\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "💡 VIP окупается если ты активно играешь!"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['купить_вип'])
def buy_vip_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /купить_вип [уровень]\nДоступно: bronze, silver, gold, platinum")
        return
    
    level = args[1].lower()
    if level not in VIP_LEVELS:
        bot.send_message(message.chat.id, "❌ Неверный уровень! Доступно: bronze, silver, gold, platinum")
        return
    
    user = get_user(user_id)
    vip_data = VIP_LEVELS[level]
    
    if user.get('vip_expires', 0) > time.time():
        bot.send_message(message.chat.id, "❌ У тебя уже есть активный VIP! Дождись окончания.")
        return
    
    if user['balance'] < vip_data['price']:
        bot.send_message(message.chat.id, 
            f"❌ Недостаточно средств! Нужно: {format_number(vip_data['price'])}")
        return
    
    with get_user_lock(user_id):
        user['balance'] -= vip_data['price']
        user['vip_level'] = level
        user['vip_expires'] = time.time() + vip_data['duration']
        user['vip_last_krds_claim'] = time.time()
        
        generate_daily_quests(user_id)
        
        save_data()
    
    text = (
        f"🎉 ** ПОЗДРАВЛЯЮ! ** 🎉\n\n"
        f"Ты купил {vip_data['color']} {vip_data['name']} VIP!\n\n"
        f"**Твои бонусы активированы:**\n"
    )
    for perk in vip_data['perks']:
        text += f"✅ {perk}\n"
    
    text += f"\n💰 Баланс: {format_number(user['balance'])}"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['вип_крдс'])
def vip_krds_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    if not user.get('vip_level') or user.get('vip_expires', 0) < time.time():
        bot.send_message(message.chat.id, "❌ У тебя нет активного VIP!")
        return
    
    vip_data = VIP_LEVELS[user['vip_level']]
    last_claim = user.get('vip_last_krds_claim', 0)
    
    if time.time() - last_claim < 7 * 86400:
        next_claim = int((7 * 86400) - (time.time() - last_claim))
        next_claim_days = next_claim / 86400
        bot.send_message(message.chat.id, 
            f"⏳ Следующие KRDS можно будет получить через {next_claim_days:.1f} дней")
        return
    
    with get_user_lock(user_id):
        user['krds_balance'] += vip_data['krds_weekly']
        user['vip_last_krds_claim'] = time.time()
        save_data()
    
    bot.send_message(message.chat.id, 
        f"💎 ** ПОЛУЧЕНО! ** 💎\n\n"
        f"Ты получил +{vip_data['krds_weekly']} KRDS за неделю VIP!\n"
        f"💎 Новый баланс KRDS: {user['krds_balance']}")

# ====================== ЕЖЕДНЕВНЫЕ КВЕСТЫ ======================
@bot.message_handler(commands=['квесты', 'quests'])
def quests_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if today not in user['daily_quests']:
        generate_daily_quests(user_id)
    
    text = "📋 ** ЕЖЕДНЕВНЫЕ КВЕСТЫ ** 📋\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    quests = user['daily_quests'].get(today, {})
    if not quests:
        text += "У тебя нет активных квестов сегодня.\n"
    else:
        for qid, qdata in quests.items():
            quest = DAILY_QUESTS.get(qid)
            if not quest:
                continue
            
            status = "✅" if qdata['completed'] else "⏳"
            current_value = user['quest_stats'].get(quest['type'], 0)
            target = qdata['target']
            
            text += (
                f"{status} {quest['icon']} {quest['name']}\n"
                f"   {quest['desc'].format(target=format_number(target))}\n"
                f"   Прогресс: {format_number(current_value)}/{format_number(target)}\n"
                f"   Награда: {format_number(qdata['reward'])} кредиксов\n\n"
            )
    
    text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "💡 Квесты обновляются каждый день!"
    
    bot.send_message(message.chat.id, text)

# ====================== СТАТИСТИКА ======================
@bot.message_handler(commands=['статистика', 'stats'])
def stats_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    total_users = len(users)
    total_balance = sum(u.get('balance', 0) for u in users.values())
    total_krds = sum(u.get('krds_balance', 0) for u in users.values())
    
    win_rate = 0
    if user.get('games_played', 0) > 0:
        win_rate = (user.get('total_wins', 0) / user['games_played']) * 100
    
    text = (
        f"📊 ** СТАТИСТИКА ** 📊\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**ГЛОБАЛЬНАЯ:**\n"
        f"👥 Всего игроков: {total_users}\n"
        f"💰 Всего кредиксов: {format_number(total_balance)}\n"
        f"💎 Всего KRDS: {total_krds}\n\n"
        f"**ТВОЯ СТАТИСТИКА:**\n"
        f"🎮 Сыграно игр: {user.get('games_played', 0)}\n"
        f"✅ Побед: {user.get('total_wins', 0)}\n"
        f"❌ Поражений: {user.get('total_losses', 0)}\n"
        f"📊 Винрейт: {win_rate:.1f}%\n"
        f"💰 Проиграно всего: {format_number(user.get('total_lost', 0))}\n"
        f"🔥 Макс стрик: {user.get('max_win_streak', 0)}\n"
        f"📋 Квестов выполнено: {user.get('quests_completed', 0)}\n\n"
        f"**АКТИВНОСТЬ:**\n"
        f"🐭 Мышек: {sum(user.get('mice', {}).values())}\n"
        f"🐾 Питомцев: {len(user.get('pets', {}))}\n"
        f"🏪 Бизнесов: {len(user.get('businesses', {}))}\n"
        f"💼 Работ: {user.get('work_count', 0)}\n"
        f"👥 Рефералов: {user.get('referrals', 0)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    bot.send_message(message.chat.id, text)

# ====================== ТОП (НОВЫЙ, ОДИН) ======================
@bot.message_handler(commands=['топ', 'Топ'])
def new_top_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    with data_lock:
        users_list = [(uid, data) for uid, data in users.items()]
        sorted_by_balance = sorted(users_list, key=lambda x: x[1].get('balance', 0), reverse=True)[:10]
        sorted_by_games = sorted(users_list, key=lambda x: x[1].get('games_played', 0), reverse=True)[:5]
        sorted_by_wins = sorted(users_list, key=lambda x: x[1].get('total_wins', 0), reverse=True)[:5]
    
    if not sorted_by_balance:
        bot.send_message(message.chat.id, "📊 Пока нет пользователей в топе.")
        return
    
    text = "🏆 ** ТОП ИГРОКОВ ** 🏆\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    text += "💰 **ПО БАЛАНСУ:**\n"
    for i, (uid, data) in enumerate(sorted_by_balance, 1):
        try:
            user = bot.get_chat(int(uid))
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"ID {uid}"
        
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {name} - {format_number(data.get('balance', 0))}\n"
    
    text += "\n🎮 **ПО ИГРАМ:**\n"
    for i, (uid, data) in enumerate(sorted_by_games, 1):
        try:
            user = bot.get_chat(int(uid))
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"ID {uid}"
        text += f"{i}. {name} - {data.get('games_played', 0)} игр\n"
    
    text += "\n✅ **ПО ПОБЕДАМ:**\n"
    for i, (uid, data) in enumerate(sorted_by_wins, 1):
        try:
            user = bot.get_chat(int(uid))
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"ID {uid}"
        text += f"{i}. {name} - {data.get('total_wins', 0)} побед\n"
    
    bot.send_message(message.chat.id, text)

# ====================== АДМИН КОМАНДЫ ======================
@bot.message_handler(commands=['Admin'])
def admin_login(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /Admin пароль")
        return
    
    password_hash = hashlib.sha256(args[1].encode()).hexdigest()
    if password_hash == ADMIN_PASSWORD_HASH:
        admin_users.add(user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
            types.InlineKeyboardButton("💰 Выдать кредиксы", callback_data="admin_add_balance"),
            types.InlineKeyboardButton("💎 Выдать KRDS", callback_data="admin_add_krds"),
            types.InlineKeyboardButton("👑 VIP", callback_data="admin_vip"),
            types.InlineKeyboardButton("🏆 Турниры", callback_data="admin_tournaments"),
            types.InlineKeyboardButton("🚫 Забанить", callback_data="admin_ban"),
            types.InlineKeyboardButton("✅ Разбанить", callback_data="admin_unban"),
            types.InlineKeyboardButton("💾 Сохранить", callback_data="admin_save"),
            types.InlineKeyboardButton("🚪 Выход", callback_data="admin_exit")
        )
        
        bot.send_message(
            message.chat.id,
            "🔑 ** АДМИН ПАНЕЛЬ ** 🔑\n\n"
            f"👤 Администратор: {message.from_user.first_name}\n"
            f"🆔 ID: {user_id}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Выберите действие:",
            reply_markup=markup
        )
    else:
        bot.send_message(message.chat.id, "🔑❌ Неверный пароль!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def admin_callback(call):
    user_id = str(call.from_user.id)
    
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ У вас нет прав администратора!")
        return
    
    data = call.data
    
    if data == "admin_stats":
        with data_lock:
            total_users = len(users)
            total_balance = sum(u.get('balance', 0) for u in users.values())
            total_krds = sum(u.get('krds_balance', 0) for u in users.values())
            banned_count = sum(1 for u in users.values() if u.get('banned', False))
            vip_count = sum(1 for u in users.values() if u.get('vip_level') and u.get('vip_expires', 0) > time.time())
            active_tournaments = sum(1 for t in tournaments.values() if t.get('active', False))
        
        text = (
            f"📊 ** СТАТИСТИКА БОТА ** 📊\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 Пользователи: {total_users}\n"
            f"💰 Баланс всего: {format_number(total_balance)}\n"
            f"💎 KRDS всего: {total_krds}\n"
            f"👑 VIP игроков: {vip_count}\n"
            f"🏆 Активных турниров: {active_tournaments}\n"
            f"⛔ Забанено: {banned_count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    
    elif data == "admin_exit":
        admin_users.remove(user_id)
        bot.edit_message_text(
            "👋 Вы вышли из режима администратора.",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_save":
        save_data()
        bot.answer_callback_query(call.id, "✅ Данные сохранены!")
    
    elif data == "admin_add_balance":
        msg = bot.edit_message_text(
            "💰 ** Выдача кредиксов **\n\n"
            "Отправь команду:\n"
            "/addbalance @ник сумма",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_krds":
        msg = bot.edit_message_text(
            "💎 ** Выдача KRDS **\n\n"
            "Отправь команду:\n"
            "/addkrds @ник сумма",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_ban":
        msg = bot.edit_message_text(
            "🚫 ** Бан пользователя **\n\n"
            "Отправь команду:\n"
            "/ban @ник",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_unban":
        msg = bot.edit_message_text(
            "✅ ** Разбан пользователя **\n\n"
            "Отправь команду:\n"
            "/unban @ник",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_vip":
        msg = bot.edit_message_text(
            "👑 ** Управление VIP **\n\n"
            "Команды:\n"
            "/addvip @ник уровень - выдать VIP\n"
            "/removevip @ник - снять VIP\n"
            "Уровни: bronze, silver, gold, platinum",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_tournaments":
        msg = bot.edit_message_text(
            "🏆 ** Управление турнирами **\n\n"
            "Команды:\n"
            "/tournament_start [тип] - запустить турнир\n"
            "/tournament_end [тип] - завершить досрочно\n"
            "/tournament_prize [тип] [сумма] - установить приз",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)

@bot.message_handler(commands=['addbalance'])
def add_balance(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /addbalance @ник сумма")
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        amount = int(args[2])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!")
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!")
        return
    
    with data_lock:
        target_user = username_cache.get(target_username)
        if not target_user:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        with get_user_lock(target_user):
            users[target_user]['balance'] = users[target_user].get('balance', 1000) + amount
            save_data()
    
    bot.send_message(message.chat.id, 
        f"➕✅ Пользователю @{target_username} начислено {format_number(amount)} кредиксов.")

@bot.message_handler(commands=['addkrds'])
def add_krds(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /addkrds @ник сумма")
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        amount = int(args[2])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!")
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!")
        return
    
    with data_lock:
        target_user = username_cache.get(target_username)
        if not target_user:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        with get_user_lock(target_user):
            users[target_user]['krds_balance'] = users[target_user].get('krds_balance', 0) + amount
            save_data()
    
    bot.send_message(message.chat.id, 
        f"💎✅ Пользователю @{target_username} начислено {amount} KRDS.")

@bot.message_handler(commands=['addvip'])
def add_vip(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /addvip @ник уровень")
        return
    
    target_username = args[1].replace('@', '').lower()
    level = args[2].lower()
    
    if level not in VIP_LEVELS:
        bot.send_message(message.chat.id, "❌ Неверный уровень! Доступно: bronze, silver, gold, platinum")
        return
    
    with data_lock:
        target_user = username_cache.get(target_username)
        if not target_user:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        with get_user_lock(target_user):
            users[target_user]['vip_level'] = level
            users[target_user]['vip_expires'] = time.time() + VIP_LEVELS[level]['duration']
            users[target_user]['vip_last_krds_claim'] = time.time()
            generate_daily_quests(target_user)
            save_data()
    
    bot.send_message(message.chat.id, 
        f"👑✅ Пользователю @{target_username} выдан {VIP_LEVELS[level]['name']} VIP на 30 дней!")

@bot.message_handler(commands=['removevip'])
def remove_vip(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /removevip @ник")
        return
    
    target_username = args[1].replace('@', '').lower()
    
    with data_lock:
        target_user = username_cache.get(target_username)
        if not target_user:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        with get_user_lock(target_user):
            users[target_user]['vip_level'] = None
            users[target_user]['vip_expires'] = 0
            save_data()
    
    bot.send_message(message.chat.id, f"✅ VIP у пользователя @{target_username} снят!")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /ban @ник")
        return
    
    target_username = args[1].replace('@', '').lower()
    
    with data_lock:
        target_user = username_cache.get(target_username)
        if not target_user:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        if target_user == user_id:
            bot.send_message(message.chat.id, "❌ Нельзя забанить самого себя!")
            return
        
        with get_user_lock(target_user):
            users[target_user]['banned'] = True
            save_data()
    
    bot.send_message(message.chat.id, f"🔨✅ Пользователь @{target_username} забанен.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /unban @ник")
        return
    
    target_username = args[1].replace('@', '').lower()
    
    with data_lock:
        target_user = username_cache.get(target_username)
        if not target_user:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        with get_user_lock(target_user):
            users[target_user]['banned'] = False
            save_data()
    
    bot.send_message(message.chat.id, f"✅ Пользователь @{target_username} разбанен.")

# ====================== СИСТЕМА РАБОТЫ ======================
@bot.message_handler(commands=['работа', 'Работа'])
def work_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    with get_user_lock(user_id):
        reward = 55
        vip_mult = get_vip_multiplier(user_id, 'work_mult')
        reward = int(reward * vip_mult)
        
        user['balance'] += reward
        user['work_count'] = user.get('work_count', 0) + 1
        
        update_quest_progress(user_id, 'works')
        
        save_data()
    
    text = (
        f"💼 ** РАБОТА ** 💼\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✅ Ты получил: +{reward} кредиксов\n"
        f"💰 Текущий баланс: {format_number(user['balance'])} кредиксов\n"
        f"📊 Всего отработано раз: {user['work_count']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 Приходи за бонусом снова!"
    )
    bot.send_message(message.chat.id, text)

# ====================== РЕФЕРАЛЬНАЯ СИСТЕМА ======================
@bot.message_handler(commands=['реф', 'Реф'])
def ref_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    bot_info = bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    user = get_user(user_id)
    
    update_quest_progress(user_id, 'referrals', user.get('referrals', 0))
    
    text = (
        "👥 ** РЕФЕРАЛЬНАЯ СИСТЕМА ** 👥\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔗 Твоя ссылка:\n{ref_link}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📊 Приглашено друзей: {user.get('referrals', 0)}\n\n"
        "🎁 ** Награда за друга: **\n"
        f"💰 +{format_number(bonus_data['referral_bonus'])} кредиксов\n"
        "💎 +5 KRDS\n\n"
        "🏆 ** Достижения: **\n"
        "▸ 10 друзей: +100,000 кредиксов\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 Отправь ссылку друзьям и получай бонусы!"
    )
    bot.send_message(message.chat.id, text)

# ====================== БАЗОВЫЕ КОМАНДЫ ======================
@bot.message_handler(commands=['start', 'Start', 'СТАРТ'])
def start_command(message):
    user_id = str(message.from_user.id)
    
    if message.from_user.username:
        update_username_cache(user_id, message.from_user.username)
    
    user = get_user(user_id)
    
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        referrer_id = args[1]
        if referrer_id != user_id and referrer_id in users:
            with get_user_lock(referrer_id), get_user_lock(user_id):
                referrer = get_user(referrer_id)
                user['referrer'] = referrer_id
                referrer['referrals'] = referrer.get('referrals', 0) + 1
                referrer['balance'] += bonus_data['referral_bonus']
                referrer['krds_balance'] += 5
                user['balance'] += 500
                
                update_quest_progress(referrer_id, 'referrals', referrer['referrals'])
                
                save_data()
                
                try:
                    bot.send_message(int(referrer_id),
                        f"🎉 По твоей ссылке зарегистрировался новый игрок!\n"
                        f"💰 +{format_number(bonus_data['referral_bonus'])} кредиксов\n"
                        f"💎 +5 KRDS")
                except:
                    pass
    
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in user['daily_quests']:
        generate_daily_quests(user_id)
    
    bot.send_message(
        message.chat.id,
        f"👋 ** Добро пожаловать в КАЗИНО БОТ! **\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💰 Твой баланс: {format_number(user['balance'])} кредиксов\n"
        f"💎 KRDS: {user['krds_balance']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 **Доступные команды:**\n"
        f"  помощь - список всех команд\n"
        f"  игры - список игр\n"
        f"  профиль - твой профиль\n"
        f"  работа - заработать\n"
        f"  бонус - ежедневные бонусы\n"
        f"  квесты - ежедневные задания\n"
        f"  вип - VIP статус\n"
        f"  турнир - турниры\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📢 Канал: {CHANNEL_USERNAME}\n"
        f"💬 Чат: {CHAT_LINK}"
    )
    print(f"✅ Новый пользователь: {user_id}")

@bot.message_handler(commands=['помощь', 'help', 'Помощь'])
def help_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    if message.from_user.username:
        update_username_cache(user_id, message.from_user.username)
    
    text = (
        "📚 ** ПОМОЩЬ ПО БОТУ ** 📚\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎮 ** ИГРЫ (без /)**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "башня [ставка] - Башня (x1-x6)\n"
        "футбол [ставка] гол/мимо - Футбол (x2)\n"
        "баскетбол [ставка] гол/мимо - Баскетбол (x2)\n"
        "дартс [ставка] - Дартс (x1.5-x10)\n"
        "покер [ставка] - Покер (x2)\n"
        "пирамида [ставка] - Пирамида (x5)\n"
        "мины [ставка] - Мины (до x12)\n"
        "джекпот [ставка] - Джекпот\n"
        "фишки [ставка] black/white - Фишки (x2)\n"
        "x2/x3/x5 [ставка] - Множители\n"
        "рулетка_рус [ставка] - Русская рулетка (x6)\n"
        "очко [ставка] - Очко (Блэкджек)\n"
        "краш [ставка] - Краш\n"
        "слоты [ставка] - Слоты\n"
        "кости [ставка] тип число - Кости\n"
        "рулетка_каз [ставка] тип число - Рулетка\n"
        "хило [ставка] - Хило (x2)\n\n"
        "📌 **Форматы ставок:**\n"
        "   1к = 1,000\n"
        "   1кк, 1ку = 1,000,000\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💎 ** KRDS СИСТЕМА **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "донат - баланс KRDS\n"
        "сенд @ник сумма - отправить KRDS\n"
        "продать количество - продать боту (3250/шт)\n"
        "обменник - P2P обменник\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🐭 ** МЫШКИ **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "мышки - магазин мышек\n"
        "купитьмышку [тип] - купить мышку\n"
        "мыши - мои мышки\n"
        "собратьмыши - собрать доход\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏦 ** БАНК **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "банк - банковские операции\n"
        "депозит [сумма] - положить под 5%\n"
        "снять [сумма] - снять с депозита\n"
        "кредит [сумма] - взять кредит\n"
        "выплатить [сумма] - выплатить кредит\n"
        "проценты - начислить проценты\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📱 ** ТЕЛЕФОН **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "телефон - твой номер\n"
        "контакты - список контактов\n"
        "добавить @ник - добавить контакт\n"
        "позвонить @ник - позвонить\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎁 ** БОНУСЫ И КВЕСТЫ **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "бонус - информация о бонусах\n"
        "daily - ежедневный бонус\n"
        "weekly - еженедельный бонус\n"
        "квесты - ежедневные задания\n"
        "вип - VIP статус\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🐾 ** ПИТОМЦЫ **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "питомцы - мои питомцы\n"
        "магазинпитомцев - купить питомца\n"
        "купитьпитомца [тип] - купить\n"
        "покормить [тип] - покормить\n"
        "собратьпитомцы - собрать доход\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏢 ** БИЗНЕС **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "бизнес - мой бизнес\n"
        "магазинбизнеса - купить бизнес\n"
        "купитьбизнес [тип] - купить\n"
        "улучшить [тип] - улучшить\n"
        "собратьбизнес - собрать доход\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 ** КЛАНЫ И ТУРНИРЫ **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "клан - информация о клане\n"
        "создатьклан [название] - создать клан\n"
        "турнир - информация о турнирах\n"
        "турнир_вступить [тип] - вступить в турнир\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💼 ** ЭКОНОМИКА **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "работа - заработок\n"
        "дать @ник сумма - перевод\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 ** СОЦИАЛ **\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "реф - реферальная ссылка\n"
        "топ - топ игроков\n"
        "профиль - профиль\n"
        "статистика - общая статистика\n"
        "отмена - отменить игру\n\n"
        f"🎉 Ивент: x{RELEASE_EVENT['multiplier']} к выигрышам!\n\n"
        f"📢 Канал: {CHANNEL_USERNAME}\n"
        f"💬 Чат: {CHAT_LINK}"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['профиль', 'Профиль'])
def profile_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    clan_name = "Нет клана"
    if user.get('clan') and user['clan'] in clans:
        clan_name = clans[user['clan']]['name']
    
    deposit = user.get('bank_deposit', {}).get('amount', 0)
    loan = user.get('bank_loan', {}).get('amount', 0)
    
    vip_status = "Нет"
    vip_icon = ""
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        vip_data = VIP_LEVELS[user['vip_level']]
        vip_status = f"{vip_data['color']} {vip_data['name']}"
        vip_icon = vip_data['color']
    
    text = (
        f"📱 ** ПРОФИЛЬ ** 📱\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🆔 ID: {user_id}\n"
        f"{vip_icon} VIP: {vip_status}\n\n"
        f"💰 ** ФИНАНСЫ **\n"
        f"💸 Кредиксы: {format_number(user['balance'])}\n"
        f"💎 KRDS: {user['krds_balance']}\n"
        f"🏦 Депозит: {format_number(deposit)}\n"
        f"📉 Кредит: {format_number(loan)}\n\n"
        f"📊 ** СТАТИСТИКА ИГР **\n"
        f"🎮 Сыграно: {user.get('games_played', 0)}\n"
        f"✅ Побед: {user.get('total_wins', 0)}\n"
        f"❌ Поражений: {user.get('total_losses', 0)}\n"
        f"🔥 Стрик: {user.get('win_streak', 0)}\n"
        f"🎰 Макс стрик: {user.get('max_win_streak', 0)}\n\n"
        f"🐭 ** МЫШКИ **\n"
        f"Всего: {sum(user.get('mice', {}).values())} шт.\n"
        f"Доход в час: {sum(MICE_DATA[m]['income'] * count for m, count in user.get('mice', {}).items() if m in MICE_DATA)}\n\n"
        f"🐾 ** ПИТОМЦЫ **\n"
        f"Всего: {len(user.get('pets', {}))} шт.\n\n"
        f"🏪 ** БИЗНЕС **\n"
        f"Всего: {len(user.get('businesses', {}))} шт.\n\n"
        f"👥 ** СОЦИАЛ **\n"
        f"👥 Рефералов: {user.get('referrals', 0)}\n"
        f"👑 Клан: {clan_name}\n"
        f"💼 Работ: {user.get('work_count', 0)}\n"
        f"📋 Квестов: {user.get('quests_completed', 0)}\n\n"
        f"📱 ** ТЕЛЕФОН **\n"
        f"📞 Номер: {user.get('phone_number', 'Нет номера')}\n"
        f"👥 Контактов: {len(user.get('phone_contacts', []))}\n\n"
        f"🎁 ** БОНУСЫ **\n"
        f"📅 Дейли стрик: {user.get('daily_bonus', {}).get('streak', 0)} дней\n"
        f"📆 Викли стрик: {user.get('weekly_bonus', {}).get('streak', 0)} недель\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['баланс', 'Баланс'])
def balance_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    text = (
        f"💰 ** БАЛАНС ** 💰\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💸 Кредиксы: {format_number(user['balance'])}\n"
        f"💎 KRDS: {user['krds_balance']}\n"
        f"🎰 Проиграно: {format_number(user.get('total_lost', 0))}\n"
        f"🐭 Мышки: {sum(user.get('mice', {}).values())} шт.\n"
        f"🐾 Питомцы: {len(user.get('pets', {}))} шт.\n"
        f"🏪 Бизнесы: {len(user.get('businesses', {}))} шт."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['игры', 'Игры'])
def games_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    text = (
        "🎮 ** СПИСОК ИГР ** 🎮\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏰 башня [ставка]\n"
        "⚽ футбол [ставка] гол/мимо\n"
        "🏀 баскетбол [ставка] гол/мимо\n"
        "🎯 дартс [ставка]\n"
        "🃏 покер [ставка]\n"
        "🔺 пирамида [ставка]\n"
        "💣 мины [ставка]\n"
        "🎰 джекпот [ставка]\n"
        "⚫️⚪️ фишки [ставка] black/white\n"
        "🎲 x2/x3/x5 [ставка]\n"
        "🔫 рулетка_рус [ставка]\n"
        "🃏 очко [ставка]\n"
        "🚀 краш [ставка]\n"
        "🎰 слоты [ставка]\n"
        "🎲 кости [ставка] тип число\n"
        "🎰 рулетка_каз [ставка] тип число\n"
        "📈 хило [ставка]\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 **Форматы ставок:**\n"
        "   1к = 1,000\n"
        "   1кк, 1ку = 1,000,000\n\n"
        "🛑 Отмена игры: отмена\n\n"
        f"🎉 Ивент: x{RELEASE_EVENT['multiplier']} к выигрышам!"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['отмена', 'Отмена', 'cancel'])
def cancel_game_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!")
        return
    
    if cancel_user_game(user_id):
        bot.send_message(message.chat.id, "🛑 Игра отменена. Ставка возвращена.")
    else:
        bot.send_message(message.chat.id, "❌ У тебя нет активной игры.")

# ====================== ОБРАБОТЧИКИ БЕЗ СЛЭША ======================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        return
    
    text = message.text.lower().strip()
    
    if text.startswith('/'):
        return
    
    if text.startswith('башня '):
        message.text = '/башня ' + text[6:]
        tower_game(message)
    
    elif text.startswith('футбол '):
        message.text = '/футбол ' + text[7:]
        football_game(message)
    
    elif text.startswith('баскетбол '):
        message.text = '/баскетбол ' + text[10:]
        basketball_game(message)
    
    elif text.startswith('дартс '):
        message.text = '/дартс ' + text[6:]
        darts_game(message)
    
    elif text.startswith('покер '):
        message.text = '/покер ' + text[6:]
        poker_game(message)
    
    elif text.startswith('пирамида '):
        message.text = '/пирамида ' + text[9:]
        pyramid_game(message)
    
    elif text.startswith('мины '):
        message.text = '/мины ' + text[5:]
        mines_game(message)
    
    elif text.startswith('джекпот '):
        message.text = '/джекпот ' + text[8:]
        jackpot_game(message)
    
    elif text.startswith('фишки '):
        message.text = '/фишки ' + text[6:]
        chips_game(message)
    
    elif text.startswith('x2 ') or text.startswith('х2 '):
        message.text = '/x2 ' + text[3:]
        multiplier_game(message)
    
    elif text.startswith('x3 ') or text.startswith('х3 '):
        message.text = '/x3 ' + text[3:]
        multiplier_game(message)
    
    elif text.startswith('x5 ') or text.startswith('х5 '):
        message.text = '/x5 ' + text[3:]
        multiplier_game(message)
    
    elif text.startswith('рулетка_рус '):
        message.text = '/рулетка_рус ' + text[12:]
        russian_roulette(message)
    
    elif text.startswith('очко '):
        message.text = '/очко ' + text[5:]
        blackjack_game(message)
    
    elif text.startswith('краш '):
        message.text = '/краш ' + text[5:]
        crash_game(message)
    
    elif text.startswith('слоты '):
        message.text = '/слоты ' + text[6:]
        slots_game(message)
    
    elif text.startswith('кости '):
        message.text = '/кости ' + text[6:]
        dice_game(message)
    
    elif text.startswith('рулетка_каз '):
        message.text = '/рулетка_каз ' + text[12:]
        casino_roulette(message)
    
    elif text.startswith('хило '):
        message.text = '/хило ' + text[5:]
        hilo_game(message)
    
    elif text.startswith('работа'):
        message.text = '/работа'
        work_command(message)
    
    elif text.startswith('банк'):
        message.text = '/банк'
        bank_command(message)
    
    elif text.startswith('депозит '):
        message.text = '/депозит ' + text[8:]
        deposit_command(message)
    
    elif text.startswith('снять '):
        message.text = '/снять ' + text[6:]
        withdraw_command(message)
    
    elif text.startswith('кредит '):
        message.text = '/кредит ' + text[7:]
        loan_command(message)
    
    elif text.startswith('выплатить '):
        message.text = '/выплатить ' + text[10:]
        repay_loan_command(message)
    
    elif text.startswith('проценты'):
        message.text = '/проценты'
        interest_command(message)
    
    elif text.startswith('мышки'):
        message.text = '/мышки'
        mice_shop_command(message)
    
    elif text.startswith('купитьмышку '):
        message.text = '/купитьмышку ' + text[12:]
        buy_mouse_command(message)
    
    elif text.startswith('мыши'):
        message.text = '/мыши'
        my_mice_command(message)
    
    elif text.startswith('собратьмыши'):
        message.text = '/собратьмыши'
        collect_mice_command(message)
    
    elif text.startswith('питомцы'):
        message.text = '/питомцы'
        pets_command(message)
    
    elif text.startswith('магазинпитомцев'):
        message.text = '/магазинпитомцев'
        pet_shop_command(message)
    
    elif text.startswith('купитьпитомца '):
        message.text = '/купитьпитомца ' + text[14:]
        buy_pet_command(message)
    
    elif text.startswith('покормить '):
        message.text = '/покормить ' + text[10:]
        feed_pet_command(message)
    
    elif text.startswith('бизнес'):
        message.text = '/бизнес'
        business_command(message)
    
    elif text.startswith('магазинбизнеса'):
        message.text = '/магазинбизнеса'
        business_shop_command(message)
    
    elif text.startswith('купитьбизнес '):
        message.text = '/купитьбизнес ' + text[13:]
        buy_business_command(message)
    
    elif text.startswith('улучшить '):
        message.text = '/улучшить ' + text[9:]
        upgrade_business_command(message)
    
    elif text.startswith('собратьбизнес'):
        message.text = '/собратьбизнес'
        collect_business_command(message)
    
    elif text.startswith('клан'):
        message.text = '/клан'
        clan_command(message)
    
    elif text.startswith('создатьклан '):
        message.text = '/создатьклан ' + text[12:]
        create_clan_command(message)
    
    elif text.startswith('телефон'):
        message.text = '/телефон'
        phone_command(message)
    
    elif text.startswith('контакты'):
        message.text = '/контакты'
        contacts_command(message)
    
    elif text.startswith('добавить '):
        message.text = '/добавить ' + text[9:]
        add_contact_command(message)
    
    elif text.startswith('позвонить '):
        message.text = '/позвонить ' + text[10:]
        call_command(message)
    
    elif text.startswith('бонус'):
        message.text = '/бонус'
        bonus_command(message)
    
    elif text.startswith('daily') or text.startswith('дейли'):
        message.text = '/daily'
        daily_bonus_command(message)
    
    elif text.startswith('weekly') or text.startswith('викли'):
        message.text = '/weekly'
        weekly_bonus_command(message)
    
    elif text.startswith('квесты') or text.startswith('quests'):
        message.text = '/квесты'
        quests_command(message)
    
    elif text.startswith('вип') or text.startswith('vip'):
        message.text = '/вип'
        vip_command(message)
    
    elif text.startswith('купить_вип '):
        message.text = '/купить_вип ' + text[11:]
        buy_vip_command(message)
    
    elif text.startswith('вип_крдс'):
        message.text = '/вип_крдс'
        vip_krds_command(message)
    
    elif text.startswith('турнир') and not text.startswith('турнир_'):
        message.text = '/турнир'
        tournament_command(message)
    
    elif text.startswith('турнир_вступить '):
        message.text = '/турнир_вступить ' + text[16:]
        tournament_join(message)
    
    elif text.startswith('турнир_покинуть '):
        message.text = '/турнир_покинуть ' + text[16:]
        tournament_leave(message)
    
    elif text.startswith('турнир_вступить '):
    message.text = '/турнир_вступить ' + text[16:]
    tournament_join(message)
    
    elif text.startswith('турнир_покинуть '):
        message.text = '/турнир_покинуть ' + text[16:]
        tournament_leave(message)
    
    elif text.startswith('донат'):
        message.text = '/донат'
        donate_command(message)
    
    elif text.startswith('сенд '):
    message.text = '/сенд ' + text[5:]
    send_krds_command(message)
    
    elif text.startswith('сенд '):
        message.text = '/сенд ' + text[5:]
        send_krds_command(message)
    
    elif text.startswith('продать '):
        message.text = '/продать ' + text[8:]
        sell_to_bot_command(message)
    
    elif text.startswith('обменник'):
        message.textds_command(message)
    
    elif text.startswith('продать '):
        message.text = '/продать ' + text[8:]
        sell_to_bot_command(message)
    
    elif text.startswith('обменник'):
        message.text = '/ = '/обменник'
        exchange_menu(message)
    
    elif text.startswith('продатькрдс '):
        message.text = '/продатькрдобменник'
        exchange_menu(message)
    
    elif text.startswith('продатькрдс '):
        message.text = '/продатькрдс ' + text[12:]
        sell_krds_command(message)
    
    elif text.startswith('моиордера'):
        message.text = '/моиордера'
        my_orders_command(message)
    
    elif text.startswithс ' + text[12:]
        sell_krds_command(message)
    
    elif text.startswith('моиордера'):
        message.text = '/моиордера'
        my_orders_command(message)
    
    elif text.startswith('ордера'):
        message.text = '/ордера'
        all_orders_command(message)
    
    elif('ордера'):
        message.text = '/ордера'
        all_orders_command(message)
    
    elif text.startswith('купить ') and len(text.split()) >=  text.startswith('купить ') and len(text.split()) >= 3 and text.split()[1].isdigit():
        message.text = '/купить ' + text[73 and text.split()[1].isdigit():
        message.text = '/купить ' +:]
        buy_krds_command(message)
    
    elif text.startswith('отменитьордер '):
        message.text = '/отменитьордер ' + text[14:]
        cancel_order_command(message text[7:]
        buy_krds_command(message)
    
    elif text.startswith('отменитьордер '):
        message.text = '/отменитьордер ' + text[14:]
        cancel_order_command(message)
    
    elif text.startswith('реф'):
        message.text = '/реф'
        ref_command(message)
    
    elif text)
    
    elif text.startswith('реф'):
        message.text = '/реф'
        ref_command(message)
    
    elif text.startswith('дать '):
        message.startswith('дать '):
        message.text = '/дать ' + text[5:]
        give_command(message)
    
    elif text.startswith('профиль'):
        message.text = '/профиль'
        profile_command(message)
    
    elif text.startswith('статистика') or text.startswith('stats'):
        message.text = '/статистика'
        stats_command(message)
    
    elif text.startswith('т.text = '/дать ' + text[5:]
        give_command(message)
    
    elif text.startswith('профиль'):
        message.text = '/профиль'
        profile_command(message)
    
    elif text.startswith('статистика') or text.startswith('stats'):
        message.text = '/статистика'
        stats_command(message)
    
    elif text.startswith('топ'):
        message.text = '/топ'
        new_top_command(message)
    
    elif text.startswith('баланс'):
        message.textоп'):
        message.text = '/топ'
        new_top_command(message)
    
    elif text.startswith('баланс'):
        message.text = '/баланс'
        balance_command(message)
    
    elif text.startswith('игры'):
        message.text = '/игры'
        games_command(message)
    
    elif text.startswith('помощь') or text.startswith('help'):
        message.text = '/помощь = '/баланс'
        balance_command(message)
    
    elif text.startswith('игры'):
        message.text = '/игры'
        games_command(message)
    
    elif text.startswith('помощь') or text.startswith('help'):
        message.text = '/помощь'
        help_command'
        help_command(message)
    
    elif text.startswith('отмена') or text.startswith(message)
    
    elif text.startswith('отмена') or text.startswith('cancel('cancel'):
        message.text = '/'):
        message.text = '/отмена'
       отмена'
        cancel_game_command(message)
    
 cancel_game_command(message)
    
    elif text.startswith('старт') or text.startswith('start'):
        message.text = '/start'
           elif text.startswith('старт') or text.startswith('start'):
        message.text = '/start'
        start_command(message)

# ====================== ОБРАБОТЧИКИ IN start_command(message)

# ====================== ОБРАБОТЧИКИ INLINE КНОПОК =================LINE КНОПОК ======================
@bot.callback_query_handler(func=lambda call: True)
=====
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = str(call.from_user.id)
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "⛔ Вы забанены!")
        return
    
    user = get_user(userdef handle_callback(call):
    user_id = str(call.from_user.id)
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "⛔ Вы забанены!")
        return
    
    user = get_user(user_id)
    
    if call.data.startswith('tower_'):
        if user.get('game') is None or user['game_id)
    
    if call.data.startswith('tower_'):
        if user.get('game') is None or user['game'].get('type') != 'tower':
            bot.answer_callback_query(call.id'].get('type') != 'tower':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            return
        
        if call.data == 'tower_take':
            game, "❌ Игра не найдена!")
            return
        
        if call.data == 'tower_take':
            game = user = user['game['game']
           ']
            if game.get(' if game.get('stage')stage') != 'playing':
                bot.answer_callback_query(call.id != 'playing':
                bot.answer_callback_query(call.id, ", "❌ Игра уже закончена!")
                return
            
            with get_user_lock(user_id):
                current_mult = TOWER_MULTIPLIERS[game['level']]
                vip_mult = get_vip_multiplier(user_id, '❌ Игра уже закончена!")
                return
            
            with get_user_lock(user_id):
                current_mult = TOWER_MULTIPLIERS[game['level']]
                vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                win_amount = int(game['bet'] * current_mult * vip_mult * get_event_multiplbonus_mult')
                win_amount = int(game['bet'] * current_mult * vip_mult * get_event_multiplier())
ier())
                
                user['balance'] += win_amount
                update_game_stats(user_id, True, game['bet'], win_amount)
                add_tournament_points                
                user['balance'] += win_amount
                update_game_stats(user_id, True, game['bet'], win_amount)
                add_tour(user_id, 'башня', game['bet'], win_amount)
                
                textnament_points(user_id, 'башня', game['bet'], win_amount)
                
                text = (
                    f"🏰 ** БА = (
                    f"🏰 ** БАШНЯ ** 🏰\n\n"
                    f"💰 Ты забрал выигрыш!\n\n"
                    f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
               ШНЯ ** 🏰\n\n"
                    f"💰 Ты забрал выигрыш!\n\n"
                    f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                save_data()
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id )
                user['game'] = None
                save_data()
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)
            return
        
        level = int(call.data.split('_')[1])
        game = user['game']
        
        if game.get('stage') != ')
            return
        
        level = int(call.data.split('_')[1])
        game = user['game']
        
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        with get_user_lock(user_id):
            cell = game['cells'][level-1]
            
            if cell == '💣':
                game['stage'] = 'lost'
                update_game_stats(user_id, False, game['bet'])
               playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        with get_user_lock(user_id):
            cell = game['cells'][level-1]
            
            if cell == '💣':
                game['stage'] = 'lost'
                update_game_stats(user_id, False, game add_tournament_points(user_id, 'башня', game['bet'], 0)
                
                text = (
                    f"🏰 ** БАШНЯ ** 🏰\n\n"
                    f"💥 Ты нашёл бомбу!\n\n"
                    f"❌ Проигрыш: -{format_number(game['bet'])} кредиксов\n"
                    f"💰 Балан['bet'])
                add_tournament_points(user_id, 'башня', game['bet'], 0)
                
                text = (
                    f"🏰 ** БАШНЯ ** 🏰\n\n"
                    f"💥 Ты нашёл бомбу!\n\n"
                    f"❌ Проигрыш: -{format_number(game['bet'])} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
           с: {format_number(user['balance'])}"
                )
                user['game'] = None
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            else:
                game['level'] += 1
                
                if game['level'] > game['max_level']:
                    vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                    win_amount = int(game[' else:
                game['level'] += 1
                
                if game['level'] > game['max_level']:
                    vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                    win_amount = int(game['bet'] * TOWER_MULTIPLIERS[game['max_level']] * vip_mult * get_event_multiplier())
                    
                    user['balance'] += win_amount
                   bet'] * TOWER_MULTIPLIERS[game['max_level']] * vip_mult * get_event_multiplier())
                    
                    user['balance'] += win_amount
                    update_game_stats(user_id, True, game['bet'], win_amount)
                    add_tournament_points(user_id, 'башня', game['bet'], win_amount)
                    
                    text = (
                        f"🏰 ** БАШНЯ ** 🏰\n\n"
                        f"🎉 Ты прош update_game_stats(user_id, True, game['bet'], win_amount)
                    add_tournament_points(user_id, 'башня', game['bet'], win_amount)
                    
                    text = (
                        f"🏰 ** БАШНЯ ** 🏰\n\n"
                        f"🎉 Ты прошёл все уровни!\n\n"
                        f"✅ Выигрыш: +{format_number(ёл все уровни!\n\n"
                        f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                        f"💰 Баланс: {format_number(user['balance'])}"
                    )
                    user['game'] = None
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                else:
                    vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                    current_mult = TOWER_MULTIPLIERS[game['level']]
                    potential_win = int(game['bet'] *win_amount)} кредиксов\n"
                        f"💰 Баланс: {format_number(user['balance'])}"
                    )
                    user['game'] = None
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
                else:
                    vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                    current_mult = TOWER_MULTIPLIERS[game['level']]
                    potential_win = int(game['bet'] * current_mult * vip_mult * get_event_multiplier())
                    
                    markup = types.InlineKeyboardMarkup(row_width=5)
                    buttons = []
                    for i in range(1, 6):
                        buttons.append(types.InlineKeyboardButton(f"{i}", callback_data=f current_mult * vip_mult * get_event_multiplier())
                    
                    markup = types.InlineKeyboardMarkup(row_width=5)
                    buttons = []
                    for i in range(1, 6):
                        buttons.append(types.InlineKeyboardButton(f"{i}", callback_data=f"tower_{i}"))
                    markup.add(*buttons)
                    markup.add(types.InlineKeyboardButton("💰 Забрать выигрыш", callback_data="tower_take"))
                    
                    bot.edit_message_text(
                        f"🏰 ** БАШНЯ ** 🏰\n\n"
"tower_{i}"))
                    markup.add(*buttons)
                    markup.add(types.InlineKeyboardButton("💰 Забрать выигрыш", callback_data="tower_take"))
                    
                    bot.edit_message_text(
                        f"🏰 ** БАШНЯ ** 🏰\n\n"
                        f"Ставка: {format_number(game['bet'])} кредиксов\n"
                        f"Уровень: {game['level']}/{game['max_level']}\n"
                        f"Множитель: x                        f"Ставка: {format_number(game['bet'])} кредиксов\n"
                        f"Уровень: {game['level']}/{game['max_level']}\n"
                        f"Множитель: x{current_mult}\n"
                        f"Забрать сейчас: {format_number(potential_win)} кредиксов\n\n"
                        f"Выбери ячейку (1-5):",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup
                    )
            
            save_data()
        bot.answer_callback_query(call{current_mult}\n"
                        f"Забрать сейчас: {format_number(potential_win)} кредиксов\n\n"
                        f"Выбери ячейку (1-5):",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup
                    )
            
            save_data()
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('mines_'):
        if user.get('game') is None or user['game'].get('type') != 'mines':
            bot.answer_callback_query(call.id, "❌ Игра не.id)
    
    elif call.data.startswith('mines_'):
        if user.get('game') is None or user['game'].get('type') != 'mines':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            return
        
        if call.data == 'mines_take':
            game = user[' найдена!")
            return
        
        if call.data == 'mines_take':
            game = user['game']
            if game.get('stage') != 'playing':
                bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
                return
            
            if game.get('steps', 0) == 0:
game']
            if game.get('stage') != 'playing':
                bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
                return
            
            if game.get('steps', 0) == 0:
                bot.answer_callback_query(call.id, "❌ Открой хотя бы одну ячейку!")
                return
            
            with get_user_lock(user_id):
                multiplier = MINES_MULTIPLI                bot.answer_callback_query(call.id, "❌ Открой хотя бы одну ячейку!")
                return
            
            with get_user_lock(user_id):
                multiplier = MINES_MULTIPLIERS[game['ERSmines']][game['steps']]
                vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                win_amount = int(game['bet'] * multiplier * vip_mult *[game['mines']][game['steps']]
                vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                win_amount = int(game['bet'] * multiplier * vip_mult * get_event_multipl get_event_multiplier())
ier())
                
                user['balance'] += win_amount
                update_game_stats(user_id, True, game['bet                
                user['balance'] += win_amount
                update_game_stats(user_id, True, game['bet'], win'], win_amount)
_amount)
                add                add_tournament_points(user_id, '_tournament_points(user_id, 'минымины', game', game['bet'], win_amount)
                
                field_display = []
               ['bet'], win_amount)
                
                field_display = []
                for i in range for i(25):
                    if game['field'][i] == ' in range(25):
                    if game['field'][i] == '💣':
💣':
                        field_display.append('💣')
                    else:
                        field                        field_display.append('💣')
                    else:
                        field_display.append('💎' if game['opened'][i] else '⬜')
                
                field_rows = []
                for i in range(0, 25, 5):
                    field_rows.append(''.join(field_display[i_display.append('💎' if game['opened'][i] else '⬜')
                
                field_rows = []
                for i in range(0, 25, 5):
                    field_rows.append(''.join(field_display[i:i+5]))
                
                text = (
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"{chr(10).join(field_rows)}\n\n"
                    f"💰 Ты забрал выигрыш!\n\n"
                    f"✅ Выигрыш: +{:i+5]))
                
                text = (
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"{chr(10).join(field_rows)}\n\n"
                    f"💰 Ты забрал выигрыш!\n\n"
                    f"✅ Выигрыш:format_number(win_amount)} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                save_data()
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)
 +{format_number(win_amount)} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                save_data()
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)
            return
        
        if call.data == 'mines_no':
                       return
        
        if call.data == 'mines_no':
            bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        pos = int(call.data.split('_')[1])
        game = user['game']
        
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        pos = int(call.data.split('_')[1])
        game = user['game']
        
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        if game['opened'][pos]:
            bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        with get_user_lock(user_id):
            game['opened'][pos] = True
            cell = game['field'][pos]
            
            if cell ==, "❌ Игра уже закончена!")
            return
        
        if game['opened'][pos]:
            bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        with get_user_lock(user_id):
            game['opened'][pos] = True
            cell = game['field'][pos]
            
            if cell == '💣':
                game['stage'] = 'lost'
                update_game_stats(user_id, False, game['bet'])
                add_tournament_points(user_id, 'мины', game['bet'], 0)
                
                field_display = []
                for i in range(25):
                    if game['field'][i] == ' '💣':
                game['stage'] = 'lost'
                update_game_stats(user_id, False, game['bet'])
                add_tournament_points(user_id, 'мины', game['bet'], 0)
                
                field_display = []
                for i in range(25):
                    if game['field'][i] == '💣':
                        field_display.append('💣')
                    elif game['opened'][i]:
                        field_display.append('💎')
                    else:
                        field_display.append('⬜')
                
                field_rows = []
                for i in range(0, 25, 5):
                    field_rows.append(''.join(field💣':
                        field_display.append('💣')
                    elif game['opened'][i]:
                        field_display.append('💎')
                    else:
                        field_display.append('⬜')
                
                field_rows = []
                for i in range(0, 25, 5):
                    field_rows.append(''.join(field_display[i:i+5]))
                
                text = (
                    f"💣 ** МИНЫ ** 💣\n\n"
_display[i:i+5]))
                
                text = (
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"{chr(10).join(field_rows)}\n\n"
                    f"💥 Ты нашёл мину!\n\n"
                    f"❌ Проигрыш: -{format_number(game['bet'])} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                bot.edit_message_text(text, call.message.chat.id, call                    f"{chr(10).join(field_rows)}\n\n"
                    f"💥 Ты нашёл мину!\n\n"
                    f"❌ Проигрыш: -{format_number(game['bet'])} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            else:
                game['steps'] += 1
                
                vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                multiplier = MINES_MULTIPLIERS[game['mines']][game['steps']]
                potential_win = int(game['bet'] * multiplier * vip_mult * get_event_multiplier.message.message_id)
            else:
                game['steps'] += 1
                
                vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
                multiplier = MINES_MULTIPLIERS[game['mines']][game['steps']]
                potential_win = int(game['bet'] * multiplier * vip_mult * get_event_multiplier())
                
                markup = types.InlineKeyboardMarkup(row_width=5)
                buttons = []
                for i in range(25):
                    if game['opened'][i]:
                        buttons.append(types.InlineKeyboardButton("💎", callback_data="mines_no"))
                    else:
                        buttons.append(types.InlineKeyboardButton("⬜", callback_data=f"mines_{i}"))
                markup.add(*buttons)
                markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="m())
                
                markup = types.InlineKeyboardMarkup(row_width=5)
                buttons = []
                for i in range(25):
                    if game['opened'][i]:
                        buttons.append(types.InlineKeyboardButton("💎", callback_data="mines_no"))
                    else:
                        buttons.append(types.InlineKeyboardButton("⬜", callback_data=f"mines_{i}"))
                markup.add(*buttons)
                markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="mines_tines_take"))
                
                bot.edit_message_text(
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"Ставake"))
                
                bot.edit_message_text(
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"Ставка: {format_number(game['bet'])}\n"
                    f"Мин: {game['mines']}\n"
                    f"Шагов: {game['steps']}\n"
                    f"Множитель: x{multiplier}\n"
                    f"Забрать сейчас: {format_number(potential_win)} кредиксов\n\n"
                    f"Открывай ячейки, но берегись мин!",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markка: {format_number(game['bet'])}\n"
                    f"Мин: {game['mines']}\n"
                    f"Шагов: {game['steps']}\n"
                    f"Множитель: x{multiplier}\n"
                    f"Забрать сейчас: {format_number(potential_win)} кредиксов\n\n"
                    f"Открывай ячейки, но берегись мин!",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup
                )
            
            save_data()
        bot.answer_callback_query(call.id)
    
    elif call.data == 'crash_take':
        if user.get('game') is None or user['game'].get('type') != 'crash':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            return
        
        game = user['game']
        if game.get('stage') != 'playing':
            bot.up=markup
                )
            
            save_data()
        bot.answer_callback_query(call.id)
    
    elif call.data == 'crash_take':
        if user.get('game') is None or user['game'].get('type') != 'crash':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            return
        
        game = user['game']
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        with get_user_lock(user_id):
            vip_mult = get_vip_multiplieranswer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        with get_user_lock(user_id):
            vip_mult = get_vip_multiplier(user_id, 'bonus_mult')
            win_amount = int(game['bet'] * game['multiplier'] * vip_mult * get_event_multiplier())
            
           (user_id, 'bonus_mult')
            win_amount = int(game['bet'] * game['multiplier'] * vip_mult * get_event_multiplier())
            
            user['balance'] += win_amount
            game['stage'] = 'taken'
            update_game_stats(user_id, True, game['bet'], win_amount)
            add_tournament_points(user_id user['balance'] += win_amount
            game['stage'] = 'taken'
            update_game_stats(user_id, True, game['bet'], win_amount)
            add_tournament_points(user_id, 'краш', game['bet'], win_amount)
            
            if user_id in crash_update_timers:
                try:
                    crash_update_timers[user_id].cancel()
                except:
                    pass
                del crash_update_timers[user_id]
            
            text = (
                f"🚀 ** КРАШ ** 🚀\n\n"
                f"💰 Ты забрал x{game['multiplier']:.2f}!\n\n"
                f"✅ Выигрыш: +{, 'краш', game['bet'], win_amount)
            
            if user_id in crash_update_timers:
                try:
                    crash_update_timers[user_id].cancel()
                except:
                    pass
                del crash_update_timers[user_id]
            
            text = (
                f"🚀 ** КРАШ ** 🚀\n\n"
                f"💰 Ты забрал x{game['multiplier']:.2f}!\n\n"
                f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                f"💰 Баланс: {format_number(user['balance'])}"
            )
            user['game'] = None
            save_data()
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
       format_number(win_amount)} кредиксов\n"
                f"💰 Баланс: {format_number(user['balance'])}"
            )
            user['game'] = None
            save_data()
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)

# ====================== ОБРАБОТЧИК ЗАВЕРШЕНИЯ ======================
def signal_handler(signum, frame):
    print("\n" + "="*50)
    print("⏳ Завершение работы бота...")
    cleanup_all_timers()
    save_data()
    print("✅ Данные сохранены")
    print("👋 Бот остановлен")
    print("="*50 bot.answer_callback_query(call.id)

# ====================== ОБРАБОТЧИК ЗАВЕРШЕНИЯ ======================
def signal_handler(signum, frame):
    print("\n" + "="*50)
    print("⏳ Завершение работы бота...")
    cleanup_all_timers()
    save_data()
    print("✅ Данные сохранены")
    print("👋 Бот остановлен")
    print("="*50)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ====================== ЗАПУСК БОТА =================)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ====================== ЗАПУСК БОТА ======================
if __name__ == '__main__':
    load_data()
    init_tournaments()
    start_tournament_checker()
    
    print("=" * 60)
    print("✅ БОТ КАЗИНО ЗАПУЩЕН!")
    print("=" * 60)
=====
if __name__ == '__main__':
    load_data()
    init_tournaments()
    start_tournament_checker()
    
    print("=" * 60)
    print("✅ БОТ КАЗИНО ЗАПУЩЕН!")
    print("=" * 60)
    print("📋 СИСТЕМЫ:")
    print("  • 🎮 Все игры (башня, футбол, баскетбол, дартс, покер, мины, джекпот, фишки, x2/x3/x5, рулетка_рус, очко, краш, слоты, кости, рулетка_каз, хило)")
    print("  • 👑 VIP система (4 уровня)")
    print("  • 📋 Ежедневные квесты")
    print    print("📋 СИСТЕМЫ:")
    print("  • 🎮 Все игры (башня, футбол, баскетбол, дартс, покер, мины, джекпот, фишки, x2/x3/x5, рулетка_рус, очко, краш, слоты, кости, рулетка_каз, хило)")
    print("  • 👑 VIP система (4 уровня)")
    print("  • 📋 Ежедневные квесты")
    print("  • 🏆 Турниры (daily/weekly/monthly)")
    print(" ("  • 🏆 Турниры (daily/weekly/monthly)")
    print("  • 💎 KRDS (валюта)")
    print("  • 📊 Расширенная статистика")
    print("  • 🐭 Мышки (пассивный доход)")
    print("  • 🐾 Питомцы (кормление, счастье)")
    print("  • 🏪 Бизнесы (покупка, улучшение)")
    print("  • 👥 Кланы (создание, управление)")
    print("  • 🏦 Банк (депозиты, кредиты)")
    print("  • 📱 Телефон (контакты, звонки)")
    print("=" * 60)
    print("🎮 ИГРЫ (можно без /):")
    print("  • башня, футбол, баскетбол")
    print("  • дартс, покер, пирамида")
    print("  • мины (ИСПРАВЛЕНО), джекпот")
    print("  • фишки, x2/x3/x5")
    print("  • русская рулетка, очко")
    print("  • краш, слоты, кости")
    print("  • рулетка, хило")
    print("=" * 60)
    print("📌 Форматы ставок:")
    print("  • 1к = 1,000")
    print("  • 1кк, 1ку = 1,000,000")
    print("=" * 60)
    print("🔑 АДМИН ПАНЕЛЬ: /Admin Kyniksvs1832")
    print("=" * 60)
    print("🛑 Для остановки нажмите Ctrl+C")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        cleanup_all_timers()
        save_data()
