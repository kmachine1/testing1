import streamlit as st
from db_funcs import *
from PIL import Image
import plotly.express as px
from datetime import datetime, timedelta


def color_df(val):

	food_or_outside_expenditure = ['Food', 'Outside_Expenditure']
	bills = ['Bill']
	if val in food_or_outside_expenditure:
		if val == "Food":
			color = "green"

		elif val == "Outside_Expenditure":
			color = "orange"

		else:
			color = 'blue'

	elif val in bills:
		if val == "Bill":
			color = "green"
		else:
			color = "blue"
	else:
		color = 'blue'

	return f'background-color: {color}'


st.set_page_config(page_title="Budgeting_App",
	page_icon="📝",
	layout="wide",
	initial_sidebar_state="expanded",
)

top_image = Image.open('static/banner_top.png')
bottom_image = Image.open('static/banner_bottom.png')
main_image = Image.open('static/main_banner.png')

st.image(main_image, use_column_width='always')
st.title("💰 Budgeting App 💰")

st.sidebar.image(top_image, use_column_width='auto')
choice = st.sidebar.selectbox("Menu", ["Create Expense ✅", "Update Expense 👨‍💻", "Delete Expense ❌", "View All Expenses 👨‍💻"])
st.sidebar.image(bottom_image, use_column_width='auto')

