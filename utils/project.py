import csv, os
from utils.utility import create_emp, get_dict, get_project, uid, filter_org,filter_project,filter_supOrg
from config import keys
def create_projOrg():
    with open('TrimmedData/Project.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        dictBody ={}
        
        for row in Data:
            if row[0] in keys.values():
                dictBody[row[0]] = row[2]
           
    orgData = filter_org(dictBody[keys['MyOrganizationName']]) 
   
    if orgData['status'] == False :  
        orgHeader = ['OrgId','OrgName','OrgHQCity','OrgHQState','OrgHQCountry']
        with open('finalData/organization.csv', 'a') as OrgFile:
            Orgwriter = csv.DictWriter(OrgFile, fieldnames = orgHeader)
            if os.stat('finalData/organization.csv').st_size > 0:
                pass
            else:
                Orgwriter.writeheader()
                
            orgId = uid()
            orgData = [orgId , dictBody[keys['MyOrganizationName']]," "," "," "]
            orgBody = get_dict(orgHeader, orgData)
            Orgwriter.writerow(orgBody)
            
            # create Owner organization
            if dictBody[keys['MyOrganizationName']]!= dictBody[keys['OwnerOrganizationName']]:
                OwnerOrgId = uid()
                OwnerOrgData = [OwnerOrgId , dictBody[keys['OwnerOrganizationName']]," "," "," "]
                OwnerOrgBody = get_dict(orgHeader, OwnerOrgData)
                Orgwriter.writerow(OwnerOrgBody)
            else:
                OwnerOrgId = orgId
    else:
        orgId = orgData['data']['OrgId']

    projData = filter_project(dictBody[keys['ProjectName']])
    if projData['status'] == False:
        projectHeader = ['ProjectId','ProjectName','OwnerOrgId','ProjectManagerId','ProjectExecId']
        with open('finalData/project.csv', 'a') as ProjectFile:
            proWriter = csv.DictWriter(ProjectFile, fieldnames=projectHeader)
            
            if os.stat('finalData/project.csv').st_size > 0:
                pass
            else:
                proWriter.writeheader()
                
            empDict = {dictBody[keys['OwnerExecutiveName']]:OwnerOrgId, dictBody[keys['OwnerManagerName']]:OwnerOrgId}
            empList =[]
            for emp in empDict:
                employee = create_emp(emp , empDict[emp])
                empList.append(employee[0])
                
            ProjectId = uid()
            projectData = [ProjectId , dictBody[keys['ProjectName']], OwnerOrgId, empList[0], empList[1]]
            projectBody = get_dict(projectHeader, projectData)
            proWriter.writerow(projectBody)
            
    project = get_project()        
    supData = filter_supOrg(orgId,project['ProjectId'])
    if supData['status'] == False and dictBody[keys['OwnerOrganizationName']] != dictBody[keys['MyOrganizationName']]:  
        empList =[]
        empDict = {dictBody[keys['SupplierLeaderName']]:orgId,dictBody[keys['SupplierExecutiveName']]:orgId} 
        for emp in empDict:
            employee = create_emp(emp , empDict[emp])
            empList.append(employee[0])
        supDataBody = [project['ProjectId'],orgId," ",project['OwnerOrgId'],empList[0],empList[1],orgId]
        supHeader = ['ProjectId','SupplierOrgId','SupplierRole','SuppliesToOrgId','SupplierPMId','SupplierExecId','OrgId'] 
        supBody = get_dict(supHeader, supDataBody)
        with open('finalData/projectSupplier.csv', 'a') as SupplierFile:
            supWriter = csv.DictWriter(SupplierFile, fieldnames= supHeader)
            if os.stat('finalData/projectSupplier.csv').st_size > 0:
                pass
            else:
                supWriter.writeheader()
            supWriter.writerow(supBody)
    return orgId