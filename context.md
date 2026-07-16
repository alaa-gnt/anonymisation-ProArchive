proarchive intrenship

# .1 Company Presentation

## ProArchive Solutions

ProArchive Solutions is a company specializing in document digitization, electronic archiving, and document management. Its core business consists of converting physical documents into searchable digital assets using high-volume scanning technologies, Optical Character Recognition (OCR), indexing systems, and electronic document management platforms.

The company serves organizations from multiple sectors including:

- Government administrations
- Banks
- Insurance companies
- Hospitals
- Educational institutions
- Legal firms
- Private companies

Consequently, the documents processed by ProArchive contain highly heterogeneous information with no predefined structure.

Unlike organizations operating within a single domain, ProArchive manages documents originating from numerous industries. This diversity introduces significant challenges regarding automated processing, information extraction, and privacy preservation.

---

# 1.2 Background

The rapid development of Large Language Models (LLMs) such as GPT-4, Claude, Gemini and Llama has dramatically changed the way organizations interact with textual information.

Instead of manually searching thousands of archived documents, users can now simply ask questions such as:

> Summarize this contract.
> 

> What is the customer's payment history?
> 

> Extract all obligations from this agreement.
> 

> Explain this medical report.
> 

This conversational interaction considerably improves productivity.

However, cloud-based LLMs require documents to be transmitted to external servers.

For organizations handling confidential archives, this creates major privacy and compliance concerns.

---

# 1.3 Problem Statement

The primary challenge addressed during this internship is:

> **How can confidential documents be safely processed by cloud-based Large Language Models without exposing sensitive information?**
> 

Although cloud LLMs provide remarkable reasoning capabilities, organizations cannot simply upload confidential documents because these documents may contain:

- Personal information
- Financial records
- Medical data
- Legal documents
- Corporate secrets
- Government identifiers

Since ProArchive serves multiple customers, document structures cannot be predicted beforehand.

Traditional rule-based anonymization designed for one document type is therefore insufficient.

---

# 1.4 Internship Objectives

The primary objective of this internship is to design and implement a Proof-of-Concept (PoC) capable of automatically detecting and anonymizing sensitive information before documents are processed by cloud LLMs.

Specific objectives include:

- Studying existing anonymization techniques.
- Identifying sensitive entities within heterogeneous documents.
- Designing a multilingual anonymization pipeline.
- Preserving document semantics after anonymization.
- Maintaining compatibility with cloud LLMs.
- Designing a modular architecture suitable for enterprise deployment.

---

# 1.5 Constraints

Several constraints define the scope of this internship.

### Cloud LLM must remain in the pipeline

The objective is **not** to replace cloud LLMs with local models.

Instead, sensitive information must be removed before interacting with external AI services.

---

### Unknown document structures

Unlike HR software or banking systems, ProArchive receives documents from completely different domains.

Consequently, no predefined schema can be assumed.

---

### Multilingual environment

Documents may appear in:

- Arabic
- French
- English

The anonymization system must therefore support multilingual document processing.

---

### Real-time processing

The anonymization stage should introduce minimal latency to preserve user experience.

---

### Extensibility

The solution should allow future integration of new entity recognizers without redesigning the entire system.

---

# 1.6 Deliverables

The internship will produce:

- Literature review
- Architecture design
- Sensitive data taxonomy
- Detection engine
- Anonymization engine
- Proof-of-Concept
- Evaluation methodology
- Technical report

---

# 1.7 Expected Contributions

This internship contributes toward the development of a privacy-preserving middleware positioned between enterprise documents and cloud-based AI systems.

The proposed solution aims to:

- Prevent accidental disclosure of confidential information.
- Improve regulatory compliance.
- Reduce legal risks.
- Enable organizations to safely leverage cloud LLMs.
- Remain independent of any specific LLM provider.

---

# 1.8 Scope of the Work

This internship focuses exclusively on the anonymization layer.

The following components are **outside the project's scope**:

- Training custom LLMs
- Developing OCR systems
- Building Retrieval-Augmented Generation (RAG) systems
- Replacing cloud LLMs with local inference
- Fine-tuning foundation models

Instead, the work concentrates on:

- Sensitive information detection
- Data anonymization
- Privacy-preserving document transformation
- Secure interaction with cloud LLMs

---

# 1.9 Research Questions

This internship seeks to answer the following research questions:

RQ1.

How can heterogeneous documents be automatically anonymized without predefined schemas?

RQ2.

Which sensitive data detection techniques provide the best balance between accuracy and computational cost?

RQ3.

How can document semantics be preserved after anonymization to maintain LLM reasoning performance?

RQ4.

Which anonymization strategy offers the best trade-off between privacy and usability?

RQ5.

How can multilingual documents be anonymized effectively?


## Approach trying to look into 

we are trying to look into working with Presidio as basline for our project 
we want to build on top of presedio to match our requirment as it should be 
working on discorvering more about presidio 

## Approach trying to look into 

working on establishing legal baseline based on the 18-07 algerian law and the 25-11 algerian law 

