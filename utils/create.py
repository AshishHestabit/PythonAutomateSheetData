import csv
import os
from dotenv import load_dotenv
from utils.utility import filter_team, get_dict, uid, filter_emp, filter_teamMember , create_emp,date, get_project
from config import memKeys, teamKeys, TeamMemberKeys, EsgKeys, TssKeys, DeiKeys

load_dotenv()

# Access environment variables
index = int(os.getenv("INDEX"))

# create employee from TeamMember sheet
def create_employee(orgId):
    with open('TrimmedData/Team Members.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        dictMemBody = {}
       
        for row in Data:
            if row[0] in memKeys.values():
                dictMemBody[row[0]] = row[index]

    with open('finalData/employee.csv', 'a') as EmpFile:
        empHeader = ['EmpId','EmpOrgId','Name','SupervisorID','SupervisorName','CommittedUtilization','PrimaryDiscipline','ExperienceYears','KeyExperienceAreas','PrefersToThinkAloneorTeam','NextDesiredRole','NextDesiredProject','Certification','MBTI','Age','Ethnicity','Gender','PrimaryWorkspace','QualityofWorkspace','Education level','EmpType','StartDate','Role','Utilization on the Team','Experience related to the role']
        empWriter = csv.DictWriter(EmpFile, fieldnames=empHeader)
        if os.stat('finalData/employee.csv').st_size > 0:
            pass
        else:
            empWriter.writeheader()
        sup = filter_emp('finalData/employee.csv', ['EmpOrgId','Name'], [orgId, dictMemBody[memKeys['SupervisorName']]])
        if sup['status'] == False:
            supData = create_emp(dictMemBody[memKeys['SupervisorName']],orgId)
            supId = supData[0]
        else:
            supId = sup['data']['EmpId']
        
        supName = dictMemBody[memKeys['SupervisorName']]
        empId = uid()
        result = filter_emp('finalData/employee.csv', ['EmpOrgId','Name'], [orgId,dictMemBody[memKeys['TeamMemberName']]])
        if result['status'] == False:
            empBody = [empId , orgId , dictMemBody[memKeys['TeamMemberName']],supId , supName ,dictMemBody[memKeys['CommittedUtilization']].strip('%'),dictMemBody[memKeys['PrimaryDiscipline']],dictMemBody[memKeys['ExperienceYears']],dictMemBody[memKeys['KeyExperienceAreas']],dictMemBody[memKeys['Preferstothinkalonefirst']],dictMemBody[memKeys['Nextdesiredrole']],dictMemBody[memKeys['Nextdesiredproject']],dictMemBody[memKeys['Certifications']],dictMemBody[memKeys['MBTIPersonalityType']],dictMemBody[memKeys['Age']],dictMemBody[memKeys['Ethnicity']],dictMemBody[memKeys['Gender']],dictMemBody[memKeys['PrimaryWorkspace']],dictMemBody[memKeys['QualityofWorkspace']],dictMemBody[memKeys['Educationlevel']]," "," ",dictMemBody[memKeys['Role']],dictMemBody[memKeys['UtilizationontheTeam']].strip('%'),dictMemBody[memKeys['Experiencerelatedtotherole']]]
            empDictBody = get_dict(empHeader, empBody)
            empWriter.writerow(empDictBody)
    return empDictBody


# Create Team

def create_team(orgId):
    with open('TrimmedData/Teams.csv', 'r') as TeamCsvFile:
        TeamData = csv.reader(TeamCsvFile)
        next(TeamData)
        dictTeamBody = {}
        for row in TeamData:
            if row[0] in teamKeys.values():
                dictTeamBody[row[0]] = row[2]
       
    TeamHeader = ['ProjectId','OrgId','TeamId','TeamName','TeamLeadId']
    result = filter_team('finalData/team.csv',['OrgId','TeamName'],[orgId, dictTeamBody['T002']]) 
    if result['status'] == False :
        with open('finalData/team.csv', 'a') as TeamFile:
            teamWriter = csv.DictWriter(TeamFile, fieldnames = TeamHeader)
            if os.stat('finalData/team.csv').st_size > 0:
                pass
            else:
                teamWriter.writeheader()
            
            project = get_project()
            TeamId = uid()
            TeamBody = [project['ProjectId'],orgId,TeamId, dictTeamBody[teamKeys['TeamName']]]
                
            input_csv_file = 'finalData/employee.csv'
            filter_field = ['EmpOrgId','Name']
            filter_value = [orgId, dictTeamBody[teamKeys['TeamLeaderName']]] # team leader name  dictTeamBody['T003']
            empData = filter_emp(input_csv_file, filter_field, filter_value) 
            if empData['status']:
                TeamBody.append(empData['data']['EmpId'])
            else :
                emp = create_emp(dictTeamBody[teamKeys['TeamLeaderName']], orgId)
                TeamBody.append(emp[0])
                
            TeamDictBody = get_dict(TeamHeader, TeamBody)
            teamWriter.writerow(TeamDictBody)
    else:
        TeamDictBody = result['data']
    return TeamDictBody

# Create project Team Members
def create_teamMember(EmpId, ProjectId, OrgId, TeamId):
    with open('TrimmedData/Team Members.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        TmDictBody = {}
        for row in Data:
            for row[0] in TeamMemberKeys.values():
                TmDictBody[row[0]] = row[index]

    with open('finalData/ProjectTeamMember.csv', 'a') as memberFile:
        memberHeader = ['MemberId','ProjectId','OrgId','TeamId','RoleName','PerUtilizationOnTheTeam']
        memberWriter = csv.DictWriter(memberFile, fieldnames= memberHeader)
        if os.stat('finalData/ProjectTeamMember.csv').st_size > 0:
            pass
        else:
            memberWriter.writeheader()
        
        result = filter_teamMember('finalData/ProjectTeamMember.csv', ['MemberId','ProjectId','OrgId','TeamId'], [EmpId ,ProjectId, OrgId , TeamId])
        if result['status'] == False:
            memberBody = [EmpId, ProjectId, OrgId , TeamId,TmDictBody[TeamMemberKeys['Role']],TmDictBody[TeamMemberKeys['UtilizationontheTeam']].strip('%')]
            DictMemberBody = get_dict(memberHeader, memberBody)
            memberWriter.writerow(DictMemberBody)
        else:
            DictMemberBody = result['data']
    return DictMemberBody
    
  
# create Tss Rating 

def create_tssRating(ratedById, OrgId):
    with open('TrimmedData/Member Ratings.csv') as csvFile:
        Data = csv.reader(csvFile)
        tssDictBody = {}
        emp= []
        for row in Data:
            if row[0] in TssKeys.values():
                if row[0] == 'TSS003':
                    findIndex = row
                    emp =[e for e in row[3:] if not e.startswith('<Member')]
                    for mem in emp:
                        tssDictBody[mem] = {}
                else:
                    for mem in emp:
                        tssDictBody[mem][row[0]] = row[findIndex.index(mem)]
       
    with open('finalData/TssRating.csv', 'a') as tssFile:
        tssHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','y_psuccess','y_tsuccess','y_cost','y_budget','y_sched','tl_collab','tl_rnf','tl_aware','tl_estand','tl_input','tl_texp','tr_bias','tr_tpart','tr_motive','tr_empathy','tr_mhealth','tr_dei','tv_vales','tv_diff','tv_tteam','tgo_agree','tgo_impact','tgo_purp','tgo_snb','trr_agree','trr_simp','trr_profi','trr_cedu','trr_skill','trr_urep','trr_initate']
        tssWriter = csv.DictWriter(tssFile,fieldnames = tssHeader)
        if os.stat('finalData/TssRating.csv').st_size > 0:
            pass
        else:
            tssWriter.writeheader()
        
        for key, value in tssDictBody.items():
            result = filter_emp('finalData/employee.csv', ['EmpOrgId','Name'], [OrgId,key])
            if result['status'] == False:
                emp = create_emp(key,OrgId)
                empId = emp[0]
            else:
                empId = result['data']['EmpId']
                
            empData = {
                'EmpId':empId,'OrgId':OrgId,'RatedById':ratedById,'RatedByOrgId':OrgId,'RatingDate':date()
            }
            for i in tssHeader[5:]:
                empData[i] = value[TssKeys[i]]
            tssWriter.writerow(empData)
    return tssDictBody


       
    
# create DEI Rating 

def create_deiRating(empId, OrgId):
    with open('TrimmedData/DEI.csv') as csvFile:
        Data = csv.reader(csvFile)
        deiDictBody ={}
        for row in Data:
            if row[0] in DeiKeys.values():
                deiDictBody[row[0]] = row[index+1]
            
    with open('finalData/deiRating.csv', 'a') as deiFile:
        deiHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','dei_axs_comfort','dei_gol_org','dei_gol_oknow','dei_gol_cust','dei_gol_cknow','dei_gol_team','dei_gol_supp','dei_gol_progress','dei_ldr_suppfocus','dei_ldr_focus','dei_rec_guide','dei_rec_effect','dei_rep_report','dei_mnt_org','dei_mnt_supp','dei_mnt_parti','dei_trn_org','dei_trn_supp','dei_trn_progress','dei_trn_progress_last']
        deiWriter = csv.DictWriter(deiFile, fieldnames= deiHeader)
        if os.stat('finalData/deiRating.csv').st_size > 0:
            pass
        else:
            deiWriter.writeheader()
            
        deiBody = {
            'EmpId':empId,'OrgId':OrgId,'RatedById':empId,'RatedByOrgId':OrgId,'RatingDate':date()
        }
        for i in deiHeader[5:]:
            deiBody[i] = deiDictBody[DeiKeys[i]]
        
        deiWriter.writerow(deiBody)
    return deiBody
      
# Create ESG Rating from ESG019 to ESG023 we don't have keys in database so we neglected here

def create_esgRating(empId, OrgId):
    with open('TrimmedData/ESG.csv') as csvFile:
        Data = csv.reader(csvFile)
        esgDictBody ={}
        for row in Data:
            if row[0] in EsgKeys.values():
                esgDictBody[row[0]] = row[index+1]
        esgHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','esg_gol_soc_prog','esg_gol_prog','esg_gol_cust','esg_gol_proj_contri','esg_gol_team','esg_gol_supp','esg_gol_proj','esg_gol_progress','esg_gol_value','esg_gol_align','esg_ldr_suppfocus','esg_ldr_focus','esg_rep_value','esg_rep_company','esg_rep_report','esg_mnt_org','esg_mnt_supp','esg_mnt_parti','esg_trn_org','esg_trn_supp','esg_trn_progress','esg_trn_progress_last']
           
    with open('finalData/esgRating.csv', 'a') as esgFile:
        esgWriter = csv.DictWriter(esgFile, fieldnames= esgHeader)
        
        if os.stat('finalData/esgRating.csv').st_size > 0:
            pass
        else:
            esgWriter.writeheader()
            
        esgBody = {
            'EmpId':empId,'OrgId':OrgId,'RatedById':empId,'RatedByOrgId':OrgId,'RatingDate':date()
        }
        for i in esgHeader[5:]:
            esgBody[i] = esgDictBody[EsgKeys[i]]
        esgWriter.writerow(esgBody)
    return esgBody
