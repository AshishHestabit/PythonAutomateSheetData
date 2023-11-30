import csv, os
from utils.utility import create_emp, get_project, uid, filter_org,filter_project,filter_supOrg


def create_projOrg():
    with open('TrimmedData/Project.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        header = []
        body = []
        # dictBody ={}
        i = 0
        # keys = {'p001':'ProjectName','p002':'OwnerOrganizationName','p003':'OwnerExecutiveName','p004':'OwnerManagerName','p005':'SupplierOrganizationName','p006':'SupplierExecutiveName','p007':'SupplierLeaderName','p008':'MyOrganizationName','p009':'MyOrganizationExecutiveName','p010':'MyOrganizationLeaderName','p011':'SuupliesToOrganization','p012':'ProjectBudget','p013':'ProjectComplexity'}

        for row in Data:
            if i < 12 :
                # dictBody[row[0]] = row[2]
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
            
            # create Owner organization
            if body[1] != body[7]:
                OwnerOrgId = uid()
                orgBody = [OwnerOrgId , body[1]," "," "," "]
                Orgwriter.writerow(orgBody)
            else:
                OwnerOrgId = orgId
        

    
    projData = filter_project(body[0])
    if projData['status'] == False:
          
        with open('finalData/project.csv', 'a') as ProjectFile:
            proWriter = csv.writer(ProjectFile)
            
            if os.stat('finalData/project.csv').st_size > 0:
                pass
            else:
                projectHeader = ['ProjectId','ProjectName','OwnerOrgId','ProjectManagerId','ProjectExecId']
                proWriter.writerow(projectHeader)
                
            empDict = {body[2]:orgId, body[3]:orgId}
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
        empDict = {body[6]:orgId,body[5]:orgId} 
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