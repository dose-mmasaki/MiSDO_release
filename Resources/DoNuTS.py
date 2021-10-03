#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DoNuTS

"""
import gc
import json
import os
import pprint
import sqlite3
import sys
import time
import tkinter as tk
from tkinter import messagebox

import pandas as pd
import pydicom

import DataBase
import donuts_datasets
import funcs

sys.path.append("./")


def main():
    print("Start DoNuTS")
    pprint.pprint("  ###        ##    #       #######   ###  ")
    pprint.pprint(" #   #       # #   #          #     #   # ")
    pprint.pprint(" #    #      #  #  #          #      #    ")
    pprint.pprint(" #    #  ##  #   # #  #  #    #       #   ")
    pprint.pprint(" #   #  #  # #    ##  #  #    #    #   #  ")
    pprint.pprint("  ###    ##  #     #  ###     #     ###   ")

    # Select Modality by tk
    MODALITY = funcs.select_modality()

    if MODALITY in ["CT", "NM", "XA", "PT"]:
        print("Selected {}".format(MODALITY))
    else:
        print("Selected Auto Mode")

    print('**************************Start Processing****************************')
    # desktop_dir = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '/Desktop'
    desktop_dir = os.path.expanduser("~") + '/Desktop'
    dicom_directory = funcs.select_directory(desktop_dir)

    start = time.time()

    # Get dicom files and path
    dicom_files, dicom_path = funcs.get_dicom_files(dicom_directory)

    # Separate: RDSR, Modality
    if int(len(dicom_files)) == 0:
        messagebox.showerror('ERROR', 'Cannot find dicom file')
        sys.exit(0)

    else:
        if MODALITY != "Auto":
            rdsr_files_dict, rdsr_path_dict, modality_files_dict, modality_path_dict = funcs.separate_dicom_files(
                dicom_files=dicom_files,
                dicom_path=dicom_path,
                MODALITY=MODALITY)

        else:
            rdsr_files_dict, rdsr_path_dict, modality_files_dict, modality_path_dict = funcs.separate_rdsr_dicom_files_and_identify_each_modality(
                dicom_files=dicom_files,
                dicom_path=dicom_path)

        print("Found RDSR files : {}".format(
            funcs.show_len_identified(rdsr_files_dict)))
        print("Fround the other dicom : {}".format(
            funcs.show_len_identified(modality_files_dict)))

    num_rdsr = funcs.count_rdsr(rdsr_files_dict)
    if num_rdsr == 0:
        messagebox.showerror('ERROR', 'Cannot find RDSR file')
        sys.exit(0)

    elif num_rdsr == 0 and funcs.count_rdsr(modality_files_dict) == 0:
        messagebox.showerror(
            'ERROR', 'Cannot find a file that can be processed．')
        sys.exit()

    # del dicom_files, num_rdsr
    # gc.collect()

    # Treate RDSR
    # Write data in rdsr_data
    rdsr_data = []
    new_data_cnt = 0
    duplicate_data_cnt = 0

    for _modality, p in zip(rdsr_files_dict, rdsr_path_dict):

        # Info of PT, NM（RadionuclideTotalDose） from  modality_file
        if _modality in ['PT', 'NM']:

            try:
                # {uniuqecode:DOSE}
                RadionuclideTotalDose_dict = funcs.extract_RadionuclideTotalDose(
                    modality_files_dict, _modality)
            except:
                pass

        if _modality != 'Unknown':
            # Connect DB
            DATABASE = DataBase.WriteDB(MODALITY=_modality, is_dev=False)
            # Get rdsr_file from each modality
            rdsr_files = rdsr_files_dict[_modality]
            rdsr_path = rdsr_path_dict[_modality]

            # Get temprate data from donuts_datasets
            try:

                _M = _modality
                temp_dict = donuts_datasets.return_json_temprate(MODALITY=_M)
            except:
                print("Cannot read temprate file. Please ask for developer.")
                sys.exit(0)

            if len(rdsr_files) != 0:
                # Main Treatments in RDSR
                try:
                    # Save each number of datas as a dict
                    events_dict = funcs.get_events_from_rdsr(
                        rdsr_files, MODALITY=_modality)
                    #     >>>  {'0':'3',
                    #     >>>   '1':'6'}

                    # total_events = funcs.calc_total_event(events_dict)
                    # Get Acquisition data
                    Acquisition_set = []
                    for r in rdsr_files:
                        Acquisition_set.append(
                            funcs.separate_Acquisition(r, MODALITY=_modality))

                    i = 0
                    # Get file, path, acquisition, irradiation-events
                    for r, path, c1, event_key in zip(rdsr_files, rdsr_path, Acquisition_set, events_dict.keys()):
                        event_cnt = int(events_dict[event_key])  # 3, 6 int

                        # Write data by irradiation event
                        # Write info to temp_dict and add it into rdsr_data by roop
                        # When done one roop, delete values of temp_dict
                        for e_c in range(event_cnt):
                            c2 = c1[e_c]  # c2:pydicom.dataelem.DataElement
                            if _modality in ["CT", "PT"]:
                                try:
                                    # acquisition
                                    acquisition_value = funcs.extract_data_from_CT_Acquisition(
                                        temp_dict, c2)
                                except:
                                    pass
                            elif _modality == "XA":
                                # Get Acquisition of XA
                                try:
                                    acquisition_value = funcs.extract_data_from_angio_Acquisition(
                                        temp_dict, c2)
                                except:
                                    pass
                            elif _modality == "NM":
                                pass

                            # Write Acquisition data
                            temp_dict.update(acquisition_value)

                            # write header info
                            temp_dict = funcs.writeHeader(r,
                                                          temp_dict,
                                                          _modality,
                                                          path)

                            # Write RadionuclideTotalDose only PT,NM
                            if _modality in ['PT', 'NM']:
                                try:
                                    # Write RadionuclideTotalDose into temp_dict
                                    each_unique_code = str(
                                        r.PatientID) + str(r.StudyDate)
                                    for u_c in RadionuclideTotalDose_dict.keys():
                                        if u_c == each_unique_code:
                                            temp_dict['RadionuclideTotalDose'] = RadionuclideTotalDose_dict[u_c]
                                except:
                                    pass

                            # Get CTDoseLengthProductTotal if CT used
                            if _modality in ["CT", "PT", "NM"]:
                                try:
                                    CTDoseLengthProductTotal = funcs.extract_CT_Dose_Length_Product_Total(
                                        rdsr_files=r)
                                    temp_dict['CTDoseLengthProductTotal'] = CTDoseLengthProductTotal
                                except:
                                    pass

                            temp_dict['PRIMARY KEY'] = str(
                                i) + '_' + temp_dict['SOPInstanceUID']
                            # Add values into rdsr_data
                            rdsr_data.append(temp_dict.copy())

                            # Act by "try" because of PRIMARY_KEY
                            try:
                                write_list = [v for v in temp_dict.values()]
                                # Write DB
                                DATABASE.main(data=write_list)

                                new_data_cnt += 1
                            except Exception as e:
                                assert "PRIMARY_KEY" in e.args[0], "DB writing Error, {}".format(
                                    e)
                                duplicate_data_cnt += 1

                            # clear temp_dict
                            temp_dict = funcs.clear_dict_value(temp_dict)
                            i += 1

                except:
                    pass

                # When (Num of RDSR file==0) and (num of modality_file!=0)
            elif len(rdsr_files_dict[_modality]) == 0 and len(modality_files_dict[_modality]) != 0:
                # write only header info
                i = 0
                for m, path in zip(modality_files_dict[_modality], modality_path_dict[_modality]):

                    # Write header info
                    temp_dict = funcs.writeHeader(m,
                                                  temp_dict,
                                                  _modality,
                                                  path)

                    # Write RadionuclideTotalDose into temp_dict
                    try:
                        each_unique_code = str(m.PatientID) + str(m.StudyDate)
                        for u_c in RadionuclideTotalDose_dict.keys():
                            if u_c == each_unique_code:
                                temp_dict['RadionuclideTotalDose'] = RadionuclideTotalDose_dict[u_c]
                    except:
                        pass
                    temp_dict['PRIMARY KEY'] = str(
                        i) + '_' + temp_dict['SOPInstanceUID']
                    # Add values into rdsr_data
                    rdsr_data.append(temp_dict.copy())

                    # Act by "try" because of PRIMARY_KEY
                    try:
                        write_list = [v for v in temp_dict.values()]
                        # Write DB
                        DATABASE.main(data=write_list)

                        new_data_cnt += 1
                    except Exception as e:
                        assert "PRIMARY_KEY" in e.args[0], "DB writing Error, {}".format(
                            e)
                        duplicate_data_cnt += 1

                    # clear temp_dict
                    temp_dict = funcs.clear_dict_value(temp_dict)
                    i += 1

            else:
                pass

            print("{} : New {} records, duplicated {} records".format(
                _modality, new_data_cnt, duplicate_data_cnt))
            # XA : new 14 records, duplicated 0 records
    DATABASE.close()

    del rdsr_files_dict, modality_files_dict, rdsr_files, temp_dict, _modality
    gc.collect()

    # Write on ALL_DATA table
    all_dict = donuts_datasets.return_json_temprate(MODALITY="Auto")
    DATABASE = DataBase.WriteDB(MODALITY="ALL_DATA", is_dev=False)
    for each_rdsr_data in rdsr_data:

        # clear all_dict of value
        all_dict = funcs.clear_dict_value(all_dict)
        try:
            # Write data into all_dict
            each_rdsr_data = funcs._setdefault(each_rdsr_data, all_dict)
            all_dict.update(each_rdsr_data)

            # Write DB
            write_list = [v for v in all_dict.values()]
            DATABASE.main(data=write_list)
        except:
            pass
    DATABASE.close()

    end = time.time()

    # Save as json, csv
    save_name = './Resources/latest'

    file_name_json = save_name + ".json"
    file_name_csv = save_name + ".csv"

    # json
    with open(file_name_json, mode='wt', encoding='utf-8') as file:
        json.dump(rdsr_data, file, ensure_ascii=False, indent=1)

    # csv
    df = pd.read_json(file_name_json)
    df.to_csv(file_name_csv, encoding='utf-8')

    print("Processing time : {} seconds".format(int(end-start)))

    print('********************Done Processing RDSR files********************')


if __name__ == '__main__':

    main()
    print("End program in 10 seconds.")
    time.sleep(10)
