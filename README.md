# General Project Information
## Group Members
- Colson Swope - swopec2@wwu.edu
- Jonathan Ly - lyj5@wwu.edu
- Ripkin Stork - storkr@wwu.edu
- Slate Colebank - colebas@wwu.edu

## Resources In Use
List any resources that you have used.

We used the CVE list, NIST documents, 

https://www.geeksforgeeks.org/create-a-file-path-with-variables-in-python/

https://chatgpt.com/share/67f16589-50a8-8003-b7fd-a843ba498f1c

https://stackoverflow.com/questions/5163144/what-are-the-special-dollar-sign-shell-variables

https://chatgpt.com/share/67d5b050-ac04-8003-92bf-678ce225dd28

https://github.com/CVEProject/cvelistV5

https://www.datacamp.com/tutorial/how-to-train-a-llm-with-pytorch

https://github.com/ollama/ollama/blob/main/docs/import.md

https://medium.com/@callumjmac/implementing-rag-in-langchain-with-chroma-a-step-by-step-guide-16fc21815339

https://csrc.nist.gov/projects/risk-management/about-rmf

https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf

https://csrc.nist.gov/projects/risk-management/about-rmf

https://press.rebus.community/requirementsengineering/back-matter/appendix-d-ieee-830-sample/

https://www.youtube.com/watch?v=g8fMRuGR5z0

https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf

https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-40ver2.pdf

https://nvd.nist.gov/

https://github.com/CVEProject/cvelistV5


## Project Outcome
List the outcome of the project:

We’ve developed a Cybersecurity AI RMF tool that collects system information from Windows 11 and Debian 12 machines, sends it to our server for processing, and generates an RMF-style report assessing the risks associated with system patches and version data.

# Project Background & Motivations
## Previous Projects
Does this project build off of any previous projects?

This is the first iteration of this project.

## Project Focus
**Motivating factors**

Manual RMF compliance processes are time-consuming and error-prone.

Organizations need a faster, automated way to assess and document patch management compliance.

There's increasing pressure to meet cybersecurity standards efficiently due to growing threats and regulatory oversight.


**Goals of the project**

Automate RMF patch management assessment using AI.

Simplify compliance reporting across Debian 12 and Windows 11 systems.

Provide accurate, secure, and actionable reports in line with NIST guidelines.

Create a user-friendly GUI to control report generation and export.

## Vision Statement
Vision for the project

The AI RMF tool is a standalone system designed to operate independently. It collects software version data from target machines, evaluates their compliance with NIST patch management standards, and recommends the changes needed to achieve compliance.

# Deliverables & Outcome
## Technology Utilized
What technology was used for the features implemented?

- CVE List and NIST documentation for vulnerability and compliance references
- ChromaDB for efficient local vector storage and retrieval
- Ollama running the LLaMA 3.2 model for natural language analysis and compliance reasoning
- Python, using PythonDocs and ReportLab for generating DOCX and PDF reports
- Target platforms include Debian 12 and Windows 11 systems for cross-OS compatibility

## Major Features
What major features were implemented?

- AI Model Integration: Uses Ollama (LLaMA 3.2) trained on NIST 800-40 Rev. 4 to assess compliance and generate recommendations.
- Cross-Platform Data Collection: Gathers patch/version data from both Windows 11 and Debian 12 systems.
- Web-Based GUI: Dashboard for generating reports, viewing report history, and exporting results.
- RMF Report Generation: Formats collected data into RMF-style reports with prioritized updates and compliance summaries.
- Export Options: Generates downloadable reports in .pdf and .docx formats using ReportLab.
- Scalability: Supports up to 10 machines , dynamically updating system info as new devices are added.
- Security Measures: Input sanitization, and isolation within WWU Cyber Range.


## Project Architecture
What is the general architecture of the features implemented?

**Client Layer:**
- Windows 11 and Debian 12 machines run scripts to collect software/patch data.

**Data Transport Layer:**
- Data is transmitted over the local network.

**Server Layer (Host Machine):**
- Receives and aggregates client data.
- Uses ChromaDB for CVE storage and retrieval.
- Runs the AI model (via Ollama using LLaMA 3.2) to assess RMF compliance.

**AI Processing Layer:**
- Takes formatted input, analyzes compliance, and generates natural language outputs based on NIST standards.

**Report Generation Layer:**
- Formats AI output using Python-docx and ReportLab into downloadable .docx and .pdf RMF-style reports.

**Presentation Layer (Web GUI):**
- Browser-accessible dashboard (compatible with Chromium and Firefox).
- Allows users to choose machines for data collection and download reports.


## Project Achievements
What did this project achieve overall?

Automated RMF Compliance: 
Streamlined the patch management assessment process using AI aligned with NIST SP 800-40 Rev. 4.

Cross-Platform Support:
Successfully collected and processed data from both Windows 11 and Debian 12 systems.

Functional AI Integration: 
Implemented a working LLaMA 3.2 model via Ollama for interpreting and evaluating compliance data.

Report Generation: 
Delivered exportable RMF-style reports in PDF/DOCX formats with actionable recommendations.

User-Friendly Interface: 
Developed a responsive web GUI for report control and management.


## Areas for Future Work
Where could future projects build upon the previous work?

Advanced AI Model Integration: 

Future work could integrate more powerful or fine-tuned LLMs (e.g. GPT-4, Claude 3) trained specifically on cybersecurity data to improve accuracy and context-awareness in compliance assessments.








