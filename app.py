from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from decimal import Decimal

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",       # or your server IP
    user="root",
    password="Mitochondria@098",
    database="bankmanagement"
)

# Create a cursor to execute queries
cursor = conn.cursor()

def select(table_name,order='*',filter='*'):
    if order!='*':
        if filter!='*':
            cursor.execute(f"select * from {table_name} order by {order} where {filter}")
        else:
            cursor.execute(f"select * from {table_name} order by {order}")
    elif filter!='*':
        if order!='*':
            cursor.execute(f"select * from {table_name} order by {order} where {filter}")
        else:
            cursor.execute(f"select * from {table_name} where {filter}")
    else:
        cursor.execute(f"select * from {table_name}")
    row=cursor.fetchall()
    return row

app = Flask(__name__)
app.secret_key = 'bank_management_secret_key'  # Required for flashing messages

# to calculate information being showed on the main dashboard page
def calculate_dashboard_stats():
    # Get data from all tables
    banks = init_banks_db()
    branches = init_branches_db()
    customers = init_customers_db()
    accounts = init_accounts_db()
    employees = init_employee_db()
    payments = init_payments_db()
    
    # Calculate stats
    stats = {
        'total_banks': len(banks),
        'total_branches': len(branches),
        'total_customers': len(customers),
        'total_accounts': len(accounts),
        'total_employees': len(employees),
        'total_transactions': sum(payment['Payment_Amount'] for payment in payments) / 100000  # Convert to Lakhs
    }
    return stats

# Initialize sample data for banks.html (replace with actual db tables data)
def init_banks_db():
    # This would typically be replaced with database operations
    global banks_data
    return banks_data

# Storage for banks (simulating a database)
data_bank=select("bank")
banks_data = [
    {
        'Bank_Code': bank[0],
        'Bank_Name': bank[1],
        'Address': bank[2],
        'City': bank[3]
    }
    for bank in data_bank
]

# Initialize sample data for employees.html (replace with actual db tables data)
def init_employee_db():
    # This would typically be replaced with database operations
    global employees_data
    return employees_data

# Storage for employees (simulating a database)
data_emp=select('employee')
employees_data = [
    {
        'Emp_ID': e[0],
        'Emp_Name': e[1],
        'Mobile_No': e[2],
        'Address': e[3],
        'Bank_Code': e[4]
    }
    for e in data_emp
]

# Initialize sample data for customers.html (replace with actual db tables data)
def init_customers_db():
    # This would typically be replaced with database operations
    global customers_data
    return customers_data

# Define global variable for customers_data
data_cust=select('customer')
customers_data = [
    {
        'Cust_ID': c[0],
        'F_Name': c[1],
        'L_Name': c[2],
        'Mobile_No': c[3],
        'E_Mail': c[4],
        'Address': c[5]
    }
    for c in data_cust
]

# Initialize sample data for transactions.html (replace with actual db tables data)
def init_payments_db():
    data_pay=select('payment')
    sample_payments = [
        {
            'Payment_No': c[0],
            'Payment_Date': c[1],
            'Payment_Amount': c[2]
        }
        for c in data_pay
    ]
    return sample_payments

# Initialize sample data for loans.html (replace with actual db tables data)

def init_loans_db():
    # Using customer IDs from the customers sample data for reference
    global loans_data
    return loans_data
#prudhvi

data_loan=select('loan')
loans_data = []

for loan in data_loan:
    # Find the customer matching the loan's Cust_ID
    customer = next(c for c in data_cust if c[0] == loan[2])  # match by Cust_ID
    loans_data.append({
        'Loan_No': loan[0],
        'Amount': float(loan[1]),  # Convert Decimal to float
        'Cust_ID': loan[2],
        'Customer_Name': f"{customer[1]} {customer[2]}"  # Full name from First + Last name
    })



# Initialize sample data for accounts.html (replace with actual db tables data)
def init_accounts_db():
    # This would typically be replaced with database operations
    global accounts_data
    return accounts_data

