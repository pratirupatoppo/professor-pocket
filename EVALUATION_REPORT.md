# Mid-Semester Prototype Evaluation

## System under test

The prototype is a local Flask web application using:

- 574 processed campus-policy chunks
- Persistent ChromaDB storage
- TF-IDF hybrid retrieval with scope-aware reranking
- Ollama
- `qwen2.5:1.5b` (optimized for faster CPU inference)

## Automated retrieval evaluation

The evaluation set contains 30 questions covering residence, attendance,
examinations, fees, scholarships, programmes, internships, XCOMM rules and
student services.

| Metric | Result | Target |
|---|---:|---:|
| Source Recall@5 | 100% | At least 85% |
| Required-term Recall@5 | 83.33% | At least 80% |
| Median retrieval latency | 18.77 ms | Under 10 seconds |
| Automated tests | 9 passed | All pass |

The source recall result means that the expected source document was present in
the top five retrieved passages for every evaluation question.

## End-to-end demonstrations

The following questions were sent through the live Flask API and answered by
the local SLM:

1. **Residence leave procedures** — returned FretBox, 48-hour, approval,
   emergency, gate-scanner and leave-register requirements.
2. **UG residence meal timings** — returned breakfast, lunch and dinner
   timings.
3. **Minimum attendance for end-semester examination** — returned 75%.

## Acceptance status

- Text question input: **Passed**
- Source retrieval: **Passed**
- Local SLM generation: **Passed**
- Grounded source metadata retained internally: **Passed**
- Source labels hidden from chat answers: **Passed**
- Missing-question validation: **Passed**
- Health endpoint: **Passed**
- Browser homepage: **Passed**
- Persistent index: **Passed**
- Automated tests: **Passed**

## Known limitations

- The source manuals contain OCR/extraction artefacts and some historical
  policy versions.
- The current evaluation checks retrieval evidence and answer examples; a
  larger human factuality review should be completed before production use.
- The current platform is text-only. Speech, robotics, sensors and navigation
  are intentionally excluded from the mid-semester milestone.
- Policy updates require rebuilding the processed chunks and ChromaDB index.
- Local SLM response time depends on the computer; the optimized 1.5B model
  returned the tested attendance answer in approximately 6.3 seconds.
