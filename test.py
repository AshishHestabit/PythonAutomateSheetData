from utils.create2 import create_employee, create_team, create_teamMember
from utils.project2 import create_projOrg
from utils.utility import empty_csv_file, get_project


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