#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import time
import sys
from tqdm import tqdm

print('Generating random data')

# Load SNOMED terms
with open('snomed_terms.json', 'r') as f:
    snomed_terms = json.load(f)

def random_int(min, max):
    return random.randint(min, max)

sex_id2code = ['Male', 'Female', 'Unknown']
eth_id2code = ['Asian', 'Black', 'White', 'Mixed', 'Other', 'Unknown']
ptt2age = {}
ptt2sex = {}
ptt2eth = {}
ptt2dod = {}
cui2ptt_pos = {}
cui2ptt_tsp = {}

ptt_num = 100000
max_ptt = 1000  # max. number of ptt a term can have
max_age = 100
die_pct = 10  # percentage of died ptt = 1 / die_pct

# Generate random patient data
print("Generating patient data...")
for i in tqdm(range(ptt_num)):
    ptt2age[i] = random_int(0, max_age)
    ptt2sex[i] = random.choice(sex_id2code)
    ptt2eth[i] = random.choice(eth_id2code)
    ptt2dod[i] = random_int(int(time.time()) - (60*60*24*365*10), int(time.time())) if random_int(0, die_pct) == 0 else 0

# Generate random mention data for each SNOMED term
print("Generating mention data...")
for i, term in tqdm(enumerate(snomed_terms), total=len(snomed_terms)):
    if not any(x in term['str'] for x in ['(disorder)', '(finding)', '(procedure)', '(substance)']):
        continue
    picked = set()
    cui2ptt_pos[i] = {}
    cui2ptt_tsp[i] = {}
    for _ in range(random_int(0, max_ptt)):
        ptt = random_int(0, ptt_num-1)
        while ptt in picked:
            ptt = random_int(0, ptt_num-1)
        picked.add(ptt)
        cui2ptt_pos[i][ptt] = random_int(1, 100)
        cui2ptt_tsp[i][ptt] = random_int(int(time.time()) - (60*60*24*365*10), int(time.time()))

# Write to files
print('Writing to files...')
with open('ptt2age.json', 'w') as f:
    json.dump(ptt2age, f)
with open('ptt2sex.json', 'w') as f:
    json.dump(ptt2sex, f)
with open('ptt2eth.json', 'w') as f:
    json.dump(ptt2eth, f)
with open('ptt2dod.json', 'w') as f:
    json.dump(ptt2dod, f)

print("Writing cui2ptt_pos and cui2ptt_tsp...")
with open('cui2ptt_pos.jsonl', 'w') as pos_out, open('cui2ptt_tsp.jsonl', 'w') as tsp_out:
    for k, v in tqdm(cui2ptt_pos.items(), total=len(cui2ptt_pos)):
        pos_out.write(json.dumps({snomed_terms[k]['cui']: v}) + '\n')
    for k, v in tqdm(cui2ptt_tsp.items(), total=len(cui2ptt_tsp)):
        tsp_out.write(json.dumps({snomed_terms[k]['cui']: v}) + '\n')

print('Finished generating random data')