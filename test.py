from utils.create2 import create_employee, create_team, create_teamMember
from utils.project2 import create_projOrg
from utils.utility import empty_csv_file, get_project, trim_csv

files = ['Project.csv','Teams.csv','Team Members.csv','Member Ratings.csv','DEI.csv','ESG.csv']
for file in files:
    empty_csv_file('TrimmedData/'+file)
    input_csv_file = 'RawData/'+file
    output_csv_file = 'TrimmedData/'+file
    trim_csv(input_csv_file, output_csv_file)
    
files = ['project.csv','employee.csv','team.csv','projectSupplier.csv','organization.csv','ProjectTeamMember.csv','TssRating.csv','deiRating.csv','esgRating.csv']
for file in files:
    empty_csv_file('finalData/'+file)
# create_projOrg()
orgId = create_projOrg()
team = create_team(orgId)
teamId = team['TeamId']

emp = create_employee(orgId)
empId = emp['EmpId']

Project = get_project()
projId = Project['ProjectId']

create_teamMember(empId, projId, orgId, teamId)