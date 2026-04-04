from data.Queries import *
from data.data_types import *
from Function.color_text import *


# Function to delete user for ADMIN only and not for any user
def delete_user_registration(
    user_email: Username, user_password: Password, cur, conn
) -> None:
    EMAIL = user_email
    PASSWORD = user_password

    cur.execute(QUERY_TO_LOGIN_USER, (EMAIL, PASSWORD))
    result = cur.fetchone()
    if result:
        cur.execute(QUERY_TO_DELETE_VALUES, (EMAIL, PASSWORD))
        conn.commit()
        color_text("User removed successfully", BLUE)
    else:
        color_text(f"{EMAIL} not found", YELLOW)
