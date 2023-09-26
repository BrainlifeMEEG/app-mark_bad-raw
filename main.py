# Copyright (c) 2020 brainlife.io
#
# This app marks bad segments and channels "by hand" in a MNE/raw file

# set up environment
import os
import json
import numpy as np
import mne
import helper
import re


# load inputs from config.json
with open('config.json') as config_json:
	config =  helper.convert_parameters_to_None(json.load(config_json))

data_file = config['mne']

raw = mne.io.read_raw_fif(data_file,verbose=False)

if config['bads']:
    # if config['bads'] is not a list, make it a list
    bads = config['bads'].split()
    #not_there = [elem for elem in bads if elem not in raw.info['ch_names']]
    #if len(not_there) > 0:
    #    raise Exception("Channels {} not present.".format(not_there))

    raw.info['bads'].append(bads)

nuan = config["annotations"]
if nuan:
    nuan = nuan.split("\n")
    nuan = [re.split("[,;-]",n) for n in nuan]
    # remove trailing spaces from each element of nuan
    for n in nuan:
        for i in range(len(n)):
            n[i] = n[i].strip()

    onset = list()
    duration = list()
    description = list()
    ch_names = list()
    for a in nuan:
        onset.append(a.pop(0))
        duration.append(a.pop(0))
        description.append(a.pop(0))
        ch_names.append(a)
        del a
        not_there = [elem for elem in ch_names[-1] if elem not in raw.info['ch_names']]
        if ch_names[-1] != [] and len(not_there) > 0:
            raise Exception("Channels {} mentioned in annotations is not present in the data.".format(not_there))

    annot = mne.Annotations(onset=onset,  # in seconds
                            duration=duration,
                            description=description,
                            ch_names = ch_names)
    print(annot)

    raw.set_annotations(annot)

raw.save(os.path.join('out_dir','meg.fif'), overwrite=True)
