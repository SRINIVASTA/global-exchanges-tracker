```mermaid
graph TD
    %% Main Columns mapped exactly to your repository tabs
    subgraph TAB1 [01. Voice-Driven Monitoring Terminal]
        F1_DESC[Replaces manual click buttons with<br>speech-to-text operation macros]
        subgraph UPGRADE1 [VOICE INTERFACE UPGRADE]
            V_Mic[🎤 Spoken: 'Run global audit'] -->|Speech Recognition| V_Macro[Trigger: tab1_dashboard.py Pipeline]
        end
    end

    subgraph TAB2 [02. Grounded RAG & Math Engine]
        F2_DESC[Runs 48hr cross-border math sweeps<br>and pulls FAISS regulatory context]
        subgraph ENGINE2 [gemma4_engine.py INTERNALS]
            S3[FAISS Vector Store] -->|RBI Master Directions| S4[ReportLab PDF Binary]
        end
    end

    subgraph TAB4 [03. ACTIVE_LOCK Containment]
        F3_DESC[Zero-trust workspace with instant<br>account containment isolation flags]
        subgraph LOCK3 [REMEDIATION ACTIONS DESK]
            S5[Section 4.2 PEP Breach] -->|ACTIVE_LOCK Trigger| S6[🔒 Ledger Blocked / Account Frozen]
        end
    end

    %% Class Assigning (GitHub safe syntax layout style)
    class F1_DESC,F2_DESC feature;
    class F3_DESC usp;
    class V_Mic,V_Macro,S3,S4,S5,S6 sketch;

    %% Global Slide Styles
    classDef default fill:#111827,stroke:#374151,stroke-width:2px,color:#F3F4F6;
    classDef feature fill:#1F2937,stroke:#4B5563,stroke-width:2px,color:#E5E7EB;
    classDef usp fill:#7F1D1D,stroke:#EF4444,stroke-width:3px,color:#FFFFFF,font-weight:bold;
    classDef sketch fill:#030712,stroke:#6B7280,stroke-width:1px,stroke-dasharray: 5 5,color:#9CA3AF,font-style:italic;

    %% Layout adjustments
    style TAB1 fill:#111827,stroke:#3B82F6,stroke-width:2px
    style TAB2 fill:#111827,stroke:#374151
    style TAB4 fill:#180808,stroke:#EF4444,stroke-width:2px
    style UPGRADE1 fill:#030712,stroke:#3B82F6,stroke-dasharray: 5 5
    style ENGINE2 fill:#030712,stroke:#6B7280,stroke-dasharray: 5 5
    style LOCK3 fill:#030712,stroke:#EF4444,stroke-dasharray: 5 5

    %% ⚡ Running Flow Animation Definitions
    linkStyle 0 stroke:#3B82F6,stroke-width:3px,stroke-dasharray: 5,animation: actionFlow 1.5s linear infinite;
    linkStyle 1 stroke:#10B981,stroke-width:3px,stroke-dasharray: 5,animation: actionFlow 2s linear infinite;
    linkStyle 2 stroke:#EF4444,stroke-width:4px,stroke-dasharray: 5,animation: actionFlow 0.4s linear infinite;

{
  "theme": "dark",
  "themeCSS": "@keyframes actionFlow { from { stroke-dashoffset: 20; } to { stroke-dashoffset: 0; } }"
}
```
