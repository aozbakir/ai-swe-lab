# System and Software Requirements
This document distinguishes between system requirements and software specifications, and further categorizes them into functional (behavioral) and non-functional (quality) requirements.

System requirements describe what the system, as experienced by its users and stakeholders, must do (functional) and under what conditions or constraints it must operate (non-functional). Software specifications define how the software must behave to fulfill those system requirements, both in terms of observable functionality and internal qualities like performance, robustness, and cost-efficiency. For further information, consult [Gathering Requirements](../../../book/06-gathering-requirements.md#requirements-elicitation-techniques)

## REQ – System Requirements

### Functional Requirements (REQ-FR)
- **REQ-FR1**: The system must generate a weekly sales report based on vendor-submitted data.
- **REQ-FR2**: The report must include sales summaries broken down by product variant and province, and be output in Markdown format.
- **REQ-FR3**: The report must be available every Monday.
- **REQ-FR4**: Vendors may submit sales data in CSV, XLSX, or PDF format.
- **REQ-FR5**: The system must support variations in vendor file formatting, including:
  - different field separators in CSV files (comma, semicolon, tab)
  - varying column orders

### Non-Functional Requirements (REQ-NFR)
- **REQ-NFR1**: The system should operate without requiring human interaction under normal conditions.
- **REQ-NFR2**: The report must be distributed before 9 AM every Monday.
- **REQ-NFR3**: Human effort required for the reporting process must not exceed 2 hours per week.
- **REQ-NFR4**: Monthly operating costs must remain below €10.
- **REQ-NFR5**: The system must tolerate missing or delayed input files and produce partial reports where feasible.
- **REQ-NFR6**: The system must log all data processing actions for auditing purposes.
- **REQ-NFR7**: The system must validate all incoming vendor data for completeness and correctness.
- **REQ-NFR8**: The system must maintain recoverable backups of the last 4 weeks of reports.


## SPEC - Software Requirements (SPEC-FR)

### Functional Requirements
- **SPEC-FR1**: The system shall read all vendor-submitted sales data files from a designated shared folder every Monday at 6 AM as input.
- **SPEC-FR2**: The system shall parse and normalize input files of types:
  - CSV (detect and handle commas, semicolons, or tab separators)
  - XLSX
  - PDF
- **SPEC-FR3**: The system shall identify relevant fields by header names, allowing column order to vary across input files.
- **SPEC-FR4**: The system shall compute weekly sales summaries grouped by product variant and province.
- **SPEC-FR5**: The system shall output the compiled sales report in Markdown format.
- **SPEC-FR6**:  The system shall save the generated report to the specified output location before 9 AM every Monday.
- **SPEC-FR7**: The system shall mark entries with missing data sources and include this information in the final report.
- **SPEC-FR8**: The system shall detect missing or invalid data fields in vendor files and apply imputation methods to fill gaps where possible before processing.



### Non-functional Requirements
- **SPEC-NFR1** (for REQ-NFR1): The system shall execute as a scheduled background task without requiring manual startup or runtime interaction.
- **SPEC-NFR2** (for REQ-NFR2): The system shall finalize and save the weekly report by 8:55 AM every Monday.
- **SPEC-NFR3** (for REQ-NFR3): The system shall include heuristics and fallback handling to reduce manual data correction to under 2 hours per week.
- **SPEC-NFR4** (for REQ-NFR4): The system shall use only free/open-source software or infrastructure already available internally to meet the cost constraint.
- **SPEC-NFR5** (for REQ-NFR5): The system shall tolerate absent input files by skipping them and generating a partial report with missing-data notices.
- **SPEC-NFR6** (for REQ-NFR6): The system shall record logs of all file processing steps, including time of access, source filename, and transformation results.
- **SPEC-NFR7** (for REQ-NFR7): The system shall verify required fields, data types, and value ranges before processing any vendor file.
- **SPEC-NFR8** (for REQ-NFR8): The system shall automatically archive reports with timestamps and maintain a rolling 4-week backup window.
