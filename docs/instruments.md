# Style Analysis Instruments

Structured framework of all detection patterns, structures, and markers.

---

## Framework Overview

```
STYLE ANALYSIS INSTRUMENTS
│
├── 1. AI DETECTION INSTRUMENTS
│   ├── Structural Markers
│   ├── Lexical Markers
│   ├── Discourse Markers
│   ├── Coherence Patterns
│   └── Stylistic Uniformity
│
├── 2. RHETORIC INSTRUMENTS
│   ├── Argumentative Structures
│   ├── Sentence-Level Patterns
│   ├── Paragraph-Level Patterns
│   ├── Classical Figures
│   └── Voice & Stance Markers
│
├── 3. PROVENANCE INSTRUMENTS
│   ├── Idiomatic Competence
│   ├── L1 Transfer Patterns
│   ├── Domain/Subcultural Markers
│   └── AI-Specific Patterns
│
└── 4. LEVEL ASSESSMENT INSTRUMENTS
    ├── Command Indicators
    ├── Complexity Indicators
    └── Composite Indices
```

---

## 1. AI Detection Instruments

### 1.1 Structural Markers

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| S01 | **Thesis-First Check** | Formulaic openings | First sentence = main claim + "This is/means..." |
| S02 | **Summary Closing Check** | Formulaic endings | Final paragraph restates points explicitly |
| S03 | **Section Preview Check** | Over-signposting | Sections begin with "This section examines..." |
| S04 | **Bullet Ratio** | List-heaviness | Count: bullet items / total sentences |
| S05 | **Table Ratio** | Over-structuring | Count: tables / 1000 words |
| S06 | **Parallel Structure Scan** | Repetitive patterns | "X does Y. X does Z. X does W." patterns |

### 1.2 Lexical Markers

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| L01 | **Register Variance** | Flat formality | Count register shifts; 0 shifts = AI signal |
| L02 | **Corporate Vocabulary Density** | Business-speak | Count: "utilize," "facilitate," "leverage" etc. |
| L03 | **Redundant Modifier Check** | Semantic padding | "fundamental change," "core principles" etc. |
| L04 | **Nominalization Ratio** | Wordiness | Count: -tion/-ment nouns vs. verb forms |
| L05 | **Filler Phrase Count** | Padding | "It is worth noting," "It is important to note" |
| L06 | **Contraction Rate** | Formality mismatch | Contractions / opportunities for contraction |
| L07 | **Idiosyncratic Vocabulary Check** | Personal style | Presence of unique/unusual word choices |

### 1.3 Discourse Markers

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| D01 | **Transition Density** | Over-explicit linking | Connectives ("Furthermore," etc.) / paragraph count |
| D02 | **Causal Chain Detection** | Over-explicit logic | "This means... This leads to... This results in..." |
| D03 | **Enumeration Pattern** | Mechanical sequencing | "First... Second... Third... Finally..." |
| D04 | **Signposting Count** | Metacommentary | "Let's examine," "Consider the following" |
| D05 | **Reader Address Check** | Generic engagement | "You might wonder," "As you can see" |
| D06 | **Section Label Check** | Over-categorization | "Example:" before examples |

### 1.4 Coherence Patterns

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| C01 | **Paragraph Connection Test** | Paragraph islands | Do topic sentences build on each other? |
| C02 | **Semantic Overlap Check** | Repetitive phrasing | Same concept in different words across paragraphs |
| C03 | **Synthesis Quality** | Missing integration | Does conclusion emerge or just restate? |
| C04 | **Certainty Variance** | Flat confidence | Distribution of hedging across claims |
| C05 | **Hedging Density** | Calibration | Epistemic markers ("perhaps," "likely") / claims |
| C06 | **Source Attribution Check** | Pseudo-authority | Claims presented as fact without grounding |

### 1.5 Stylistic Uniformity

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| U01 | **Sentence Length Variance** | Monotonous rhythm | Std dev of words/sentence |
| U02 | **Complexity Variance** | Uniform syntax | Mix of simple and complex clauses |
| U03 | **Rhythm Analysis** | Predictability | Short-after-long patterns |
| U04 | **Paragraph Length Variance** | Block uniformity | Std dev of sentences/paragraph |
| U05 | **First-Person Rate** | Voice presence | "I" occurrences / 1000 words |
| U06 | **Personality Intrusion Check** | Stance visibility | Humor, irritation, enthusiasm markers |

