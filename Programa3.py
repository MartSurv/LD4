import json

class Employee:

    ''' This is a class which describes an employee object. '''

    __raise_amt = 1.04 # Private Global attribute (encapsulation)

    def __init__(self, first, last, pay, **kwargs): # Constructor
        '''
        The constructor for class Employee.

        Parameters:
            first(str): First name of an employee.
            last(str): Last name of an employee.
            pay(str): Annual salary of an employee.
        '''
        self.first = first
        self.last = last
        self.email = self.first + '.' + self.last + '@companyemail.com'
        self.__pay = int(pay) # Private attribute (encapsulation)

    def apply_raise(self): # A method
        '''A function, which applies a salary raise for an employee.'''
        self.pay = int(self.__pay * self.__raise_amt)

    def to_json(self): # A method
        '''A function, which converts an object to a dictionary ready for adding JSON.'''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    @staticmethod # A static method which 
    def add_emps(new_emp, failas):
        '''
        A function, which loads a list of employees from JSON, adds a new employee and writes the data back JSON.

        Parameters:
            new_emp(obj): An object.
            failas(str): A name of a file.
        '''
        new_emp = json.loads(new_emp.to_json()) # new_emp object is converted to a dictionary
        with open(failas + '.json', 'r') as infile:
            data = json.load(infile) # loading a list of dictionaries from a JSON file
            data.append(new_emp) # appending new_emp dictionary to the list
            with open(failas + '.json', 'w') as outfile:
                json.dump(data, outfile, indent=4) # writing an updated list to a JSON file

    @staticmethod
    def remove_load_emp(first, last, failas, veiksmas):
        '''
        A function, which loads a list of employees from JSON, removes an employee, writes the data back to JSON and returns an employee dict.
        
        Parameters:
            first(str): First name of an employee.
            last(str): Last name of an employee.
            failas(str): A name of a file.
            veiksmas(str): An action which should be performed.
            IF veiksmas 'del-load': remove employee from loaded data, write data back to JSON, return an employee dict.
            IF veiksmas 'load': return an employee dict.

        Returns:
            An employee data from a JSON file as a dict.
        '''
        with open(failas + '.json', 'r') as infile:
            data = json.load(infile) # loading a list of dictionaries from a JSON file
            if veiksmas == 'del-load':
                for emp in data:
                    if emp['first'] == first and emp['last'] == last: # Identifying an employee by its first name and last name
                        data.remove(emp) # removing an employee from the list
                        with open(failas + '.json', 'w') as outfile:
                            json.dump(data, outfile, indent=4) # writing an updated list to a JSON file
                        return emp # returning employee data as a dictionary
            elif veiksmas == 'load':
                for emp in data:
                    if emp['first'] == first and emp['last'] == last:
                        return emp

class Developer(Employee): # Inheritance from a class Employee

    '''This is a child class of an Employee class, which describes a developer object.'''

    __raise_amt = 1.05 # Private Global attribute

    def __init__(self, first, last, pay, prog_lang, **kwargs): # Constructor
        '''
        The constructor for class Developer.

        Parameters:
            first(str): First name of an employee.
            last(str): Last name of an employee.
            pay(str): Annual salary of an employee.
            prog_lang(str): A name of a programming language.
        
        Inherited Employee class parameters:
            first(str): First name of an employee.
            last(str): Last name of an employee.
            pay(str): Annual salary of an employee.
        '''
        super().__init__(first, last, pay, **kwargs) # Employee class attributes inheritance

        self.prog_lang = prog_lang

class Manager(Developer): # Inheritance from a class Developer

    '''This is a child class of a Developer class, which describes a manager object.'''

    __raise_amt = 1.08 # Private Global attribute

    def __init__(self, first, last, pay, prog_lang, employees=None, **kwargs): # Constructor
        '''
        The constructor for class Manager.

        Parameters:
            first(str): First name of an employee.
            last(str): Last name of an employee.
            pay(str): Annual salary of an employee.
            prog_lang(str): Names of a programming languages/frameworks.
            employees(list): A list with employees data dictionaries.
        
        Inherited Developer class parameters:
            first(str): First name of an employee.
            last(str): Last name of an employee.
            pay(str): Annual salary of an employee.
            prog_lang(str): A name of a programming language.
        '''
        super().__init__(first, last, pay, prog_lang, **kwargs) # Developer class attributes inheritance

        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp): # A method
        '''A function which assigns a developer to a manager.'''
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp): # A method
        '''A function which unassigns a developer from a manager.'''
        if emp in self.employees:
            self.employees.remove(emp)


print('-'*10)
print('1. Add employee')
print('2. Remove employee')
print('3. Show current employees')
print("4. Raise employee's salary")
print('5. Assign a developer to a manager')
print('6. Unassign a developer from a manager')
print('7. Help')

pasirinkimas = int(input('Choose an option from the menu: '))

