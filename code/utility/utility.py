import csv , os , uuid


def uid():
    return str(int(uuid.uuid4()) % 1000000)

def filter_csv(input_file, filter_field, filter_value):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row.get(filter_field) == filter_value:
                return {'status':True, 'data':row}
    return {'status':False, 'data':{}}

def filter_emp(input_file, filter_field, filter_value):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row.get(filter_field[0]) == filter_value[0] and row.get(filter_field[1]) == filter_value[1]:
                return {'status':True, 'data':row}
    return {'status':False, 'data':{}}


def filter_teamMember(input_file, filter_field, filter_value):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row.get(filter_field[0]) == filter_value[0] and row.get(filter_field[1]) == filter_value[1] and row.get(filter_field[2]) == filter_value[2] and row.get(filter_field[3]) == filter_value[3]:
                return {'status':True, 'data':row}
    return {'status':False, 'data':{}}

def filter_team(input_file, filter_field, filter_value):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row.get(filter_field[0]) == filter_value[0] and row.get(filter_field[1]) == filter_value[1]:
                return {'status':True, 'data':row}
    return {'status':False, 'data':{}}
                
            
    
def create_emp(empName , empOrgid):
    with open('../finalData/employee.csv', 'a') as empFile:
        empWriter = csv.writer(empFile)
        
        if os.stat('../finalData/employee.csv').st_size > 0:
            pass
        else:
            empHeader = ['EmpId','EmpOrgId','Name','SupervisorID','SupervisorName','CommittedUtilization','PrimaryDiscipline','ExperienceYears','KeyExperienceAreas','PrefersToThinkAloneorTeam','NextDesiredRole','NextDesiredProject','Certification','MBTI','Age','Ethnicity','Gender','PrimaryWorkspace','QualityofWorkspace','Education level','EmpType','StartDate','Role','Utilization on the Team','Experience related to the role']
            empWriter.writerow(empHeader)
        
        empId = uid()
        empBody = [empId, empOrgid, empName]
        empWriter.writerow(empBody)
    return empBody
    
# empty the csv files

def empty_csv_file(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        pass  # Using 'pass' here effectively does nothing, but it truncates the file




