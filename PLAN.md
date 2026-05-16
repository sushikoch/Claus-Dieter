# Pi – Persönlicher Voice-Assistent

## Ziel

Lokaler Voice-Assistent auf macOS (x86), der per Wake-Word oder Push-to-Talk aktiviert wird, Sprache versteht, Kalender/Mail/Apps steuert und antwortet.

## Architektur

```
Mikrofon
 → Wake-Word (openWakeWord) / Push-to-Talk
 → STT: faster-whisper (lokal)
 → LLM: Hermes 3 70B via OpenRouter
 → Tools: Kalender, Mail, Apps (PyObjC + AppleScript)
 → TTS: Kokoro (lokal)
 → Lautsprecher
```

## Tech-Stack

|Komponente   |Tool               |Hosting           |Permissions      |
|-------------|-------------------|------------------|-----------------|
|LLM          |Hermes 3 70B       |OpenRouter (Cloud)| API Key         |
|Wake-Word    |openWakeWord       |Lokal             | Keine           |
|STT          |faster-whisper     |Lokal             | Microphone      |
|TTS          |Kokoro             |Lokal             | Speaker         |
|Agent/Tools  |Python             |Lokal             | Accessibility   |
|Kalender     |PyObjC (EventKit)  |Lokal (macOS API) | Calendar Access |
|Mail         |PyObjC (MailKit)   |Lokal (macOS API) | Mail Access     |
|Andere Apps  |AppleScript        |Lokal             | Accessibility   |
|Spotify      |AppleScript        |Lokal             | Keine (optional)|
|Memory       |JSON / SQLite      |Lokal             | File I/O        |

## macOS Permissions & Setup

### Erforderliche Berechtigungen

Diese Berechtigungen müssen der Python-Anwendung/dem Terminal gewährt werden:

| Permission | Ort | Zweck |
|-----------|-----|-------|
| **Microphone** | System Preferences → Security & Privacy → Microphone | Audio-Eingabe für STT |
| **Accessibility** | System Preferences → Security & Privacy → Accessibility | AppleScript Ausführung, App-Steuerung |
| **Calendar** | System Preferences → Security & Privacy → Calendars | Zugriff auf Kalender via PyObjC |
| **Mail** | System Preferences → Security & Privacy → Mail | Zugriff auf E-Mail via PyObjC |

### Permission-Prüfungs-Checkliste (für Setup-Guide)

```
Vor dem ersten Start:
1. [ ] Terminal/Python zu Accessibility hinzugefügt
2. [ ] Microphone-Permission erteilt
3. [ ] Calendar-Permission erteilt
4. [ ] Mail-Permission erteilt
5. [ ] Test: osascript -e 'tell app "Calendar" to activate'
6. [ ] Test: python -c "from EventKit import EKEventStore; print('OK')"
```

## Meilensteine

|#|Milestone  |Inhalt                                                                                       |Tasks                                |
|-|-----------|---------------------------------------------------------------------------------------------|-------------------------------------|
|1|LLM-Basis  |OpenRouter-API, Hermes Tool-Calling, einfacher Text-Loop                                     |Setup API, Basis-Agent                |
|2|Tools & Permissions  |**Permissions testen**, Kalender lesen/schreiben (PyObjC), Mail lesen, Spotify, Obsidian, Notizen via AppleScript| Permission-Setup, PyObjC Integration |
|3|STT        |faster-whisper einbinden, Mikrofon → Text                                                    |Audio I/O, Whisper Setup             |
|4|TTS        |Kokoro einbinden, Text → Sprache                                                             |Kokoro Setup, Audio Output           |
|5|Wake-Word  |openWakeWord + Push-to-Talk integrieren                                                      |Wake-Word Models, Audio Loop         |
|6|Memory     |Sitzungsübergreifenden Kontext implementieren (JSON/SQLite)                                  |Persistenz-Layer                     |
|7|Integration|Alles zusammenführen, Latenz optimieren                                                      |End-to-End Testing, Performance      |

## Entscheidungen

|Thema       |Entscheidung                                                           |Begründung                                        |
|------------|-----------------------------------------------------------------------|--------------------------------------------------|
|TTS         |**Kokoro** (Qualität bevorzugt)                                        |Bessere Sprachqualität als lokale Alternativen    |
|Wake-Word   |Konfigurierbar; Standard: **„Hermes"**                                 |Thematisch passend, zuverlässig                   |
|Sensitivität|**Konservativ** (muss deutlich gesprochen werden, weniger Fehlauslöser)| Bessere User Experience                          |
|Apps/Dienste|Kalender, Mail, Spotify, Obsidian, Notizen                             |Häufige Office-Tasks                              |
|Memory      |**Ja** – lokale Persistenz (JSON/SQLite), sitzungsübergreifend         |Besserer Kontext über Sessions                    |
|Calendar/Mail|**PyObjC statt AppleScript** für native API-Zugriff                    |Zuverlässiger, bessere Permission-Handling, mehr Features|
|Audio-Libs  |`sounddevice` für Mikrofon/Lautsprecher                                |Einfach, plattformübergreifend, zuverlässig      |

## Risiken & Mitigationen

|Risiko                      |Mitigation                                                       |Priorität |
|----------------------------|-----------------------------------------------------------------|----------|
|Latenz STT+TTS lokal auf x86|Whisper tiny/base Modell als Fallback, Benchmarking              |Hoch      |
|Tool-Calling Qualität       |Hermes System-Prompt Engineering, ggf. Hermes 3 8B testen        |Hoch      |
|macOS App-Steuerung begrenzt|Shortcuts App als Erweiterung, PyObjC für tiefere Integration   |Mittel    |
|**Permission-Denial**       |**Klare Setup-Dokumentation, Fallback-Modi, Permission-Test (M2)**|**Hoch**  |
|PyObjC Kompatibilität       |Early Testing auf Ziel-macOS-Version, Python 3.11+ verwenden     |Mittel    |
|OpenRouter API Ausfälle     |Offline-Fallback-LLM (z.B. Llama.cpp lokal)                      |Niedrig   |

## Implementierungsprioritäten

1. **M1 (LLM-Basis)** – Grundlegende Agent-Logik
2. **M2 (Tools & Permissions)** – Permission-Testing + PyObjC Integration (CRITICAL PATH)
3. **M3 (STT)** – Audio-Input
4. **M4 (TTS)** – Audio-Output
5. **M5 (Wake-Word)** – Kontinuierliches Listening
6. **M6 (Memory)** – Persistenz
7. **M7 (Integration)** – End-to-End

## Dependencies & Requirements

```
Python 3.11+
macOS 12+ (Monterey+)

pip:
- anthropic / openrouter SDK
- faster-whisper
- kokoro (oder TTS library)
- openWakeWord
- sounddevice
- pyobjc (für Calendar/Mail)
- sqlite3 (built-in)

System:
- Microphone + Speaker
- macOS Permissions konfiguriert
```

## Nächste Schritte

1. ✅ Berechtigungen dokumentieren
2. ⬜ M1 (LLM-Setup) beginnen
3. ⬜ M2 (Permission-Test + PyObjC) implementieren
4. ⬜ Latenz-Benchmarks für x86 macOS
5. ⬜ System-Prompt für Hermes optimieren
