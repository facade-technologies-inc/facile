'''
This extension is kind of a hacky way of doing things.

The original goal was to make a test_procedure directive that would create all necessary fields
and images for a test procedure. The difficulties with this are:

- The Sphinx API is weird

So I decided to make an extension that just directly writes the rst code in the initialization
phase.
'''

import random
import pandas as pd
import numpy as np

rchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ATP file path relative to "facile/docs"
atp_file_path = "./source/docs/ATP/ATP.rst"
procedures_file = "./source/docs/ATP/procedures.xlsx"

header = """
*************************
Acceptance Test Procedure
*************************

"""

preamble_template = """
----------------------------------------------------------------------------------------------------
{}
----------------------------------------------------------------------------------------------------

============
Introduction
============

{}

====================
Referenced Documents
====================

{}

=======================
Required Test Equipment
=======================

{}

=========================
Requirements Summary
=========================

{}

===================
Pre-Test Conditions
===================

{}

"""

figure_template = """

.. _{}:

.. figure:: ./images/{}
    :alt: {}
    
    {}
    
"""


def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

def read_procedure_data(filename):
    wb = pd.ExcelFile(filename)
    sheetnames = [name for name in wb.sheet_names if name != "Introduction"]
    test_procedures = []
    for name in sheetnames:
        df = pd.read_excel(wb, name)
        proc = {}
        proc['title'] = df['Title'][0]
        proc['intro'] = df['Introduction'][0]
        proc['refer'] = [a for a in df['Referenced Documents'] if type(a) == str]
        proc['equip'] = [b for b in df['Required Equipment'] if type(b) == str]
        proc['summa'] = df['Requirements Summary'][0]
        proc['preco'] = [c for c in df['Pre-Test Conditions'] if type(c) == str]
        proc['steps'] = []
        proc['figre'] = {}
        
        for i in range(len(df['Steps (Action)'])):
            if type(df['Steps (Action)'][i]) == str and type(df['Steps (Expected Result)'][i]) == str:
                crumbs = df['Steps (Expected Result)'][i].split()
                for j in range(len(crumbs)):
                    crumb = crumbs[j]
                    if len(crumb) > 1:
                        if crumb[0] == '@':
                            img_filename = crumb[1:]
                            if img_filename in proc['figre'].keys():
                                ref_name = proc['figre'][img_filename][0]
                            else:
                                ref_name = crumb[1:].split('.')[0].replace("_", "")+random_string_generator(8, rchars)
                                proc['figre'][img_filename] = (ref_name, "")
                            df['Steps (Expected Result)'][i] = df['Steps (Expected Result)'][i].replace("@"+img_filename, ':num:`Fig. #{}`'.format(ref_name.lower()))
                proc['steps'].append((df['Steps (Action)'][i], df['Steps (Expected Result)'][i]))
            else:
                break
                
                
        for i in range(len(df['Figure (filename)'])):
            if type(df['Figure (filename)'][i]) == str and type(df['Figure (caption)'][i]) == str:
                fname = df['Figure (filename)'][i]
                caption = df['Figure (caption)'][i]
                if fname in proc['figre']:
                    proc['figre'][fname] = (proc['figre'][fname][0], caption)
                else:
                    raise Exception("Figure {} cannot be included without refering to it using "
                                    "'@' in testcase {}".format(fname, name))
                proc['steps'].append((df['Steps (Action)'][i], df['Steps (Expected Result)'][i]))
            else:
                break
                
        test_procedures.append(proc)
    return test_procedures
    
def build_table(steps:list) -> str:
    
    if len(steps) >= 30:
        raise Exception("Test Procedure must have less than 30 steps")
    
    head = ("Step", "Action", "Expected Result")
    max_action_length = len(head[1])
    max_result_length = len(head[2])
    for action, result in steps:
        max_action_length = max(max_action_length, len(action))
        max_result_length = max(max_result_length, len(result))
        
    widths = (len(head[0]), max_action_length, max_result_length)
    table_horizontal = "\t+-{}-+-{}-+-{}-+\n".format("-"*widths[0], "-"*widths[1], "-"*widths[2])
    
    table =  ".. tabularcolumns:: |c|L|L|\n"
    table += ".. table:: Test Procedure Steps\n\n"

    table += table_horizontal
    table += "\t| {}{} | {}{} | {}{} |\n".format(head[0], " "*(widths[0]-len(head[0])),
                                             head[1], " "*(widths[1]-len(head[1])),
                                             head[2], " "*(widths[2]-len(head[2])))
    table += table_horizontal.replace("-", "=")
    
    step_count = 0
    for action, result in steps:
        step_count += 1
        table += "\t| {:4} | {}{} | {}{} |\n".format(step_count,
                                                 action, " "*(widths[1] - len(action)),
                                                 result, " "*(widths[2] - len(result)))
        table += table_horizontal
    
    return table

def build_figs(fig_refs):
    
    fig_str = ""
    
    for ref in fig_refs:
        fig_str += figure_template.format(fig_refs[ref][0], ref, fig_refs[ref][1], fig_refs[ref][1])
        
    return fig_str
    
def setup(app):
    global procedures_file
    global test_procedures
    test_procedures = read_procedure_data(procedures_file)
    
    with open(atp_file_path, "w") as atp_file:
        atp_file.write(header)
        
        for proc in test_procedures:
            title = proc['title']
            intro = proc['intro']
            refer = "\n".join(["- {}".format(r) for r in proc['refer']])
            equip = "\n".join(["- {}".format(e) for e in proc['equip']])
            summa = proc['summa']
            preco = "\n".join(["- {}".format(p) for p in proc['preco']])
            
            preamble = preamble_template.format(title, intro, refer, equip, summa, preco)
            
            atp_file.write(preamble)
            atp_file.write(build_table(proc['steps']))
            atp_file.write(build_figs(proc['figre']))
            
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

# For debugging only
if __name__ == "__main__":
    procedures_file = "../docs/ATP/procedures.xlsx"
    atp_file_path = "../docs/ATP/ATP.rst"
    setup(None)