data_acc=select('account')
accounts_data = [
    {
        'Account_No': c[0],
        'balance': c[1],
        'Cust_ID': c[2]
    }
    for c in data_acc
]
   

# Initialize sample data for branches.html (replace with actual db tables data)
def init_branches_db():
    # This would typically be replaced with database operations
    global branches_data
    return branches_data

# Storage for branches (simulating a database)
# Define global variable for customers_data
data_branch=select('branch')
branches_data = [
    {
        'Branch_Code': c[0],
        'Branch_Name': c[1],
        'Address': c[2],
        'Bank_Code': c[3]
    }
    for c in data_branch
]


# Initialize sample data for account_types.html (replace with actual db tables data)
def init_account_types_db():
    data_a_t=select('account_types')
    sample_account_types = [
        {
            'Account_No': c[0],
            'Type': c[1]
        }
        for c in data_a_t
    ]
    return sample_account_types

## Initialize sample data for loan_payments.html (replace with actual db tables data)
def init_loan_payments_db():
    # Creating sample data that references the loans from init_loans_db()
    data_l_p=select('loan_payment')
    sample_loan_payments = []

    for loan in data_l_p:
        # Find the customer matching the loan's Cust_ID
        l=next(l for l in data_loan if l[0]==loan[0])
        customer = next(c for c in data_cust if c[0] == l[2])  # match by Cust_ID
        sample_loan_payments.append({
            'Loan_No': loan[0],
            'Payment_No': loan[1],  # Convert Decimal to float
            'Loan_Amount': l[1],
            'Customer_Name': f"{customer[1]} {customer[2]}"  # Full name from First + Last name
        })
    
    return sample_loan_payments


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    stats = calculate_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/banks')
def banks():
    return render_template('banks.html', banks=init_banks_db())

