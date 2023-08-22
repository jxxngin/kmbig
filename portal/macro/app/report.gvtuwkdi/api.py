import os
import pandas as pd
import numpy as np
import math
import statistics as st
import matplotlib.pyplot as plt
from datetime import datetime
import openpyxl
from openpyxl.drawing.image import Image

wiz.session = wiz.model("session").use()
userID = wiz.session.get("id")
def load():
    rawpath = wiz.request.query("path", True)

    now = datetime.now()
    today = str(now.date()).replace('-','')

    try:
        raw_df = pd.read_excel(rawpath, engine='openpyxl')

        udpga_m1 = list(raw_df[1])+list(raw_df[3])+list(raw_df[5])
        udpga_m2 = list(raw_df[2])+list(raw_df[4])+list(raw_df[6])

        udpga_p1 = list(raw_df[7])+list(raw_df[9])+list(raw_df[11])
        udpga_p2 = list(raw_df[8])+list(raw_df[10])+list(raw_df[12])

        index = [' ','Diclofenac','Diclofenac','Diclofenac','Diclofenac','Diclofenac','Diclofenac','Diclofenac','KE-57','KE-57','KE-57','KE-57','KE-57','KE-58','KE-58','KE-58','KE-58','KE-58','KE-59','KE-59','KE-59','KE-59','KE-59','KE-59']

        replicate = ['(-)UGT',0,62.5,125,250,500,1000,2000,62.5,125,250,500,1000,62.5,125,250,500,1000,31.25,62.5,125,250,500,1000]

        df = pd.DataFrame({
            'replicate' : replicate,
            '(-)UDPGA_1' : udpga_m1,
            '(-)UDPGA_2' : udpga_m2,
            '(+)UDPGA_1' : udpga_p1,
            '(+)UDPGA_2' : udpga_p2,
        }, index = index)

        df['AVR (A)'] = (df['(-)UDPGA_1']+df['(-)UDPGA_2'])/2
        df['AVR (B)'] = (df['(+)UDPGA_1']+df['(+)UDPGA_2'])/2

        C = math.ceil((df['(-)UDPGA_1'][0]-df['AVR (B)'][0]+df['(-)UDPGA_2'][0]-df['AVR (B)'][0])/2)

        D1 = np.ceil(np.ceil(df['(+)UDPGA_1'][1:])+C)
        D2 = np.ceil(df['(+)UDPGA_2'][1:]+C)

        F1 = np.ceil(df['AVR (A)'][1:] - D1)
        F2 = np.ceil(df['AVR (A)'][1:] - D2)

        substrate1 = np.round(F1/df['AVR (A)'][1]*100,2)
        substrate2 = np.round(F2/df['AVR (A)'][1]*100,2)

        substrate_avr = np.round((substrate1+substrate2)/2,2)

        inhibition1 = np.round(100-((np.array(substrate1)/np.array(substrate_avr)[0])*100),2)
        inhibition2 = np.round(100-((np.array(substrate2)/np.array(substrate_avr)[0])*100),2)

        inhibition_avr = np.round((inhibition1+inhibition2)/2,2)

        result_df = pd.DataFrame({
            'replicate' : df['replicate'][1:],
            'D1' : D1,
            'D2' : D2,
            'F1' : F1,
            'F2' : F2,
            'Substrate Consumed %1' : substrate1,
            'Substrate Consumed %2' : substrate2,
            'Substrate AVR(%)' : substrate_avr,
            'inhibition 1' : inhibition1,
            'inhibition 2' : inhibition2,
            'inhibition AVR' : inhibition_avr
        })

        title_list = ['Diclofenac', 'KE-57', 'KE-58', 'KE-59']
        img_paths = []
        for title in title_list:
            plt.clf()
            target_df = result_df.loc[title]

            x = target_df['replicate'].tolist()
            y = target_df['Substrate AVR(%)'].tolist()

            plt.figure(figsize=(4,3))
            plt.scatter(x,y)
            plt.title("UGT1A1_"+title)

            plt.xlabel("Conc")
            plt.ylabel("Percent Substrate Consumed")
            
            storage = wiz.model("fs").use(f"user/{userID}")
            abspath = storage.abspath()
            graphDir = "분석결과"
            if not storage.exists(graphDir):
                storage.makedirs(graphDir)
            imgPath = os.path.join(abspath, graphDir, f"{title}.png") 
            plt.savefig(imgPath)

            img_dict = dict()
            img_dict['filename'] = f"{title}.png"
            img_dict['filepath'] = imgPath.replace('/var/www/kmbig_admin/storage', '/file/download')
            # img_dict['filepath'] = imgPath
            img_paths.append(img_dict)
        
    except Exception as e:
        print(e)
        wiz.response.status(500, False)
    
    wiz.response.status(200, img_paths)