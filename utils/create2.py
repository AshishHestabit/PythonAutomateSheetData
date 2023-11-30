import csv
import os
from utils.utility import filter_team, get_dict, uid, filter_emp, filter_teamMember , create_emp,date, get_project
# all types pf files data insertion will be here

# create employee from TeamMember sheet
def create_employee(orgId):
    with open('TrimmedData/Team Members.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        header = []
        EmpBody = []
        dictMemBody = {}
        memKeys = {'TM001': 'ProjectName', 'TM002': 'TeamName', 'TM003': 'TeamMemberName',
                   'TM004': 'SupervisorName', 'TM005': 'Role', 'TM006': 'UtilizationontheTeam',
                   'TM007': 'CommittedUtilization', 'TM008': 'PrimaryDiscipline', 
                   'TM009': 'ExperienceYears', 'TM010': 'Experiencerelatedtotherole', 
                   'TM011': 'KeyExperienceAreas', 'TM012': 'Preferstothinkalonefirst', 
                   'TM013': 'Nextdesiredrole', 'TM014': 'Nextdesiredproject', 'TM015': 'Certifications',
                   'TM016': 'MBTIPersonalityType', 'TM017': 'OtherPersonalityType', 'TM018': 'Country', 
                   'TM019': 'State', 'TM020': 'City', 'TM021': 'Age', 'TM022': 'Ethnicity', 'TM023': 'Gender',
                   'TM024': 'PrimaryWorkspace', 'TM025': 'QualityofWorkspace', 'TM026': 'Educationlevel'}
       
        for row in Data:
            dictMemBody[row[0]] = row[4]

    with open('finalData/employee.csv', 'a') as EmpFile:
        empWriter = csv.writer(EmpFile)
        empHeader = ['EmpId','EmpOrgId','Name','SupervisorID','SupervisorName','CommittedUtilization','PrimaryDiscipline','ExperienceYears','KeyExperienceAreas','PrefersToThinkAloneorTeam','NextDesiredRole','NextDesiredProject','Certification','MBTI','Age','Ethnicity','Gender','PrimaryWorkspace','QualityofWorkspace','Education level','EmpType','StartDate','Role','Utilization on the Team','Experience related to the role']
        if os.stat('finalData/employee.csv').st_size > 0:
            pass
        else:
            empWriter.writerow(empHeader)
        sup = filter_emp('finalData/employee.csv', ['EmpOrgId','Name'], [orgId, dictMemBody['TM004']])
        if sup['status'] == False:
            supData = create_emp(dictMemBody['TM004'],orgId)
            supId = supData[0]
        else:
            supId = sup['data']['EmpId']
        
        supName = dictMemBody['TM004']
        empId = uid()
        result = filter_emp('finalData/employee.csv', ['EmpOrgId','Name'], [orgId,dictMemBody['TM003']])
        if result['status'] == False:
            empBody = [empId , orgId , dictMemBody['TM003'],supId , supName ,dictMemBody['TM007'].strip('%'),dictMemBody['TM008'],dictMemBody['TM009'],dictMemBody['TM011'],dictMemBody['TM012'],dictMemBody['TM013'],dictMemBody['TM014'],dictMemBody['TM015'],dictMemBody['TM016'],dictMemBody['TM020'],dictMemBody['TM021'],dictMemBody['TM022'],dictMemBody['TM023'],dictMemBody['TM024'],dictMemBody['TM025']," "," ",dictMemBody['TM005'],dictMemBody['TM006'].strip('%'),dictMemBody['TM010']]
            empDictBody = get_dict(empHeader, empBody)
            empWriter.writerow(empBody)
    return empDictBody


# Create teams
teamKeys = {'T001':'ProjectName','T002':'TeamName','T003':'TeamLeaderName'}

def create_team(orgId):
    # Create Team
    with open('TrimmedData/Teams.csv', 'r') as TeamCsvFile:
        TeamData = csv.reader(TeamCsvFile)
        next(TeamData)
        dictTeamBody = {}
        i = 0
        for row in TeamData:
            dictTeamBody[row[0]] = row[2]
        # print(dictTeamBody)
       
    TeamHeader = ['ProjectId','OrgId','TeamId','TeamName','TeamLeadId']
    result = filter_team('finalData/team.csv',['OrgId','TeamName'],[orgId, dictTeamBody['T002']]) 
    if result['status'] == False :
        with open('finalData/team.csv', 'a') as TeamFile:
            teamWriter = csv.writer(TeamFile)
            if os.stat('finalData/team.csv').st_size > 0:
                pass
            else:
                teamWriter.writerow(TeamHeader)
            
            project = get_project()
            TeamId = uid()
            TeamBody = [project['ProjectId'],orgId,TeamId, dictTeamBody['T002']]
                
            input_csv_file = 'finalData/employee.csv'
            filter_field = ['EmpOrgId','Name']
            filter_value = [orgId, dictTeamBody['T003']] # team leader name  dictTeamBody['T003']
            empData = filter_emp(input_csv_file, filter_field, filter_value) 
            if empData['status']:
                TeamBody.append(empData['data']['EmpId'])
            else :
                emp = create_emp(dictTeamBody['T003'], orgId)
                TeamBody.append(emp[0])
                
            teamWriter.writerow(TeamBody)
            TeamDictBody = get_dict(TeamHeader, TeamBody)
    else:
        TeamDictBody = result['data']
    return TeamDictBody

# Create project Team Members
TeamMemberKeys = {'TM005':'Role','TM006': 'UtilizationontheTeam'}
def create_teamMember(EmpId, ProjectId, OrgId, TeamId):
    with open('TrimmedData/Team Members.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        TmDictBody = {}
        for row in Data:
            if row[0] in TeamMemberKeys.keys():
                TmDictBody[row[0]] = row[4]

    with open('finalData/ProjectTeamMember.csv', 'a') as memberFile:
        memberWriter = csv.writer(memberFile)
        if os.stat('finalData/ProjectTeamMember.csv').st_size > 0:
            pass
        else:
            memberHeader = ['MemberId','ProjectId','OrgId','TeamId','RoleName','PerUtilizationOnTheTeam']
            memberWriter.writerow(memberHeader)
        
        result = filter_teamMember('finalData/ProjectTeamMember.csv', ['MemberId','ProjectId','OrgId','TeamId'], [EmpId ,ProjectId, OrgId , TeamId])
        if result['status'] == False:
            memberBody = [EmpId, ProjectId, OrgId , TeamId,TmDictBody['TM005'],TmDictBody['TM006'].strip('%')]
            memberWriter.writerow(memberBody)
            DictMemberBody = get_dict(memberHeader, memberBody)
            # print(DictMemberBody)
        else:
            DictMemberBody = result['data']
    return DictMemberBody
    
  
# create Tss Rating 
TssKeys ={'TSS001':'ProjectName','TSS002':'TeamName',
          'TSS003':'TeamMemberName','TSS004':'y_psuccess',
          'TSS005':'y_tsuccess','TSS006':'y_cost',
          'TSS007':'y_budget','TSS008':'y_sched',
          'TSS009':'tl_collab','TSS010':'tl_rnf',
          'TSS011':'tl_aware','TSS012':'tl_estand',
          'TSS013':'tl_input','TSS014':'tl_texp',
          'TSS015':'tr_bias','TSS016':'tr_tpart',
          'TSS017':'tr_motive','TSS018':'tr_empathy',
          'TSS019':'tr_mhealth','TSS020':'tr_dei',
          'TSS021':'tv_vales','TSS022':'tv_diff',
          'TSS023':'tv_tteam','TSS024':'tgo_agree',
          'TSS025':'tgo_impact','TSS026':'tgo_purp',
          'TSS027':'tgo_snb','TSS028':'trr_agree',
          'TSS029':'trr_simp','TSS030':'trr_profi',
          'TSS031':'trr_cedu','TSS032':'trr_skill',
          'TSS033':'trr_urep','TSS034':'trr_initate'}
# def create_tssRating(ratedById, OrgId):
#     with open('TrimmedData/Member Ratings.csv') as csvFile:
#         Data = csv.reader(csvFile)
#         next(Data)
#         next(Data)
#         next(Data)
#         tssBody = [[],[],[],[],[],[],[]]
#         tssDictBody = {}
#         emp= []
#         for row in Data:
#             if row[0] == 'TSS003':
#                 findIndex = row
#                 emp =[e for e in row[3:] if not e.startswith('<Member')]
#                 for mem in emp:
#                     tssDictBody[mem] = {}
#             else:
#                 for mem in emp:
#                     tssDictBody[mem][row[0]] = row[findIndex.index(mem)]
#             # tssDictBody[0][row[0]]= row[3].strip('%')
#             # tssDictBody[1][row[0]]= row[4].strip('%')
#             # tssDictBody[2][row[0]]= row[5].strip('%')
#             # tssDictBody[3][row[0]]= row[6].strip('%')
#             # tssDictBody[4][row[0]]= row[7].strip('%')
#             # tssDictBody[5][row[0]]= row[8].strip('%')
#             # tssDictBody[6][row[0]]= row[9].strip('%')
#         # print(len(emp.count('<Member>')))
#         print(tssDictBody['Andy Williamson'])
        
            
            
            
#             # tssBody[0].append(row[2].strip('%'))
#             # tssBody[1].append(row[3].strip('%'))
#             # tssBody[2].append(row[4].strip('%'))
#             # tssBody[3].append(row[5].strip('%'))
#             # tssBody[4].append(row[6].strip('%'))
#             # tssBody[5].append(row[7].strip('%'))
#             # tssBody[6].append(row[8].strip('%'))
      
    
#     with open('finalData/TssRating.csv', 'a') as tssFile:
#         tssWriter = csv.writer(tssFile)
        
#         if os.stat('finalData/TssRating.csv').st_size > 0:
#             pass
#         else:
#             tssHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','y_psuccess','y_tsuccess','y_cost','y_budget','y_sched','tl_collab','tl_rnf','tl_aware','tl_estand','tl_input','tl_texp','tr_bias','tr_tpart','tr_motive','tr_empathy','tr_mhealth','tr_dei','tv_vales','tv_diff','tv_tteam','tgo_agree','tgo_impact','tgo_purp','tgo_snb','trr_agree','trr_simp','trr_profi','trr_cedu','trr_skill','trr_urep','trr_initate']
#             tssWriter.writerow(tssHeader)
        
#         for empRating in tssDictBody:
#             result = filter_emp('finalData/employee.csv', ['EmpOrgId','Name'], [OrgId,empRating])
#             if result['status'] == False:
#                 emp = create_emp(empRating,OrgId)
#                 empId = emp[0]
#             else:
#                 empId = result['data']['EmpId']
                
#             # empRating.pop(0)
#             for rating in tssDictBody[empRating]:
#                 empData = list(rating.values())
#                 empRating.insert(0,empId)
#             # tssDictBody[empRating]['EmpId'] = empId
#                 empRating[1:1] = OrgId,ratedById,OrgId , date()
#                 tssWriter.writerow(empRating)
#     return tssDictBody


            
"""    
    
# create DEI Rating 

def create_deiRating(empId, OrgId):
    with open('TrimmedData/DEI.csv') as csvFile:
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
            
    with open('finalData/deiRating.csv', 'a') as deiFile:
        deiWriter = csv.writer(deiFile)
        
        if os.stat('finalData/deiRating.csv').st_size > 0:
            pass
        else:
            deiHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','dei_axs_comfort','dei_gol_org','dei_gol_oknow','dei_gol_cust','dei_gol_cknow','dei_gol_team','dei_gol_supp','dei_gol_progress','dei_ldr_suppfocus','dei_ldr_focus','dei_rec_guide','dei_rec_effect','dei_rep_report','dei_mnt_org','dei_mnt_supp','dei_mnt_parti','dei_trn_org','dei_trn_supp','dei_trn_progress','dei_trn_progress_last']
            deiWriter.writerow(deiHeader)
        
        deiWriter.writerow(deiBody)
    return deiBody



# Create ESG Rating

def create_esgRating(empId, OrgId):
    with open('TrimmedData/ESG.csv') as csvFile:
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
            
    with open('finalData/esgRating.csv', 'a') as esgFile:
        esgWriter = csv.writer(esgFile)
        
        if os.stat('finalData/esgRating.csv').st_size > 0:
            pass
        else:
            esgHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','esg_gol_soc_prog','esg_gol_prog','esg_gol_cust','esg_gol_proj_contri','esg_gol_team','esg_gol_supp','esg_gol_proj','esg_gol_progress','esg_gol_value','esg_gol_align','esg_ldr_suppfocus','esg_ldr_focus','esg_rep_value','esg_rep_company','esg_rep_report','esg_mnt_org','esg_mnt_supp','esg_mnt_parti','esg_trn_org','esg_trn_supp','esg_trn_progress','esg_trn_progress_last']
            esgWriter.writerow(esgHeader)
        
        esgWriter.writerow(esgBody)
    return esgBody

"""