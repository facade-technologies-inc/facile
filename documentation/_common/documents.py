# this variable contains the folder names that are inside of the documentation folder. They must
# be spelt exactly the same as the folders.

"""
DOCS:
============================================
Doc 1  - TDP
Doc 2  - IDL
Doc 3  - System Requirements Document
Doc 4  - Verification Documentation
	- ATP
	- Data Sheets
Doc 5  - Hardware Drawing Package
	- (Say not applicable)
Doc 6  - Software Drawing Package
Doc 7  - Software Version Description Document
Doc 8  - Software Design Document
Doc 9  - Models
	- Filled out data sheets
Doc 10 - User Manual
Doc 11 - Client Feedback Document
"""


order = [
	"TDP",
	"IDL",
	"SRD",
	"VD",
	"HDP",
	"SDP",
	"SVDD",
	"SDD",
	"Models",
	"UserManual",
	"CFD"
]

docnames = {
	# Documents that make up the TDP
	"TDP":        "19033_Facile_Technical_Data_Package",
	"IDL":        "19033_Facile_Indentured_Document_List",
	"SRD":        "19033_Facile_System_Requirements_Document",
	"VD":         "19033_Facile_Verification_Document",
	"HDP":        "19033_Facile_Hardware_Drawing_Package",
	"SDP":        "19033_Facile_Software_Drawing_Package",
	"SVDD":       "19033_Facile_Software_Verification_Description_Document",
	"SDD":        "19033_Facile_Software_Design_Document",
	"Models":     "19033_Facile_Models",
	"UserManual": "19033_Facile_User_Manual",
	"CFD":        "19033_Facile_Client_Feedback_Document",

	# Documents no longer in TDP
	"SCG":        "19033_Facile_Security_Classification_Guide",
	"ConOps":     "19033_Facile_Concept_of_Operations",
	"Proposal":   "19033_Facile_Unsolicited_Proposal",
	"Risk":       "19033_Facile_Risk_Analysis",
	"ATP":        "19033_Facile_Acceptance_Test_Procedures",
	"DataSheets": "19033_Facile_Acceptance_Test_Data_Sheets"
}

releases = {
	# Documents that make up the TDP
	"TDP":        "B1",
	"IDL":        "A1",
	"SRD":        "D1",
	"VD":         "A1",
	"HDP":        "A1",
	"SDP":        "B1", # Renamed from "Drawings"
	"SVDD":       "A1",
	"SDD":        "B1",
	"Models":     "A1",
	"UserManual": "A1",
	"CFD":        "A1",

	# Documents no longer in TDP.
	"Risk":       "A1",
	"ATP":        "A1",
	"DataSheets": "A1",
	"Proposal":   "A1",
	"ConOps":     "B1",
	"SCG":        "A1"
}