create_table()
create_table2()
create_table3()
if choice == "Create Expense ✅":
	st.subheader("Add Item")
	col1, col2 = st.columns(2)

	with col1:
		expense = st.text_area("Expense")
		expense_cost = st.number_input("Expense Cost")
		expense_type = st.selectbox('Expense Type', ["Food", "Bill", "Outside_Expenditure", "Savings"])

	with col2:

		expense_date = st.date_input("Date")

	col3, col4, col5 = st.columns(3)

	with col3:
		list_of_expenses = [i[0] for i in view_all_expense_names2()]
	if st.button("Add Food or Outside_Expenditure Expense"):
		if (expense != '') and (expense not in list_of_expenses):
			add_data2(expense, expense_cost, expense_type, expense_date)
			st.success("Added expense \"{}\" ✅".format(expense))
			st.snow()
		else:
			st.error('This is an error', icon="🚨")

	with col4:
		list_of_expenses = [i[0] for i in view_all_expense_names()]
	if st.button("Add Bill Expense"):
		if (expense != '') and (expense not in list_of_expenses):
			add_data(expense, expense_cost, expense_type, expense_date)
			st.success("Added expense \"{}\" ✅".format(expense))
			st.snow()
		else:
			st.error('This is an error', icon="🚨")

	with col5:
		list_of_savings = [i[0] for i in view_all_savings_names()]
	if st.button("Add Savings"):
		if (expense != '') and (expense not in list_of_expenses):
			add_data3(expense, expense_cost, expense_type, expense_date)
			st.success("Added expense \"{}\" ✅".format(expense))
			st.snow()
		else:
			st.error('This is an error', icon="🚨")

	with st.expander("View Food or Outside_Expenditure Data 💫"):
		result = view_all_data2()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))
	with st.expander("View Bill Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))
	with st.expander("View Savings Data 💫"):
		result = view_all_data3()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

elif choice == "Update Expense 👨‍💻":
	st.subheader("Edit Items")
	with st.expander("Current Data"):
		result = view_all_data()
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))
	which_expense = st.selectbox("Which Expense?", ['Food or Outside_Expenditure', 'Bill', 'Savings'])
	if which_expense == 'Food or Outside_Expenditure':
		list_of_expenses2 = [i[0] for i in view_all_expense_names2()]
		selected_expense2 = st.selectbox("Expense Food or Outside_Expenditure", list_of_expenses2)
		expense_result2 = get_expense2(selected_expense2)
		expense = expense_result2[0][0]
		expense_cost = expense_result2[0][1]
		expense_type = expense_result2[0][2]
		expense_date = expense_result2[0][3]

	elif which_expense == 'Bill':
		list_of_expenses = [i[0] for i in view_all_expense_names()]
		selected_expense = st.selectbox("Expense Bills", list_of_expenses)
		expense_result = get_expense(selected_expense)

		expense = expense_result[0][0]
		expense_cost = expense_result[0][1]
		expense_type = expense_result[0][2]
		expense_date = expense_result[0][3]

	else:
		list_of_savings = [i[0] for i in view_all_savings_names()]
		selected_savings = st.selectbox("Expense Bills", list_of_savings)
		expense_result3 = get_savings(selected_savings)

		expense = expense_result3[0][0]
		expense_cost = expense_result3[0][1]
		expense_type = expense_result3[0][2]
		expense_date = expense_result3[0][3]

	col1, col2 = st.columns(2)

	with col1:
		new_expense = st.text_area("Expense Rename", expense)

		new_expense_cost = st.number_input("Expense Cost", expense_cost)

		expense_list = ["Bill", "Food", "Outside_Expenditure", "Savings"]
		new_ex = [i for i, j in enumerate(expense_list) if j == expense_type]
		new_expense_type = st.selectbox('Expense Type', ["Bill", "Food", "Outside_Expenditure", "Savings"], index=new_ex[0])

	with col2:

		expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()
		new_expense_date = st.date_input("Date", expense_date)

	col3, col4, col5 = st.columns(3)

	with col3:
		if st.button("Update Food or Outside_Expenditure Expense 👨‍💻"):

			edit_expense_data2(new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date)
			st.success("Updated expense \"{}\" ✅".format(expense, new_expense))

	with col4:
		if st.button("Update Bill Expense 👨‍💻"):

			edit_expense_data(new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date)
			st.success("Updated expense \"{}\" ✅".format(expense, new_expense))

	with col5:
		if st.button("Update Savings 👨‍💻"):
			edit_save_data(new_expense, new_expense_cost, new_expense_type, new_expense_date, expense, expense_cost, expense_type, expense_date)
			st.success("Updated expense \"{}\" ✅".format(expense, new_expense))

	with st.expander("View Food or Outside_Expenditure Data 💫"):
		result = view_all_data2()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))
	with st.expander("View Bill Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

	with st.expander("View Savings Data 💫"):
		result = view_all_data3()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

elif choice == "Delete Expense ❌":
	st.subheader("Delete")
	with st.expander("View Data"):
		col1, col2, col3 = st.columns(3)

		with col1:
			st.write("Food or Outside_Expenditure")
			result = view_all_data2()
		# st.write(result)
			clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
			st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

		with col2:
			st.write("Bills")
			result = view_all_data()
		# st.write(result)
			clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
			st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

		with col3:
			st.write("Saving")
			result = view_all_data3()
		# st.write(result)
			clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
			st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

	with st.expander("Delete by"):
		col1, col2, col3 = st.columns(3)

		with col1:
			st.write("Food or Outside_Expenditure")
			unique_list1 = [i[0] for i in view_all_date_names2()]

			delete_by_expense_month = st.selectbox("Select Month", unique_list1)
			if st.button("Delete by Month ❌"):
				delete_data_month(delete_by_expense_month)
				st.warning("Deleted Month \"{}\" ✅".format(delete_by_expense_month))

			unique_list = [i[0] for i in view_all_expense_names2()]

			delete_by_expense_name = st.selectbox("Select Food or Outside_Expenditure Expense", unique_list)
			if st.button("Delete by Food or Outside_Expenditure expense ❌"):
				delete_data_expense2(delete_by_expense_name)
				st.warning("Deleted expense \"{}\" ✅".format(delete_by_expense_name))

		with col2:
			st.write("Bills")
			unique_list1 = [i[0] for i in view_all_date_names()]

			delete_by_expense_date = st.selectbox("Select Date", unique_list1)
			if st.button("Delete by Date ❌"):
				delete_data_date(delete_by_expense_date)
				st.warning("Deleted Date \"{}\" ✅".format(delete_by_expense_date))

			unique_list = [i[0] for i in view_all_expense_names()]

			delete_by_expense_name = st.selectbox("Select Bills Expense", unique_list)
			if st.button("Delete by Bills expense ❌"):
				delete_data_expense(delete_by_expense_name)
				st.warning("Deleted expense \"{}\" ✅".format(delete_by_expense_name))

		with col3:
			st.write("Savings")
			unique_list1 = [i[0] for i in view_all_date_names3()]

			delete_by_savings_month = st.selectbox("Select Month for Savings", unique_list1)
			if st.button("Delete by Month for Savings❌"):
				delete_data_month2(delete_by_savings_month)
				st.warning("Deleted Month \"{}\" ✅".format(delete_by_savings_month))

			unique_list = [i[0] for i in view_all_savings_names()]

			delete_by_savings_name = st.selectbox("Select Food or Outside_Expenditure Expense or Savings", unique_list)
			if st.button("Delete by Savings ❌"):
				delete_data_expense3(delete_by_savings_name)
				st.warning("Deleted expense \"{}\" ✅".format(delete_by_savings_name))

	with st.expander("View Food or Outside_Expenditure Data 💫"):
		result = view_all_data2()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))
	with st.expander("View Bill Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))
	with st.expander("View Savings Data 💫"):
		result = view_all_data3()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

else:

	result3 = view_all_data3()
	clean_df3 = pd.DataFrame(result3, columns=["Expense", "Cost", "Type", "Date"])
	result2 = view_all_data2()
	clean_df2 = pd.DataFrame(result2, columns=["Expense", "Cost", "Type", "Date"])
	result = view_all_data()
	clean_df = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])

	today = datetime.today()
	last_day = last_day_of_month(today)

	close_to_end_of_month = last_day-timedelta(days=3)

	first_day = datetime.strptime(first_day, '%Y-%m-%d').date()

	clean_df3['Date'] = pd.to_datetime(clean_df3['Date'])
	clean_df3 = clean_df3[(clean_df3['Date'].dt.date >= first_day) & (clean_df3['Date'].dt.date < last_day.date())]

	clean_df2['Date'] = pd.to_datetime(clean_df2['Date'])
	clean_df2 = clean_df2[(clean_df2['Date'].dt.date >= first_day) & (clean_df2['Date'].dt.date < last_day.date())]

	clean_df['Date'] = pd.to_datetime(clean_df['Date'])
	clean_df = clean_df[(clean_df['Date'].dt.date >= first_day) & (clean_df['Date'].dt.date < last_day.date())]

	new_row1 = {"Expense": "outside_expenditure", "Cost": sum(clean_df2[clean_df2['Type'] == 'Outside_Expenditure']['Cost']), "Type": "Food", "Date": ''}
	clean_df.loc[len(clean_df)] = new_row1

	clean_df_food = clean_df2[clean_df2['Type'] == 'Food']
	with st.expander("View All 📝"):
		col1, col2 = st.columns(2)

		with col1:
			st.write("Food")

			st.dataframe(clean_df_food.style.applymap(color_df, subset=['Type']))

		with col2:
			st.write("Bills")
			st.dataframe(clean_df.style.applymap(color_df, subset=['Type']))

	with st.expander("Expense Monthly/Weekly Score 🏆"):

		food_budget_per_month = 217
		food_budget_per_week = 52
		outside_expenditure = 100
		percentage_month = sum(clean_df2['Cost'])/217

		st.subheader('Outside_Expenditure per Month Breakdown')
		clean_df_outside = clean_df2[clean_df2['Type'] == 'Outside_Expenditure']

		if len(clean_df_outside) == 0:
			outside_spend = 0
			st.write(f'<p style="font-size:40px; text-align: center; color:green;">SUCCESS keep, consistent, £{100}!!!</p>', unsafe_allow_html=True)

		else:

			outside_spend = sum(clean_df_outside['Cost'])
			percentage_outside = outside_spend/outside_expenditure
			outside_saved = outside_expenditure-outside_spend

			if percentage_outside < 0.5:
				st.write(f'<p style="font-size:40px; text-align: center; color:yellow;">SUCCESS keep, consistent!!! {percentage_outside:.0%} SPENT, £{round(outside_saved, 2)} saved </p>', unsafe_allow_html=True)

			elif percentage_outside > 0.5:
				st.write(f'<p style="font-size:40px; text-align: center; color:red;">You FAILED, do better next time!!! {percentage_outside:.0%} SPENT, £{round(outside_saved, 2)} saved </p>', unsafe_allow_html=True)

		if today.date() == close_to_end_of_month.date():
			st.subheader('Monthly Breakdown')
			if percentage_month < 1:
				st.write(f'<p style="font-size:40px; text-align: center; color:green;">SUCCESS keep, consistent!!! {percentage_month:.0%}</p>', unsafe_allow_html=True)

			elif percentage_month > 1:
				st.write(f'<p style="font-size:40px; text-align: center; color:red;">You FAILED, do better next time!!! {percentage_month:.0%}</p>', unsafe_allow_html=True)

		beginning_of_week, end_of_week = week_magic(today)

		clean_df_food = clean_df2[clean_df2['Type'] == 'Food']
		st.write(clean_df_food)
		clean_df_week = clean_df_food[(clean_df_food['Date'].dt.date >= beginning_of_week.date()) & (clean_df_food['Date'].dt.date <= end_of_week.date())]

		amount_spent = sum(clean_df_week['Cost'])
		saved = 52 - sum(clean_df_week['Cost'])
		percentage_week = sum(clean_df_week['Cost'])/52

		if (today.date() <= end_of_week.date()) and (today.date() >= beginning_of_week.date()):
			st.subheader('Weekly Breakdown')
			if percentage_week < 1:
				st.write(f'<p style="font-size:40px; text-align: center; color:green;">£ {round(amount_spent,2)} spent, SUCCESS keep, consistent!!! {percentage_week:.0%} SPENT, £{round(saved, 2)} saved </p>', unsafe_allow_html=True)

			elif percentage_week > 1:
				st.write(f'<p style="font-size:40px; text-align: center; color:red;">£ {round(amount_spent,2)} spent, You FAILED, do better next time!!! {percentage_week:.0%} SPENT, nothing saved</p>', unsafe_allow_html=True)

			else:
				st.write('something')

		if today.date() == end_of_week.date():

			w = week_of_month(today.date())
			expense = f'week{w}'
			expense_cost = saved
			expense_type = 'Saving'
			expense_date = today.date()
			add_data3(expense, expense_cost, expense_type, expense_date)

	with st.expander("Expense Food or Outside_Expenditure Charts 📝"):
		clean_df2 = clean_df2[clean_df2['Type'] == 'Food']
		st.dataframe(clean_df2)

		food_spend = sum(clean_df2['Cost'])

		percentage_month_food = food_spend/217
		if food_spend <= 217:
			p1 = px.pie(clean_df_food, names='Expense', values='Cost')
			st.plotly_chart(p1, use_container_width=True)

			if today.date() == last_day:
				st.write(f'<p style="font-size:40px; text-align: center; color:red;">SUCCESS, £{food_spend} spent, that"s {percentage_month_food}% !!! </p>', unsafe_allow_html=True)

		else:
			st.write('<p style="font-size:40px; text-align: center; color:red;">You FAILED, do better next time!!! </p>', unsafe_allow_html=True)

	if sum(clean_df2['Cost']) <= 217:
		new_row = {"Expense": "groceries", "Cost": 217, "Type": "Food", "Date": ''}
		clean_df.loc[len(clean_df)] = new_row
	elif sum(clean_df2['Cost']) > 217:
		new_row = {"Expense": "groceries", "Cost": sum(clean_df2['Cost']), "Type": "Food", "Date": ''}
		clean_df.loc[len(clean_df)] = new_row

	with st.expander("Full Expense Breakdown Charts 📝"):

		st.dataframe(clean_df)
		# sum groceries create new row make new pie
		p1 = px.pie(clean_df, names='Expense', values='Cost')
		st.plotly_chart(p1, use_container_width=True)
	with st.expander("Expense Total Score 🏆"):
		income = 2042
		st.dataframe(clean_df)

		total_spent = sum(clean_df['Cost'])
		saved_this_month = income - total_spent

		total_percentage_month = total_spent/income

		if total_percentage_month < 1:
			st.write(f'<p style="font-size:40px; text-align: center; color:green;">SUCCESS keep, consistent!!! {total_percentage_month:.0%} SPENT, £{round(saved_this_month, 2)} saved </p>', unsafe_allow_html=True)

		elif total_percentage_month > 1:
			st.write(f'<p style="font-size:40px; text-align: center; color:red;">You FAILED, do better next time!!! {total_percentage_month:.0%} SPENT, nothing saved</p>', unsafe_allow_html=True)

	with st.expander("View Savings Data 💫"):
		result = view_all_data3()
		# st.write(result)
		clean_df3 = pd.DataFrame(result, columns=["Expense", "Cost", "Type", "Date"])
		st.dataframe(clean_df3.style.applymap(color_df, subset=['Type']))

	with open("data.db", "rb") as fp:
		btn = st.download_button(
			label="Download db file",
			data=fp,
			file_name="data.db",
			mime="application/octet-stream"
		)
