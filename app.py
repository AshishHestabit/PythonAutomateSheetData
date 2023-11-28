import csv
import os
from utils.utility import filter_emp, uid , create_emp , empty_csv_file, get_project, trim_csv
from utils.create import create_employee ,create_teamMember , create_tssRating, create_deiRating, create_esgRating
 
 # Trim all the csv files
 
files = ['Project.csv','Teams.csv','Team Members.csv','Member Ratings.csv','DEI.csv','ESG.csv','Emails.csv']
for file in files:
    empty_csv_file('TrimmedData/'+file)
    input_csv_file = 'RawData/'+file
    output_csv_file = 'TrimmedData/'+file
    trim_csv(input_csv_file, output_csv_file)
 
 
# empty csv file

files = ['employee.csv','team.csv','projectSupplier.csv','organization.csv','ProjectTeamMember.csv','TssRating.csv','deiRating.csv','esgRating.csv']
for file in files:
    empty_csv_file('finalData/'+file)
    
# end

with open('TrimmedData/Project.csv') as csvFile:
    Data = csv.reader(csvFile)
    next(Data)
    header = []
    body = []
    i = 0
    for row in Data:
        if i < 12 :
            header.append(row[0])
            body.append(row[1])
            i = i+1
        else:
            break
        
        
with open('finalData/organization.csv', 'a') as OrgFile:
    Orgwriter = csv.writer(OrgFile)
    if os.stat('finalData/organization.csv').st_size > 0:
        pass
    else:
        orgHeader = ['OrgId','OrgName','OrgHQCity','OrgHQState','OrgHQCountry']
        Orgwriter.writerow(orgHeader)
        
    orgId = uid()
    orgBody = [orgId , body[7]," "," "," "]
    Orgwriter.writerow(orgBody)
    

# for now owner org employees org is empty
if header[1] != header[7]:
    empDict = {body[6]:orgId,body[5]:orgId} 
else:
    empDict = {body[2]:orgId, body[3]:orgId} 
    
empList =[]
for emp in empDict:
    employee = create_emp(emp , empDict[emp])
    empList.append(employee[0])
# print(empList)

if header[1] == header[7]:
    OwnerOrgId = orgId      
    with open('finalData/project.csv', 'a') as ProjectFile:
        proWriter = csv.writer(ProjectFile)
        
        if os.stat('finalData/project.csv').st_size > 0:
            pass
        else:
            projectHeader = ['ProjectId','ProjectName','OwnerOrgId','ProjectManagerId','ProjectExecId']
            proWriter.writerow(projectHeader)
            
        ProjectId = uid()
        projectBody = [ProjectId , body[0], OwnerOrgId, empList[0], empList[1]]
        # projectBody = [ProjectId , body[0], None, None, None] #it's temporary data
        proWriter.writerow(projectBody)
        
    
if header[1] != header[7]:
    project = get_project()
    supBody = [project['ProjectId'],orgId," ",project['OwnerOrgId'],empList[0],empList[1],orgId]
        
    with open('finalData/projectSupplier.csv', 'a') as SupplierFile:
        supWriter = csv.writer(SupplierFile)
        if os.stat('finalData/projectSupplier.csv').st_size > 0:
            pass
        else:
            supHeader = ['ProjectId','SupplierOrgId','SupplierRole','SuppliesToOrgId','SupplierPMId','SupplierExecId','OrgId'] 
            supWriter.writerow(supHeader)
        supWriter.writerow(supBody)
         
# Create Team
with open('TrimmedData/Teams.csv', 'r') as TeamCsvFile:
    TeamData = csv.reader(TeamCsvFile)
    next(TeamData)
    TeamDataBody = []
    i = 0
    for row in TeamData:
        if i < 3 :
            TeamDataBody.append(row[1])
            i = i+1
        else:
            break
        
        
with open('finalData/team.csv', 'a') as TeamFile:
    teamWriter = csv.writer(TeamFile)
    
    if os.stat('finalData/team.csv').st_size > 0:
        pass
    else:
        TeamHeader = ['ProjectId','OrgId','TeamId','TeamName','TeamLeadId']
        teamWriter.writerow(TeamHeader)
        
    
    project = get_project()
    TeamId = uid()
    TeamBody = [project['ProjectId'],orgId,TeamId, TeamDataBody[1]]
        
        
    input_csv_file = 'finalData/employee.csv'
    filter_field = ['EmpOrgId','Name']
    filter_value = [orgId,TeamDataBody[2]] # team leader name  TeamDataBody[2]
    empData = filter_emp(input_csv_file, filter_field, filter_value) 
    if empData['status']:
        TeamBody.append(empData['data']['EmpId'])
    else :
        emp = create_emp('sathia', orgId)
        TeamBody.append(emp[0])
          
    teamWriter.writerow(TeamBody)   


emp = create_employee(orgId)
empId = emp[0]
Project = get_project()
proId = project['ProjectId']
create_teamMember(empId, proId, orgId, TeamId)

create_tssRating(empId, orgId)

create_deiRating(empId, orgId)

create_esgRating(empId, orgId)

