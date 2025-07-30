import sqlite3
import datetime

# Databse structure
# position: all active positions
# targets: all target markets that have not been closed

from config import (
    SELL_COUNTDOWN,
    BUY_COUNTDOWN
)

con = sqlite3.connect('trading.db')
c = con.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS positions (
          marketTicker TEXT PRIMARY KEY,
          sellCountdown INTEGER DEFAULT NULL,
          lastChecked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )''')
c.execute('''CREATE TABLE IF NOT EXISTS targets (
          marketTicker TEXT PRIMARY KEY, 
          buyCountdown INTEGER,
          lastChecked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )''')

def get_buy_countdown(marketTicker):
    c.execute('SELECT buyCountdown FROM targets WHERE marketTicker=?', (marketTicker,))
    result = c.fetchone()
    return result[0] if result else None

def decrease_buy_countdown(marketTicker, lastChecked):
    c.execute('UPDATE targets SET buyCountdown=buyCountdown-? WHERE marketTicker=?', (lastChecked, marketTicker))
    con.commit()

def update_target_timestamp(marketTicker):
    c.execute('UPDATE targets SET lastChecked=CURRENT_TIMESTAMP WHERE marketTicker=?', (marketTicker,))
    con.commit()

def get_target_timestamp_age(marketTicker):
    c.execute('SELECT lastChecked FROM targets WHERE marketTicker=?', (marketTicker,))
    result = c.fetchone()
    if result:
        return (datetime.now() - datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')).total_seconds()
    return None

def create_position(marketTicker):
    c.execute('INSERT INTO positions (marketTicker) VALUES (?)', (marketTicker,))

def is_target(marketTicker):
    c.execute('SELECT marketTicker FROM targets WHERE marketTicker=?', (marketTicker,))
    return c.fetchone() is not None

def create_target(marketTicker):
    c.execute(f'INSERT INTO targets (marketTicker, buyCountdown) VALUES (?, {BUY_COUNTDOWN})', (marketTicker,))

def start_sell_countdown(marketTicker):
    c.execute(f'UPDATE positions SET sellCountdown={SELL_COUNTDOWN} WHERE marketTicker=?', (marketTicker,))

def get_sell_countdown(marketTicker):
    c.execute('SELECT sellCountdown FROM positions WHERE marketTicker=?', (marketTicker,))
    result = c.fetchone()
    return result[0] if result else None

def get_position_timestamp_age(marketTicker):
    c.execute('SELECT lastChecked FROM positions WHERE marketTicker=?', (marketTicker,))
    result = c.fetchone()
    if result:
        return (datetime.now() - datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')).total_seconds()
    return None

def update_position_timestamp(marketTicker):
    c.execute('UPDATE positions SET lastChecked=CURRENT_TIMESTAMP WHERE marketTicker=?', (marketTicker,))

def decrease_sell_countdown(marketTicker, lastChecked):
    c.execute('UPDATE positions SET sellCountdown=MAX(sellCountdown-?, 0) WHERE marketTicker=?', (lastChecked, marketTicker))

con.commit()
con.close()