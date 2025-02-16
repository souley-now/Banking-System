from Account import *

class AccountManager(object):
    """"A class for managing account operations.
    """
    
    # We do not have an __init__ function and will call the default constructor.
    def round_balance(self, bank_accounts, account_number):
        '''Rounds the balance of the account with the given account_number to two decimal places.
        '''
        account = self.get_account(bank_accounts, account_number)
        if account is not None:
            account.balance = round(account.balance, 2)
            bank_accounts[account_number] = account
            return account
        else:
            print('Sorry, the account does not exist.')
            return None
        
        
    def get_account(self, bank_accounts, account_number):
        '''Returns the Account object for the given account_number.
        If the account doesn't exist, returns None
        '''
        return bank_accounts.get(account_number)

    def withdraw(self, bank_accounts, account_number, amount):
        '''Withdraws the given amount from the account with the given account_number.
        Rounds the new balance to 2 decimal places.
        If the account doesn't exist, prints a friendly message.
        Raises a RuntimeError if the given amount is greater than the available balance.
        Prints the new balance.
        '''
        account = self.round_balance(bank_accounts, account_number)
        
        if account is None:
            print('Your account does not exist!')
            return ''

        if amount > account.balance:
            print('Not enought money in your bank account.')
            raise RuntimeError('Insuficient funds')
       
        account.balance = round(account.balance - amount, 2)
        print(f"Your balance is {account.balance}.")
        bank_accounts[account_number] = account
        return account
        

    def deposit(self, bank_accounts, account_number, amount):
        '''Deposits the given amount into the account with the given account_number.
        Rounds the new balance to 2 decimal places.
        If the account doesn't exist, prints a friendly message.
        Prints the new balance.
        '''

        account = self.round_balance(bank_accounts, account_number)
        if account is not None:
            account.balance = round(account.balance + amount,2)
            bank_accounts[account_number] = account
            print(f"Your new balance is: {account.balance}")
        else:
            print("Your account does not exist.")


    def purchase(self, bank_accounts, account_number, amounts):
        '''Makes a purchase with the total of the given amounts from the account with the given account_number.
        If the account doesn't exist, prints a friendly message.
        Calculates the total purchase amount based on the sum of the given amounts, plus (6%) sales tax.
        Raises a RuntimeError if the total purchase amount is greater than the available balance.
        Prints the new balance.
        '''

        account = self.get_account(bank_accounts, account_number)

        if account is None:
            print('Your account does not exist!')
            return

        total_amount = sum(amounts)
        salestax = self.calculate_sales_tax(total_amount)
        purchase = total_amount + salestax

        if purchase > account.balance:
            raise RuntimeError('Insuficient funds to make purchases!')
        else:
            account.balance = round(account.balance - purchase, 2)
            bank_accounts[account_number] = account
            print(f"Your balance is: {account.balance}")


    @staticmethod
    def calculate_sales_tax(amount):
        '''Calculates and returns a 6% sales tax for the given amount.'''

        return amount * 0.06

    def sort_accounts(self, bank_accounts, sort_type, sort_direction):
        '''First get the bank_accounts dictionary as a list of tuples. Then based on the specified sort_type
        and sort_direction returns the sorted list of those tuples.
        
        If the sort_type argument is the string 'account_number', sorts based on
        the account number (e.g. '3', '5') in the given sort_direction (e.g.
        'asc', 'desc').
        Example sorted results based on account_number in ascending order:
        Account Number: 1, First Name: Brandon, Last Name: Krakowsky, Balance: 6557.59
        Account Number: 2, First Name: Chenyun, Last Name: Wei, Balance: 4716.89
        Account Number: 3, First Name: Dingyi, Last Name: Shen, Balance: 4.14
        
        Otherwise, if the sort_type argument is 'first_name', 'last_name' or
        'balance', sorts based on the associated values (e.g. 'Brandon',
        'Krakowsky', 6557.59) in the given sort direction (e.g. 'asc' or 'desc')
        Example sorted results based on 'balance' in descending order:
        Account Number: 6, First Name: Karishma, Last Name: Jain, Balance: 6700.19
        Account Number: 1, First Name: Brandon, Last Name: Krakowsky, Balance: 6557.59
        Account Number: 2, First Name: Chenyun, Last Name: Wei, Balance: 4716.89
        '''

        # Check if the given sort_type is valid
        if sort_type.lower() not in ['account_number', 'first_name', 'last_name', 'balance']:
            return 'Invalid input'
        
        # Check if the given sort_direction is valid
        if sort_direction.lower() not in ['asc', 'desc']:
            return 'Invalid input'
        
        # Convert bank_accounts dictionary to a list of Account objects
        accounts_list = list(bank_accounts.values())
        
        # Determine if the sorting should be in reverse order
        reverse = sort_direction.lower() == 'desc'
        
        # Sort based on the specified sort_type
        if sort_type.lower() == 'account_number':
            accounts_list.sort(key=lambda account: account.account_number, reverse=reverse)
        elif sort_type.lower() == 'first_name':
            accounts_list.sort(key=lambda account: account.first_name, reverse=reverse)
        elif sort_type.lower() == 'last_name':
            accounts_list.sort(key=lambda account: account.last_name, reverse=reverse)
        elif sort_type.lower() == 'balance':
            accounts_list.sort(key=lambda account: account.balance, reverse=reverse)
        
        return [(account.account_number, account.first_name, account.last_name, account.balance) for account in accounts_list]

    def export_statement(self, bank_accounts, account_number, output_file):
        '''Exports the given account information to the given output file in the following format:

        First Name: Huize
        Last Name: Huang
        Balance: 34.57
        '''
        account = self.get_account(bank_accounts, account_number)
        if account:
            with open(output_file, 'w') as file:
                file.write(f"First Name: {account.first_name}\n")
                file.write(f"Last Name: {account.last_name}\n")
                file.write(f"Balance: {account.balance:.2f}\n")
        else:
            print("Your account does not exist.")