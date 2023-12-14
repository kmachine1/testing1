import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


first_day = datetime.today().replace(day=1).strftime('%Y-%m-%d')


def create_table3():
	c.execute('CREATE TABLE IF NOT EXISTS expensesavingstable(expense TEXT,expense_cost FLOAT,expense_type TEXT,expense_date DATE)')


def create_table2():
	c.execute('CREATE TABLE IF NOT EXISTS expensetracktable(expense TEXT,expense_cost FLOAT,expense_type TEXT,expense_date DATE)')


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS expensestable(expense TEXT,expense_cost FLOAT,expense_type TEXT,expense_date DATE)')
	data = pd.read_sql_query("SELECT * FROM expensestable", conn)

	if data.empty == True:
		expense = ['rent', 'microsoft', 'aig life ', 'gym', 'netflix', 'spotify', 'o2', 'youtube', 'breaking', 'medium', 'other']
		cost = [780.0, 6.0, 7.82, 19.99, 6.99, 9.99, 37.01, 16.99, 0.0, 4.1, 0.0]
		type = ['Bill', 'Bill', 'Bill', 'Bill', 'Bill', 'Bill', 'Bill', 'Bill', 'Bill', 'Bill', 'Bill']
		date = [first_day, first_day, first_day, first_day, first_day, first_day, first_day, first_day, first_day, first_day, first_day]

		data = {'expense': expense, 'expense_cost': cost, 'expense_type': type, 'expense_date': date}

		df = pd.DataFrame(data)
	# push the dataframe to sql
		df.to_sql("expensestable", conn, if_exists="append", index=False)


def add_data(expense, expense_cost, expense_type, expense_date):
	c.execute('INSERT INTO expensestable(expense,expense_cost,expense_type,expense_date) VALUES (?,?,?,?)', (expense, expense_cost, expense_type, expense_date))
	conn.commit()


def add_data2(expense, expense_cost, expense_type, expense_date):
	c.execute('INSERT INTO expensetracktable(expense,expense_cost,expense_type,expense_date) VALUES (?,?,?,?)', (expense, expense_cost, expense_type, expense_date))
	conn.commit()


def add_data3(expense, expense_cost, expense_type, expense_date):
	c.execute('INSERT INTO expensesavingstable(expense,expense_cost,expense_type,expense_date) VALUES (?,?,?,?)', (expense, expense_cost, expense_type, expense_date))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM expensestable')
	data = c.fetchall()
	return data


def view_all_data2():
	c.execute('SELECT * FROM expensetracktable')
	data = c.fetchall()
	return data


def view_all_data3():
	c.execute('SELECT * FROM expensesavingstable')
	data = c.fetchall()
	return data


def view_all_expense_names():
	c.execute('SELECT DISTINCT expense FROM expensestable')
	data = c.fetchall()
	return data


def view_all_expense_names2():
	c.execute('SELECT expense FROM expensetracktable')
	data = c.fetchall()
	return data


def view_all_savings_names():
	c.execute('SELECT expense FROM expensesavingstable')
	data = c.fetchall()
	return data


def view_all_date_names():
	c.execute('SELECT DISTINCT expense_date FROM expensestable')
	data = c.fetchall()
	return data


def view_all_date_names2():
	# c.execute('SELECT DISTINCT expense_date FROM expensetracktable')
	c.execute("SELECT strftime('%m',expense_date) FROM expensetracktable")
	data = c.fetchall()
	return data


def view_all_date_names3():
	# c.execute('SELECT DISTINCT expense_date FROM expensetracktable')
	c.execute("SELECT strftime('%m',expense_date) FROM expensesavingstable")
	data = c.fetchall()
	return data


def get_expense(expense):
	c.execute('SELECT * FROM expensestable WHERE expense="{}"'.format(expense))
	data = c.fetchall()
	return data


def get_savings(saving):
	c.execute('SELECT * FROM expensesavingstable WHERE expense="{}"'.format(saving))
	data = c.fetchall()
	return data


def get_expense2(expense):
	c.execute('SELECT * FROM expensetracktable WHERE expense="{}"'.format(expense))
	data = c.fetchall()
	return data


def get_expense_by_status(expense_cost):
	c.execute('SELECT * FROM expensestable WHERE expense_cost="{}"'.format(expense_cost))
	data = c.fetchall()
	return data


def edit_expense_data(new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date):
	c.execute("UPDATE expensestable SET expense =?,expense_cost=?,expense_type=?,expense_date=? WHERE expense=? and expense_cost=? and expense_type=? and expense_date=?", (new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date))
	conn.commit()
	data = c.fetchall()
	return data


def edit_expense_data2(new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date):
	c.execute("UPDATE expensetracktable SET expense =?,expense_cost=?,expense_type=?,expense_date=? WHERE expense=? and expense_cost=? and expense_type=? and expense_date=?", (new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date))
	conn.commit()
	data = c.fetchall()
	return data


def edit_save_data(new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date):
	c.execute("UPDATE expensesavingstable SET expense =?,expense_cost=?,expense_type=?,expense_date=? WHERE expense=? and expense_cost=? and expense_type=? and expense_date=?", (new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date))
	conn.commit()
	data = c.fetchall()
	return data


def delete_data_expense(expense):
	c.execute('DELETE FROM expensestable WHERE expense="{}"'.format(expense))
	conn.commit()


def delete_data_expense2(expense):
	c.execute('DELETE FROM expensetracktable WHERE expense="{}"'.format(expense))
	conn.commit()


def delete_data_expense3(expense):
	c.execute('DELETE FROM expensesavingstable WHERE expense="{}"'.format(expense))
	conn.commit()


def delete_data_month(month):
	c.execute('DELETE FROM expensetracktable WHERE strftime("%m",expense_date)="{}"'.format(month))
	conn.commit()


def delete_data_month2(month):
	c.execute('DELETE FROM expensesavingstable WHERE strftime("%m",expense_date)="{}"'.format(month))
	conn.commit()


def delete_data_date(date):
	c.execute('DELETE FROM expensestable WHERE expense_date="{}"'.format(date))
	conn.commit()


def last_day_of_month(any_day):
	# The day 28 exists in every month. 4 days later, it's always next month
	next_month = any_day.replace(day=28) + timedelta(days=4)
	# subtracting the number of the current day brings us back one month
	return next_month - timedelta(days=next_month.day)


def week_magic(day):
	day_of_week = day.weekday()

	to_beginning_of_week = timedelta(days=day_of_week)
	beginning_of_week = day - to_beginning_of_week

	to_end_of_week = timedelta(days=6 - day_of_week)
	end_of_week = day + to_end_of_week

	return beginning_of_week, end_of_week


def week_of_month(date):
	month = date.month
	week = 0
	while date.month == month:
		week += 1
		date -= timedelta(days=7)

	return week
