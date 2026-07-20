# Algerian Documents — Types & PII Entities

## 1. Document Categories

### 1.1 Identity Documents
| Document | Arabic | French | Common Entities |
|----------|--------|--------|-----------------|
| National ID Card | بطاقة التعريف الوطنية | Carte d'Identité Nationale (CIN) | NIN (18 digits), full name, filiation (parents' names), DOB, birthplace, address, photo, wilaya |
| Passport | جواز السفر | Passeport | Passport number (2 letters + 6 digits), full name, DOB, birthplace, nationality, issue/expiry date, MRZ code |
| Driver's License | رخصة السياقة | Permis de Conduire | License number, full name, DOB, address, blood type, category, issue/expiry |
| Family Record Book | عقد العائلة أو دفتر العائلة | Livret de Famille | All family members' full names, DOBs, marriage date, spouses' names, children's NINs |
| Birth Certificate | شهادة ميلاد أو عقود الميلاد | Acte de Naissance / Extrait S.12 | Full name, DOB & time, birthplace, parents' full names, parents' professions, marginal notes |
| Residence Permit | بطاقة الإقامة | Carte de Séjour | Permit number, full name, nationality, employer, address, validity period |
| Death Certificate | شهادة وفاة | Acte de Décès | Full name, DOB, death date & place, surviving spouse |

### 1.2 Education Documents
| Document | Entites |
|----------|---------|
| Transcript / Relevé de Notes | Student full name, DOB, institution, diploma ID, grades, academic year |
| Diploma / Diplôme (BAC, Master, etc.) | Full name, DOB, diploma number, institution, date, average |
| School Certificate / Certificat de Scolarité | Full name, DOB, institution, class, academic year |
| Exam Invitation / Convocation | Full name, DOB, exam center, candidate number, date |

### 1.3 Medical Documents
| Document | Languages | Entities |
|----------|-----------|----------|
| Medical Record / Dossier Médical | FR / AR | Full name, DOB, NIN, **diagnosis (Cat III)**, **test results (Cat III)**, doctor name, hospital, dates |
| Prescription / Ordonnance | FR / AR | Patient name, DOB, doctor name, medications, date |
| Medical Certificate / Certificat Médical | FR / AR | Full name, DOB, **condition (Cat III)**, doctor name, date |
| Analysis Results | FR | Full name, DOB, **biological data (Cat III)**, lab name, date |
| Hospitalization Report | FR / AR | Full name, DOB, NIN, **diagnosis (Cat III)**, doctor name, hospital, admission/discharge dates |
| Radiology Report / Compte Rendu | FR / AR | Full name, DOB, **clinical findings (Cat III)**, doctor name, date |

### 1.4 Financial & Banking Documents
| Document | Languages | Entities |
|----------|-----------|----------|
| Bank Statement / Relevé Bancaire | FR | Full name, account number (RIB — 20 digits), balance, transactions, IBAN, BIC/SWIFT |
| Loan Agreement / Contrat de Prêt | FR / AR | Full name, employer, salary, loan amount, duration, interest rate, RIB, guarantor info, address |
| Payslip / Fiche de Paie | FR | Full name, employee ID, employer name, net/gross salary, social charges, bank details |
| Invoice / Facture | FR / AR | Company name, RC, NIF, NIS, Article, client name, address, amounts, TVA |
| Tax Declaration / Déclaration Fiscale | FR | Full name, NIF, address, income, employer, tax amount, fiscal year |
| RIB (Bank Identity) | FR | Full name, bank name, account number, agency code, IBAN |

### 1.5 Employment Documents
| Document | Languages | Entities |
|----------|-----------|----------|
| Employment Contract | FR / AR | Full name, DOB, employer, salary, job title, address, start date |
| CV / Resume | FR / AR / EN | Full name, DOB, address, phone, email, education history, work history |
| Work Certificate / Attestation de Travail | FR / AR | Full name, employer, job title, start date, salary |
| Resignation Letter | FR / AR | Full name, employer, date |
| Transfer Decision | FR / AR | Full name, old/new department, date |

### 1.6 Legal Documents
| Document | Languages | Entities |
|----------|-----------|----------|
| Court Judgment / Jugement | FR / AR | All party names, judge name, lawyer names, case number, dates, addresses, amounts |
| Notarized Act / Acte Notarié | FR / AR | Full names of all signatories, DOBs, addresses, NINs, property details, amounts |
| Official Report / Procès-Verbal | FR / AR | Full names, NINs, addresses, dates, officer name, badge number |
| Contract / Contrat | FR / AR | Full names, addresses, NINs, RC, NIF, amounts, dates |

