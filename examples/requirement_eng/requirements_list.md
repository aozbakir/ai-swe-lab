# System and Software Requirements
This document distinguishes between system requirements and software specifications, and further categorizes them into functional (behavioral) and non-functional (quality) requirements.

System requirements describe what the system, as experienced by its users and stakeholders, must do (functional) and under what conditions or constraints it must operate (non-functional). Software specifications define how the software must behave to fulfill those system requirements, both in terms of observable functionality and internal qualities like performance, robustness, and cost-efficiency. For further information, consult [Gathering Requirements](../../../book/06-gathering-requirements.md#requirements-elicitation-techniques)

## Assumptions and Prerequisites
- **A1**: Vendors will submit their sales data files by Sunday 11:59 PM.
- **A1a**: Designated employees must save files by **8:00 AM Monday** (30-minute buffer).
- **A1b**: Files saved to the shared folder after 8:30 AM Monday will not be included in the current week’s report generation but can be processed in subsequent manual runs or the next scheduled run.
- **A2**: The shared folder structure is managed by IT and always accessible. If shared folder is unavailable, system alerts IT and retries for 15 minutes before failing gracefully.
- **A3**: All vendor files contain at minimum the fields: date, product, quantity, and region, formatted as expected.  
  *Files violating this assumption will be handled according to validation rules defined in REQ-NFR7.*
  - **A4**: System has read/write access to required network locations.
- **A5**: Windows Task Scheduler is available for automation. *This supports the requirement SPEC-NFR1 for scheduled, unattended execution of the system.*
- **A6**: Sales team members have access to view Markdown/PDF files.
- **A7**: Manual intervention is acceptable for severe data quality issues, provided automated alerts notify the responsible team promptly.

## Definitions

- **Imputation Methods**: Techniques used to fill missing or invalid data fields, such as replacing with averages, default values, or using simple heuristics to maintain data completeness.
- **Partial Reports**: Reports generated despite missing or incomplete vendor files, containing available data summaries and clearly indicating absent or incomplete sources without causing system errors.
- **Heuristics**: Rule-based methods or simplified decision-making strategies used by the system to handle data irregularities or uncertainties, such as guessing missing values based on historical patterns or default assumptions.
- **Normalize**: The process of transforming and standardizing input data files to a common structure and format, including converting separators, harmonizing column names, and standardizing data types to enable uniform processing.
- **Designated Employees**: Sales Data Coordinators (IT-managed Active Directory group `Sales_Uploaders`) with write permissions to `./vendor_uploads/`. Responsible for saving vendor files by 8:30 AM Monday.  
- **Authorized Users**: Members of the `Sales_Report_Admins` group with permissions to:  
  - Manually trigger report regeneration (REQ-FR6)  
  - Access partial/final reports in `./reports/`  

## Process Overview:
- Vendors submit sales data via email by Sunday 23:59.
- Designated employees collect and save these files into the shared folder by 8:30 AM Monday.
- The system reads all files in the shared folder at 8:30 AM Monday.
- If files are missing, the system generates partial reports and sends alerts.
- Authorized users can manually re-run reports if late files are added after 8:30 AM.
- The weekly report is finalized and distributed by 9 AM Monday.

## REQ – System Requirements

### Functional Requirements (REQ-FR)
- **REQ-FR1**: The system must generate a weekly sales report based on vendor-submitted data.
- **REQ-FR2**: The report must include sales summaries broken down by product variant and province, and be output in Markdown format.
- **REQ-FR3**: The report must be available every Monday.
- **REQ-FR4**: Vendors should submit sales data in CSV or XLSX.
- **REQ-FR5**: The system should support variations in vendor file formatting, including different separators and varying column orders.
- **REQ-FR6**: The system must support manual or ad-hoc report generation triggered by authorized users to accommodate late-arriving vendor files.
- **REQ-FR7**: The system must save the generated Markdown report to a designated `./reports/` folder and optionally convert it to PDF for wider compatibility among stakeholders.

### Non-Functional Requirements (REQ-NFR)
- **REQ-NFR1**: The system must operate without requiring human interaction under normal conditions.
- **REQ-NFR2**: The report must be distributed before 9 AM every Monday.
- **REQ-NFR3**: Human effort required for the reporting process should not exceed 2 hours per week.
**Acceptance Criteria**:
   - Logging shows manual correction steps take less than 2 hours on average during sample weeks.
   - User feedback confirms no more than 2 hours of manual work weekly.
- **REQ-NFR4**: The system should target monthly operating costs below €10, prioritizing free/open-source solutions. Costs up to €20 are permitted if justified by measurable benefits (e.g., reduced manual effort or improved reliability). Exceeding €20 requires stakeholder approval.
- **REQ-NFR5**: The system must tolerate missing or delayed input files and produce partial reports where feasible.  
**Acceptance Criteria**:
  - If one or more vendor files are missing, the report generation proceeds with available data.
  - The report clearly notes which vendor files were missing or incomplete.
  - No errors or crashes occur during missing file scenarios.
- **REQ-NFR6**: The system must log all data processing actions for auditing purposes.
- **REQ-NFR7**: The system must validate all incoming vendor data to ensure that mandatory fields (date, product, quantity, region) are present and that values fall within acceptable ranges or formats (e.g., non-negative quantities, valid dates).
**Acceptance Criteria**:
  - All required fields (date, product, quantity, region) must be present.
  - Numeric fields contain only valid numbers within expected ranges (e.g., quantity ≥ 0).
  - Invalid or missing data triggers a warning and causes the system to either correct (if possible) or mark affected entries.
- **REQ-NFR8**: The system must automatically archive generated reports as compressed files (e.g., ZIP) with timestamps, stored in a dedicated backup folder (e.g., `./backups/`). A rolling window of the last 4 weeks of backups must be maintained, deleting older archives to manage storage.
**Acceptance Criteria**:
  - Backup storage contains exactly 4 archived reports at any time.
  - Older backups beyond 4 weeks are automatically deleted to maintain the rolling window.
- **REQ-NFR9**: The system must automatically generate and send alerts to the operations team when severe data quality issues (e.g., missing mandatory fields in >20% of records) are detected, enabling timely manual intervention.
*Such issues are considered severe if they render more than 15% of the report data unreliable.*

## SPEC - Software Requirements (SPEC-FR)

### Functional Requirements
- **SPEC-FR1**: The system must begin reading all vendor-submitted sales data files from the designated shared folder at 8:00 AM every Monday, only after verifying that all files have been saved by designated employees according to assumption A1a.
- **SPEC-FR2**: The system must parse and normalize input files of types CSV or XLSX
- **SPEC-FR3**: The system must identify fields by header names (case-insensitive) or predefined aliases.
- **SPEC-FR4**: The system must compute weekly sales summaries grouped by product variant and province.
- **SPEC-FR5**: The system must output the compiled sales report in Markdown format.
- **SPEC-FR6**: The system must save the generated report to the specified output location before 9 AM every Monday.
- **SPEC-FR7**: The system must mark entries with missing data sources and include this information in the final report.
- **SPEC-FR8**:  The system should detect missing or invalid data fields in vendor files and apply imputation methods (see Definitions) or using simple heuristics to maintain data completeness before processing.
- **SPEC-FR9**: CLI command (`generate_report --force`) for manual regeneration. 

### Non-functional Requirements
- **SPEC-NFR1** (for REQ-NFR1): The system must execute as a scheduled background task without requiring manual startup or runtime interaction.
- **SPEC-NFR2** (for REQ-NFR2): The system must complete processing and finalize the weekly report by 8:50   AM every Monday.
- **SPEC-NFR3** (for REQ-NFR3): The system should include heuristics and fallback handling to reduce manual data correction to under 2 hours per week.
- **SPEC-NFR4** (for REQ-NFR4): The system could use only free/open-source software or infrastructure already available internally to meet the cost constraint.
- **SPEC-NFR5** (for REQ-NFR5): The system must tolerate absent input files by skipping them and generating a partial report with missing-data notices.
- **SPEC-NFR6** (for REQ-NFR6): The system must record logs of all file processing steps, including time of access, source filename, and transformation results.
- **SPEC-NFR7** (for REQ-NFR7): The system must verify required fields, data types, and value ranges before processing any vendor file.
- **SPEC-NFR8** (for REQ-NFR8): The system should automatically archive reports with timestamps and maintain a rolling 4-week backup window.
- **SPEC-NFR9**: Use only FOSS libraries to meet cost targets.
- **SPEC-NFR10**: Email alerts to `Sales_Ops_Team@company.com` for severe issues.
