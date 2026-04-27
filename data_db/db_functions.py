import random
from datetime import datetime
from .db_session import create_session
from .users import User
from flask_login import current_user

simbs = 'qwertyuiopasdfghjklzxcvbnm'
simbs += simbs.upper()
simbs += '1234567890'


def check_api_key(key: str) -> bool:
    db_sess = create_session()
    exist_key = db_sess.query(User).filter(User.api_key == key).first()
    if exist_key:
        return True
    return False


def generate_api_key():
    while True:
        ans = ''
        for s in datetime.now().strftime('%Y-%m-%d-%H-%M-%S'):
            ans += s
            ans += random.choice(simbs)

        db_sess = create_session()
        exist_key = db_sess.query(User).filter(User.api_key == ans).first()
        db_sess.close()
        if not exist_key:
            return ans


def get_api_key(user_name):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.name == user_name).first()
    if not user:
        db_sess.close()
        return None
    if user.api_key is None:
        user.api_key = generate_api_key()
        db_sess.commit()

    api_key = user.api_key
    db_sess.close()
    return api_key


def get_user_info(user_id=None, user_name=None):
    if user_name:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.name == user_name).first()
        db_sess.close()
    elif user_id:
        db_sess = create_session()
        user = db_sess.query(User).filter_by(id=user_id).first()
        db_sess.close()
    else:
        return 0, 0

    if not user:
        return 0, 0

    cnt = user.games_cnt or 0
    sm = user.sum_points or 0

    return cnt, sm


def is_authorized():
    return current_user.is_authenticated


def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.id
    return None


def get_current_user_name():
    if current_user.is_authenticated:
        return current_user.name
    return None

def update_user_stats(user_id=None, user_name=None, points=0):
    db_sess = create_session()
    if user_id:
        user = db_sess.query(User).filter(User.id == user_id).first()
    elif user_name:
        user = db_sess.query(User).filter(User.username == user_name).first()
    else:
        db_sess.close()
        return

    if not user:
        db_sess.close()
        return

    user.games_cnt = (user.games_cnt or 0 ) + 1
    user.sum_points = (user.sum_points or 0) + points

    db_sess.commit()
    db_sess.close()

