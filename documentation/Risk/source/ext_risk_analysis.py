"""
/------------------------------------------------------------------------------\
|                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
|------------------------------------------------------------------------------|
|                                                                              |
|    Copyright [2019] Facade Technologies Inc.                                 |
|    All Rights Reserved.                                                      |
|                                                                              |
| NOTICE:  All information contained herein is, and remains the property of    |
| Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
| and technical concepts contained herein are proprietary to Facade            |
| Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
| Patents, patents in process, and are protected by trade secret or copyright  |
| law.  Dissemination of this information or reproduction of this material is  |
| strictly forbidden unless prior written permission is obtained from Facade   |
| Technologies Inc.                                                            |
|                                                                              |
\------------------------------------------------------------------------------/

Necessary Risk Info for TDP:
----------------------------

- Table of risk criticality
- Risk matrix
- Risk Descriptions and Mitigation Plans
- Risk Status

Each risk must have:
--------------------
	- Title?
	- Description
	- likelihood (1-5)
	- consequence (1-5)
	- action (M, R, etc.)

NOTES:
- Can copy picture of cells (Good for risk matrix):
  https://stackoverflow.com/questions/37180097/copy-image-from-excel-and-save-it-using-python

"""
import time
import os
import pandas as pd
import openpyxl
import excel2img
import csv

risk_file_path = os.path.abspath("../Risk/source/contents.rst")
risk_sheet_csv = os.path.abspath("../Risk/source/risks.csv")
matrix_sheet_xlsx = os.path.abspath("../Risk/source/matrix.xlsx")
summary_sheet_csv = os.path.abspath("../Risk/source/risk_summary.csv")
severity_sheet_csv = os.path.abspath("../Risk/source/risk_severity.csv")
matrix_picture_file = os.path.abspath("../Risk/source/risk_matrix.png")


actions = {
	"A": "Accept",
	"M": "Mitigate",
	"W": "Watch",
	"R": "Research",
}

rst_template = """
***********************
Risk Analysis
***********************

.. todo::
	Insert Risk Analysis introduction
	
.. csv-table:: Risk summary
	:widths: 20 100 100 50
	:header: "Risk #", "Name", "Statement", "Category"
	:file: {summary_file}
	
.. csv-table:: Risk Severities
	:widths: 20 100 100 100 50
	:header: "Risk #", "Likelihood (0-1)", "Consequence (0-1)", "Criticality LxC (0-1)", "Action"
	:file: {severity_file}
	
.. figure:: {risk_matrix_picture}
	:alt: A visual representation of risk severity
	
	A visual representation of risk severity

---------------------
Risk Descriptions
---------------------

{risk_descriptions}
"""

description_template = """
================================================================================
Risk {num} - {title}
================================================================================

.. table:: Likeliness, Consequence, and Severity

	+-------------------+----------------------+----------------------+
	| Likeliness (0-1)  | Consequence (0-1)    | Severity (0-1)       |
	+===================+======================+======================+
	|                   |                      |                      |
	+-------------------+----------------------+----------------------+
	
	{likeliness:}
	

{statement}

{description}

We plan to **{action}** this risk by following this plan:

{plan}

"""

def read_risks():
	data = pd.read_csv(risk_sheet_csv)
	data.index += 1
	return data

def calculate_criticality(data):
	data['Criticality'] = data['Likelihood'] * data['Consequence']
	
def write_summary_file(data):
	print("writing summary")
	data.to_csv(summary_sheet_csv, columns=["Name", "Statement", "Category"], header=False)
	print("summary written")
	
def write_severity_file(data):
	print("writing severity")
	data.to_csv(severity_sheet_csv, columns=["Likelihood", "Consequence", "Criticality", "Action"], header=False)
	print("severity written")
	
def categorize_risks(risks):
	grid = []
	for i in range(5):
		row = []
		for j in range(5):
			row.append([])
		grid.append(row)
	
	for likelihood in range(0,5):
		lowerLikelihood = round(likelihood * 0.2, 1)
		upperLikelihood = round(lowerLikelihood + 0.2, 1)
		
		if lowerLikelihood == 0:
			lowerLikelihood = -1
		
		for consequence in range(0, 5):
			lowerConsequence = round(consequence * 0.2, 1)
			upperConsequence = round(lowerConsequence + 0.2, 1)
			
			if lowerConsequence == 0:
				lowerConsequence = -1
			
			curBucketRisks = risks[risks.Consequence > lowerConsequence][["Likelihood","Consequence"]]
			curBucketRisks = curBucketRisks[risks.Consequence <= upperConsequence]
			curBucketRisks = curBucketRisks[risks.Likelihood > lowerLikelihood]
			curBucketRisks = curBucketRisks[risks.Likelihood <= upperLikelihood]
			curBucketRisks = curBucketRisks.index
			
			grid[likelihood][consequence] = ", ".join([str(i) for i in list(curBucketRisks)])
			
	return grid
	
def write_matrix(grid):
	workbook = openpyxl.load_workbook(matrix_sheet_xlsx)
	matrix_sheet = workbook.active
	cols = ["C", "D", "E", "F", "G"]
	rows = [2, 3, 4, 5, 6]
	for col in cols:
		for row in rows:
			consequence = cols.index(col)
			likelihood = rows.index(row)
			cell = col+str(row)
			r = likelihood+2
			c = consequence+3
			#matrix_sheet[cell] = ", ".join(grid[row][col])
			matrix_sheet.cell(row=r,column=c).value = grid[4-(r-2)][c-3]
			
	workbook.save(matrix_sheet_xlsx)
		

def capture_matrix():
	excel2img.export_img(matrix_sheet_xlsx, matrix_picture_file, "", "Matrix!A1:G8")
	
def create_descriptions(risks):
	descriptions = ""
	for index, row in risks.iterrows():
		descriptions += description_template.format(num = index,
		                                            title = row["Name"],
		                                            statement = row["Statement"],
		                                            description = row["Description"],
		                                            action = actions[row["Action"]],
		                                            plan = row["Action Plan"])
	return descriptions
	

def write_rst_file(descriptions):
	rst_contents = rst_template.format(summary_file=summary_sheet_csv,
	                                   severity_file=severity_sheet_csv,
	                                   risk_matrix_picture=matrix_picture_file,
	                                   risk_descriptions=descriptions)
	
	with open(risk_file_path, "w") as risk_file:
		risk_file.write(rst_contents)

if __name__ == "__main__":
	risk_file_path = os.path.abspath("./contents.rst")
	risk_sheet_csv = os.path.abspath("./risks.csv")
	matrix_sheet_xlsx = os.path.abspath("./matrix.xlsx")
	summary_sheet_csv = os.path.abspath("./risk_summary.csv")
	severity_sheet_csv = os.path.abspath("./risk_severity.csv")
	matrix_picture_file = os.path.abspath("./risk_matrix.png")
	
	risks = read_risks()
	calculate_criticality(risks)
	write_summary_file(risks)
	write_severity_file(risks)
	grid = categorize_risks(risks)
	write_matrix(grid)
	capture_matrix()
	descriptions = create_descriptions(risks)
	write_rst_file(descriptions)