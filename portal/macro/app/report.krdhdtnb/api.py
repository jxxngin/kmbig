import os
import pandas as pd
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
from datetime import datetime
import openpyxl
from openpyxl.drawing.image import Image

wiz.session = wiz.model("session").use()
userID = wiz.session.get("id")
def load():
    input_path = wiz.request.query("path", True)

    now = datetime.now()
    today = str(now.date()).replace('-','')

    try:
        raw_df = pd.read_excel(input_path, engine='openpyxl')

        factor = raw_df['factor']
        a = float(factor[0])
        b = float(factor[1])
        x0 = float(factor[2])
        y0 = float(factor[3])

        # standard 
        standard_df = pd.DataFrame({
            'Conc (pg/mL)' : [0, 15.625, 31.25, 62.5, 125, 250, 500, 1000],
            'Abs.-1' : raw_df[1],
            'Abs.-2' : raw_df[2]
        })

        raw_df_2 = raw_df.drop([1,2, 9, 10,11, 12,'factor'], axis=1)

        raw_values = raw_df_2.values
        raw_list = []
        raw_list.append(raw_values)

        raw_array = np.array(raw_list).T
        raw_list = raw_array.reshape(1,48)

        standard_df['Mean'] = standard_df.apply(lambda x: np.round(np.mean([x['Abs.-1'], x['Abs.-2']]), 3), axis=1)
        standard_df['Net Abs.-1'] = standard_df.apply(lambda x: x['Abs.-1']-standard_df['Mean'][0], axis=1)
        standard_df['Net Abs.-2'] = standard_df.apply(lambda x: x['Abs.-2']-standard_df['Mean'][0], axis=1)
        standard_df['Mean_Net'] = standard_df.apply(lambda x: np.round(np.mean([x['Net Abs.-1'], x['Net Abs.-2']]), 3), axis=1)
        standard_df['SEM_NET'] = standard_df.apply(lambda x: np.round(np.std([x['Net Abs.-1'], x['Net Abs.-2']])/np.sqrt(2),3), axis=1)

        raw_p_df = pd.DataFrame({
            'Abs.':raw_list[0][:-3].tolist()
        })

        dilution = 50

        raw_p_df['Net Abs.'] = raw_p_df.apply(lambda x: x['Abs.']-standard_df['Mean'][0], axis=1)
        raw_p_df['A=y-y0'] = raw_p_df.apply(lambda x: x['Net Abs.']-y0, axis=1)
        raw_p_df['B=(a/A)-1'] = raw_p_df.apply(lambda x: (a/x['A=y-y0'])-1, axis=1)
        raw_p_df['C=log(B,10)/b'] = raw_p_df.apply(lambda x: (np.log10(x['B=(a/A)-1'])/b), axis=1)
        raw_p_df['D=power(10,C)*x0'] = raw_p_df.apply(lambda x: (np.power(10, x['C=log(B,10)/b'])*x0), axis=1)
        raw_p_df['TNF-a'] = raw_p_df.apply(lambda x: np.round(x['D=power(10,C)*x0']*dilution/1000, 2), axis=1)
        raw_p_df['TNF-a'] = raw_p_df['TNF-a'].replace(np.nan, 0)

        tnf_mean = []
        tnf_sem = []
        tnf_sum = 0
        tnf_std = []

        for i in range(len(raw_p_df)) :
            tnf_sum += raw_p_df['TNF-a'][i]
            tnf_std.append(raw_p_df['TNF-a'][i])
            if (i+1)%3 == 0 :
                tnf_mean.append(np.round(tnf_sum/3,2))
                tnf_sum=0

                tnf_sem.append(np.round(st.stdev(tnf_std)/np.sqrt(3),2))
                tnf_std = []

        # of LPS
        raw_p_df['of LPS'] = raw_p_df.apply(lambda x: (x['TNF-a']-tnf_mean[0])/(tnf_mean[1]-tnf_mean[0])*100, axis=1)

        # LPS mean, sem
        lps_mean = []
        lps_sem = []

        lps_sum = 0
        lps_std = []

        for i in range(len(raw_p_df)) :
            lps_sum += raw_p_df['of LPS'][i]
            lps_std.append(raw_p_df['of LPS'][i])
            if (i+1)%3 == 0:
                lps_mean.append(round(lps_sum/3,2))
                lps_sum=0

                lps_sem.append(np.round(st.stdev(lps_std)/np.sqrt(3),2))
                lps_std = []

        result_list = [tnf_mean, tnf_sem, lps_mean, lps_sem]
        title_list = ['TNF-a Mean','TNF-a SEM','LPS Mean','LPS SEM']
        img_paths = []
        for i in range(len(result_list)):
            fig, axes = plt.subplots(nrows=1, ncols=6, sharey=True, figsize=(8,4))

            x_label = ["250", "500", "1000"]

            # Tnf-a mean
            axes[0].bar(x_label, result_list[i][0])
            axes[0].set_title("Control")
            axes[0].set_ylabel(title_list[i])
            axes[0].xaxis.set_visible(False)

            axes[1].bar(x_label, [result_list[i][1],0,0])
            axes[1].set_title("LPS")
            axes[1].xaxis.set_visible(False)
            axes[1].set_xlim(-1.5, 1.5)

            axes[2].bar(x_label, result_list[i][3:6])
            axes[2].set_title("KE-71")

            axes[3].bar(x_label, result_list[i][6:9])
            axes[3].set_title("KE71+LPS")

            axes[4].bar(x_label, result_list[i][9:12])
            axes[4].set_title("KE-72")

            axes[5].bar(x_label, result_list[i][12:])
            axes[5].set_title("KE-72+LPS")
            
            storage = wiz.model("fs").use(f"user/{userID}")
            abspath = storage.abspath()
            graphDir = "분석결과"
            if not storage.exists(graphDir):
                storage.makedirs(graphDir)
            imgPath = os.path.join(abspath, graphDir, f"{title_list[i]}.png") 
            plt.savefig(imgPath)

            img_dict = dict()
            img_dict['filename'] = title_list[i] + ".png"
            img_dict['filepath'] = imgPath.replace('/var/www/kmbig_admin/storage', '/file/download')
            # img_dict['filepath'] = imgPath
            img_paths.append(img_dict)

    except Exception as e:
        print(e)
        wiz.response.status(500, e)

    wiz.response.status(200, img_paths)