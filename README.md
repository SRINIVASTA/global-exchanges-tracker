```mermaid
graph TD
    %% Main Application Frame Mockup
    subgraph APP [💻 ENTERPRISE RISK-GEMMA4-AGENT WORKSPACE INTERFACE]
        
        %% Central Navigation Tabs Mock
        subgraph NAV [🌐 Central Navigation Tab Bar Router]
            T1[📊 Tab 1: Terminal]
            T2[🧠 Tab 2: Gemma Desk]
            T3[🔍 Tab 3: Customer 360]
            T4[⚡ Tab 4: Remediation]
            T5[🔐 Tab 5: IAM View]
        end

        %% Left Column: Voice Control Workspace Component
        subgraph COL1 [🎙️ Hands-Free Voice Controller Sidebar]
            V1[🎤 Mic Status: LISTENING]
            V2["🗣️ Live Stream: 'Run Section 4.2 Audit'"]
            V3[🎛️ Action Macro Triggered]
            V1 --> V2 --> V3
        end

        %% Center Column: Core Analytics View Component
        subgraph COL2 [📊 Core Analytical Pipeline Monitoring View]
            M1[📈 Global Ledger Monitoring Logs]
            M2[🧬 FAISS Vector Store Query Stream]
            M3[📄 ReportLab Automated PDF Builder]
            M1 --> M2 --> M3
        end

        %% Right Column: Security Isolation Threat Console Component
        subgraph COL3 [🚨 Zero-Trust Threat Containment Console]
            A1[⚠️ Section 4.2 PEP Risk Alert]
            A2[🔴 SYSTEM OVERRIDE INITIATED]
            A3[🔒 ACTIVE_LOCK: SYSTEM CONTAINMENT ENGAGED]
            A1 --> A2 --> A3
        end

    end

    %% Class Assigning (Moved from inline to footer block to satisfy GitHub strict compilation)
    class T1,T2,T3,T4,T5,V2,V3,M1,M3,A1 widget;
    class V1 voiceActive;
    class A2,A3 alertActive;
    class M2 dataNode;

    %% Global Workspace Styles (Using deep charcoal slate grey instead of pure black background)
    classDef default fill:#1E293B,stroke:#475569,stroke-width:2px,color:#F8FAFC;
    classDef widget fill:#334155,stroke:#475569,stroke-width:1px,color:#F1F5F9;
    classDef voiceActive fill:#1D4ED8,stroke:#60A5FA,stroke-width:2px,color:#FFFFFF,font-weight:bold;
    classDef alertActive fill:#991B1B,stroke:#F87171,stroke-width:3px,color:#FFFFFF,font-weight:bold;
    classDef dataNode fill:#0F172A,stroke:#64748B,stroke-width:1px,stroke-dasharray: 3 3,color:#CBD5E1;

    %% Apply structural layout formatting to top boxes
    style APP fill:#0F172A,stroke:#334155,stroke-width:2px
    style NAV fill:#1E293B,stroke:#475569
    style COL1 fill:#1E293B,stroke:#3B82F6,stroke-width:1px
    style COL2 fill:#1E293B,stroke:#475569,stroke-width:1px
    style COL3 fill:#2D1515,stroke:#EF4444,stroke-width:1px

    %% Inter-widget interface dependencies data routing pathways
    V3 -->|Automated Trigger Pipeline| M1
    M2 -->|Signal Detection Flag Issued| A1
    A3 -->|Bidirectional Security Lockout| T3
```
