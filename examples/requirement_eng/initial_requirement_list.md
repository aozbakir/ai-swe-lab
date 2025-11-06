# 📋 Stroopwafel Co. - Initial Requirements Specification

## ✅ Functional Requirements

### 📁 Data Collection & Parsing
- **FR1**: The system shall automatically retrieve vendor sales reports from email attachments.
- **FR2**: The system shall support parsing of `.csv`, `.xlsx`, and `.pdf` formats.
- **FR3**: The system shall handle variable field separators (comma, semicolon, tab).
- **FR4**: The system shall detect and adapt to different column orders in incoming files.
- **FR5**: The system shall extract key fields: date, vendor name, product variant, units sold, revenue, and location.

### 🧹 Data Cleaning
- **FR6**: The system shall impute missing numerical values (e.g., mean, median).
- **FR7**: The system shall standardize product names and codes using a predefined mapping.
- **FR8**: The system shall convert all dates to `YYYY-MM-DD` format.
- **FR9**: The system shall remove duplicate rows from vendor reports.
- **FR10**: The system shall flag and log malformed or incomplete files for manual review.

### 📊 Analysis & Report Generation
- **FR11**: The system shall calculate metrics like units sold, revenue, sales variance, and promo impact.
- **FR12**: The system shall generate human-readable weekly reports in Markdown format.
- **FR13**: The system shall optionally export reports as PDFs.
- **FR14**: The system shall include breakdowns by product variant and by province.

### 🔄 Workflow & Distribution
- **FR15**: The system shall store generated reports in a shared internal folder.
- **FR16**: The system shall retain prior versions of reports for traceability.
- **FR17**: The system shall log all data corrections and transformation steps.

### ⚠️ Exception Handling
- **FR18**: The system shall alert users when critical fields (e.g., revenue, units) are missing.
- **FR19**: The system shall allow manual correction or annotation of problematic entries before final reporting.

---

## 📐 Non-Functional Requirements

### ⏱️ Performance & Efficiency
- **NFR1**: The system shall reduce weekly manual effort from 10–15 hours to under 2 hours.
- **NFR2**: The system shall process a full week’s worth of reports within 10 minutes of initiation.

### 🧪 Accuracy & Data Quality
- **NFR3**: The system shall achieve ≥95% accuracy in parsing structured files.
- **NFR4**: The system shall identify and log ≥98% of missing or malformed entries.

### 📦 Scalability & Maintainability
- **NFR5**: The system shall support the addition of new vendors or changing report formats with minimal reconfiguration.
- **NFR6**: The system shall support modular processing steps (e.g., parsing, cleaning, analysis) for easier updates.

### 🔐 Security & Access Control
- **NFR7**: The system shall restrict access to sensitive data using role-based access control (RBAC).
- **NFR8**: The system shall log all data access and modifications for audit purposes.
- **NFR9**: The system shall encrypt data at rest and during transmission.

### 🧯 Reliability & Resilience
- **NFR10**: The system shall provide graceful error messages and recovery for failed file reads or parsing errors.
- **NFR11**: The system shall store backups of raw vendor files before processing.
