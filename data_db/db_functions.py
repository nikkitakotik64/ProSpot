from .db_session import create_session
from .users import User


def get_user_info(user_id=None, user_name=None):
    if user_name:
        user = user_name
    elif user_id:
        db_sess = create_session()
        user = db_sess.query(User).filter_by(id=user_id).first()
        db_sess.close()
    else:
        return 0, 0.0

    if not user:
        return 0, 0.0

    cnt = user.games_cnt or 0
    sm = user.sum_points or 0.0

    return cnt, sm