# Automated Report Generator Agent
Based on the following project trace, your assignment is to develop a comprehensive requirements document for an automated report generator system. Using LLM-assisted analysis to simulate customer and stakeholder requests, you will define the functional and technical specifications needed to process inconsistent weekly sales reports, aggregate and summarize sales data, and produce reliable outputs under strict local infrastructure and maintainability constraints. The requirements should address all aspects of the solution, including data parsing, normalization, automation, output formatting, error handling, and future adaptability.

## 📍 Context

Stroopwafel Co. is a mid-sized Dutch manufacturer distributing products through regional vendors and small retailers. These vendors submit **weekly sales reports** by email, typically as `.csv` or `.xlsx` attachments. 

Administrative staff save these files into a **shared internal folder**, but:

- File **names** are inconsistent (`"sales_final_v3.xlsx"`, `"friesland_2025-03.csv"`, etc.).
- File **formats vary** widely: different column names, merged cells, added notes, inconsistent date formats.
- Some vendors use **worksheets named by region**; others use **postal codes or city names**.
- No centralized database is in use.
- The company prefers to keep everything **local**, with **no cloud infrastructure** and **minimal external dependencies**.

---

##  🎯 Objective

Design a system that automatically generates a **weekly sales report** every Monday at 9:00 AM. The report must include:

- Total **sales per Dutch province** for the previous week (Monday to Sunday),
- (If possible) A **breakdown by product variant**,
- A short **human-readable summary** of the week’s performance,
- Output in **PDF format**,
- A **log of which files were processed**, and which were skipped (and why),
- Optionally: automatic email distribution to the Sales team.

---

##  🔒 Constraints

- ❌ No cloud services or SaaS tools,
- ❌ No relational database,
- ✅ Local filesystem access (Windows or Linux),
- ✅ Python or equivalent local scripting tools allowed,
- ✅ Minimal third-party dependencies (must be maintainable by non-developers),
- ✅ Should tolerate malformed or inconsistent files without crashing.

---

## 💡 Motivation for Agentic Systems

Over time, the company has seen increasing variation in how vendors submit their files. For example:
- Some send spreadsheets with summary rows and hand-written notes.
- Others use inconsistent region names (e.g., “Zuid-Holl.”, “ZHolland”, “Zuid-Holland”).

**Traditional script-based approaches have become brittle and high-maintenance.**

The company is open to considering **LLM-powered agentic systems** that can:
- Interpret irregular spreadsheets contextually,
- Infer structure dynamically,
- Map fuzzy geographic names to standard provinces,
- Generate summaries in natural language.

---

##  📋 Your Task

Propose a **complete solution architecture** that satisfies the company’s needs. Your proposal must include:

1. **Architecture Diagram**: Show major components and their interactions.
2. **Design Justification**: Explain your design choices—why you chose traditional vs. agentic approaches, libraries, tools, and file handling strategies.
3. **Parsing Strategy**: Describe how you will extract structured sales data from inconsistent input files.
4. **Region Mapping**: Explain how regional data will be normalized.
5. **Automation Plan**: Outline how the weekly scheduling will be implemented (cron, task scheduler, etc.).
6. **Output Generation**: Describe how PDF reports will be created and formatted.
7. **Logging & Error Handling**: Show how the system will handle failed files or ambiguous content.
8. **Maintainability**: Suggest how non-developers could monitor or adapt the system if vendor file formats change.