---

## 2. Rhetoric Instruments

### 2.1 Argumentative Structures

| ID | Instrument | What It Analyzes | Detection Method |
|----|------------|------------------|------------------|
| A01 | **Thesis Position Mapping** | Argument structure | Where is main claim? (first/delayed/embedded/absent) |
| A02 | **Evidence Pattern Classification** | Proof strategy | Example-first / Principle-first / Accumulation / Single decisive |
| A03 | **Concession Detection** | Objection handling | "This isn't about X" / "True, but..." / Strawman / Steel-man |

### 2.2 Sentence-Level Patterns

| ID | Instrument | What It Analyzes | Detection Method |
|----|------------|------------------|------------------|
| R01 | **Sentence Type Distribution** | Variety | % declarative-short / declarative-complex / interrogative / imperative / fragment |
| R02 | **Clause Relationship Analysis** | Syntax style | Parataxis vs. hypotaxis ratio |
| R03 | **Position Effect Mapping** | Emphasis patterns | Initial/final/parenthetical content placement |
| R04 | **Asyndeton/Polysyndeton Detection** | Rhythm devices | Lists without/with repeated conjunctions |

### 2.3 Paragraph-Level Patterns

| ID | Instrument | What It Analyzes | Detection Method |
|----|------------|------------------|------------------|
| P01 | **Paragraph Structure Classification** | Organization | Topic-support / Inductive / Pivoting / Narrative / Enumerative |
| P02 | **Transition Type Mapping** | Connection style | Additive / Adversative / Causal / Temporal / Implicit |
| P03 | **Cohesion Device Inventory** | Linking methods | Repetition / Synonymy / Pronoun / Parallel structure |

### 2.4 Classical Figures

| ID | Instrument | What It Analyzes | Detection Method |
|----|------------|------------------|------------------|
| F01 | **Repetition Figure Scan** | Emphasis patterns | Anaphora / Epistrophe / Anadiplosis |
| F02 | **Contrast Figure Scan** | Opposition patterns | Antithesis / Oxymoron / Paradox / Chiasmus |
| F03 | **Amplification Figure Scan** | Scale patterns | Hyperbole / Climax / Litotes |

### 2.5 Voice & Stance Markers

| ID | Instrument | What It Analyzes | Detection Method |
|----|------------|------------------|------------------|
| V01 | **Epistemic Modality Inventory** | Certainty calibration | Certainty / Probability / Possibility / Necessity distribution |
| V02 | **Evidentiality Mapping** | Source marking | Direct / Inference / Hearsay / Assumption |
| V03 | **Evaluative Language Classification** | Judgment style | Explicit / Implicit / Distancing |
| V04 | **Metaphor Pattern Analysis** | Conceptual framing | Journey / Architecture / Flow / Warfare / Organism domains |
| V05 | **Frame Detection** | Topic framing | Shift / Tool / Partner / Threat frames |

---

## 3. Provenance Instruments

### 3.1 Idiomatic Competence

| ID | Instrument | What It Assesses | Detection Method |
|----|------------|------------------|------------------|
| I01 | **Collocation Accuracy Check** | Native-like pairings | Sample 10 collocations; count errors |
| I02 | **Phrasal Verb Ratio** | Phrasal vs. Latinate | Phrasal verbs / Latinate equivalents |
| I03 | **Idiom Use Assessment** | Fixed expression competence | Idiom count; appropriateness check |
| I04 | **Preposition Accuracy** | L1 interference | Systematic preposition error patterns |

### 3.2 L1 Transfer Patterns

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| T01 | **German Transfer Check** | German L1 markers | Verb-final calques, compound formation, article patterns |
| T02 | **Romance Transfer Check** | Romance L1 markers | Adjective position, article insertion |
| T03 | **East Asian Transfer Check** | East Asian L1 markers | Article/plural difficulties |
| T04 | **Hyper-Correctness Scan** | Over-application | Whom overuse, subjunctive extension, formal vocabulary |
| T05 | **Avoidance Pattern Detection** | What's missing | Phrasal verb avoidance, idiom under-use, no contractions, no fragments |

