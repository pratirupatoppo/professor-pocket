# Software Requirements Specification

## Edge AI-Based Smart Campus Information Robot Using Small Language Models

### Mid-Semester AI Assistant Prototype

**Version:** 1.0  
**Project:** Thesis-I  
**Prepared for:** XIM University campus-information prototype

## 1. Purpose

This document specifies the requirements for the mid-semester deliverable: a
working campus-information assistant that answers student and visitor questions
using verified campus documents, retrieval-augmented generation (RAG), and a
small language model (SLM).

The mid-semester prototype is software-first. Robot movement, speech
interaction, and edge-hardware integration are reserved for the end-semester
phase.

## 2. Reference sources

The initial knowledge base will use:

- `Mop_UG_AY 2023-24.txt` — university-wide undergraduate policies and
  programme structures.
- `345_Resident_Student_Policy_2025_26_NC.txt` — 2025–26 residence,
  services, timings, contacts, and residence rules.
- `MOP1.txt` — XCOMM-specific policies for B.Sc. (Hons.) and MA Mass
  Communication.
- `Abstract.pdf` — project objectives and proposed system capabilities.

The system shall preserve each source's title, scope, effective period, section,
and source location. The source documents are not assumed to have equal
authority or equal currency.

## 3. Scope

### 3.1 In scope

- Text-based question and answer interaction.
- Document ingestion and text cleaning.
- Metadata-aware chunking.
- Embedding generation and vector retrieval.
- SLM-based answer generation using retrieved context.
- Source and section attribution.
- Explicit handling of insufficient or conflicting evidence.
- Basic web or desktop interface.
- Evaluation of retrieval quality, factual correctness, attribution, and
  response latency.

### 3.2 Out of scope for mid-semester

- Autonomous robot movement.
- Mapping, localization, and obstacle avoidance.
- Speech recognition and text-to-speech.
- Production authentication and student-record access.
- Automatic policy updates from the internet.
- Binding interpretation of disciplinary, medical, or legal matters.

## 4. Users and user classes

| User | Typical needs |
|---|---|
| UG student | Attendance, examinations, fees, programme and course information |
| PG/PhD resident | Residence rules, leave, mess, medical and contact information |
| XCOMM student | School-specific attendance, examination, studio and programme rules |
| Visitor | General campus services and publicly appropriate directions |
| Knowledge-base administrator | Add, remove, validate, and version source documents |

The prototype should ask a clarifying question when the answer depends on
programme, school, residence status, or academic year.

## 5. Functional requirements

### FR-01: Accept questions

The system shall accept a natural-language text question and provide a response
without requiring the user to know the wording used in the source document.

### FR-02: Identify query context

The system shall identify, or ask for, relevant context including:

- user category;
- programme or school;
- resident/non-resident status;
- academic year; and
- question topic.

### FR-03: Ingest documents

The administrator shall be able to ingest a source document with metadata:

```text
document_id
title
source_filename
scope
audience
school
academic_year
effective_from
effective_to
authority
revision
```

### FR-04: Preserve structure

The ingestion process shall preserve headings, numbered rules, tables,
programme names, semester numbers, course names, credits, and source locations
where they can be reliably extracted.

### FR-05: Retrieve evidence

For each query, the system shall retrieve one or more relevant passages and
retain their source metadata. Retrieval should support both semantic similarity
and exact matching for names, numbers, dates, timings, fees, and contact
details.

### FR-06: Apply source scope and currency

The retrieval layer shall prefer the newest applicable source and shall not
combine rules from different scopes unless the response clearly distinguishes
them.

Recommended precedence:

1. Current policy applicable to the user's programme or residence.
2. Current university-wide policy.
3. School-specific policy where the school owns the procedure.
4. Older policy only when no applicable current source is available.

This precedence is a prototype rule and must be confirmed by the University
before production use.

### FR-07: Generate grounded answers

The SLM shall answer only from retrieved evidence and shall not invent campus
facts, contacts, policies, timings, or procedures.

### FR-08: Cite sources

Each substantive answer shall include the source document and section or
location used to form the answer.

### FR-09: Handle missing evidence

When relevant evidence is not retrieved, the system shall say that it cannot
verify the answer and shall direct the user to an appropriate office or
administrator where possible.

### FR-10: Handle conflicts

When applicable sources disagree, the system shall:

1. identify the conflicting scope or effective period;
2. avoid presenting the conflict as one unified rule;
3. prefer the configured current source; and
4. recommend confirmation from the responsible authority.

### FR-11: Provide structured answers

The interface shall render lists, steps, timings, tables, and source citations
in a readable form.

### FR-12: Record evaluation data

For testing, the system shall record query text, retrieved source identifiers,
response latency, answer status, and evaluator judgement. Personal information
shall not be recorded in test logs.

## 6. Non-functional requirements

### NFR-01: Factuality

The answer must be supported by at least one retrieved passage for every
policy-specific claim.

### NFR-02: Attribution

At least 95% of evaluated answers should include a correct source and section
reference in the target test set.

### NFR-03: Retrieval quality

The target is at least 85% Recall@5 on the curated question set.

### NFR-04: Response time

On the development machine, the target is a median end-to-end response time of
10 seconds or less. The result shall be reported separately for retrieval and
generation.

### NFR-05: Reproducibility

The team shall record the model, embedding model, chunking settings, index
configuration, and source-document revisions used for each evaluation.

### NFR-06: Privacy

The prototype shall not collect student identity, parent contact data, or
personal conversation history unless explicitly required for testing. Sensitive
contact details shall be access-controlled or masked before a public
demonstration.

### NFR-07: Availability

The assistant shall return a clear error or unavailable-evidence message rather
than a fabricated answer when the model, index, or source files are unavailable.

## 7. Knowledge-base requirements

Each chunk shall contain:

```text
chunk_id
document_id
text
heading_path
section_number
page_or_line_reference
scope
audience
school
programme
academic_year
effective_from
effective_to
source_priority
```

Exact-value records should additionally be stored in structured tables for:

- contacts;
- office and service hours;
- meal timings;
- fees and penalties;
- attendance thresholds;
- grade thresholds;
- programme duration and credits; and
- semester-wise courses.

## 8. Safety and limitations

The assistant shall not:

- make disciplinary decisions;
- approve leave or examination exceptions;
- provide diagnosis or emergency medical advice;
- expose restricted personal contact information to unauthorised users;
- claim that an old manual is current;
- infer a user's programme when that choice affects the answer.

Emergency, medical, disciplinary, and legal questions shall include a
recommendation to contact the relevant authorised office or emergency service.

## 9. Acceptance criteria

The mid-semester prototype is acceptable when:

1. A user can submit a campus question through the interface.
2. The system retrieves relevant passages from the supplied documents.
3. The SLM produces a grounded answer.
4. The answer includes a source citation.
5. The system can state when evidence is missing.
6. At least one programme-specific conflict is detected or safely disambiguated.
7. The evaluation set includes at least 30 questions across academic,
   residence, contact, examination, and programme topics.
8. Retrieval quality, attribution, factuality, and latency are reported.

## 10. Future-phase requirements

The end-semester system may extend this SRS with:

- local edge inference;
- speech-to-text;
- text-to-speech;
- touch-screen interaction;
- destination selection;
- navigation and obstacle avoidance;
- robot hardware control; and
- offline operation on the target device.

