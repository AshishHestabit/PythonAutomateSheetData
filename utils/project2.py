import csv, os
from utils.utility import create_emp, get_project, uid, filter_org,filter_project,filter_supOrg


def create_projOrg():
    with open('TrimmedData/Project.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        dictBody ={}
        i = 0
        keys = {'P001':'ProjectName','P002':'OwnerOrganizationName','P003':'OwnerExecutiveName','P004':'OwnerManagerName','P005':'SupplierOrganizationName','P006':'SupplierExecutiveName','P007':'SupplierLeaderName','P008':'MyOrganizationName','P009':'MyOrganizationExecutiveName','P010':'MyOrganizationLeaderName','P011':'SuupliesToOrganization','P012':'ProjectBudget','P013':'ProjectComplexity'}

        for row in Data:
            dictBody[row[0]] = row[2]
        # print(dictBody)
           
        
    orgData = filter_org(dictBody['P008']) 
        
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
            orgBody = [orgId , dictBody['P008']," "," "," "]
            Orgwriter.writerow(orgBody)
            
            # create Owner organization
            if dictBody['P008'] != dictBody['P002']:
                OwnerOrgId = uid()
                orgBody = [OwnerOrgId , dictBody['P002']," "," "," "]
                Orgwriter.writerow(orgBody)
            else:
                OwnerOrgId = orgId
        

    
    projData = filter_project(dictBody['P001'])
    if projData['status'] == False:
          
        with open('finalData/project.csv', 'a') as ProjectFile:
            proWriter = csv.writer(ProjectFile)
            
            if os.stat('finalData/project.csv').st_size > 0:
                pass
            else:
                projectHeader = ['ProjectId','ProjectName','OwnerOrgId','ProjectManagerId','ProjectExecId']
                proWriter.writerow(projectHeader)
                
            empDict = {dictBody['P003']:orgId, dictBody['P004']:orgId}
            empList =[]
            for emp in empDict:
                employee = create_emp(emp , empDict[emp])
                empList.append(employee[0])
                
            ProjectId = uid()
            projectBody = [ProjectId , dictBody['P001'], OwnerOrgId, empList[0], empList[1]]
            # projectBody = [ProjectId , body[0], None, None, None] #it's temporary data
            proWriter.writerow(projectBody)
            
            
    project = get_project()        
    supData = filter_supOrg(orgId,project['ProjectId'])
    if supData['status'] == False and dictBody['P002'] != dictBody['P008']:  
          
        empList =[]
        empDict = {dictBody['P007']:orgId,dictBody['P006']:orgId} 
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