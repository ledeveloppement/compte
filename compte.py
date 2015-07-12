#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import time
import re
import json
import random
COMPTE_DIR=os.path.expanduser('~/.compte/compte_cheque.paris_olivier.cmb')
now=time.gmtime()
def save_op(op):
    d=os.path.join(
            COMPTE_DIR,
            str(op['date'].tm_year),
            str(op['date'].tm_mon).zfill(2),
            str(op['date'].tm_mday).zfill(2),
        )
    n=1
    f=os.path.join(d,'{}.json'.format(str(n).zfill(5)))
    while os.path.isfile(f):
        n=n+1
        f=os.path.join(d,'{}.json'.format(str(n).zfill(5)))
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(f,'w') as fh:
        try:
            json.dump(op,fh,sort_keys=True,indent=4)
        except:
            print('error w {}'.format(f))
def load_dir(d=COMPTE_DIR):
    ops=[]
    for root,dirs,files in os.walk(d):
        for f in files:
            if None is re.search('\.json$',f,re.I):
                continue
            with open(os.path.join(root,f),'r') as fh:
                try:
                    ops.append(json.load(fh))
                except:
                    print('error r {}'.format(f))
    return ops
def print_month(month='{}-{}'.format(now.tm_year,str(now.tm_mon).zfill(2)),solde=0):
    a,m=month.split('-')
    ops=load_dir(os.path.join(COMPTE_DIR,a,m))
    print('{} opérations dans la base'.format(len(ops)))
    for op in sorted(ops,key=lambda o:o['date']):
        solde=solde+op['val']
        print('{date}[{type:3s}]{label:30s} {val:-7.2f} {solde:-7.2f}'.format(
                date=time.asctime(tuple(op['date'])),
                type=op['type'],
                label=op['label'],
                val=op['val'],
                solde=solde,
            ))

op={
    'date':now,
    'label':'Kerbio',
    'val':random.random()*100-50,
    'type':'chq',
    'envelope':'Alimentaire',
}
save_op(op)
print_month()