if pasirinkimas == 1:
    emp_type = str(input('Enter an employee type(Developer/Manager): '))
    if emp_type == 'Developer':
        new_dev = Developer(input('First Name: '), input('Last Name: '), input('Pay: '), input('Programming language: ')) # Instantiation of a Developer object new_dev
        Employee.add_emps(new_dev, 'developers')
        print('Developer', new_dev.first, new_dev.last, 'has been added successfully.')
    elif emp_type == 'Manager':
        new_mgr = Manager(input('First Name: '), input('Last Name: '), input('Pay: '), [str(x) for x in input("Programming languages/frameworks: ").split()])
        Employee.add_emps(new_mgr, 'managers')
        print('Manager', new_mgr.first, new_mgr.last, 'has been added successfully.')
    else:
        print('-'*5)
        print('Employee type error.')
        print('-'*5)

elif pasirinkimas == 2:
    emp_type = str(input('Enter an employee type(Developer/Manager): '))
    if emp_type == 'Developer':
        Employee.remove_load_emp(input('First Name: '), input('Last Name: '), 'developers','del-load')
    elif emp_type == 'Manager':
        Employee.remove_load_emp(input('First Name: '), input('Last Name: '), 'managers', 'del-load')
    else:
        print('-'*5)
        print('Employee type error.')
        print('-'*5)

elif pasirinkimas == 3:
    print('-'*10, 'Developers', '-'*10)
    data = json.load(open('developers.json')) # Loading data from a JSON file as a list containing dictionaries
    for i in data: # Printing out key values of the dictionaries inside the list
        print('Name: ', i['first'], i['last'])
        print('Email: ', i['email'])
        print('Programming Language: ', i['prog_lang'])
        print('-'*5)
    print('-'*10, 'Managers', '-'*10)
    data = json.load(open('managers.json')) # Loading data from a JSON file as a list containing dictionaries
    for i in data: # Printing out key values of the dictionaries inside the list
        print('Name: ', i['first'], i['last'])
        print('Email: ', i['email'])
        print('Prog. languages/frameworks: ', ', '.join(i['prog_lang']))
        print('Managing:')
        if not i['employees']:
            print('None')
        else:
            for j in i['employees']:
                print(j['first'], j['last'])
        print('-'*5)

elif pasirinkimas == 4:
    emp_type = str(input('Enter an employee type(Developer/Manager): '))
    try:
        if emp_type == 'Developer':
            z = Developer(**Developer.remove_load_emp(input('First Name: '), input('Last Name: '),'developers', 'del-load')) # Instantiation of a Developer object z
            # remove_load_emp returns a dict with key values which are passed as parameters to the Developer class
            z.apply_raise() # updates Developer object's pay parameter
            Employee.add_emps(z, 'developers') # writes an updated data back to the JSON file
            print('The salary for', z.first, z.last, 'has been raised successfully.')

        elif emp_type == 'Manager':
            x = Manager(**Manager.remove_load_emp(input('First Name: '), input('Last Name: '), 'managers', 'del-load'))
            x.apply_raise()
            Employee.add_emps(x, 'managers')
            print('The salary for', x.first, x.last, 'has been raised successfully.')
        else:
            print('-'*5)
            print('Employee type error.')
            print('-'*5)

    except TypeError:
        print('-'*5)
        print('Employee name error. Please check if the employee exists.')
        print('-'*5)

elif pasirinkimas == 5:
    try:
        print('-'*3,'Enter the First Name and the Last Name of a Manager','-'*3)
        x = Manager(**Manager.remove_load_emp(input('First Name: '), input('Last Name: '), 'managers', 'del-load')) # Instantiation of a Manager object x
        # remove_load_emp returns a dict with key values which are passed as parameters to the Developer class
        print('-'*3,'Enter the First Name and the Last Name of a Developer','-'*3)
        y = Developer(**Developer.remove_load_emp(input('First Name: '), input('Last Name: '), 'developers', 'load'))
        x.add_emp(y.__dict__) # y Developer object is appended to a list as a dict which is a value of a key 'employees'
        Employee.add_emps(x, 'managers')
        print('Developer', y.first, y.last, 'has been assigned to', x.first, x.last)
    except TypeError:
        print('-'*5)
        print('Employee name error. Please check if the employee exists.')
        print('-'*5)

elif pasirinkimas == 6:
    try:
        print('-'*3,'Enter the First Name and the Last Name of a Manager','-'*3)
        x = Manager(**Manager.remove_load_emp(input('First Name: '), input('Last Name: '), 'managers', 'del-load'))
        print('-'*3,'Enter the First Name and the Last Name of a Developer','-'*3)
        y = Developer(**Developer.remove_load_emp(input('First Name: '), input('Last Name: '), 'developers', 'load'))
        x.remove_emp(y.__dict__)
        Employee.add_emps(x, 'managers')
        print('Developer', y.first, y.last, 'has been unassigned from', x.first, x.last)
    except TypeError:
        print('-'*5)
        print('Employee name error. Please check if the employee exists.')
        print('-'*5)

elif pasirinkimas == 7:
    h = str(input('Type in a class (Employee/Developer/Manager: '))
    if h == 'Employee':
        print(help(Employee))
    elif h == 'Developer':
        print(help(Developer))
    elif h == 'Manager':
        print(help(Manager))
    else:
        print('-'*5)
        print('Menu selection error.')
        print('-'*5)
else:
    print('-'*5)
    print('Menu selection error.')
    print('-'*5)
