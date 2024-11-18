import datetime
from database.db_config import get_connection
def get_cu_expense_perday(email):
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    conn = get_connection()
    cursor = conn.cursor()
    query = f"""
    SELECT rent+groceries+shopping+daily_spending+loan+bills+other_expenses AS cum_expense,tracked_date  
    from tracker 
    WHERE MONTH(tracked_date)={month} AND YEAR(tracked_date) = {year} AND email = {email}
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    cu_expenses = []
    date_list = []
    for val in data:
        cu_expenses.append(val[0])
        date_list.append(val[1])
    return date_list,cu_expenses
