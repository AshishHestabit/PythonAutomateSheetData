import csv , os , uuid
from datetime import datetime

def uid():
    return str(int(uuid.uuid4()) % 1000000)

# Trim csv file

def trim_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            trimmed_row = [field.strip() for field in row]
            writer.writerow(trimmed_row)
            
# Get today's date
def date():
    today = datetime.today()
    rounded_down_date = today.replace(day=1)
    formatted_date = rounded_down_date.strftime("%m/%d/%Y")
    return formatted_date

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
    with open('finalData/employee.csv', 'a') as empFile:
        empWriter = csv.writer(empFile)
        
        if os.stat('finalData/employee.csv').st_size > 0:
            pass
        else:
            empHeader = ['EmpId','EmpOrgId','Name','SupervisorID','SupervisorName','CommittedUtilization','PrimaryDiscipline','ExperienceYears','KeyExperienceAreas','PrefersToThinkAloneorTeam','NextDesiredRole','NextDesiredProject','Certification','MBTI','Age','Ethnicity','Gender','PrimaryWorkspace','QualityofWorkspace','Education level','EmpType','StartDate','Role','Utilization on the Team','Experience related to the role']
            empWriter.writerow(empHeader)
            # print(len(empHeader))
        
        empId = uid()
        empBody = [empId, empOrgid, empName,'','','','','','','','','','','','','','','','','','','','','','']
        empWriter.writerow(empBody)
        # print(len(empBody))
        
    return empBody
    
# empty the csv files

def empty_csv_file(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        pass  # Using 'pass' here effectively does nothing, but it truncates the file


# get project 

def get_project():
    with open('finalData/project.csv', 'r') as ProjectData:
        ProjData = csv.DictReader(ProjectData)
        project = next(ProjData)
    return project

# Filter organization
def filter_org(orgName):
    with open('finalData/organization.csv', 'r') as orgFile:
        orgData = csv.DictReader(orgFile)
        for org in orgData:
            if org.get('OrgName') == orgName:
                return {'status': True, 'data': org}
    return {'status': False, 'data': {}}

# Filter Project
def filter_project(projName):
    with open('finalData/project.csv', 'r') as projFile:
        projData = csv.DictReader(projFile)
        for proj in projData:
            if proj.get('ProjectName') == projName:
                return {'status': True, 'data': proj}
    return {'status': False, 'data': {}}

# Filter Supplier
def filter_supOrg(supId, projId):
    with open('finalData/projectSupplier.csv', 'r') as supFile:
        supData = csv.DictReader(supFile)
        for supp in supData:
            if supp.get('SupplierOrgId') == supId and supp.get('ProjectId') == projId:
                return {'status': True, 'data': supp}
    return {'status': False, 'data': {}}