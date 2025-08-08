# Traceability Matrix

| ID            | System Requirement                 | Software Specifications          | Assumptions | Coverage | Notes |
|---------------|------------------------------------|----------------------------------|-------------|----------|-------|
| **REQ-FR1**   | Generate weekly sales report       | SPEC-FR1, SPEC-FR4, SPEC-FR5    | A1, A1a, A3 | ✔        |       |
| **REQ-FR2**   | Markdown/PDF output format         | SPEC-FR5, SPEC-FR6              | A6          | ✔        |       |
| **REQ-FR3**   | Monday availability               | SPEC-FR1, SPEC-NFR2             | A1a, A1b    | ✔        |       |
| **REQ-FR4**   | CSV/XLSX input support            | SPEC-FR2                        | A3          | ✔        |       |
| **REQ-FR5**   | Handle format variations          | SPEC-FR3, SPEC-FR8              | A3          | ✔        |       |
| **REQ-FR6**   | Manual report trigger             | SPEC-FR9                        | A7          | ✔        | Added SPEC-FR9 |
| **REQ-FR7**   | Save to `./reports/`              | SPEC-FR6                        | A4          | ✔        |       |
| **REQ-NFR1**  | Unattended operation              | SPEC-NFR1                       | A5          | ✔        |       |
| **REQ-NFR2**  | Report by 9 AM Monday             | SPEC-NFR2                       | A1a, A1b    | ✔        |       |
| **REQ-NFR3**  | ≤2 hrs manual effort              | SPEC-NFR3                       | A7          | ✔        |       |
| **REQ-NFR4**  | Cost <€10/month                   | SPEC-NFR4, SPEC-NFR9            | -           | ✔        | Added SPEC-NFR9 |
| **REQ-NFR5**  | Partial reports                   | SPEC-FR7, SPEC-NFR5             | A1b         | ✔        |       |
| **REQ-NFR6**  | Audit logging                     | SPEC-NFR6                       | -           | ✔        |       |
| **REQ-NFR7**  | Data validation                   | SPEC-FR8, SPEC-NFR7             | A3          | ✔        |       |
| **REQ-NFR8**  | Report archiving                  | SPEC-NFR8                       | -           | ✔        |       |
| **REQ-NFR9**  | Alerts for data issues            | SPEC-NFR10                      | A7          | ✔        | Added SPEC-NFR10 |