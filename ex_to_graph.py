import datetime
import os
import sys
import traceback
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import warnings
from pandas.core.common import SettingWithCopyWarning
from pandas.errors import EmptyDataError
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

stamp=datetime.datetime.now()
date=stamp.strftime("%Y-%m-%d")
time=stamp.strftime("%X")

path="./IN"
out_path="./OUT/"
tmp="./tmp/"
tm_lst="./TM"
role="./ROLE/"
role_txt="./ROLE_TXT/"
files=os.listdir(path)
files_xlsx = [i for i in files if i.endswith('.xlsx')]
if len(files_xlsx) == 0 or len(files_xlsx) > 1:
	print("Oops..! IN DIR error Please check. IN DIR contains either 0 or more than 1 .xlsx file,Please place only latets .xlsx")
else:
	try:
		arg=sys.argv[1]
		if arg == "a":
			print(files_xlsx)
			xl_path=path+"/"+files_xlsx[0]
			read_file=pd.read_excel(xl_path,engine="openpyxl", sheet_name="Data")
			read_file.to_csv (tmp+date+"_temp_.csv",index = None,header=True)
			df = pd.read_csv(tmp+date+"_temp_.csv")
			os.remove(tmp+date+"_temp_.csv")
			inc_count=df[["Assigned to","Priority"]].value_counts()
			total_inc_count=df[["Assigned to"]].value_counts()
			total_inc_count.to_csv(tmp+date+"_total_interm.csv", sep=',', encoding='utf-8',header=False)
			inc_count.to_csv(tmp+date+"_interm.csv", sep=',', encoding='utf-8',header=False)
			col_name_change=['Engineer_Name','Priority','Count']
			tfpd=pd.read_csv(tmp+date+'_interm.csv',sep=',', encoding='utf-8',names=col_name_change)

			fpd=tfpd.sort_values('Engineer_Name')
			p1_fdp=fpd[fpd['Priority'] == '1 - Critical']
			p2_fdp=fpd[fpd['Priority'] == '2 - High']
			p3_fdp=fpd[fpd['Priority'] == '3 - Moderate']
			p4_fdp=fpd[fpd['Priority'] == '4 - Low']
			p5_fdp=fpd[fpd['Priority'] == '5 - Planning']
			sheet_list=['Total','1 - Critical','2 - High','3 - Moderate','4 - Low','5 - Planning',]
			df_list=[tfpd,p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
			if not os.path.exists(out_path+date):
				os.makedirs(out_path+date)
			out_dir=out_path+date+"/All/"
			if not os.path.exists(out_dir):
				os.makedirs(out_dir)	
			writer = pd.ExcelWriter(out_dir+date+"_final.xlsx",engine='xlsxwriter')
			for dataframe, sheet in zip(df_list, sheet_list):
				if dataframe.empty:
					print("Ommiting Empty DataFrame")
				else:	
					dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0,index=False)
			writer.save()
			fpd.to_csv(out_dir+date+"_final.csv", sep=',', encoding='utf-8',index=False)

			for df_name,plot_name in zip (df_list,sheet_list):
				if df_name.empty:
					print("Ommiting Empty DataFrame")
				else:	
					fig,ax =plt.subplots(figsize=(15, 5))
					plt.rcParams["figure.autolayout"] = True
					bl=ax.bar(df_name['Engineer_Name'],df_name['Count'])
					plt.xticks(rotation='vertical',fontsize ='xx-small')
					ax.set_xlabel('Incident Count')
					ax.set_title('Engineer VS '+plot_name+' Incident')
					ax.bar_label(bl, label_type="edge", padding=3,fontsize ='small')
					plt.savefig(out_dir+plot_name+"-"+date+".png",bbox_inches='tight',dpi=500)
			print("All anaysis reoprt created at %s",out_dir)
			os.remove(tmp+date+"_interm.csv")
			os.remove(tmp+date+"_total_interm.csv")
			os.chmod(out_dir, 0o777)
				
		elif arg == "t":
			print (arg)
			print(files_xlsx)
			xl_path=path+"/"+files_xlsx[0]
			read_file=pd.read_excel(xl_path,engine="openpyxl", sheet_name="Data")
			read_file.to_csv (tmp+date+"_temp_.csv",index = None,header=True)
			df = pd.read_csv(tmp+date+"_temp_.csv")
			os.remove(tmp+date+"_temp_.csv")
			inc_count=df[["Assigned to","Priority"]].value_counts()
			total_inc_count=df[["Assigned to"]].value_counts()
			total_inc_count.to_csv(tmp+date+"_total_interm.csv", sep=',', encoding='utf-8',header=False)
			inc_count.to_csv(tmp+date+"_interm.csv", sep=',', encoding='utf-8',header=False)
			col_name_change=['Engineer_Name','Priority','Count']
			tfpd=pd.read_csv(tmp+date+'_interm.csv',sep=',', encoding='utf-8',names=col_name_change)
			total_view=['Engineer_Name',"Count"]
			totalfpd=pd.read_csv(tmp+date+'_total_interm.csv',sep=',', encoding='utf-8',names=total_view)
			totalfpd.sort_values('Engineer_Name')
			total_df_list=[totalfpd]
			fpd=tfpd.sort_values('Engineer_Name')
			p1_fdp=fpd[fpd['Priority'] == '1 - Critical']
			p2_fdp=fpd[fpd['Priority'] == '2 - High']
			p3_fdp=fpd[fpd['Priority'] == '3 - Moderate']
			p4_fdp=fpd[fpd['Priority'] == '4 - Low']
			p5_fdp=fpd[fpd['Priority'] == '5 - Planning']
			df_list=[p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
			team=[line.rstrip('\n') for line in open(tm_lst+'/team_member_list.txt','r')]
			if len(team) == 0:
				print("Oops..! team_member_list.txt is Empty!")
			else:	
				team_totaL_sort_list=[]
				team_sort_df_list=[]
				print(team)
				for tnm in team:
					for dfl in df_list:
						name=str(tnm)
						sfdp=dfl[dfl['Engineer_Name'] == name ]
						team_sort_df_list.append(sfdp)
				for tnm in team:
					for tdfl in total_df_list:
						name=str(tnm)
						sfdp=tdfl[tdfl['Engineer_Name'] == name ]
						team_totaL_sort_list.append(sfdp)	

				fdft = pd.concat(team_sort_df_list)
				fdfttotal=pd.concat(team_totaL_sort_list)
				print(fdfttotal)
				fpdtf=fdft.sort_values('Engineer_Name')
				p1_fdp=fpdtf[fpdtf['Priority'] == '1 - Critical']
				p2_fdp=fpdtf[fpdtf['Priority'] == '2 - High']
				p3_fdp=fpdtf[fpdtf['Priority'] == '3 - Moderate']
				p4_fdp=fpdtf[fpdtf['Priority'] == '4 - Low']
				p5_fdp=fpdtf[fpdtf['Priority'] == '5 - Planning']
				sheet_list=['Total','1 - Critical','2 - High','3 - Moderate','4 - Low','5 - Planning',]
				df_list=[fdfttotal,p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
				if not os.path.exists(out_path+date):
					os.makedirs(out_path+date)
				out_dir=out_path+date+"/Team/"
				if not os.path.exists(out_dir):
					os.makedirs(out_dir)	
				writer = pd.ExcelWriter(out_dir+date+"_team_final.xlsx",engine='xlsxwriter')
				for dataframe, sheet in zip(df_list, sheet_list):
					if dataframe.empty:
						print("Ommiting Empty DataFrame")
					else:	
						dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0,index=False)
				writer.save()
				fpdtf.to_csv(out_dir+date+"_final.csv", sep=',', encoding='utf-8',index=False)
				for df_name,plot_name in zip (df_list,sheet_list):
					if df_name.empty:
						print("Ommiting Empty DataFrame")
					else:	
						y_pos=np.arange(len(df_name['Engineer_Name']))
						fig,ax = plt.subplots(figsize=(10, 5))
						bl=ax.barh(df_name['Engineer_Name'],df_name['Count'],color='#fdaa48')
						#ax.set_yticks(rotation='vertical',fontsize = 'xx-small')
						ax.set_yticks(y_pos, labels=df_name['Engineer_Name'],fontsize ='large')
						ax.invert_yaxis()  # labels read top-to-bottom
						ax.set_xlabel('Incident Count')
						ax.set_title('Engineer VS '+plot_name+' Incident')
						ax.bar_label(bl, label_type="edge", padding=3)
						plt.savefig(out_dir+plot_name+"-"+date+"_team.png",bbox_inches='tight',dpi=500)
				print("Team anaysis reoprt created at %s",out_dir)
				os.remove(tmp+date+"_interm.csv")
				os.remove(tmp+date+"_total_interm.csv")
				os.chmod(out_dir, 0o777)
		else:
			print(files_xlsx)
			xl_path=path+"/"+files_xlsx[0]
			read_file=pd.read_excel(xl_path,engine="openpyxl", sheet_name="Data")
			read_file.to_csv (tmp+date+"_temp_.csv",index = None,header=True)
			df = pd.read_csv(tmp+date+"_temp_.csv")
			os.remove(tmp+date+"_temp_.csv")
			inc_count=df[["Assigned to","Priority"]].value_counts()
			total_inc_count=df[["Assigned to"]].value_counts()
			total_inc_count.to_csv(tmp+date+"_total_interm.csv", sep=',', encoding='utf-8',header=False)
			inc_count.to_csv(tmp+date+"_interm.csv", sep=',', encoding='utf-8',header=False)
			col_name_change=['Engineer_Name','Priority','Count']
			tfpd=pd.read_csv(tmp+date+'_interm.csv',sep=',', encoding='utf-8',names=col_name_change)
			total_view=['Engineer_Name',"Count"]
			totalfpd=pd.read_csv(tmp+date+'_total_interm.csv',sep=',', encoding='utf-8',names=total_view)
			totalfpd.sort_values('Engineer_Name')
			total_df_list=[totalfpd]
			fpd=tfpd.sort_values('Engineer_Name')
			p1_fdp=fpd[fpd['Priority'] == '1 - Critical']
			p2_fdp=fpd[fpd['Priority'] == '2 - High']
			p3_fdp=fpd[fpd['Priority'] == '3 - Moderate']
			p4_fdp=fpd[fpd['Priority'] == '4 - Low']
			p5_fdp=fpd[fpd['Priority'] == '5 - Planning']
			df_list=[p1_fdp,p2_fdp,p3_fdp,p4_fdp,p5_fdp]
			role_file=os.listdir(role)
			role_xlsx = [i for i in role_file if i.endswith('.xlsx')]

			if len(role_xlsx) > 1 or len(role_xlsx) == 0:

				print("Oops ROLE Dir empty or more than 1 role xlsx is found.. ")

			else:	
				role_file=pd.read_excel(role+role_xlsx[0],engine="openpyxl", sheet_name="Role")
				role_file.to_csv (tmp+date+"_role_temp_.csv",index = None,header=True)#del
				dfl=pd.read_csv(tmp+date+"_role_temp_.csv")
				role_uni=dfl['Designation'].unique()
				role_lst=list(role_uni)
				role_name=[]
				for i in role_lst:
					df_name="df_"+i
					df_name=dfl[dfl["Designation"]== i]
					df_role_names=df_name["Full Name"]
					df_role_names.to_csv(role_txt+i+".txt", header=None, index=None, sep='\t', mode='w')
				if not os.path.exists(out_path+date):
					os.makedirs(out_path+date)
				inct_out_dir=out_path+date+"/Role_All/INC_TOTAL/"
				inctp_out_dir=out_path+date+"/Role_All/INC_PRIORITY_TOTAL/"
				if not os.path.exists(inct_out_dir):
					os.makedirs(inct_out_dir)
					os.makedirs(inctp_out_dir)
				role_txt_lst=os.listdir(role_txt)
				role_name_final=[]
				for name in role_txt_lst:
					base=os.path.basename(role_txt+name)
					os.path.splitext(base)
					namef=os.path.splitext(base)[0]
					role_name_final.append(namef)	
				for x,y in zip(role_txt_lst,role_name_final):
					role_txt_read=[line.rstrip('\n') for line in open(role_txt+x,'r')]
					if len(role_txt_read) == 0:
						print("Empty %s  list",x)
					else:
						role_total_sort_lst=[]
						role_sort_lst=[]	
						for tnm in role_txt_read:
							for dfl in df_list:
								#print(dfl)
								name=str(tnm)
								if dfl.empty:
									print("Ommiting Empty DataFrame "+name)
								else:	
									sfdp=dfl[dfl['Engineer_Name'] == name ]
									sort_sfdp=sfdp.sort_values('Engineer_Name')
									role_sort_lst.append(sort_sfdp)
						for tnm in role_txt_read:
							for tdfl in total_df_list:
								#print(tdfl)
								name=str(tnm)
								if tdfl.empty:
									print("Ommiting Empty DataFrame "+name)
								else:	
									sfdp=tdfl[tdfl['Engineer_Name'] == name ]
									sort_sfdp=sfdp.sort_values('Engineer_Name')
									role_total_sort_lst.append(sort_sfdp)
						fdft = pd.concat(role_sort_lst)
						fdfttotal=pd.concat(role_total_sort_lst)
						inct_out_dir=out_path+date+"/Role_All/INC_TOTAL/"
						fdfttotal.to_csv(inct_out_dir+y+".csv", sep=',', encoding='utf-8',index=False)
						inctp_out_dir=out_path+date+"/Role_All/INC_PRIORITY_TOTAL/"
						fdft.to_csv(inctp_out_dir+y+".csv", sep=',', encoding='utf-8',index=False)
				role_files=os.listdir(inct_out_dir)
				role_name_all_lst= list(filter(lambda f: f.endswith('.csv'),role_files))
				role_name_final=['LSRE','DA','ASRE','SDevOps','CCPM','TW','SSRE','SRE','SE','UT','DevOps','SLSRE', 'SNE']
				
				dft_lst=[]
				for dft in role_name_all_lst:
					try:
						df = pd.read_csv(inct_out_dir+dft)
					except EmptyDataError:
						df = pd.DataFrame()
					dft_lst.append(df)
				print(role_name_all_lst)	
				writer = pd.ExcelWriter(inct_out_dir+date+"_all_final.xlsx",engine='xlsxwriter')
				for dataframe, sheet in zip( dft_lst,role_name_final):
					if dataframe.empty:
						print("Ommiting Empty DataFrame")
					else:
						dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0,index=False)
				writer.save()
				print("Enginner_role VS INC  anaysis reoprt created at %s",str(inctp_out_dir))
				for df_name,plot_name in zip (dft_lst,role_name_final):
					if df_name.empty:
						print("Ommiting Empty DataFrame")
					else:	
						y_pos=np.arange(len(df_name['Engineer_Name']))
						fig,ax = plt.subplots(figsize=(10, 5))
						bl=ax.barh(df_name['Engineer_Name'],df_name['Count'],color='#fdaa48')
						#ax.set_yticks(rotation='vertical',fontsize = 'xx-small')
						ax.set_yticks(y_pos, labels=df_name['Engineer_Name'],fontsize ='large')
						ax.invert_yaxis()  # labels read top-to-bottom
						ax.set_xlabel('Incident Count')
						ax.set_title(plot_name+' VS Incident')
						ax.bar_label(bl, label_type="edge", padding=3)
						plt.savefig(inct_out_dir+plot_name+"-"+date+"_team.png",bbox_inches='tight',dpi=500)
				
				dftr_lst=[]
				for dft in role_name_all_lst:
					try:
						df = pd.read_csv(inctp_out_dir+dft)
					except EmptyDataError:
						df = pd.DataFrame()
					dftr_lst.append(df)	
				writer = pd.ExcelWriter(inctp_out_dir+date+"_all_role_final.xlsx",engine='xlsxwriter')
				for dataframe, sheet in zip( dftr_lst,role_name_final):
					if dataframe.empty:
						print("Ommiting Empty DataFrame ")
					else:	
						dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0,index=False)
				writer.save()
				for df,plot_name in zip(dftr_lst,role_name_final):
					df2 = pd.pivot_table(df, index='Engineer_Name', columns=['Priority'], values='Count', fill_value=0).reset_index().rename_axis(None, axis=1)
					df2.rename(columns = {'Engineer_Name':'Engineer_Name','1 - Critical':'P1', '2 - High':'P2','3 - Moderate':'P3','4 - Low':'P4','5 - Planning':'P5'}, inplace = True)
					df3=df2.reindex(columns=['Engineer_Name', 'P1', 'P2', 'P3', 'P4', 'P5'])
					if df3.empty:
						print("Ommiting Empty DataFrame ")
					else:
						df3.fillna(0,inplace=True)
						fig, ax = plt.subplots()
						df3.plot.bar(x='Engineer_Name', ax=ax,fontsize = 'small',width=1,figsize=(20,10))
						ax.set_title(plot_name+' VS Incident')
						plt.subplots_adjust(bottom=0.15)
						plt.savefig(inctp_out_dir+plot_name+"-"+date+"_team.png",bbox_inches='tight',dpi=500)
				os.remove(tmp+date+"_interm.csv")
				os.remove(tmp+date+"_total_interm.csv")
				os.remove(tmp+date+"_role_temp_.csv")
				os.chmod(out_path+date, 0o777)		
				print("Enginner_role VS Priority  anaysis reoprt created at %s", str(inctp_out_dir))
	except Exception as e:
		print(e)
		traceback.print_exc()
		print("Please pass args as for all report -a , for team report -t")		