### 1.7 Government & Administrative Documents
| Document | Languages | Entities |
|----------|-----------|----------|
| Commercial Register / Registre de Commerce | FR / AR | Company name, RC number, NIF, NIS, Article, owner name, address, activity |
| Company Statutes / Statuts | FR / AR | Owner names, NINs, addresses, capital amount, company name |
| Building Permit / Permis de Construire | FR / AR | Owner name, property address, permit number, architect name, date |
| Vehicle Registration / Carte Grise | FR / AR | Owner name, address, NIN, registration number, vehicle details |
| Ministerial Decision | FR / AR | Official names, reference numbers, dates |

### 1.8 Real Estate Documents
| Document | Languages | Entities |
|----------|-----------|----------|
| Property Title / Titre de Propriété | FR / AR | Owner name, NIN, property address, boundaries, area |
| Lease Agreement / Contrat de Location | FR / AR | Tenant name, landlord name, property address, rent amount, duration |
| Sales Deed / Acte de Vente | FR / AR | Buyer/Seller names, NINs, property details, amounts, notary name |

---

## 2. Complete Entity Reference

### 2.1 Algerian-Specific Entities

| Entity | Format | Example | Doc Types |
|--------|--------|---------|-----------|
| NIN (Numéro d'Identité Nationale) | 18 digits (6-6-6) | `123456 123456 123456` | Identity, Legal, Employment |
| Passport Number | 2 letters + 6 digits | `AB123456` | Passport only |
| RIB (Relevé d'Identité Bancaire) | 20 digits | `007 12345 6789100A BCD50` | Banking, Payroll |
| RC (Registre de Commerce) | 2 letters + 9+ digits | `B1234567890` | Invoices, Company docs |
| NIF (Numéro d'Identification Fiscale) | 15 digits | `123456789012345` | Invoices, Tax, Company |
| NIS (Numéro d'Identification Statistique) | 8 digits | `12345678` | Invoices, Company |
| Article (TVA) code | Alphanumeric | `123456A` | Invoices |
| Wilaya code | 2-digit (01-58) | `16` (Alger) | Addresses, all |
| Algerian Phone | 10 digits, starts 05/06/07 | `0551234567` | All |
| Algerian ZIP Code | 5 digits | `16000` | Addresses |
| Employee ID | Varies by company | `EMP-12345` | Employment, Payroll |
| Social Security N° | Probably 10+ digits | — | Medical, Employment |

### 2.2 Generic Entities (Across All Documents)

| Entity | Category (Legal) | Examples |
|--------|-----------------|----------|
| PERSON | I | Full names of individuals, signatories, officials |
| EMAIL_ADDRESS | I | mehdi@example.com |
| PHONE (DZ_PHONE) | I | 0551234567 |
| ADDRESS / LOCATION | I / II | Street, city, wilaya, country |
| NIN / ID_NUMBER | I | NIN, passport, RC, NIF, RIB |
| DATE_OF_BIRTH | I / II | 15/03/1990 |
| DATE | II | Document dates, signatures |
| AGE | II | 35 years |
| PROFESSION / TITLE | II | Doctor, Engineer, Manager |
| SALARY | II | 120,000 DZD |
| COMPANY_NAME | II | Sarl XYZ, Spa ABC |
| FINANCIAL_AMOUNT | II | 5,000,000 DZD |
| SIGNATURE | I | Names in signature blocks |
| HEALTH_DATA | III | Diagnosis, test results, medical condition |
| RELIGION | III | Mentioned in certain identity docs |
| POLITICAL_OPINION | III | Rare — membership, activity |
| GENETIC_DATA | III | Medical analysis results |

---

## 3. Risk Category Mapping (Loi 18-07 / 25-11)

| Category | Entities | Action |
|----------|----------|--------|
| **I — Direct Identifiers** | PERSON, NIN, EMAIL, PHONE, PASSPORT, RIB, RC, NIF, Signature | Mandatory removal before LLM |
| **II — Quasi-Identifiers** | DOB, AGE, PROFESSION, SALARY, ADDRESS (partial), ZIP, COMPANY | k-anonymize (cohort ≥ 5) |
| **III — Sensitive** | HEALTH, DIAGNOSIS, GENETIC, RELIGION, POLITICS | Absolute block — reject document |

---

## 4. Priority List for Implementation

Based on document frequency in Algerian enterprise archiving:

1. **Identity Docs** (CIN, Passport, Birth Certificate) — highest frequency
2. **Contracts & Invoices** — core business documents
3. **Payslips** — common HR archive items
4. **Medical Reports** — highest risk (Cat III)
5. **Bank Statements** — financial privacy
6. **Diplomas & CVs** — recruitment archives
7. **Court Judgments** — legal archives
8. **Property Titles** — real estate archives
