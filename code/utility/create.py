import csv
import os
from utility.utility import uid, filter_emp, filter_teamMember , create_emp,date
# all types pf files data insertion will be here

# create employee from TeamMember sheet
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
        result = filter_emp('../finalData/employee.csv', ['EmpOrgId','Name'], [orgId,EmpBody[2]])
        if result['status'] == False:
            empBody = [empId , orgId , EmpBody[2],supId , supName ,EmpBody[6].strip('%'),EmpBody[7],EmpBody[8],EmpBody[10],EmpBody[11],EmpBody[12],EmpBody[13],EmpBody[14],EmpBody[15],EmpBody[19],EmpBody[20],EmpBody[21],EmpBody[22],EmpBody[23],EmpBody[24]," "," ",EmpBody[4],EmpBody[5].strip('%'),EmpBody[9]]
            empWriter.writerow(empBody)
    return empBody


# Create project Team Members
def create_teamMember(EmpId, ProjectId, OrgId, TeamId):
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
    
    with open('../finalData/ProjectTeamMember.csv', 'a') as memberFile:
        memberWriter = csv.writer(memberFile)
        
        if os.stat('../finalData/ProjectTeamMember.csv').st_size > 0:
            pass
        else:
            memberHeader = ['MemberId','ProjectId','OrgId','TeamId','RoleName','PerUtilizationOnTheTeam']
            memberWriter.writerow(memberHeader)
        
        result = filter_teamMember('../finalData/ProjectTeamMember.csv', ['MemberId','ProjectId','OrgId','TeamId'], [EmpId ,ProjectId, OrgId , TeamId])
        if result['status'] == False:
            memberBody = [EmpId ,ProjectId, OrgId , TeamId,EmpBody[4],EmpBody[5].strip('%')]
            memberWriter.writerow(memberBody)
    return memberBody
    
    
# create Tss Rating 

def create_tssRating(ratedById, OrgId):
    with open('../TrimmedData/Member Ratings.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        next(Data)
        next(Data)
        tssBody = [[],[],[],[],[],[],[]]
        i = 0
        for row in Data:
            if i < 34 :
                tssBody[0].append(row[2])
                tssBody[1].append(row[3])
                tssBody[2].append(row[4])
                tssBody[3].append(row[5])
                tssBody[4].append(row[6])
                tssBody[5].append(row[7])
                tssBody[6].append(row[8])
                i = i+1
            else:
                break
            
    with open('../finalData/TssRating.csv', 'a') as tssFile:
        tssWriter = csv.writer(tssFile)
        
        if os.stat('../finalData/TssRating.csv').st_size > 0:
            pass
        else:
            tssHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','y_psuccess','y_tsuccess','y_cost','y_budget','y_sched','tl_collab','tl_rnf','tl_aware','tl_estand','tl_input','tl_texp','tr_bias','tr_tpart','tr_motive','tr_empathy','tr_mhealth','tr_dei','tv_vales','tv_diff','tv_tteam','tgo_agree','tgo_impact','tgo_purp','tgo_snb','trr_agree','trr_simp','trr_profi','trr_cedu','trr_skill','trr_urep','trr_initate']
            tssWriter.writerow(tssHeader)
        
        for empRating in tssBody:
            result = filter_emp('../finalData/employee.csv', ['EmpOrgId','Name'], [OrgId,empRating[0]])
            if result['status'] == False:
                emp = create_emp(empRating[0],OrgId)
                empId = emp[0]
            else:
                empId = result['data']['EmpId']
                
            empRating.pop(0)
            empRating.insert(0,empId)
            # empRating.insert(1,OrgId,ratedById,OrgId , '')
            empRating[1:1] = OrgId,ratedById,OrgId , date()
            tssWriter.writerow(empRating)
    return tssBody



    
# create DEI Rating 

def create_deiRating(empId, OrgId):
    with open('../TrimmedData/DEI.csv') as csvFile:
        Data = csv.reader(csvFile)
        count=0
        while(count < 11):
            next(Data)
            count = count+1
        deiBody = [empId, OrgId,empId,OrgId , date()]
        i = 0
        for row in Data:
            if i < 20:
                deiBody.append(row[4])
                i = i+1
            else:
                break
            
    with open('../finalData/deiRating.csv', 'a') as deiFile:
        deiWriter = csv.writer(deiFile)
        
        if os.stat('../finalData/deiRating.csv').st_size > 0:
            pass
        else:
            deiHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','dei_axs_comfort','dei_gol_org','dei_gol_oknow','dei_gol_cust','dei_gol_cknow','dei_gol_team','dei_gol_supp','dei_gol_progress','dei_ldr_suppfocus','dei_ldr_focus','dei_rec_guide','dei_rec_effect','dei_rep_report','dei_mnt_org','dei_mnt_supp','dei_mnt_parti','dei_trn_org','dei_trn_supp','dei_trn_progress','dei_trn_progress_last']
            deiWriter.writerow(deiHeader)
        
        deiWriter.writerow(deiBody)
    return deiBody



# Create ESG Rating

def create_esgRating(empId, OrgId):
    with open('../TrimmedData/ESG.csv') as csvFile:
        Data = csv.reader(csvFile)
        count=0
        while(count < 11):
            next(Data)
            count = count+1
        esgBody = [empId, OrgId, empId, OrgId, date()]
        i = 0
        for row in Data:
            if i < 27:
                if i > 7  and i < 13:
                    pass
                else:
                    esgBody.append(row[4])
                i = i+1
            else:
                break
            
    with open('../finalData/esgRating.csv', 'a') as esgFile:
        esgWriter = csv.writer(esgFile)
        
        if os.stat('../finalData/esgRating.csv').st_size > 0:
            pass
        else:
            esgHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','esg_gol_soc_prog','esg_gol_prog','esg_gol_cust','esg_gol_proj_contri','esg_gol_team','esg_gol_supp','esg_gol_proj','esg_gol_progress','esg_gol_value','esg_gol_align','esg_ldr_suppfocus','esg_ldr_focus','esg_rep_value','esg_rep_company','esg_rep_report','esg_mnt_org','esg_mnt_supp','esg_mnt_parti','esg_trn_org','esg_trn_supp','esg_trn_progress','esg_trn_progress_last']
            esgWriter.writerow(esgHeader)
        
        esgWriter.writerow(esgBody)
    return esgBody

