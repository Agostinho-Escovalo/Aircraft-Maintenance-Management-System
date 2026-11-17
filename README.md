# **Aircraft Maintenance Information System**

An information system for managing aircraft fleet, components, and maintenance history. Built with Python and PostgreSQL, providing a complete workflow for tracking maintenance operations, specialists, and spare parts.

## Table of Contents

- Overview
- Features
- Tech Stack
- Usage

### *Overview*

The system is designed for aviation maintenance organizations and covers the full lifecycle of aircraft maintenance:
- Registering aircraft and their models
  <img width="1474" height="736" alt="image" src="https://github.com/user-attachments/assets/d3235fbb-8ef0-4140-b39a-a11b95ec74c8" />

- Scheduling and recording maintenance events
  <img width="1349" height="631" alt="image" src="https://github.com/user-attachments/assets/5249225c-f0a3-4c18-87b6-64d8d3f3d64a" />
- Generating and exporting maintenance history reports
  <img width="1333" height="520" alt="image" src="https://github.com/user-attachments/assets/c0bf26b5-78f5-479a-991c-c5623104084f" />
- Showing statistics
  <img width="1353" height="528" alt="image" src="https://github.com/user-attachments/assets/03536dd9-8a43-420a-bf02-c3089d1dc44b" />

### *Features*

Based on four main user scenarios:
1. Browse & Filter Aircraft
- Filter by airline, model (via JOIN), flight hours range, and maintenance status
- Results displayed in a sortable table with pagination

2. Add New Records
- Register a new aircraft (ID, registration number, model, airline, production date, hours, cycles)
- Install a new component: select aircraft, component type, serial number, installation date

3. Edit & Delete
- Edit maintenance records and change status: Scheduled → In Progress → Completed
- Deletion is blocked when the record has related work_execution entries (referential integrity)

4. Generate Reports
- Select an aircraft and view full maintenance history
- Details include: work name, work type, assigned specialists, and used spare parts
- Export to CSV using Python's csv.writer

### *Tech Stack*

   Layer         →                           Technology
   
  Database        →                           PostgreSQL
  
  DB Management       →                       pgAdmin
  
  Language             →                     Python 3 
  
  Data Access          →                    SQL (SELECT, JOIN, INSERT, UPDATE, DELETE) 

### *Usage*

1. Launch the application — the main menu appears
2. Navigate between sections: Aircraft, Maintenance, Components, Reports
3. Use filters on the Aircraft page to narrow results
4. Click "Add Component" to register a new component for an aircraft
5. Open a maintenance record to edit its status or delete it
6. Go to Reports, select an aircraft, and export the maintenance history to CSV



### Author

Agostinho Xicote Escovalo

Developed as a Master's project in Aviation Systems, Data Analysis.
