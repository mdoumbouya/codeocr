import pandas as pd
import csv
import requests
from PIL import Image
import editdistance
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from csv import writer
from pathlib import Path
from google.cloud import vision
from code_ocr.global_utils import *
import base64
from cleantext import clean
import black
from black import InvalidInput
import timeit


data_wcomment = pd.read_csv('FINAL DATA/wcommentall.csv')
data_woutcomment = pd.read_csv('FINAL DATA/woutcommentall.csv')

loop_count = len(data_wcomment['Ground Truth'])

wcomment_low = []
wcomment_medium = []
wcomment_high = []

woutcomment_low = []
woutcomment_medium = []
woutcomment_high = []

difference = []

temperature = 0.0

print('\n')

azure_percentage_list = []

for i in range(55):
    wcomment_gt_len = len(data_wcomment['Ground Truth'][i])
    azure_percentage_list.append(int(data_wcomment['ED Azure'][i])/wcomment_gt_len * 100)
    
print("Azure Average")
print(len(azure_percentage_list))
print(round(sum(azure_percentage_list)/55, 2))

for i in range(loop_count):
    wcomment_gt_len = len(data_wcomment['Ground Truth'][i])
    woutcomment_gt_len = len(data_woutcomment['Ground Truth'][i])
    
    wcomment_percentage_Azure_LM_Low = round(int(data_wcomment['ED Azure LM Low'][i])/wcomment_gt_len, 5)
    wcomment_low.append(wcomment_percentage_Azure_LM_Low)
    wcomment_percentage_Azure_LM_Medium = round(int(data_wcomment['ED Azure LM Medium'][i])/wcomment_gt_len, 5)
    wcomment_medium.append(wcomment_percentage_Azure_LM_Medium)
    wcomment_percentage_Azure_LM_High = round(int(data_wcomment['ED Azure LM High'][i])/wcomment_gt_len, 5)
    wcomment_high.append(wcomment_percentage_Azure_LM_High)
    
    woutcomment_percentage_Azure_LM_Low = round(int(data_woutcomment['ED Azure LM Low'][i])/woutcomment_gt_len, 5)
    woutcomment_low.append(woutcomment_percentage_Azure_LM_Low)
    woutcomment_percentage_Azure_LM_Medium = round(int(data_woutcomment['ED Azure LM Medium'][i])/woutcomment_gt_len, 5)
    woutcomment_medium.append(woutcomment_percentage_Azure_LM_Medium)
    woutcomment_percentage_Azure_LM_High = round(int(data_woutcomment['ED Azure LM High'][i])/woutcomment_gt_len, 5)
    woutcomment_high.append(woutcomment_percentage_Azure_LM_High)
    
    # if i < 55:
    #     if (wcomment_percentage_Azure_LM_Low != woutcomment_percentage_Azure_LM_Low
    #     or wcomment_percentage_Azure_LM_Medium != woutcomment_percentage_Azure_LM_Medium
    #     or wcomment_percentage_Azure_LM_High != woutcomment_percentage_Azure_LM_High):
    #         difference.append(i)

    #         print("-----------------------------------------------------------------------------------------------------------------")
    #         print(f"Data ID: {i}")
    #         print(f"Low -> with comment: {wcomment_percentage_Azure_LM_Low}% | without comment: {woutcomment_percentage_Azure_LM_Low}%")
    #         print(f"Medium -> with comment: {wcomment_percentage_Azure_LM_Medium}% | without comment: {woutcomment_percentage_Azure_LM_Medium}%")
    #         print(f"High -> with comment: {wcomment_percentage_Azure_LM_High}% | without comment: {woutcomment_percentage_Azure_LM_High}%")
    #         print("-----------------------------------------------------------------------------------------------------------------")
    
    if (i + 1) % 55 == 0:
        print(f"For Temperature {temperature}")
        # print(f"Iterration: {i}")
        # print(len(wcomment_low[(i - 54):]))
        # print(len(woutcomment_low[(i - 54):]))
        temperature += 0.2
        print("-----------------------------------------------------------------------------------------------------------------")
        print(f"With Comment Low Average: {round(sum(wcomment_low[(i - 54):])/55 * 100, 2)}%")
        print(f"Without Comment Low Average: {round(sum(woutcomment_low[(i - 54):])/55 * 100, 2)}%")
        print("-----------------------------------------------------------------------------------------------------------------")

        print("-----------------------------------------------------------------------------------------------------------------")
        print(f"With Comment Medium Average: {round(sum(wcomment_medium[(i - 54):])/55 * 100, 2)}%")
        print(f"Without Comment Medium Average: {round(sum(woutcomment_medium[(i - 54):])/55 * 100, 2)}%")
        print("-----------------------------------------------------------------------------------------------------------------")

        print("-----------------------------------------------------------------------------------------------------------------")
        print(f"With Comment High Average: {round(sum(wcomment_high[(i - 54):])/55 * 100, 2)}%")
        print(f"Without Comment High Average: {round(sum(woutcomment_high[(i - 54):])/55 * 100, 2)}%")
        print("-----------------------------------------------------------------------------------------------------------------")
        print("\n")
        

print("|****************************************************************************************************************|\n")
print("                                                 Global Statistics                                                 ")
print("-----------------------------------------------------------------------------------------------------------------")
print(f"With Comment Low Average: {round(sum(wcomment_low)/len(wcomment_low) * 100, 2)}%")
print(f"Without Comment Low Average: {round(sum(woutcomment_low)/len(woutcomment_low) * 100, 2)}%")
print("-----------------------------------------------------------------------------------------------------------------")

print("-----------------------------------------------------------------------------------------------------------------")
print(f"With Comment Medium Average: {round(sum(wcomment_medium)/len(wcomment_medium) * 100, 2)}%")
print(f"Without Comment Medium Average: {round(sum(woutcomment_medium)/len(woutcomment_medium) * 100, 2)}%")
print("-----------------------------------------------------------------------------------------------------------------")

print("-----------------------------------------------------------------------------------------------------------------")
print(f"With Comment High Average: {round(sum(wcomment_high)/len(wcomment_high) * 100, 2)}%")
print(f"Without Comment High Average: {round(sum(woutcomment_high)/len(woutcomment_high) * 100, 2)}%")
print("-----------------------------------------------------------------------------------------------------------------")
print("|****************************************************************************************************************|")

print('\n')