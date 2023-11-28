# def create_esgRating(empId, OrgId):
#     with open('../TrimmedData/esg.csv') as csvFile:
#         Data = csv.reader(csvFile)
#         count=0
#         while(count < 11):
#             next(Data)
#             count = count+1
#         esgBody = []
#         i = 0
#         for row in Data:
#             if i < 20:
#                 esgBody.append(row[4])
#                 i = i+1
#             else:
#                 break
            
#     with open('../finalData/esgRating.csv', 'a') as esgFile:
#         esgWriter = csv.writer(esgFile)
        
#         if os.stat('../finalData/esgRating.csv').st_size > 0:
#             pass
#         else:
#             esgHeader = ['EmpId','OrgId','RatedById','RatedByOrgId','RatingDate','esg_axs_comfort','esg_gol_org','esg_gol_oknow','esg_gol_cust','esg_gol_cknow','esg_gol_team','esg_gol_supp','esg_gol_progress','esg_ldr_suppfocus','esg_ldr_focus','esg_rec_guide','esg_rec_effect','esg_rep_report','esg_mnt_org','esg_mnt_supp','esg_mnt_parti','esg_trn_org','esg_trn_supp','esg_trn_progress','esg_trn_progress_last']
#             esgWriter.writerow(esgHeader)
        
#         esgBody.insert(0,empId)
#         esgBody[1:1] = OrgId,empId,OrgId , date()
#         esgWriter.writerow(esgBody)
#         # print(esgBody)
#     return esgBody

from utility.create import create_esgRating

create_esgRating(1,1)





