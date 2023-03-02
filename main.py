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

not_there = [elem for elem in config['bads'] if elem not in raw.info['ch_names']]
if len(not_there) > 0:
    raise Exception("Channels {} not present.".format(not_there))

raw.info['bads'] = config['bads']

nuan = config["annotations"]

nuan = nuan.split("\n")
nuan = [re.split("[,;-]",n) for n in nuan]

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
    not_there = [elem for elem in ch_names if elem not in raw.info['ch_names']]
    if len(not_there) > 0:
        raise Exception("Channels {} mentioned in annotations is not present in the data.".format(not_there))

annot = mne.Annotations(onset=onset,  # in seconds
                        duration=duration,
                        description=description,
                        ch_names = ch_names)
print(annot)

raw.set_annotations(annot)

raw.save(os.path.join('out_dir','meg.fif'))
