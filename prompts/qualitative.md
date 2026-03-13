# Qualitative Analysis Prompts

Prompts für die nicht-automatisierbaren Instrumente.

---

## A01: Thesis Position / These-Position

**Frage:** Wo befindet sich die Hauptthese?

**Klassifikation:**
- `THESIS_FIRST`: Hauptaussage im ersten Absatz
- `THESIS_DELAYED`: Evidenz baut zur Schlussfolgerung auf
- `THESIS_EMBEDDED`: These emergiert aus Erzählung
- `THESIS_ABSENT`: Leser muss inferieren

**Suche nach:**
- Erster Satz: Macht er eine Behauptung?
- Letzter Absatz: Kommt dort erst die Pointe?
- Narrative Struktur: Erzählt der Text eine Geschichte?

---

## A02: Evidence Pattern / Evidenz-Muster

**Frage:** Wie wird Evidenz eingesetzt?

**Klassifikation:**
- `EXAMPLE_FIRST`: Konkreter Fall → Prinzip
- `PRINCIPLE_FIRST`: Regel → Illustration
- `ACCUMULATION`: Mehrere Beispiele bauen Muster auf
- `SINGLE_DECISIVE`: Ein Beispiel trägt das Argument

**Suche nach:**
- Reihenfolge: Kommt das Beispiel vor oder nach der Regel?
- Anzahl: Wie viele Beispiele gibt es?
- Gewicht: Trägt ein Beispiel das Argument allein?

---

## A03: Concession Pattern / Konzessionsmuster

**Frage:** Wie werden Einwände behandelt?

**Klassifikation:**
- `ACKNOWLEDGE_PIVOT`: "Das ist nicht X. Es ist Y."
- `YES_BUT`: "Stimmt, aber..."
- `STRAWMAN`: Schwache Version wird widerlegt
- `STEELMAN`: Stärkste Gegenposition adressiert
- `NONE`: Keine Konzessionen

**Suche nach:**
- "This isn't about X being wrong"
- "True, but..." / "This remains partially true. But..."
- "Some might say..." / "The standard pitch goes..."

---

## C03: Synthesis Quality / Synthese-Qualität

**Frage:** Emergiert die Schlussfolgerung aus dem Argument?

**Klassifikation:**
- `WEAK`: Restatement ("Wir haben 5 Punkte besprochen")
- `MODERATE`: Zusammenfassung mit etwas Mehrwert
- `STRONG`: Synthese emergiert aus dem Argument
- `EXCELLENT`: Neue Einsicht, die nur durch das Argument möglich war

**Suche nach:**
- Schlussabsatz: Könnte er am Anfang stehen?
- Emergenz: Folgt er notwendig aus dem Vorangegangenen?
- Resonanz: Bleibt ein Bild/Gedanke hängen?

---

## V01: Epistemic Modality / Epistemische Modalität

**Frage:** Wie verteilt sich die Sicherheit über Behauptungen?

**Inventar:**
- **Gewissheit:** ist, tut, wird, muss
- **Wahrscheinlichkeit:** wahrscheinlich, vermutlich, tendenziell
- **Möglichkeit:** könnte, mag, vielleicht
- **Notwendigkeit:** muss, sollte, braucht

**AI-Signal:** Gleichmäßige Verteilung (alles gleich sicher)
**Human-Signal:** Strategische Variation (sicher wo sicher, vorsichtig wo unsicher)

---

## V02: Evaluative Language / Bewertende Sprache

**Frage:** Wie wird Urteil ausgedrückt?

**Klassifikation:**
- `EXPLICIT`: "Das ist problematisch" / "Das ist wichtig"
- `IMPLICIT`: Wortwahl trägt Urteil ("Strudel", "berauschend")
- `DISTANCED`: "Manche argumentieren..."

**Suche nach:**
- Adjektive mit Wertung
- Metaphern mit Konnotation
- Distanzierungsmarker

---

## V05: Framing / Rahmung

**Frage:** Welcher konzeptuelle Rahmen wird verwendet?

**Typen:**
- `SHIFT`: Wandel als natürlich/unvermeidlich
- `TOOL`: AI als Werkzeug
- `PARTNER`: AI als Kollaborateur
- `THREAT`: AI als Gefahr (auch ironisch)

**Suche nach:**
- Metaphern für AI
- Verb-Subjekt-Beziehungen (Wer handelt?)
- Implizite Bewertung der Entwicklung

---

## I01-I04: Idiomatic Competence / Idiomatische Kompetenz

**Frage:** Wie idiomatisch ist der Text?

**Prüfpunkte:**
1. **Kollokationen:** 5 Stichproben - korrekt?
2. **Phrasale Verben:** Vorhanden oder vermieden?
3. **Redewendungen:** Natürlich eingesetzt?
4. **Präpositionen:** Systematische Fehler?

**Native Signal:** Phrasale Verben bevorzugt, Idiome natürlich
**Non-Native Signal:** Latinate Alternativen, Idiom-Vermeidung

---

## M01-M04: Domain & Provenance / Domäne & Herkunft

**Frage:** Welche Domäne? Welche L1?

**Domänen-Vokabular:**
- Software: codebase, sprint, refactoring, hooks
- Agile/Management: velocity, backlog, story points
- Philosophie: hermeneutisch, Mündigkeit, Vorurteil
- Startup: crushes it, game-changer

**L1-Marker:**
- Deutsch: Unübersetzte Begriffe (Denkarbeit), Verb-End-Tendenzen
- Romanisch: Adjektiv-Position
- Ostasiatisch: Artikel-/Plural-Muster

---

## Output-Template

```yaml
qualitative:
  thesis_position:
    classification: "[THESIS_FIRST|THESIS_DELAYED|THESIS_EMBEDDED|THESIS_ABSENT]"
    evidence: "[Zitat aus Text]"

  evidence_pattern:
    classification: "[EXAMPLE_FIRST|PRINCIPLE_FIRST|ACCUMULATION|SINGLE_DECISIVE]"
    evidence: "[Zitat aus Text]"

  concession_pattern:
    classification: "[ACKNOWLEDGE_PIVOT|YES_BUT|STRAWMAN|STEELMAN|NONE]"
    evidence: "[Zitat aus Text]"

  synthesis_quality:
    classification: "[WEAK|MODERATE|STRONG|EXCELLENT]"
    evidence: "[Zitat aus Text]"

  epistemic_modality:
    distribution: "[UNIFORM|VARIED]"
    signal: "[AI|HUMAN|NEUTRAL]"
    evidence: "[Beispiele aus Text]"

  evaluative_language:
    type: "[EXPLICIT|IMPLICIT|DISTANCED]"
    examples: ["...", "..."]

  framing:
    type: "[SHIFT|TOOL|PARTNER|THREAT]"
    evidence: "[Zitat aus Text]"

  idiomatic_competence:
    collocations: "[ACCURATE|MINOR_ERRORS|ERRORS]"
    phrasal_verbs: "[PREFERRED|BALANCED|AVOIDED]"
    idioms: "[NATURAL|AWKWARD|ABSENT]"

  provenance:
    l1_hypothesis: "[GERMAN|ENGLISH|ROMANCE|EAST_ASIAN|OTHER]"
    l1_evidence: ["...", "..."]
    domain: ["...", "..."]
    generation: "[PRE_DIGITAL|DIGITAL_NATIVE|AI_ERA]"
```
