import json

class Employee:

    raise_amt = 1.04

    def __init__(self, first, last, pay, **kwargs):
        self.first = first
        self.last = last
        self.email = self.first + '.' + self.last + '@companyemail.com'
        self.pay = int(pay)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    @staticmethod
    def add_emps(new_emp, failas):
        new_emp = json.loads(new_emp.toJSON())
        with open(failas + '.json', 'r') as infile:
            data = json.load(infile)
            data.append(new_emp)
            with open(failas + '.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)

    @staticmethod
    def remove_load_emp(first, last, failas, veiksmas):
        with open(failas + '.json', 'r') as infile:
            data = json.load(infile)
            if veiksmas == 'del-load':
                for emp in data:
                    if emp['first'] == first and emp['last'] == last:
                        data.remove(emp)
                        with open(failas + '.json', 'w') as outfile:
                            json.dump(data, outfile, indent=4)
                return emp
            elif veiksmas == 'load':
                for emp in data:
                    if emp['first'] == first and emp['last'] == last:
                        return emp

class Developer(Employee):

    raise_amt = 1.05

    def __init__(self, first, last, pay, prog_lang, **kwargs):
        super().__init__(first, last, pay, **kwargs)
        self.prog_lang = prog_lang

class Manager(Employee):

    raise_amt = 1.08

    def __init__(self, first, last, pay, employees=None, **kwargs):
        super().__init__(first, last, pay, **kwargs)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

def meniu():
    print('-'*10)
    print('1. Prideti darbuotoja')
    print('2. Pasalinti darbuotoja')
    print('3. Parodyti esamus darbuotojus')
    print('4. Pakelti alga')
    print('5. Priskirti Developeri Manageriui')
    print('6. Atskirti Developeri nuo Managerio')

def user_input():
    pasirinkimas = int(input('Iveskite pasirinkima is meniu: '))
    if pasirinkimas == 1:
        emp_type = str(input('Iveskite darbuotojo tipa(Developer/Manager): '))
        if emp_type == 'Developer':
            new_dev = Developer(input('Name: '), input('Lastname: '), input('Pay: '), input('Programming language: '))
            Employee.add_emps(new_dev, 'developers')
        elif emp_type == 'Manager':
            new_mgr = Manager(input('Name: '), input('Lastname: '), input('Pay: '))
            Employee.add_emps(new_mgr, 'managers')
        else:
            print('Klaida.')

    elif pasirinkimas == 2:
        emp_type = str(input('Iveskite darbuotojo tipa(Developer/Manager): '))
        if emp_type == 'Developer':
            Employee.remove_load_emp(input('Name: '), input('Lastname: '), 'developers','del-load')
        elif emp_type == 'Manager':
            Employee.remove_load_emp(input('Name: '), input('Lastname: '), 'managers', 'del-load')
        else:
            print('Klaida.')

    elif pasirinkimas == 3:
        print('-'*10, 'Developers', '-'*10)
        data = json.load(open('developers.json'))
        for i in data:
            print('Name: ', i['first'], i['last'])
            print('Email: ', i['email'])
            print('Programming Language: ', i['prog_lang'])
            print('-'*5)
        print('-'*10, 'Managers', '-'*10)
        data = json.load(open('managers.json'))
        for i in data:
            print('Name: ', i['first'], i['last'])
            print('Email: ', i['email'])
            print('Managing:')
            for j in i['employees']:
                print(j['first'], j['last'])
            print('-'*5)
    
    elif pasirinkimas == 4:
        emp_type = str(input('Iveskite darbuotojo tipa(Developer/Manager): '))
        if emp_type == 'Developer':
            x = Developer(**Developer.remove_load_emp(input('Name: '), input('Lastname: '), 'developers', 'del-load'))
            x.apply_raise()
            Employee.add_emps(x, 'developers')

        elif emp_type == 'Manager':
            x = Manager(**Manager.remove_load_emp(input('Name: '), input('Lastname: '), 'managers', 'del-load'))
            x.apply_raise()
            Employee.add_emps(x, 'managers')
        else:
            print('Klaida.')
    
    elif pasirinkimas == 5:
        print('Iveskite Manager varda ir pavarde')
        x = Manager(**Manager.remove_load_emp(input('Name: '), input('Lastname: '), 'managers', 'del-load'))
        y = Developer(**Developer.remove_load_emp(input('Name: '), input('Lastname: '), 'developers', 'load'))
        x.add_emp(y.__dict__)
        Employee.add_emps(x, 'managers')
        print('Developeris', y.first, y.last, 'priskirtas manageriui', x.first, x.last)
    
    elif pasirinkimas == 6:
        print('Iveskite Manager varda ir pavarde')
        x = Manager(**Manager.remove_load_emp(input('Name: '), input('Lastname: '), 'managers', 'del-load'))
        y = Developer(**Developer.remove_load_emp(input('Name: '), input('Lastname: '), 'developers', 'load'))
        x.remove_emp(y.__dict__)
        Employee.add_emps(x, 'managers')
        print('Developeris', y.first, y.last, 'atskirtas nuo managerio', x.first, x.last)
meniu()
user_input()
