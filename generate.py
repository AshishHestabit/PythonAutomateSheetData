import csv
# import random
import uuid, os
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
        
        
    orgId = str(uuid.uuid4())
    orgBody = [orgId , body[7]," "," "," "]
    Orgwriter.writerow(orgBody)
    
# empList = [body[2], body[3] ,body[6],body[5]]

# for now owner org employees org is empty
if header[1] != header[7]:
    empDict = {body[6]:orgId,body[5]:orgId} 
else:
    empDict = {body[2]:orgId, body[3]:orgId} 
    
empList ={}
with open('finalData/employee.csv', 'a') as empFile:
    empWriter = csv.writer(empFile)
    
    if os.stat('finalData/employee.csv').st_size > 0:
        pass
    else:
        empHeader = ['EmpId','EmpOrgId','Name','SupervisorID','SupervisorName','CommittedUtilization','PrimaryDiscipline','ExperienceYears','KeyExperienceAreas','PrefersToThinkAloneorTeam','NextDesiredRole','NextDesiredProject','Certification','MBTI','Age','Ethnicity','Gender','PrimaryWorkspace','QualityofWorkspace','Education level','EmpType','StartDate','Role','Utilization on the Team','Experience related to the role']
        empWriter.writerow(empHeader)
       
    for emp in empDict:
        empId = str(uuid.uuid4())
        empBody = [empId , empDict[emp],emp]
        empWriter.writerow(empBody)
        empList[emp] = empId
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
            
        ProjectId = str(uuid.uuid4())
        projectBody = [ProjectId , body[0], OwnerOrgId, empList[body[3]], empList[body[2]]]
        # projectBody = [ProjectId , body[0], None, None, None] #it's temporary data
        proWriter.writerow(projectBody)
        
    
if header[1] != header[7]:
    with open('finalData/project.csv', 'r') as ProjectData:
        ProjData = csv.reader(ProjectData)
        next(ProjData)
        d = next(ProjData)
        # print(d)
        supBody = [d[0],orgId," ",d[2],empList[body[6]],empList[body[5]],orgId]
        
    with open('finalData/projectSupplier.csv', 'a') as SupplierFile:
        supWriter = csv.writer(SupplierFile)
        if os.stat('finalData/projectSupplier.csv').st_size > 0:
            pass
        else:
            supHeader = ['ProjectId','SupplierOrgId','SupplierRole','SuppliesToOrgId','SupplierPMId','SupplierExecId','OrgId'] 
            supWriter.writerow(supHeader)
        supWriter.writerow(supBody)
         
    