# route for adding a bank
@app.route('/add_bank', methods=['POST'])
def add_bank():
    global banks_data
    if request.method == 'POST':
        # Getting form data
        new_bank = {
            'Bank_Code': int(request.form['Bank_Code']),
            'Bank_Name': request.form['Bank_Name'],
            'Address': request.form['Address'],
            'City': request.form['City']
        }
        
        # Checking if all required fields are filled
        if not new_bank['Bank_Name'] or not new_bank['Address'] or not new_bank['City'] or not new_bank['Bank_Code']:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('banks'))
        
        # Checking if bank code already exists
        for bank in banks_data:
            if bank['Bank_Code'] == new_bank['Bank_Code']:
                flash('Bank code already exists', 'error')
                return redirect(url_for('banks'))
        
        # Insert the new bank into the database with parameterized queries
        try:
            cursor.execute("""
                INSERT INTO bank (Bank_Code, Bank_Name, Address, City)
                VALUES (%s, %s, %s, %s)
            """, (new_bank['Bank_Code'], new_bank['Bank_Name'], new_bank['Address'], new_bank['City']))
            conn.commit()  # Commit the transaction
            banks_data.append(new_bank)

            flash('Bank added successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('banks'))


# New route for updating a bank
@app.route('/update_bank', methods=['POST'])
def update_bank():
    global banks_data
    if request.method == 'POST':
        bank_code = int(request.form['Bank_Code'])
        bank_name = request.form['Bank_Name']
        address = request.form['Address']
        city = request.form['City']

        if not bank_name or not address or not city or not bank_code:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('banks'))
        
        # Checking if bank code already exists
        c=0
        for bank in banks_data:
            if bank['Bank_Code'] == bank_code:
                c+=1
        if c==0:
            flash('Bank code does not exists', 'error')
            return redirect(url_for('banks'))
        try:
            # Execute the update query with parameterized values
            cursor.execute("""
                UPDATE bank 
                SET Bank_Name = %s, Address = %s, City = %s 
                WHERE Bank_Code = %s
            """, (bank_name, address, city, bank_code))
            conn.commit()  # Commit the transaction

            # Update the bank data in the local list
            for bank in banks_data:
                if bank['Bank_Code'] == bank_code:
                    bank['Bank_Name'] = bank_name
                    bank['Address'] = address
                    bank['City'] = city
                    break

            flash('Bank updated successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('banks'))


# New route for deleting a bank
@app.route('/delete_bank', methods=['POST'])
def delete_bank():
    global banks_data
    if request.method == 'POST':
        bank_code = int(request.form['Bank_Code'])
        try:
            cursor.execute("""
                delete from bank WHERE Bank_Code = %s
            """, (bank_code,))
            conn.commit()  # Commit the transaction
            banks_data = [bank for bank in banks_data if bank['Bank_Code'] != bank_code]

        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        flash('Bank deleted successfully', 'success')
        return redirect(url_for('banks'))

@app.route('/branches')
def branches():
    return render_template('branches.html', branches=init_branches_db())

# Route for adding a branch
@app.route('/add_branch', methods=['POST'])
def add_branch():
    global branches_data
    if request.method == 'POST':
        new_branch = {
            'Branch_Code': int(request.form['Branch_Code']),
            'Branch_Name': request.form['Branch_Name'],
            'Address': request.form['Address'],
            'Bank_Code': int(request.form['Bank_Code'])
        }
        # Checking if all required fields are filled
        
        if not new_branch['Branch_Code'] or not new_branch['Address'] or not new_branch['Branch_Name'] or not new_branch['Bank_Code']:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('branches'))
        
        # Checking if bank code already exists
        for branch in branches_data:
            if branch['Branch_Code'] == new_branch['Branch_Code']:
                flash('Branch code already exists', 'error')
                return redirect(url_for('branches'))
        
        # Insert the new bank into the database with parameterized queries
        try:
            cursor.execute("""
                INSERT INTO branch (Branch_Code, Branch_Name, Address, Bank_Code)
                VALUES (%s, %s, %s, %s)
            """, (new_branch['Branch_Code'], new_branch['Branch_Name'], new_branch['Address'], new_branch['Bank_Code'],))
            conn.commit()  # Commit the transaction
            branches_data.append(new_branch)

            flash('Branch added successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('branches'))

# Route for updating a branch
@app.route('/update_branch', methods=['POST'])
def update_branch():
    global branches_data
    if request.method == 'POST':
        branch_code = int(request.form['Branch_Code'])
        branch_name = request.form['Branch_Name']
        address = request.form['Address']
        bank_code = int(request.form['Bank_Code'])
        
        if not branch_code or not address or not branch_name or not bank_code:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('branches'))
        
        # Checking if bank code already exists
        c=0
        for branch in branches_data:
            if branch['Branch_Code'] == branch_code:
                c+=1
        if c==0:
            flash('Branch code does not exists', 'error')
            return redirect(url_for('branches'))
        try:
            # Execute the update query with parameterized values
            cursor.execute("""
                UPDATE branch 
                SET branch_name = %s, Address = %s, bank_code = %s 
                WHERE branch_code = %s
            """, (branch_name, address, bank_code,branch_code))
            conn.commit()  # Commit the transaction

            # Update the bank data in the local list
            for branch in branches_data:
                if branch['Branch_Code'] == branch_code:
                    branch['Branch_Name'] = branch_name
                    branch['Address'] = address
                    branch['Bank_Code'] = bank_code
                    break

            flash('Branch updated successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')
                
        return redirect(url_for('branches'))

# Route for deleting a branch
@app.route('/delete_branch', methods=['POST'])
def delete_branch():
    global branches_data
    if request.method == 'POST':
        branch_code = int(request.form['Branch_Code'])
        
        try:
            cursor.execute("""
                delete from branch WHERE Branch_Code = %s
            """, (branch_code,))
            conn.commit()  # Commit the transaction
            branches_data = [branch for branch in branches_data if branch['Branch_Code'] != branch_code]
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')
        # Find the branch with the given code and remove it
        
        flash('Branch deleted successfully', 'success')
        return redirect(url_for('branches'))

