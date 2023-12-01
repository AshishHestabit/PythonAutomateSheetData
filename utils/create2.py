import csv
import os
from dotenv import load_dotenv
from utils.utility import filter_team, get_dict, uid, filter_emp, filter_teamMember , create_emp,date, get_project

load_dotenv()

# Access environment variables
index = int(os.getenv("INDEX"))
# all types pf files data insertion will be here

# create employee from TeamMember sheet
def create_employee(orgId):
    with open('TrimmedData/Team Members.csv') as csvFile:
        Data = csv.reader(csvFile)
        next(Data)
        # header = []
        # EmpBody = []
        dictMemBody = {}
        # memKeys = {'TM001': 'ProjectName', 'TM002': 'TeamName', 'TM003': 'TeamMemberName',
        #            'TM004': 'SupervisorName', 'TM005': 'Role', 'TM006': 'UtilizationontheTeam',
        #            'TM007': 'CommittedUtilization', 'TM008': 'PrimaryDiscipline', 
        #            'TM009': 'ExperienceYears', 'TM010': 'Experiencerelatedtotherole', 
        #            'TM011': 'KeyExperienceAreas', 'TM012': 'Preferstothinkalonefirst', 
        #            'TM013': 'Nextdesiredrole', 'TM014': 'Nextdesiredproject', 'TM015': 'Certifications',
        #            'TM016': 'MBTIPersonalityType', 'TM017': 'OtherPersonalityType', 'TM018': 'Country', 
        #            'TM019': 'State', 'TM020': 'City', 'TM021': 'Age', 'TM022': 'Ethnicity', 'TM023': 'Gender',
        #            'TM024': 'PrimaryWorkspace', 'TM025': 'QualityofWorkspace', 'TM026': 'Educationlevel'}
        
        # swapped_dict = {value: key for key, value in memKeys.items()}
        
        memKeys = {'ProjectName': 'TM001', 'TeamName': 'TM002', 'TeamMemberName': 'TM003',
                   'SupervisorName': 'TM004', 'Role': 'TM005', 'UtilizationontheTeam': 'TM006',
                   'CommittedUtilization': 'TM007', 'PrimaryDiscipline': 'TM008',
                   'ExperienceYears': 'TM009', 'Experiencerelatedtotherole': 'TM010',
                   'KeyExperienceAreas': 'TM011', 'Preferstothinkalonefirst': 'TM012',
                   'Nextdesiredrole': 'TM013', 'Nextdesiredproject': 'TM014', 'Certifications': 'TM015',
                   'MBTIPersonalityType': 'TM016', 'OtherPersonalityType': 'TM017', 'Country': 'TM018',
                   'State': 'TM019', 'City': 'TM020', 'Age': 'TM021', 'Ethnicity': 'TM022', 
                   'Gender': 'TM023', 'PrimaryWorkspace': 'TM024', 'QualityofWorkspace': 'TM025',
                   'Educationlevel': 'TM026'}

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


# Create teams
teamKeys = {'ProjectName':'T001','TeamName':'T002','TeamLeaderName':'T003'}

def create_team(orgId):
    # Create Team
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
TeamMemberKeys = {'Role':'TM005','UtilizationontheTeam':'TM006'}
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
# TssKeys ={'TSS001':'ProjectName','TSS002':'TeamName',
#           'TSS003':'TeamMemberName','TSS004':'y_psuccess',
#           'TSS005':'y_tsuccess','TSS006':'y_cost',
#           'TSS007':'y_budget','TSS008':'y_sched',
#           'TSS009':'tl_collab','TSS010':'tl_rnf',
#           'TSS011':'tl_aware','TSS012':'tl_estand',
#           'TSS013':'tl_input','TSS014':'tl_texp',
#           'TSS015':'tr_bias','TSS016':'tr_tpart',
#           'TSS017':'tr_motive','TSS018':'tr_empathy',
#           'TSS019':'tr_mhealth','TSS020':'tr_dei',
#           'TSS021':'tv_vales','TSS022':'tv_diff',
#           'TSS023':'tv_tteam','TSS024':'tgo_agree',
#           'TSS025':'tgo_impact','TSS026':'tgo_purp',
#           'TSS027':'tgo_snb','TSS028':'trr_agree',
#           'TSS029':'trr_simp','TSS030':'trr_profi',
#           'TSS031':'trr_cedu','TSS032':'trr_skill',
#           'TSS033':'trr_urep','TSS034':'trr_initate'}

