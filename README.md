# AutiTrack AI

## AI-Assisted Developmental Observation Tracker

AutiTrack AI is an AI-assisted observation tracking platform designed
to organize caregiver observations and identify longitudinal patterns
for discussion with qualified professionals.

## Important

AutiTrack AI is NOT a diagnostic system.

The application does not diagnose autism or any other medical or
developmental condition.

It organizes recorded observations and generates neutral summaries.

---

## Features

### 1. Observation Analysis

Users can enter an observation along with:

- Context
- Activity
- Date

The AI organizes the observation into predefined domains:

- Communication
- Social Interaction
- Sensory
- Routine
- Behavior
- Daily Activity

---

### 2. Personal Baseline

The system calculates observation patterns against the user's
historical observation record.

The system focuses on the individual's own longitudinal record
rather than comparing individuals.

---

### 3. Context-Aware Patterns

Observations are grouped by:

- Context
- Activity
- Domain

This helps identify recurring recorded patterns in different
environments.

---

### 4. AI Trend Summary

The AI converts calculated analytics into a concise neutral summary.

---

### 5. AI Professional Session Brief

The system generates:

- Observation overview
- Recent changes
- Contextual patterns
- Notable observations
- Discussion points

The brief is intended to support discussion with a qualified
professional.

---

## Architecture

```text
                    ┌──────────────────┐
                    │  Streamlit UI    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Observation      │
                    │ Input            │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Gemini AI        │
                    │ Analysis         │
                    └────────┬─────────┘
                             │
                             ▼
             ┌──────────────────────────────┐
             │ Structured Observation Data  │
             └──────────────┬───────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        ┌──────────────┐        ┌──────────────┐
        │ SQLite       │        │ Analytics    │
        │ Database     │        │ Engine       │
        └──────────────┘        └──────┬───────┘
                                       │
                                       ▼
                              ┌────────────────┐
                              │ AI Trend       │
                              │ Summary        │
                              └───────┬────────┘
                                      │
                                      ▼
                              ┌────────────────┐
                              │ Session Brief  │
                              └────────────────┘
