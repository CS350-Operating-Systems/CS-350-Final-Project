# -*- coding: utf-8 -*-
"""
CS350 Operating Systems Project 

Authors: 

Egemen Iscan, S018748, egemen.iscan@ozu.edu.tr
Baris Karaer, S015497, baris.karaer@ozu.edu.tr
Ertan Ayanlar, S014576, ertan.ayanlar@ozu.edu.tr

"""

import os
import shutil
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def main():
    
    # You may have to modify these directories
    ssd_drive = "C:\\Users\\hp\\Desktop\\"
    hdd_drive = "D:\\"
    
    # Go to subdirectories and create list of file name, file size and size category
    files = []
    sizes = []
    size_categories = []
    
    print("\nAccessing files...")
    
    for root, dir, file in os.walk(ssd_drive):
        for i in file:
            try:
                newfile = os.path.join(root, i)
                size = os.path.getsize(str(newfile))
                files.append(newfile.strip())
                sizes.append(float(size))
                size_categories.append(compareSize(size))
            except FileNotFoundError as err:
                print(err)
            except OSError as err:
                print(err)
            
    """
            # ATTENTION! RUNNING THIS CODE MAY ALTER THE LOCATION OF YOUR FILES!
            
            size_megabytes = size / 1000000
            if (size_megabytes > 1000) :
                if newfile.startswith(hdd_drive):
                    continue
                total, used, free = shutil.disk_usage(hdd_drive)
                if size_megabytes > free * 1000000:
                    print(f"{newfile} {size} B - Not enough space on HDD !")
                    continue
                file_path = newfile.replace(ssd_drive, hdd_drive, 1)
                file_dir = root.replace(ssd_drive, hdd_drive, 1)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                shutil.move(newfile, file_path)
        
    """
        
    print("\nDone!")
    
    # Create a Pandas DataFrame from the previously created lists
    df = pd.DataFrame({
        'file_name':files,
        'file_size':sizes,
        'size_category':size_categories
        })

    df = df.sort_values(by=['file_size'])
    
    # Check for missing values
    print("There are {} rows and {} columns in the initial dataset.".format(df.shape[0],df.shape[1]))
    na_cols = df.columns[df.isna().any()].tolist()
    if not na_cols:
        print("No missing values.")
    else:
        print(f"Columns which include NA rows: {na_cols}.") 
    
    # Print file count
    intervals = ['0K','1K','10K','100K','1M','10M','100M','1GB','∞']

    counts = df.size_category.astype(pd.api.types.CategoricalDtype(categories=range(8), ordered=True))
    counts = counts.value_counts().sort_index()
    print("\nDistribution of File Size:\n")
    for num, count in enumerate(counts):
        print("\t{} files with size {} - {}".format(str(count), intervals[num], intervals[num+1]))
   
    # Hypothesis 1: "90% of the files in a specified directory are smaller than 100KB."
    percentage = df[df['size_category'] < 3].shape[0] / df.shape[0]
    hypothesis1 = percentage >= 0.9
    print("\n{}% of the files in a specified directory are smaller than 100KB. \nTherefore the first hypotheses is {}.".format(
        str(round(percentage*100,2)), str(hypothesis1).lower()))
    
    # Calculate PDF and CDF for File Size
    sizedist = []
    for i in range(8):
        sizedist.append(df[df['size_category']==i]['file_size'].sum(axis=0, skipna=True))
    sizedist = [x/sum(sizes) for x in sizedist]
    sizedist_cumulative = np.cumsum(sizedist).tolist() 
    
    # Hypothesis 2: "80% of the disk/SSD space is occuppied by files whose size are greater than 100MB."
    print("\n")
    print(str(round(sum(sizedist[-2:]*100),2)) + "% of the disk space is occupied by files whose size are greater than 100MB.")
    hypothesis2 = sum(sizedist[-2:]) >= 0.8
    print("Therefore the second hypotheses is {}.".format(str(hypothesis2).lower()))
        
    # Plot PDF and CDF for File Size
    sizedist.append(sizedist[-1])
    sizedist_cumulative.append(sizedist_cumulative[-1])
    intervals.insert(0,"")
    fbins = np.arange(9)
    fig_size = plt.figure(figsize=(10,10))
    ax1 = fig_size.add_subplot(211)
    ax1.step(fbins, sizedist, where='post', color='m', label='PDF')
    ax1.step(fbins, sizedist_cumulative, where='post', color='b', label='CDF')
    ax1.yaxis.grid(True, which='both')
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.legend(loc='right')
    ax1.set_xticklabels(intervals)
    ax1.set_title('Density Histogram (File Size)')
    ax1.set_xlabel('File size')
    ax1.set_ylabel('Likelihood of occurrence')

    # Plot CDF and PDF for File Count
    fig_count = plt.figure(figsize=(10,10))
    ax2 = fig_count.add_subplot(211)
    ax2.hist(df['size_category'], fbins, density=1, histtype='step', cumulative=True, label='CDF', color='b')
    ax2.hist(df['size_category'], fbins, histtype='step', density=1, label='PDF', color='m')
    ax2.yaxis.grid(True, which='both')
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.legend(loc='right')
    ax2.set_xticklabels(intervals)
    ax2.set_title('Density Histogram (File Count)')
    ax2.set_xlabel('File size')
    ax2.set_ylabel('Likelihood of occurrence')
    
    # Display figures
    plt.show(block=True)
    
    print("\nProgram executed.")
    

# =============================================================================
#  compareSize returns a number between 0-7 which represents 
#  <1K, <10K, <100K, <1M, <10M, <100M, <1GB, >=1GB, respectively
# =============================================================================
    
def compareSize(sizeB):
    if(sizeB == 0):
        return 0
    else:
        return min(7, max(0, int(math.log10(sizeB))-2))
    
   
if __name__ == "__main__":
    main()


