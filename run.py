import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")    

        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("data is valid")
            break

    return sales_data            


def validate_data(values):

    """
    converts all values to intergers
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:     
        print(f"invalid data {e} please try again.\n")  
        return False

    return True   
 

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    (f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):    
    """
    calulates the data from the stack and data from the sales 
    to add together to add to
    the surplus tab. this tells the user how many sanwiches 
    they need to make for the next day 
    """
    print("calculating surplus data.....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data  


def get_last_5_entries_sales():
    """
    gathring the data from the last 5 entires of the sales worksheet
        """    
    sales = SHEET.worksheet("sales")
    
    colums = []
    for ind in range(1, 7):
        colum = sales.col_values(ind)
        colums.append(colum[-5:])

    return colums  


def calculate_stock_data(data):
    """
    calculate the new stock by creating an avarage from the last 5 numbers 
    from each 
    sales colum 
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data    


def main():
    """
    run all program fucntions
    """
    data = get_sales_data()   
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_colums = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_colums)
    update_worksheet(stock_data, "stock")

    
print("Welcome to Love Sandwiches data automation")
main()




