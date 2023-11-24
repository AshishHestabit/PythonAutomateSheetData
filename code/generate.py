import csv
import os
from utility.utility import filter_csv, uid , create_emp , empty_csv_file

# empty csv file

files = ['employee.csv','team.csv','projectSupplier.csv','organization.csv']
for file in files:
    empty_csv_file('../finalData/'+file)
    
# end

with open('../TrimmedData/Project.csv') as csvFile:
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
        
        
with open('../finalData/organization.csv', 'a') as OrgFile:
    Orgwriter = csv.writer(OrgFile)
    if os.stat('../finalData/organization.csv').st_size > 0:
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
    with open('../finalData/project.csv', 'a') as ProjectFile:
        proWriter = csv.writer(ProjectFile)
        
        if os.stat('../finalData/project.csv').st_size > 0:
            pass
        else:
            projectHeader = ['ProjectId','ProjectName','OwnerOrgId','ProjectManagerId','ProjectExecId']
            proWriter.writerow(projectHeader)
            
        ProjectId = uid()
        projectBody = [ProjectId , body[0], OwnerOrgId, empList[0], empList[1]]
        # projectBody = [ProjectId , body[0], None, None, None] #it's temporary data
        proWriter.writerow(projectBody)
        
    
if header[1] != header[7]:
    with open('../finalData/project.csv', 'r') as ProjectData:
        ProjData = csv.reader(ProjectData)
        next(ProjData)
        d = next(ProjData)
        supBody = [d[0],orgId," ",d[2],empList[0],empList[1],orgId]
        
    with open('../finalData/projectSupplier.csv', 'a') as SupplierFile:
        supWriter = csv.writer(SupplierFile)
        if os.stat('../finalData/projectSupplier.csv').st_size > 0:
            pass
        else:
            supHeader = ['ProjectId','SupplierOrgId','SupplierRole','SuppliesToOrgId','SupplierPMId','SupplierExecId','OrgId'] 
            supWriter.writerow(supHeader)
        supWriter.writerow(supBody)
         
# Create Team
with open('../TrimmedData/Teams.csv', 'r') as TeamCsvFile:
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
        
        
with open('../finalData/team.csv', 'a') as TeamFile:
    teamWriter = csv.writer(TeamFile)
    
    if os.stat('../finalData/team.csv').st_size > 0:
        pass
    else:
        TeamHeader = ['ProjectId','OrgId','TeamId','TeamName','TeamLeadId']
        teamWriter.writerow(TeamHeader)
        
    
    with open('../finalData/project.csv', 'r') as ProjectData:
        ProjData = csv.reader(ProjectData)
        next(ProjData)
        d = next(ProjData)
        TeamId = uid()
        TeamBody = [d[0],orgId,TeamId, TeamDataBody[1]]
        
        
    input_csv_file = '../finalData/employee.csv'
    filter_field = 'Name'  
    filter_value = 'sathia' # team leader name  TeamDataBody[2]
    empData = filter_csv(input_csv_file, filter_field, filter_value) 
    if empData['status']:
        TeamBody.append(empData['data']['EmpId'])
    else :
        emp = create_emp('sathia', orgId)
        TeamBody.append(emp[0])
          
    teamWriter.writerow(TeamBody)   
