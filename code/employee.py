import csv
import os
from utility.utility import uid

def create_employee(orgId):
    with open('../TrimmedData/Team Members.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        header = []
        EmpBody = []
        i = 0
        for row in Data:
            if i < 26 :
                header.append(row[0].split('\n')[0])
                EmpBody.append(row[3])
                i = i+1
            else:
                break
        
        
    # create employee  

    # orgId =  '5030c79d-e881-492f-982c-3920ddb630fe'    
    with open('../finalData/employee.csv', 'a') as EmpFile:
        empWriter = csv.writer(EmpFile)
        
        if os.stat('../finalData/employee.csv').st_size > 0:
            pass
        else:
            empHeader = ['EmpId','EmpOrgId','Name','SupervisorID','SupervisorName','CommittedUtilization','PrimaryDiscipline','ExperienceYears','KeyExperienceAreas','PrefersToThinkAloneorTeam','NextDesiredRole','NextDesiredProject','Certification','MBTI','Age','Ethnicity','Gender','PrimaryWorkspace','QualityofWorkspace','Education level','EmpType','StartDate','Role','Utilization on the Team','Experience related to the role']
            empWriter.writerow(empHeader)
        supId =  ''
        supName = EmpBody[3]
        empId = uid()
        empBody = [empId , orgId , EmpBody[2],supId , supName ,EmpBody[6],EmpBody[7],EmpBody[8],EmpBody[10],EmpBody[11],EmpBody[12],EmpBody[13],EmpBody[14],EmpBody[15],EmpBody[19],EmpBody[20],EmpBody[21],EmpBody[22],EmpBody[23],EmpBody[24]," "," ",EmpBody[4],EmpBody[5],EmpBody[9]]
        empWriter.writerow(empBody)
    return empBody


print(create_employee('1111111'))        