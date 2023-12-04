from utils.create import create_deiRating, create_employee, create_esgRating, create_team, create_teamMember, create_tssRating
from utils.project import create_projOrg
from utils.utility import empty_csv_file, get_project, trim_csv

files = ['Project.csv','Teams.csv','Team Members.csv','Member Ratings.csv','DEI.csv','ESG.csv']
for file in files:
    empty_csv_file('TrimmedData/'+file)
    input_csv_file = 'RawData/'+file
    output_csv_file = 'TrimmedData/'+file
    trim_csv(input_csv_file, output_csv_file)
    
files = ['project.csv','employee.csv','team.csv','projectSupplier.csv','organization.csv','projectTeamMember.csv','tssRating.csv','deiRating.csv','esgRating.csv']
for file in files:
    empty_csv_file('FinalData/'+file)
    
    
# create_projOrg()
orgId = create_projOrg()
team = create_team(orgId)
teamId = team['TeamId']

emp = create_employee(orgId)
empId = emp['EmpId']

Project = get_project()
projId = Project['ProjectId']
create_teamMember(empId, projId, orgId, teamId)

create_tssRating(empId, orgId)

create_deiRating(empId, orgId)

create_esgRating(empId, orgId)


# api_url = 'https://tsp-v-001.bubbleapps.io/version-hesta/api/1.1/wf/post-project'
# data = Project 
# response = requests.post(api_url, json = data)
# if response.status_code == 200:
#     data = response.json()
#     print(data)

# json_data = json.dumps(emp, indent=2)
# print(json_data) 