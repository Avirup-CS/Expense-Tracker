import sys
import json
import datetime
import os

class Expense:

    def __init__(self, expenseList=None):
        if expenseList is None:
            self.expenseList = {}
        else:
            self.expenseList = expenseList
        self.dayCost = 0

    #load the data from the json file
    def load_expenses(self):
        
            def is_file_empty(file_path):
                # Checks if a file is empty based on its size
                return os.path.getsize(file_path) == 0

            checkFile = is_file_empty('expense.json')
            if checkFile:
                print("No expense record found!!")
            else:
                try:
                    with open('expense.json','r') as file:
                        print(f"------------------------------------------------------\nStatus: Data is Loaded successfully!!\n------------------------------------------------------")
                        self.expenseList =  json.load(file)
                except FileNotFoundError as e:
                    return {}


    # add an expense with a date
    def addExpense(self):

        # add an expense with a date
        while True:
            try:
                date = input("Enter the date (dd-mm-yyyy): ")
                datetime.datetime.strptime(date, '%d-%m-%Y')  # Validate date format
                break
            except ValueError as e:
                print("Invalid Date Format!!")

                                
        dic = {}

        while True:
            ch = input("Do you want to add items (Y/N): ").strip().upper()
                            
            categories = [
                "Education", "Food & Dining", "Transportation", "Travel", "Healthcare",
                "Entertainment", "Healthcare", "Housing", "Shopping", "Others"
            ]

            if ch == 'Y':
                print("\nThe Categories of Expenses:")
                for val in range(len(categories)):
                    print(f"{val+1}. {categories[val]}")
                print()
                                
                try:
                    expenseTypeName = int(input("Enter the Expense Category: "))
                    itemName = input("Enter the Description: ").strip()
                    itemPrice = float(input("Enter the Amount Spent: ").strip())
                except (ValueError,TypeError):
                    print("\nStatus: Invalid Choice Or Wrong Data Entered!!")
                    continue

                if categories[expenseTypeName-1] not in dic:
                    dic[categories[expenseTypeName-1]] = []


                dic[categories[expenseTypeName-1]].append(itemName)
                dic[categories[expenseTypeName-1]].append(itemPrice)

                print(f"------------------------------------------------------\nStatus: The Expense on {date} is added successfully!\n------------------------------------------------------")

            elif ch == 'N':
                break
            else:
                print("\nInvalid input, please enter 'Y' or 'N'.")
                continue

        # If the date already exists in the dictionary
        if date in self.expenseList:
            for key, value in dic.items():
                    if key in self.expenseList[date]:
                        self.expenseList[date][key].extend(value)
                    else:
                        self.expenseList[date][key] = value
        else:
            self.expenseList.update({date:dic})

        # This line will print the expense data stored in json form
        # print(self.expenseList) 
                    


    # calculate category-wise expenses for each day
    def calculateExpensesCategorywise(self):
        
        for dates, expenses in self.expenseList.items():
            print(f"------------------------------------------------------\nDate: {dates}\n------------------------------------------------------")
            for item,pricelist in expenses.items():
                item_name = item
                sum = 0
                for price in range(1,len(pricelist),2):
                    sum += pricelist[price]
                print(f"\nTotal Amount Spent on {item_name}: Rs. {sum}")


    # calculate total expense cost of a day
    def calculateTotalExpensesADay(self):
        while True:
            try:
                inp_date = input("\nEnter the date that you want to view total amount spent: ")
                datetime.datetime.strptime(inp_date, '%d-%m-%Y')  # Validate date format
                break
            except ValueError as e:
                print("Invalid Date Format!!")

        for dates, expenses in self.expenseList.items():
            if(dates == inp_date):
                sum = 0
                for pricelist in expenses.values():
                    for price in range(1,len(pricelist),2):
                        sum += pricelist[price]
                print(f"\nTotal Amount Spent: Rs. {sum}")
                break
        else:
            print(f"No Expenses found for the date: {inp_date} !!")


    # display total expenses category-wise including items by date
    def displayAllExpensesTillNow(self):
        for dates, expenses in self.expenseList.items():
            print(f"------------------------------------------------------\nDate: {dates}\n------------------------------------------------------")
            for category,pricelist in expenses.items():
                print(f"\nExpense Category: {category}\n")
                for item_Name_Price in range(len(pricelist)):
                    if(item_Name_Price % 2 == 0):
                        print(pricelist[item_Name_Price],end=" --> ")
                    else:
                        print(f"Rs. {pricelist[item_Name_Price]}\n")
                print("---------------------------")


    # delete all expenses of a day
    def deleteExpensesOfADay(self):
        while True:
            try:
                delete_date = input("Enter the date that you want to delete expenses: ")
                datetime.datetime.strptime(delete_date, '%d-%m-%Y')  # Validate date format
                break
            except ValueError as e:
                print("Invalid Date Format !!")

        if delete_date not in self.expenseList.keys():
            print(f"No Expenses found for the date: {delete_date}. So expenses can't be deleted!!")
        else:
            del self.expenseList[delete_date]
            print(f"------------------------------------------------------\nStatus: The Expenses on {delete_date} is deleted successfully!!\n------------------------------------------------------")


    # calculate the monthly expenses
    def mothlyExpenses(self):
        month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

        summary = {}
        for date, expenses in self.expenseList.items():
            month, year = date.split('-')[1:] #Extract month and year
            month_num = int(month)
            month_name = month_dict[month_num]
            year = int(year)

            if(month_name, year) not in summary:
                summary[(month_name, year)] = {}
            
            for category, items in expenses.items():
                if category not in summary[(month_name, year)]:
                    summary[(month_name, year)][category] = 0

                for i in range(1, len(items), 2):
                    summary[(month_name, year)][category] += items[i]

        sorted_summary = sorted(summary.items(), key=lambda x: (x[0][1], x[0][0]))

        for month_year, expense_data in sorted_summary:
            month, year = month_year
            allExpenseMonthTotal = 0
            print("------------------------------------------------------")
            print(f"\n{month} - {year}")
            for category, total in expense_data.items():
                allExpenseMonthTotal += total
                print(f"\nTotal Amount Spent on {category}: Rs. {total}")
            print("------------------------------------------------------")
    
            print(f"\nTotal Amount Spent on {month} - {year} is: Rs. {allExpenseMonthTotal}")


    def saveData(self):
        # save the data into the json file
        try:
            with open('expense.json','w') as file:
                    json.dump(self.expenseList, file)

            print(f"------------------------------------------------------\nStatus: Data Saved Successfully!!\n------------------------------------------------------")

        except FileNotFoundError as e:
                return {}
        

# This is the Menu Section
et = Expense()

while(True):
    
    def display_menu():
        print("\n======================================================\nWelcome to the Expense Tracker!")
        print("======================================================")
        print("\nExpense Tracker Menu:")
        print("1. Add an Expense")
        print("2. View Expenses by Category")
        print("3. View Total Expenses for a Day")
        print("4. View All Expenses By Date")
        print("5. Delete an Expense")
        print("6. View Monthly Expenses")
        print("7. Load Data From File")
        print("8. Save Data into File")
        print("9. Exit")
        print("======================================================")
        
        choice = input("Enter Your Choice: ")
        return choice

    user_choice = display_menu()

    match user_choice:
        case '1': 
            et.addExpense()

        case '2': 
            et.calculateExpensesCategorywise()

        case '3': 
            et.calculateTotalExpensesADay()
            
        case '4':
            et.displayAllExpensesTillNow()

        case '5':
            et.deleteExpensesOfADay()

        case '6':
            et.mothlyExpenses()

        case '7': 
            et.load_expenses()

        case '8':
            et.saveData()

        case '9':
            sys.exit()

        case _:
             print("Invalid choice!! Please enter a number between 1 and 8.\n")
        