### 3.3 Domain/Subcultural Markers

| ID | Instrument | What It Identifies | Detection Method |
|----|------------|-------------------|------------------|
| M01 | **Domain Vocabulary Profile** | Professional affiliation | Software / Agile / Philosophy / Startup vocabulary density |
| M02 | **Academic vs. Trade Classification** | Discourse community | Hedging level, citation style, claim directness |
| M03 | **Generational Marker Check** | Generation markers | Pre-digital / Digital native / AI-era patterns |
| M04 | **Code-Switching Analysis** | Language mixing | Lexical insertion, calques, flagged borrowing |

### 3.4 AI-Specific Patterns

| ID | Instrument | What It Detects | Detection Method |
|----|------------|-----------------|------------------|
| AI01 | **Idiom Avoidance Check** | Generic phrasing | Absence where idiom expected |
| AI02 | **Collocation Consistency** | Generic correctness | Always correct but never creative |
| AI03 | **Register Uniformity Test** | No code-switching | Flat formality throughout |
| AI04 | **Cultural Reference Check** | Generic equivalents | No proverbs, no specific allusions |
| AI05 | **Hybrid Register Detection** | AI-assisted markers | Voice appears/disappears across sections |
| AI06 | **Idiom Island Detection** | Inconsistent distribution | Human idioms in generic matrix |
| AI07 | **Over-Structure Detection** | Too-neat organization | Tables and bullets organizing original ideas |

---

## 4. Level Assessment Instruments

### 4.1 Command Indicators

| ID | Instrument | What It Measures | Method |
|----|------------|------------------|--------|
| CMD01 | **Vocabulary Range** | Lexical breadth | Type-token ratio |
| CMD02 | **Word Choice Precision** | Semantic accuracy | Generic vs. exact term ratio |
| CMD03 | **Collocation Error Rate** | Idiomatic accuracy | Errors / opportunities |
| CMD04 | **Register Vocabulary Match** | Context sensitivity | Appropriate terms for context |
| CMD05 | **Clause Complexity Range** | Grammatical range | Simple to complex sentence distribution |
| CMD06 | **Subordination Fluency** | Syntactic control | Correct vs. avoided/incorrect subordination |
| CMD07 | **Tense/Aspect Control** | Temporal precision | Accuracy in complex temporal marking |
| CMD08 | **Cohesion Device Variety** | Discourse range | Count of different cohesion types used |
| CMD09 | **Hedging Calibration** | Pragmatic skill | Strategic vs. random hedging |
| CMD10 | **Implicature Success** | Indirect meaning | Effective implicit communication |

### 4.2 Complexity Indicators

| ID | Instrument | What It Measures | Method |
|----|------------|------------------|--------|
| CX01 | **Sentence Length Mean** | Syntactic complexity | Average words/sentence |
| CX02 | **Clause Depth Max** | Embedding complexity | Maximum nesting level |
| CX03 | **Subordination Ratio** | Syntactic density | Dependent clauses / total |
| CX04 | **T-Unit Length** | Minimal unit complexity | Words per T-unit |
| CX05 | **Word Frequency Profile** | Lexical difficulty | % high-frequency words |
| CX06 | **Academic Vocabulary %** | Academic register | AWL words / total |
| CX07 | **Technical Density** | Specialization | Domain terms / total |
| CX08 | **Abstraction Level** | Conceptual demand | Concrete vs. abstract concept ratio |
| CX09 | **Concept Density** | Idea packing | Distinct ideas / paragraph |
| CX10 | **Prior Knowledge Load** | Assumed context | Unexplained references count |

### 4.3 Composite Indices

