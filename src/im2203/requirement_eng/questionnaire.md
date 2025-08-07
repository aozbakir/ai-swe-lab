# 📋 Requirements Elicitation Interview Template
**Project Goal**: Automate the process of generating standardized weekly sales reports from heterogeneous vendor files.

---

## ✅ 1. Stakeholder Identification & Roles

- Who are the main users of the sales reports?  
- What are their roles or departments (e.g., Sales, Logistics, Management)?  
- Who is responsible for collecting, cleaning, and compiling the data?  
- Are there any stakeholders who approve or review the final report?  
- Who receives the final reports, and how are they distributed?

---

## 🔍 2. Current System Understanding

- Can you walk me through the current process of generating the weekly sales report?  
- What are the most important numbers or insights you personally look for in each report?  
- Does your current report contain all of this information?  
- What tools or software are used to compile and format the reports (e.g., Excel, Python, Notepad)?  
- Do you have an example report I can review?  
- Are the reports archived or version-controlled in any way?  
- How long does it typically take to generate one report from start to finish?  
- How often do reports need to be revised due to errors or missing data?  
- What are some common issues or pain points in the current process?

---

## 📂 3. Input Data Requirements

- Where do the vendor files come from (email, portal, shared drive)?  
- In what formats do vendors send their data (CSV, Excel, PDF, plain text)?  
- Do you get different formats from different vendors?  
- Do they use different field separators (e.g., comma, semicolon, tab)?  
- Are the columns always in the same order?  
- Do all reports include the same essential fields (e.g., date, vendor name, city, product, units, revenue)?  
- Do all vendors include a city or location in their reports?  
- What kinds of inconsistencies or errors do you commonly find in the incoming data?  
- Do vendors follow a consistent naming convention for files or products?  
- Are there vendors whose data is especially difficult to work with? Why?  
- How do you handle reports with missing or malformed data?

---

## 🧹 4. Data Cleaning & Preprocessing

- What steps are taken to clean the data before analysis?  
- Are there predefined rules for cleaning or is it done case-by-case?  
- What tools are used for cleaning (manual editing, Excel macros, scripts)?  
- How is missing or incorrect data typically resolved?  
- Is there a standardized schema or template the cleaned data conforms to?  
- Are any validation checks performed before the report is generated?  
- Are there any audit logs or documentation of what was cleaned/edited?

---

## 📈 5. Business Objectives

- What are the main business goals this report supports (e.g., inventory planning, sales performance, pricing decisions)?  
- What decisions are made based on this report?  
- What would happen if the report were delayed or incorrect?  
- Are there reports with similar structure used in other departments (e.g., marketing, finance)?

---

## ⚙️ 6. Automation Goals

- What would success look like for you if this process were automated?  
- Which parts of the workflow do you want to automate?  
- Are there any steps that must remain manual (e.g., approval, commentary)?  
- What data quality standards must an automated system meet?  
- What are the main risks you foresee with automation?  
- How often do new vendors join or change their reporting format?

---

## 📊 7. KPIs & Non-Functional Requirements

- Are there specific KPIs or metrics used to measure success (e.g., time saved, fewer errors)?  
- What is the current time spent per week on report preparation?  
- How accurate is the current manual process?  
- How consistent are the report formats across weeks and vendors?  
- Should the automated system generate human-readable reports (e.g., Markdown, PDF)?  
- Do you have preferences for which technologies should be used (Excel, Python, Google Sheets, etc.)?  
- Do you have existing infrastructure that we need to integrate with (e.g., shared folders, cloud storage, internal tools)?  
- Are there any security, access control, or compliance requirements?

---

## 🧠 8. Future Scalability & Change Handling

- How many vendors currently submit weekly sales reports?  
- How frequently do their file formats change?  
- Do you anticipate scaling this system for more vendors or other types of reports?  
- Would you want automated alerts for missing or inconsistent files?  
- Should the system adapt to new vendor formats automatically, or notify someone for manual intervention?

