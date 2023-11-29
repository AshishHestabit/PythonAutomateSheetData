import csv, os
from utils.utility import create_emp, get_project, uid, filter_org,filter_project,filter_supOrg


def create_projOrg():
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
        
    orgData = filter_org(body[7]) 
        
    if orgData['status']:  
        orgId = orgData['data']['OrgId']
    if orgData['status'] == False :  
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
    if body[1] != body[7]: #when org is supplier
        empDict = {body[6]:orgId,body[5]:orgId} 
    else:                   #when org is owner
        empDict = {body[2]:orgId, body[3]:orgId} 
        
    
    projData = filter_project(body[0])
    if projData['status'] == False and body[1] == body[7]:
        OwnerOrgId = orgId      
        with open('finalData/project.csv', 'a') as ProjectFile:
            proWriter = csv.writer(ProjectFile)
            
            if os.stat('finalData/project.csv').st_size > 0:
                pass
            else:
                projectHeader = ['ProjectId','ProjectName','OwnerOrgId','ProjectManagerId','ProjectExecId']
                proWriter.writerow(projectHeader)
            
            empList =[]
            for emp in empDict:
                employee = create_emp(emp , empDict[emp])
                empList.append(employee[0])
                
            ProjectId = uid()
            projectBody = [ProjectId , body[0], OwnerOrgId, empList[0], empList[1]]
            # projectBody = [ProjectId , body[0], None, None, None] #it's temporary data
            proWriter.writerow(projectBody)
            
            
    project = get_project()        
    supData = filter_supOrg(orgId,project['ProjectId'])
    if supData['status'] == False and body[1] != body[7]:    
        empList =[]
        for emp in empDict:
            employee = create_emp(emp , empDict[emp])
            empList.append(employee[0])
        supBody = [project['ProjectId'],orgId," ",project['OwnerOrgId'],empList[0],empList[1],orgId]
            
        with open('finalData/projectSupplier.csv', 'a') as SupplierFile:
            supWriter = csv.writer(SupplierFile)
            if os.stat('finalData/projectSupplier.csv').st_size > 0:
                pass
            else:
                supHeader = ['ProjectId','SupplierOrgId','SupplierRole','SuppliesToOrgId','SupplierPMId','SupplierExecId','OrgId'] 
                supWriter.writerow(supHeader)
            supWriter.writerow(supBody)
    return orgId