import streamlit as st
import pandas as pd
from datetime import date
import sys

# File path for storing the expense data
FILE_PATH = "expense_data.csv"

# Function to load expense data from CSV file
def load_data():
    try:
        df = pd.read_csv(FILE_PATH)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Goods', 'Price', 'Date', 'Expense Type'])
    return df

# Function to save expense data to CSV file
def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# Main Streamlit app
def main():
    st.title('Expense Tracker')

    options = [
        'Add Groceries Expense',
        'Add Home Rent Expense',
        'Add Transportation Expense',
        'Show Report',
        'Delete Expense',
        'Exit'
    ]
    option = st.sidebar.selectbox('Select an option', options)

    if option == 'Add Groceries Expense':
        add_expense_form('Groceries')
    elif option == 'Add Home Rent Expense':
        add_expense_form('Home Rent')
    elif option == 'Add Transportation Expense':
        add_expense_form('Transportation')
    elif option == 'Show Report':
        show_report()
    elif option == 'Delete Expense':
        delete_expense()
    elif option == 'Exit':
        sys.exit()

# Function to create the form for adding expenses
def add_expense_form(expense_type):
    st.subheader(f'Add {expense_type} Expense')

    goods = st.text_input('Enter the goods for the expense type', key=f'goods_{expense_type}')
    price = st.number_input('Enter the price for goods', step=1, min_value=0, key=f'price_{expense_type}')

    if st.button('Add Expense'):
        today = date.today()
        add_expense(goods, price, today, expense_type)
        st.success('Expense added successfully!')

# Function to show the expense report
def show_report():
    st.subheader('Expense Report')
    df = load_data()
    st.dataframe(df)

# Function to add expense details to the DataFrame and save to CSV file
def add_expense(goods, price, date, expense_type):
    df = load_data()
    new_row = pd.DataFrame([[goods, price, date, expense_type]], columns=['Goods', 'Price', 'Date', 'Expense Type'])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

# Function to delete expense
def delete_expense():
    st.subheader('Delete Expense')
    df = load_data()

    if df.empty:
        st.warning("No expenses to delete.")
        return

    # Display with index so user knows which row to delete
    st.dataframe(df)

    # Select row by index
    index_to_delete = st.number_input('Enter the index of the expense to delete', min_value=0, max_value=len(df)-1, step=1)

    if st.button('Delete Selected Expense'):
        df = df.drop(index=index_to_delete).reset_index(drop=True)
        save_data(df)
        st.success('Expense deleted successfully!')
        st.dataframe(df)

# Run the app
if __name__ == '__main__':
    main()
