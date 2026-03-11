# Safety, Privacy, and Data Handling

## Overview
Safety and privacy practices reduce harm and ensure sensitive data is handled
responsibly across the full LLM lifecycle.

## Why it matters
LLMs can expose confidential data, amplify bias, and be exploited by prompt
injection if safeguards are missing.

## Key ideas
- Data minimization limits sensitive exposure
- PII detection and redaction protect users
- Access control and audit logs enforce governance
- Prompt injection and data exfiltration are common threats

## Practical workflow
- Classify data and define allowed use cases
- Mask or redact sensitive fields before inference
- Separate user data from shared prompts and memory
- Provide clear user consent and retention policies

## Failure modes
- Leaking secrets through logs or prompts
- Model memorization of sensitive data
- Inadequate redaction for structured inputs
- Inconsistent retention and deletion processes

## Checklist
- Maintain a data handling policy and DPIA
- Encrypt data at rest and in transit
- Add red-team tests for prompt injection
- Review vendor policies and security controls

## References
- NIST AI Risk Management Framework — https://www.nist.gov/itl/ai-risk-management-framework
- OWASP LLM Top 10 — https://owasp.org/www-project-top-10-for-large-language-model-applications/
