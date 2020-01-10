'''
This extension is kind of a hacky way of doing things.

The original goal was to make a test_procedure directive that would create all necessary fields
and images for a test procedure. The difficulties with this are:

- The Sphinx API is weird

So I decided to make an extension that just directly writes the rst code in the initialization
phase.
'''

# ATP file path relative to "facile/docs"
atp_file_path = "./source/docs/ATP/ATP.rst"
procedures_file = "./source/docs/ATP/ATP.xlsx"

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

test_procedures = [
    {
        "title": "Operating System Acceptance Test",
        "intro": "This acceptance test document verifies that the software system, Facile is "
                 "functional on 64 Bit Windows 10 Home Version 1903.  This acceptance test "
                 "establishes the framework used by the acceptance test team to plan, execute, "
                 "and document acceptance testing.  It describes the scope of the work performed "
                 "and the approach taken to execute the tests created to validate that the system "
                 "performs as required with the intended operating system. The details of this "
                 "acceptance test are developed according to the requirements specifications and "
                 "show traceability back to those specifications.",
        "refer": ["System Requirements Document, Rev B, 10/27/2019"],
        "equip": ["PC (Personal Computer)"],
        "summa": "To verify SR4.2.1 - Facile shall operate on 64-bit Windows 10 Home Version "
                 "1903.",
        "preco": [
                 "Need to be running application on Operating system Windows 10 Home Version "
                 "1903.",
                 "Python 3.7.4 is installed and added to the PATH."
                 ],
        "steps": [
            ("Right click on **Explorer**", "A context menu of items open up"),
            ("Select **System**", "**Settings** is open"),
            ("Scroll to **Device specifications,** and verify the System type, Edition, "
             "and Version", "Refer to Figure 1.1"),
            ("Click on **Windows Search Bar**", "Windows Search Bar comes into focus"),
            ("Type cmd and press enter", "A **Command Prompt** terminal opens"),
            ("Click on the **Command Prompt**", "The **Command Prompt** comes into focus"),
            ('Type "python facile.py" in the **Command Prompt**', "Facile should run. Test Case "
                                                                  "Completed.")
        ]
    }
]

def build_table(steps:list) -> str:
    
    if len(steps) >= 30:
        raise Exception("Test Procedure must have less than 30 steps")
    
    head = ("Steps", "Action", "Expected Result")
    max_action_length = len(head[1])
    max_result_length = len(head[2])
    for action, result in steps:
        max_action_length = max(max_action_length, len(action))
        max_result_length = max(max_result_length, len(result))
        
    widths = (len(head[0]), max_action_length, max_result_length)
    table_horizontal = "+-{}-+-{}-+-{}-+\n".format("-"*widths[0], "-"*widths[1], "-"*widths[2])
    
    table = table_horizontal
    table += "| {}{} | {}{} | {}{} |\n".format(head[0], " "*(widths[0]-len(head[0])),
                                             head[1], " "*(widths[1]-len(head[1])),
                                             head[2], " "*(widths[2]-len(head[2])))
    table += table_horizontal.replace("-", "=")
    
    step_count = 0
    for action, result in steps:
        step_count += 1
        table += "| {:5} | {}{} | {}{} |\n".format(step_count,
                                                 action, " "*(widths[1] - len(action)),
                                                 result, " "*(widths[2] - len(result)))
        table += table_horizontal
    
    return table
    
def setup(app):
    with open(atp_file_path, "w") as atp_file:
        atp_file.write(header)
        
        for proc in test_procedures:
            title = proc['title']
            intro = proc['intro']
            refer = "\n".join(["- {}".format(r) for r in proc['refer']])
            equip = "\n".join(["- {}".format(e) for e in proc['equip']])
            summa = proc['summa']
            preco = "\n".join(["- {}".format(p) for p in proc['equip']])
            
            preamble = preamble_template.format(title, intro, refer, equip, summa, preco)
            
            atp_file.write(preamble)
            atp_file.write(build_table(proc['steps']))
            # TODO: find images and create figures.
            
        
            

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }