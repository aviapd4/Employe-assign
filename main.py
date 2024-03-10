import json

class Employee:
    def __init__(self, name, emp_id, title, department):
        self.name = name
        self.emp_id = emp_id
        self.title = title
        self.department = department
    
    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Employee ID: {self.emp_id}")
        print(f"Title: {self.title}")
        print(f"Department: {self.department}")
    
    def __str__(self):
        return f"{self.name} ({self.emp_id})"

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []
    
    def add_employee(self, employee):
        self.employees.append(employee)
    
    def remove_employee(self, emp_id):
        self.employees = [emp for emp in self.employees if emp.emp_id != emp_id]
    
    def list_employees(self):
        print(f"Employees in {self.name} department:")
        for emp in self.employees:
            print(emp)
    
class Company:
    def __init__(self):
        self.departments = {}

    def add_department(self, department):
        self.departments[department.name] = department
    
    def remove_department(self, department_name):
        del self.departments[department_name]

    def display_departments(self):
        print("Departments:")
        for department_name in self.departments:
            print(department_name)

def save_company_data(company):
    with open('company_data.json', 'w') as f:
        data = {}
        for department_name, department_obj in company.departments.items():
            data[department_name] = [emp.__dict__ for emp in department_obj.employees]
        json.dump(data, f)

def load_company_data():
    try:
        with open('company_data.json', 'r') as f:
            data = json.load(f)
            company = Company()
            for department_name, employees in data.items():
                department = Department(department_name)
                for emp_data in employees:
                    emp = Employee(**emp_data)
                    department.add_employee(emp)
                company.add_department(department)
            return company
    except FileNotFoundError:
        return Company()

def main():
    print("Welcome to Employee Management System")

    company = load_company_data()

    while True:
        print("\nMenu:")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. List Employees in Department")
        print("4. Add Department")
        print("5. Remove Department")
        print("6. List Departments")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter employee name: ")
            emp_id = input("Enter employee ID: ")
            title = input("Enter employee title: ")
            department = input("Enter employee department: ")

            if department not in company.departments:
                print("Department does not exist.")
                continue

            emp = Employee(name, emp_id, title, department)
            company.departments[department].add_employee(emp)
            save_company_data(company)
            print("Employee added successfully.")
        
        elif choice == '2':
            emp_id = input("Enter employee ID to remove: ")

            for department in company.departments.values():
                department.remove_employee(emp_id)
            
            save_company_data(company)
            print("Employee removed successfully.")
        
        elif choice == '3':
            department_name = input("Enter department name to list employees: ")

            if department_name in company.departments:
                company.departments[department_name].list_employees()
            else:
                print("Department does not exist.")
        
        elif choice == '4':
            department_name = input("Enter department name to add: ")
            department = Department(department_name)
            company.add_department(department)
            save_company_data(company)
            print("Department added successfully.")
        
        elif choice == '5':
            department_name = input("Enter department name to remove: ")
            company.remove_department(department_name)
            save_company_data(company)
            print("Department removed successfully.")
        
        elif choice == '6':
            company.display_departments()
        
        elif choice == '7':
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