| ID | Instrument | Components | Formula/Method |
|----|------------|------------|----------------|
| IX01 | **Flesch-Kincaid** | Sentence length, syllables | Standard FK formula |
| IX02 | **Gunning Fog** | Sentence length, complex words | Standard GF formula |
| IX03 | **SMOG** | Polysyllabic words | Standard SMOG formula |
| IX04 | **Custom Complexity Score** | Syntactic, Lexical, Conceptual, Structural | 0.3S + 0.3L + 0.2C + 0.2St |
| IX05 | **CEFR Command Estimate** | Multiple command indicators | Map to B1-C2 scale |
| IX06 | **CEFR Complexity Estimate** | Multiple complexity indicators | Map to B1-C2 text level |

---

## Instrument Application Protocols

### Quick Analysis Protocol (5 minutes)

**AI Detection:**
1. Run S01 (Thesis-First) + S02 (Summary Closing) → framing check
2. Run L06 (Contraction Rate) + U05 (First-Person Rate) → voice check
3. Run U01 (Sentence Length Variance) → rhythm check

**Rhetoric:**
1. Run A01 (Thesis Position) → structure classification
2. Run R01 (Sentence Type Distribution) → variety check

**Provenance:**
1. Run I02 (Phrasal Verb Ratio) → native-likeness check
2. Run M01 (Domain Vocabulary) → affiliation identification

### Standard Analysis Protocol (15 minutes)

**AI Detection (all S, L, D instruments):**
- Full structural marker scan
- Full lexical marker scan
- Full discourse marker scan

**Rhetoric (A, R, P instruments):**
- Argument structure mapping
- Sentence pattern distribution
- Paragraph structure classification

**Provenance (I, T, M instruments):**
- Idiomatic competence assessment
- L1 transfer hypothesis
- Domain identification

**Level (CMD, CX instruments):**
- Command level estimation
- Complexity level estimation

### Deep Analysis Protocol (45+ minutes)

Run all instruments with:
- Cross-text comparison if multiple texts available
- Genre normalization
- Error pattern consistency check
- Synthesis and integration of findings

---

## Instrument Interaction Map

```
AI DETECTION ←→ PROVENANCE
    ↑               ↑
    │               │
    ↓               ↓
 RHETORIC ←→ LEVEL ASSESSMENT
```

**Key Interactions:**

| Instrument Set 1 | Instrument Set 2 | Interaction |
|------------------|------------------|-------------|
| AI Detection (U01-U06) | Provenance (AI01-AI07) | Overlapping AI signals |
| Rhetoric (V01-V03) | Level (CMD05-CMD10) | Voice = Command evidence |
| AI Detection (L01-L07) | Provenance (I01-I04) | Lexical patterns = provenance |
| Rhetoric (A01-A03) | Level (CX08-CX10) | Argument = complexity |

---

## Instrument Output Formats

### Single Instrument Output
```yaml
instrument_id: U01
instrument_name: Sentence Length Variance
value: 4.2
interpretation: LOW
signal: AI
confidence: 0.7
evidence: ["sentence lengths: 18, 19, 17, 20, 18, 19"]
```

### Instrument Set Summary
```yaml
set: AI_DETECTION
instruments_run: [S01, S02, L06, U01, U05]
ai_signals: 3
human_signals: 2
assessment: LIKELY_AI_ASSISTED
confidence: 0.65
key_findings:
  - "Low sentence length variance (U01)"
  - "Low first-person rate (U05)"
  - "Natural contraction rate (L06)"
```

### Full Analysis Output
```yaml
text: "filename.txt"
analysis_date: "2026-03-11"
protocol: "standard"

ai_detection:
  assessment: LIKELY_AI_ASSISTED
  confidence: 0.65
  key_signals: ["U01", "U05", "D01"]

rhetoric:
  thesis_position: THESIS_FIRST
  evidence_pattern: PRINCIPLE_FIRST
  dominant_figures: ["antithesis", "paradox"]

provenance:
  l1_hypothesis: GERMAN
  confidence: 0.8
  domain: [SOFTWARE, PHILOSOPHY]
  generation: MIXED

level:
  command: C1
  complexity: C1
  quality_type: HIGH_COMMAND_COMPLEX

synthesis:
  "Likely AI-assisted text by German L1 speaker with
   software/philosophy background. High command, complex
   text. AI assistance visible in structure and uniformity,
   human voice in domain vocabulary and philosophical depth."
```
