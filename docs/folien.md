# Struktur
- Containerisierung mit Docker
    - einfaches Deployment
- Aufteilung in skalierbare Nodes
- Frontend in Node.js-Container

# Struktur
![Docker Structure](structure_release.png)

# Docker & Skalierung
- Container kommunizieren nur über Schnittstellen
- Celery für Messaging
- Redis als Message-Broker
- Replizierte Worker-/API-Nodes zur Skalierung

# Workflow
- GitHub mit feature-Branching
- GitHub Actions für CI-Pipeline
    - Trigger: PR
    - automatisierte Docker Builds
    - pytest
- vor Merge: Pipeline-Checks + Review
- ermöglicht sowohl Aufgabenteilung als auch paralleles Arbeiten

# Perspektive & Weiterentwicklung
- Verbesserte Usability
- Ausbau pytest & Continuous Delivery
- Verbesserte Speicherung
    - .csv-Uploads in Datenbank anstatt Filesystem
- Einführung & Guides