@app.route('/employees')
def employees():
    return render_template('employees.html', employees=init_employee_db())

# Route for adding an employee
@app.route('/add_employee', methods=['POST'])
def add_employee():
    global employees_data
    if request.method == 'POST':
        new_employee = {
            'Emp_ID': int(request.form['Emp_ID']),
            'Emp_Name': request.form['Emp_Name'],
            'Mobile_No': request.form['Mobile_No'],
            'Address': request.form['Address'],
            'Bank_Code': int(request.form['Bank_Code'])
        }
        if not new_employee['Emp_ID'] or not new_employee['Emp_Name'] or not new_employee['Mobile_No'] or not new_employee['Address'] or not new_employee['Bank_Code']:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('employees'))
        # Check if employee ID already exists
        for employee in employees_data:
            if employee['Emp_ID'] == new_employee['Emp_ID']:
                flash('Employee ID already exists', 'error')
                return redirect(url_for('employees'))
        c=0
        for bank in banks_data:
            if bank['Bank_Code'] == new_employee['Bank_Code']:
                c+=1
        if c==0:
            flash('Bank code does not exists', 'error')
            return redirect(url_for('employees'))
        
        try:
            cursor.execute("""
                INSERT INTO employee (Emp_ID, Emp_Name, Mobile_No, Address, Bank_Code)
                VALUES (%s, %s, %s, %s, %s)
            """, (new_employee['Emp_ID'], new_employee['Emp_Name'], new_employee['Mobile_No'], new_employee['Address'], new_employee['Bank_Code']))
            conn.commit()  # Commit the transaction

            # Add the new employee to the in-memory list (if applicable)
            employees_data.append(new_employee)

            flash('Employee added successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('employees'))

# Route for updating an employee
@app.route('/update_employee', methods=['POST'])
def update_employee():
    global employees_data
    if request.method == 'POST':
        emp_id = int(request.form['Emp_ID'])
        emp_name = request.form['Emp_Name']
        mobile_no = request.form['Mobile_No']
        address = request.form['Address']
        bank_code = int(request.form['Bank_Code'])
        
        # Checking if all required fields are filled
        if not emp_id or not emp_name or not mobile_no or not address or not bank_code:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('employees'))
        
        # Checking if the employee exists
        cursor.execute("SELECT * FROM employee WHERE Emp_ID = %s", (emp_id,))
        existing_employee = cursor.fetchone()
        if not existing_employee:
            flash('Employee ID does not exist', 'error')
            return redirect(url_for('employees'))
        
        # Check if the bank code exists
        cursor.execute("SELECT * FROM bank WHERE Bank_Code = %s", (bank_code,))
        existing_bank = cursor.fetchone()
        if not existing_bank:
            flash('Invalid Bank Code', 'error')
            return redirect(url_for('employees'))

        # Execute the update query with parameterized values
        try:
            cursor.execute("""
                UPDATE employee 
                SET Emp_Name = %s, Mobile_No = %s, Address = %s, Bank_Code = %s 
                WHERE Emp_ID = %s
            """, (emp_name, mobile_no, address, bank_code, emp_id))
            conn.commit()  # Commit the transaction

            # Update the employee data in the local list
            for employee in employees_data:
                if employee['Emp_ID'] == emp_id:
                    employee['Emp_Name'] = emp_name
                    employee['Mobile_No'] = mobile_no
                    employee['Address'] = address
                    employee['Bank_Code'] = bank_code
                    break

            flash('Employee updated successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('employees'))


# Route for deleting an employee
@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    global employees_data
    if request.method == 'POST':
        emp_id = int(request.form['Emp_ID'])
        
        try:
            # Execute the delete query with parameterized values
            cursor.execute("DELETE FROM employee WHERE Emp_ID = %s", (emp_id,))
            conn.commit()  # Commit the transaction
            
            # Remove the employee from the local data list
            employees_data = [employee for employee in employees_data if employee['Emp_ID'] != emp_id]

            flash('Employee deleted successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('employees'))

@app.route('/customers')
def customers():
    return render_template('customers.html',customers=init_customers_db())

# Route for adding a customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    global customers_data
    if request.method == 'POST':
        new_customer = {
            'Cust_ID': int(request.form['Cust_ID']),
            'F_Name': request.form['F_Name'],
            'L_Name': request.form['L_Name'],
            'Mobile_No': request.form['Mobile_No'],
            'E_Mail': request.form['E_Mail'],
            'Address': request.form['Address']
        }

        if not new_customer['Cust_ID'] or not new_customer['F_Name'] or not new_customer['L_Name'] or not new_customer['Mobile_No'] or not new_customer['E_Mail'] or not new_customer['Address']:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('customers'))
        
        # Checking if customer ID already exists in the database
        cursor.execute("SELECT * FROM customer WHERE Cust_ID = %s", (new_customer['Cust_ID'],))
        existing_customer = cursor.fetchone()
        
        if existing_customer:
            flash('Customer ID already exists', 'error')
            return redirect(url_for('customers'))
        
        try:
            cursor.execute("""
                INSERT INTO customer (Cust_ID, F_Name, L_Name, Mobile_No, E_Mail, Address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (new_customer['Cust_ID'], new_customer['F_Name'], new_customer['L_Name'], new_customer['Mobile_No'], new_customer['E_Mail'], new_customer['Address']))
            conn.commit()  # Commit the transaction

            # Add the new customer to the local data list
            customers_data.append(new_customer)

            flash('Customer added successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('customers'))

# Route for updating a customer
@app.route('/update_customer', methods=['POST'])
def update_customer():
    global customers_data
    if request.method == 'POST':
        cust_id = int(request.form['Cust_ID'])
        f_name = request.form['F_Name']
        l_name = request.form['L_Name']
        mobile_no = request.form['Mobile_No']
        e_mail = request.form['E_Mail']
        address = request.form['Address']

        # Checking if all required fields are filled
        if not cust_id or not f_name or not l_name or not mobile_no or not e_mail or not address:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('customers'))

        # Checking if customer exists in the database
        cursor.execute("SELECT * FROM customer WHERE Cust_ID = %s", (cust_id,))
        existing_customer = cursor.fetchone()
        
        if not existing_customer:
            flash('Customer ID does not exist', 'error')
            return redirect(url_for('customers'))

        try:
            # Execute the update query with parameterized values
            cursor.execute("""
                UPDATE customer
                SET F_Name = %s, L_Name = %s, Mobile_No = %s, E_Mail = %s, Address = %s
                WHERE Cust_ID = %s
            """, (f_name, l_name, mobile_no, e_mail, address, cust_id))
            conn.commit()  # Commit the transaction

            # Update the customer data in the local list
            for customer in customers_data:
                if customer['Cust_ID'] == cust_id:
                    customer['F_Name'] = f_name
                    customer['L_Name'] = l_name
                    customer['Mobile_No'] = mobile_no
                    customer['E_Mail'] = e_mail
                    customer['Address'] = address
                    break

            flash('Customer updated successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('customers'))

# Route for deleting a customer
@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    global customers_data
    if request.method == 'POST':
        cust_id = int(request.form['Cust_ID'])
        
        try:
            # Execute the delete query with parameterized values
            cursor.execute("DELETE FROM customer WHERE Cust_ID = %s", (cust_id,))
            conn.commit()  # Commit the transaction

            # Remove the customer from the local data list
            customers_data = [customer for customer in customers_data if customer['Cust_ID'] != cust_id]

            flash('Customer deleted successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('customers'))

@app.route('/transactions')
def transactions():
    payments = init_payments_db()
    # Calculate summary metrics
    total_amount = sum(payment['Payment_Amount'] for payment in payments)
    latest_date = max(payment['Payment_Date'] for payment in payments)
    return render_template('transactions.html', payments=payments, total_amount=total_amount, latest_date=latest_date)

@app.route('/loans')
def loans():
    global loans_data
    # Calculate summary metrics
    total_amount = sum(loan['Amount'] for loan in loans_data)
    avg_amount = round(total_amount / len(loans_data), 2) if loans_data else 0
    return render_template('loans.html', loans=loans_data, total_amount=total_amount, avg_amount=avg_amount)

@app.route('/accounts')
def accounts():
    return render_template('accounts.html', accounts=init_accounts_db())

@app.route('/account_types')
def account_types():
    account_types_data = init_account_types_db()
    
    # Calculate summary metrics
    savings_count = sum(1 for account in account_types_data if account['Type'] == 'Savings_Account')
    current_count = sum(1 for account in account_types_data if account['Type'] == 'Current_Account')
    
    return render_template('account_types.html', 
                           account_types=account_types_data,
                           savings_count=savings_count,
                           current_count=current_count)

@app.route('/loan_payments')
def loan_payments():
    loan_payments_data = init_loan_payments_db()
    
    # Calculate summary metrics
    unique_loans = set(payment['Loan_No'] for payment in loan_payments_data)
    unique_loans_count = len(unique_loans)
    
    # Calculate average payments per loan
    if unique_loans_count > 0:
        avg_payments_per_loan = round(len(loan_payments_data) / unique_loans_count, 2)
    else:
        avg_payments_per_loan = 0
    
    return render_template('loan_payments.html', 
                          loan_payments=loan_payments_data,
                          unique_loans_count=unique_loans_count,
                          avg_payments_per_loan=avg_payments_per_loan)

# Route for adding a loan
@app.route('/add_loan', methods=['POST'])
def add_loan():
    global loans_data
    if request.method == 'POST':
        new_loan = {
            'Loan_No': int(request.form['Loan_No']),
            'Amount': float(request.form['Amount']),
            'Cust_ID': int(request.form['Cust_ID']),
            'Customer_Name': request.form['Customer_Name']
        }

        # Checking if the customer exists in the database
        cursor.execute("SELECT * FROM customer WHERE Cust_ID = %s", (new_loan['Cust_ID'],))
        existing_customer = cursor.fetchone()
        
        if not existing_customer:
            flash('Customer ID does not exist', 'error')
            return redirect(url_for('loans'))
        
        # Check if loan number already exists in the database
        cursor.execute("SELECT * FROM loan WHERE Loan_No = %s", (new_loan['Loan_No'],))
        existing_loan = cursor.fetchone()
        
        if existing_loan:
            flash('Loan number already exists', 'error')
            return redirect(url_for('loans'))

        try:
            # Insert the new loan into the database with parameterized queries
            cursor.execute("""
                INSERT INTO loan (Loan_No, Amount, Cust_ID)
                VALUES (%s, %s, %s)
            """, (new_loan['Loan_No'], new_loan['Amount'], new_loan['Cust_ID']))
            conn.commit()  # Commit the transaction

            # Add the new loan to the local list
            loans_data.append(new_loan)

            flash('Loan added successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('loans'))

# Route for updating a loan
@app.route('/update_loan', methods=['POST'])
def update_loan():
    global loans_data
    if request.method == 'POST':
        loan_no = int(request.form['Loan_No'])
        amount = float(request.form['Amount'])
        cust_id = int(request.form['Cust_ID'])
        customer_name = request.form['Customer_Name']

        # Check if the loan exists in the database
        cursor.execute("SELECT * FROM loan WHERE Loan_No = %s", (loan_no,))
        existing_loan = cursor.fetchone()

        if not existing_loan:
            flash('Loan number does not exist', 'error')
            return redirect(url_for('loans'))

        # Check if the customer exists in the database
        cursor.execute("SELECT * FROM customer WHERE Cust_ID = %s", (cust_id,))
        existing_customer = cursor.fetchone()

        if not existing_customer:
            flash('Customer ID does not exist', 'error')
            return redirect(url_for('loans'))

        try:
            # Update the loan in the database with parameterized queries
            cursor.execute("""
                UPDATE loan
                SET Amount = %s, Cust_ID = %s
                WHERE Loan_No = %s
            """, (amount, cust_id, loan_no))
            conn.commit()  # Commit the transaction

            # Update the loan data in the local list
            for loan in loans_data:
                if loan['Loan_No'] == loan_no:
                    loan['Amount'] = amount
                    loan['Cust_ID'] = cust_id
                    loan['Customer_Name'] = customer_name
                    break

            flash('Loan updated successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('loans'))


# Route for deleting a loan
@app.route('/delete_loan', methods=['POST'])
def delete_loan():
    global loans_data
    if request.method == 'POST':
        loan_no = int(request.form['Loan_No'])
        
        # try:
        # Delete the loan from the database
        cursor.execute("DELETE FROM loan WHERE Loan_No = %s", (loan_no,))
        conn.commit()  # Commit the transaction

        # Remove the loan from the local data list
        loans_data = [loan for loan in loans_data if loan['Loan_No'] != loan_no]

        flash('Loan deleted successfully', 'success')
        # except Exception as e:
        #     conn.rollback()  # Rollback in case of error
        #     flash(f"Error: {e}", 'error')

        return redirect(url_for('loans'))
# Route for adding an account
@app.route('/add_account', methods=['POST'])
def add_account():
    global accounts_data
    if request.method == 'POST':
        new_account = {
            'Account_No': int(request.form['Account_No']),
            'balance': Decimal(request.form['balance']),
            'Cust_ID': int(request.form['Cust_ID'])
        }

        # Check if account number already exists
        for account in accounts_data:
            if account['Account_No'] == new_account['Account_No']:
                flash('Account number already exists', 'error')
                return redirect(url_for('accounts'))

        # Insert the new account into the database with parameterized queries
        try:
            cursor.execute("""
                INSERT INTO account (Account_No, balance, Cust_ID)
                VALUES (%s, %s, %s)
            """, (new_account['Account_No'], new_account['balance'], new_account['Cust_ID']))
            conn.commit()  # Commit the transaction
            accounts_data.append(new_account)

            # flash('Account added successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('accounts'))

# Route for updating an account
@app.route('/update_account', methods=['POST'])
def update_account():
    if request.method == 'POST':
        account_no = int(request.form['Account_No'])
        balance = Decimal(request.form['balance'])  # Use float if balance column is stored as float
        cust_id = int(request.form['Cust_ID'])

        # Checking if all required fields are filled
        if not account_no or not balance or not cust_id:
            flash('Please fill all the fields', 'error')
            return redirect(url_for('accounts'))

        try:
            # Execute the update query with parameterized values
            cursor.execute("""
                UPDATE account
                SET balance = %s, Cust_ID = %s
                WHERE Account_No = %s
            """, (balance, cust_id, account_no))
            conn.commit()  # Commit the transaction
            for account in accounts_data:
                if account['Account_No'] == account_no:
                    account['balance'] = balance
                    account['Cust_ID'] = cust_id
                    break
            flash('Account updated successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('accounts'))


# Route for deleting an account
@app.route('/delete_account', methods=['POST'])
def delete_account():
    global accounts_data
    if request.method == 'POST':
        account_no = int(request.form['Account_No'])
        try:
            # Execute the delete query with parameterized value
            cursor.execute("DELETE FROM account WHERE Account_No = %s", (account_no,))
            conn.commit()  # Commit the transaction
            accounts_data = [account for account in accounts_data if account['Account_No'] != account_no]

            flash('Account deleted successfully', 'success')
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'error')

        return redirect(url_for('accounts'))
    
    
if __name__ == '__main__':
    app.run(debug=True)