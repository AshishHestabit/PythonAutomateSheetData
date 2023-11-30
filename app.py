import csv
import os ,requests
from utils.utility import empty_csv_file, get_project, trim_csv
from utils.create import create_employee ,create_teamMember , create_tssRating, create_deiRating, create_esgRating, create_team
from utils.project import create_projOrg
 
# Trim all the raw csv files data
 
files = ['Project.csv','Teams.csv','Team Members.csv','Member Ratings.csv','DEI.csv','ESG.csv']
for file in files:
    empty_csv_file('TrimmedData/'+file)
    input_csv_file = 'RawData/'+file
    output_csv_file = 'TrimmedData/'+file
    trim_csv(input_csv_file, output_csv_file)
 
 
# Empty all the final csv file

files = ['project.csv','employee.csv','team.csv','projectSupplier.csv','organization.csv','ProjectTeamMember.csv','TssRating.csv','deiRating.csv','esgRating.csv']
for file in files:
    empty_csv_file('finalData/'+file)


# Create Project, Organization and Project Supplier
orgId = create_projOrg()

team = create_team(orgId)
teamId = team[2]

emp = create_employee(orgId)
empId = emp[0]

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