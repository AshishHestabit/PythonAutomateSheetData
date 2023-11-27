# import uuid

# def generate_short_id(length=8):
#     # Generate a UUID
#     new_uuid = uuid.uuid4()

#     # Convert the UUID to a hex string and truncate to the desired length
#     short_id = str(new_uuid.hex)[:length]

#     return short_id

# # Example usage
# short_id = generate_short_id()
# print(short_id)
import csv
with open('../finalData/project.csv', 'r') as ProjectData:
        ProjData = csv.DictReader(ProjectData)
        d = next(ProjData)
        print(d['ProjectId'])