TssKeys = {'ProjectName': 'TSS001', 'TeamName': 'TSS002',
           'TeamMemberName': 'TSS003', 'y_psuccess': 'TSS004',
           'y_tsuccess': 'TSS005', 'y_cost': 'TSS006',
           'y_budget': 'TSS007', 'y_sched': 'TSS008',
           'tl_collab': 'TSS009', 'tl_rnf': 'TSS010',
           'tl_aware': 'TSS011', 'tl_estand': 'TSS012',
           'tl_input': 'TSS013', 'tl_texp': 'TSS014',
           'tr_bias': 'TSS015', 'tr_tpart': 'TSS016',
           'tr_motive': 'TSS017', 'tr_empathy': 'TSS018',
           'tr_mhealth': 'TSS019', 'tr_dei': 'TSS020',
           'tv_vales': 'TSS021', 'tv_diff': 'TSS022',
           'tv_tteam': 'TSS023', 'tgo_agree': 'TSS024',
           'tgo_impact': 'TSS025', 'tgo_purp': 'TSS026',
           'tgo_snb': 'TSS027', 'trr_agree': 'TSS028',
           'trr_simp': 'TSS029', 'trr_profi': 'TSS030',
           'trr_cedu': 'TSS031', 'trr_skill': 'TSS032',
           'trr_urep': 'TSS033', 'trr_initate': 'TSS034'}

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
        # print(tssDictBody)
       
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
# DeiKeys = {'DEI001': 'ProjectName', 'DEI002': 'TeamName', 'DEI003': 'TeamMemberName',
#            'DEI004': 'Yourself', 'DEI005': 'Your Team', 'DEI006': 'Your Team Leader',
#            'DEI007': 'Your Suppliers', 'DEI008': 'Your Customer', 'DEI009': 'This Project',
#            'DEI010': 'Your Company', 'DEI011': 'dei_axs_comfort', 'DEI012': 'dei_gol_org',
#            'DEI013': 'dei_gol_oknow', 'DEI014': 'dei_gol_cust', 'DEI015': 'dei_gol_cknow',
#            'DEI016': 'dei_gol_team', 'DEI017': 'dei_gol_supp', 'DEI018': 'dei_gol_progress',
#            'DEI019': 'dei_ldr_suppfocus', 'DEI020': 'dei_ldr_focus', 'DEI021': 'dei_rec_guide',
#            'DEI022': 'dei_rec_effect', 'DEI023': 'dei_rep_report', 'DEI024': 'dei_mnt_org',
#            'DEI025': 'dei_mnt_supp', 'DEI026': 'dei_mnt_parti', 'DEI027': 'dei_trn_org',
#            'DEI028': 'dei_trn_supp', 'DEI029': 'dei_trn_progress', 
#            'DEI030': 'dei_trn_progress_last'}


DeiKeys ={'ProjectName': 'DEI001', 'TeamName': 'DEI002', 'TeamMemberName': 'DEI003',
          'Yourself': 'DEI004', 'Your Team': 'DEI005', 'Your Team Leader': 'DEI006',
          'Your Suppliers': 'DEI007', 'Your Customer': 'DEI008', 'This Project': 'DEI009',
          'Your Company': 'DEI010', 'dei_axs_comfort': 'DEI011', 'dei_gol_org': 'DEI012',
          'dei_gol_oknow': 'DEI013', 'dei_gol_cust': 'DEI014', 'dei_gol_cknow': 'DEI015',
          'dei_gol_team': 'DEI016', 'dei_gol_supp': 'DEI017', 'dei_gol_progress': 'DEI018',
          'dei_ldr_suppfocus': 'DEI019', 'dei_ldr_focus': 'DEI020', 'dei_rec_guide': 'DEI021',
          'dei_rec_effect': 'DEI022', 'dei_rep_report': 'DEI023', 'dei_mnt_org': 'DEI024',
          'dei_mnt_supp': 'DEI025', 'dei_mnt_parti': 'DEI026', 'dei_trn_org': 'DEI027',
          'dei_trn_supp': 'DEI028', 'dei_trn_progress': 'DEI029', 'dei_trn_progress_last': 'DEI030'}

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
EsgKeys = {'ProjectName': 'ESG001', 'TeamName': 'ESG002', 'TeamMemberName': 'ESG003',
          'Yourself': 'ESG004', 'Your Team': 'ESG005', 'Your Team Leader': 'ESG006',
          'Your Suppliers': 'ESG007', 'Your Customer': 'ESG008', 'This Project': 'ESG009',
          'Your Company': 'ESG010','esg_gol_soc_prog': 'ESG011', 'esg_gol_prog': 'ESG012',
          'esg_gol_cust': 'ESG013', 'esg_gol_proj_contri': 'ESG014', 'esg_gol_team': 'ESG015',
          'esg_gol_supp': 'ESG016', 'esg_gol_proj': 'ESG017', 'esg_gol_progress': 'ESG018',
          'esg_gol_value': 'ESG024', 'esg_gol_align': 'ESG025', 'esg_ldr_suppfocus': 'ESG026',
          'esg_ldr_focus': 'ESG027', 'esg_rep_value': 'ESG028', 'esg_rep_company': 'ESG029',
          'esg_rep_report': 'ESG030', 'esg_mnt_org': 'ESG031', 'esg_mnt_supp': 'ESG032',
          'esg_mnt_parti': 'ESG033', 'esg_trn_org': 'ESG034', 'esg_trn_supp': 'ESG035',
          'esg_trn_progress': 'ESG036', 'esg_trn_progress_last': 'ESG037'}

def create_esgRating(empId, OrgId):
    with open('TrimmedData/ESG.csv') as csvFile:
        Data = csv.reader(csvFile)
        esgDictBody ={}
        for row in Data:
            if row[0] in EsgKeys.values():
                esgDictBody[row[0]] = row[index+1]
        esgHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','esg_gol_soc_prog','esg_gol_prog','esg_gol_cust','esg_gol_proj_contri','esg_gol_team','esg_gol_supp','esg_gol_proj','esg_gol_progress','esg_gol_value','esg_gol_align','esg_ldr_suppfocus','esg_ldr_focus','esg_rep_value','esg_rep_company','esg_rep_report','esg_mnt_org','esg_mnt_supp','esg_mnt_parti','esg_trn_org','esg_trn_supp','esg_trn_progress','esg_trn_progress_last']
           
    with open('finalData/esgRating.csv', 'a') as esgFile:
        esgWriter = csv.DictWriter(esgFile, fieldnames= esgHeader) # , fieldnames= esgHeader
        
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
