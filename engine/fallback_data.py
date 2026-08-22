"""Offline domain knowledge base and fallback roadmap generator.

Provides rich pre-structured 3-phase DAG curriculums across major tech,
creative, lifestyle, and academic domains, with a dynamic universal generator
for any custom goal.
"""

import re
from typing import Dict, List, Any

DOMAIN_TEMPLATES: List[Dict[str, Any]] = [
    {
        "role": "AI & ML Engineer",
        "keywords": ("ai", "machine learning", "ml", "deep learning", "nlp", "computer vision", "llm", "neural"),
        "phases": [
            {
                "phase": "Phase 1: Mathematical Foundations & Python DSA",
                "nodes": [
                    {
                        "id": "AI101",
                        "title": "Mathematics for Machine Learning",
                        "type": "Course",
                        "provider": "Imperial College London / Coursera",
                        "duration": "3 weeks",
                        "prereqs": [],
                        "why": "Establishes linear algebra, multivariate calculus, and matrix decomposition essential for neural networks.",
                        "skills": ["Linear Algebra", "Multivariate Calculus", "Matrix Decompositions"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "AI102",
                        "title": "Python for Data Science & Vectorized Compute",
                        "type": "Course",
                        "provider": "MIT OCW / freeCodeCamp",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Master NumPy, Pandas vectorization, and computational complexity for large datasets.",
                        "skills": ["Python", "NumPy", "Pandas", "Algorithms"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Core ML & Deep Learning Architectures",
                "nodes": [
                    {
                        "id": "AI201",
                        "title": "Supervised & Unsupervised Machine Learning",
                        "type": "Course",
                        "provider": "DeepLearning.AI / Stanford",
                        "duration": "4 weeks",
                        "prereqs": ["AI101", "AI102"],
                        "why": "Covers gradient descent, regularization, tree ensembles, and clustering algorithms.",
                        "skills": ["Scikit-Learn", "Regression", "Tree Ensembles", "Cross-Validation"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "AI202",
                        "title": "Neural Networks & PyTorch Deep Learning",
                        "type": "Project",
                        "provider": "Fast.ai / PyTorch Lab",
                        "duration": "4 weeks",
                        "prereqs": ["AI201"],
                        "why": "Hands-on implementation of CNNs, Transformers, and custom loss functions in PyTorch.",
                        "skills": ["PyTorch", "Transformers", "Backpropagation", "GPU Optimization"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Production MLOps & LLM Systems",
                "nodes": [
                    {
                        "id": "AI301",
                        "title": "MLOps, Model Serving & Docker Pipelines",
                        "type": "Course",
                        "provider": "Full Stack Deep Learning",
                        "duration": "3 weeks",
                        "prereqs": ["AI202"],
                        "why": "Teaches low-latency FastAPI model serving, Docker containerization, and monitoring.",
                        "skills": ["MLOps", "Docker", "FastAPI", "Model Monitoring"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "AI302",
                        "title": "Enterprise Generative AI & Agentic RAG Capstone",
                        "type": "Project",
                        "provider": "Portfolio Lab / Open Source",
                        "duration": "4 weeks",
                        "prereqs": ["AI301"],
                        "why": "Production capstone demonstrating retrieval-augmented generation, vector search, and agentic workflows.",
                        "skills": ["RAG", "Vector DBs", "LangChain", "Autonomous Agents"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Full-Stack Web Developer",
        "keywords": ("web", "full stack", "fullstack", "frontend", "backend", "react", "next.js", "node", "javascript", "typescript"),
        "phases": [
            {
                "phase": "Phase 1: Modern Web Foundations & TypeScript",
                "nodes": [
                    {
                        "id": "FS101",
                        "title": "Modern JavaScript (ESNext) & TypeScript Mastery",
                        "type": "Course",
                        "provider": "freeCodeCamp / Total TypeScript",
                        "duration": "3 weeks",
                        "prereqs": [],
                        "why": "Strong typing and async programming prevent runtime bugs and scale large codebases.",
                        "skills": ["JavaScript", "TypeScript", "Async/Await", "DOM Manipulation"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "FS102",
                        "title": "Responsive UI Craft with Tailwind CSS",
                        "type": "Course",
                        "provider": "Tailwind Labs / Scrimba",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Teaches accessible mobile-first responsive layout design and design tokens.",
                        "skills": ["HTML5", "CSS3", "Tailwind CSS", "A11y Accessibility"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: React Ecosystem & Backend API Engineering",
                "nodes": [
                    {
                        "id": "FS201",
                        "title": "React 19 & Next.js App Router Architecture",
                        "type": "Course",
                        "provider": "Next.js Official / Epic React",
                        "duration": "4 weeks",
                        "prereqs": ["FS101", "FS102"],
                        "why": "Server Components, hooks, state management, and SSR routing for high-performance apps.",
                        "skills": ["React", "Next.js", "Server Components", "State Management"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "FS202",
                        "title": "REST & GraphQL Backend Microservices with Node/PostgreSQL",
                        "type": "Project",
                        "provider": "Prisma / PostgreSQL Academy",
                        "duration": "3 weeks",
                        "prereqs": ["FS101"],
                        "why": "Relational data modeling, connection pooling, and secure JWT/OAuth authentication.",
                        "skills": ["Node.js", "PostgreSQL", "Prisma ORM", "Auth"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Real-Time Systems, CI/CD & Cloud Deployment",
                "nodes": [
                    {
                        "id": "FS301",
                        "title": "WebSockets, Caching & Cloud Infrastructure",
                        "type": "Course",
                        "provider": "AWS Academy / Redis University",
                        "duration": "3 weeks",
                        "prereqs": ["FS201", "FS202"],
                        "why": "Sub-100ms real-time event streaming and Redis caching for distributed scale.",
                        "skills": ["WebSockets", "Redis", "AWS S3/ECS", "CI/CD Actions"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "FS302",
                        "title": "Full-Stack SaaS Platform Capstone with Stripe",
                        "type": "Project",
                        "provider": "Portfolio Lab",
                        "duration": "4 weeks",
                        "prereqs": ["FS301"],
                        "why": "Complete production SaaS with multi-tenancy, Stripe payments, and automated telemetry.",
                        "skills": ["SaaS Architecture", "Stripe API", "Telemetry", "Deployment"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Data Scientist",
        "keywords": ("data science", "analytics", "statistics", "pandas", "bi", "tableau", "visualization", "predictive"),
        "phases": [
            {
                "phase": "Phase 1: Statistical Inference & Advanced SQL",
                "nodes": [
                    {
                        "id": "DS101",
                        "title": "Applied Statistical Inference & Hypothesis Testing",
                        "type": "Course",
                        "provider": "MIT OCW / Khan Academy",
                        "duration": "3 weeks",
                        "prereqs": [],
                        "why": "Confidence intervals, p-values, and Bayesian thinking form the basis of valid data analysis.",
                        "skills": ["Probability", "Hypothesis Testing", "A/B Testing"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "DS102",
                        "title": "Advanced SQL & Query Optimization for Analytics",
                        "type": "Course",
                        "provider": "Mode Analytics / DataCamp",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Window functions, CTEs, and partition optimization for multi-million row databases.",
                        "skills": ["Advanced SQL", "Window Functions", "CTEs", "Data Warehousing"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Exploratory Data Analysis & Predictive Modeling",
                "nodes": [
                    {
                        "id": "DS201",
                        "title": "Exploratory Data Analysis & Interactive Visual Storytelling",
                        "type": "Course",
                        "provider": "HarvardX / Plotly Academy",
                        "duration": "3 weeks",
                        "prereqs": ["DS101", "DS102"],
                        "why": "Turn complex distributions into actionable executive dashboards.",
                        "skills": ["Plotly", "Seaborn", "Feature Engineering", "Data Cleaning"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "DS202",
                        "title": "Predictive Machine Learning & Time Series Forecasting",
                        "type": "Project",
                        "provider": "Kaggle Competitions Lab",
                        "duration": "4 weeks",
                        "prereqs": ["DS201"],
                        "why": "End-to-end model pipeline: cross-validation, hyperparameter tuning, and ARIMA forecasting.",
                        "skills": ["XGBoost", "Time Series", "Model Evaluation", "SHAP Explainability"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Big Data Engines & Production Insights",
                "nodes": [
                    {
                        "id": "DS301",
                        "title": "Distributed Big Data Processing with PySpark",
                        "type": "Course",
                        "provider": "Databricks Academy",
                        "duration": "3 weeks",
                        "prereqs": ["DS202"],
                        "why": "Scaling data transformations across clusters with Apache Spark DataFrames.",
                        "skills": ["PySpark", "Distributed Compute", "Data Lakehouse"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "DS302",
                        "title": "End-to-End Enterprise Analytics Capstone",
                        "type": "Project",
                        "provider": "Portfolio Lab",
                        "duration": "4 weeks",
                        "prereqs": ["DS301"],
                        "why": "Published analytics case study demonstrating real-world business impact and ROI.",
                        "skills": ["Business Intelligence", "Executive Presentation", "Portfolio"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Cybersecurity Analyst",
        "keywords": ("security", "cyber", "cybersecurity", "soc", "ethical hack", "penetration", "network security"),
        "phases": [
            {
                "phase": "Phase 1: Computer Networking & Linux Administration",
                "nodes": [
                    {
                        "id": "CY101",
                        "title": "Network Protocols & Traffic Analysis with Wireshark",
                        "type": "Course",
                        "provider": "CompTIA Network+ / Professor Messer",
                        "duration": "3 weeks",
                        "prereqs": [],
                        "why": "Understanding TCP/IP, DNS, SSL/TLS, and packet inspection is critical for threat detection.",
                        "skills": ["TCP/IP", "Wireshark", "Packet Analysis", "DNS Security"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "CY102",
                        "title": "Linux Security & System Hardening",
                        "type": "Course",
                        "provider": "OverTheWire / Linux Foundation",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Command-line privilege management, permissions, and service auditing.",
                        "skills": ["Linux CLI", "Permissions", "Bash Scripting", "System Hardening"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Vulnerability Assessment & Defensive Operations",
                "nodes": [
                    {
                        "id": "CY201",
                        "title": "SOC Operations, SIEM & Incident Response",
                        "type": "Course",
                        "provider": "TryHackMe / Splunk Fundamentals",
                        "duration": "4 weeks",
                        "prereqs": ["CY101", "CY102"],
                        "why": "Log correlation, MITRE ATT&CK framework mapping, and incident triage.",
                        "skills": ["Splunk", "SIEM", "Incident Response", "MITRE ATT&CK"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "CY202",
                        "title": "Ethical Hacking & Web App Penetration Testing",
                        "type": "Project",
                        "provider": "PortSwigger Web Security Academy",
                        "duration": "3 weeks",
                        "prereqs": ["CY201"],
                        "why": "Exploiting OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF, SSRF) in controlled sandboxes.",
                        "skills": ["OWASP Top 10", "Burp Suite", "Penetration Testing"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Threat Hunting & Cloud Security",
                "nodes": [
                    {
                        "id": "CY301",
                        "title": "Cloud Security Architecture & IAM Governance",
                        "type": "Course",
                        "provider": "AWS Certified Security / SANS",
                        "duration": "3 weeks",
                        "prereqs": ["CY201"],
                        "why": "Securing cloud workloads, Zero Trust architecture, and cryptographic key vaults.",
                        "skills": ["Cloud Security", "IAM", "Zero Trust", "KMS Encryption"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "CY302",
                        "title": "Enterprise Threat Defense & Purple Team Capstone",
                        "type": "Project",
                        "provider": "HackTheBox Pro Labs",
                        "duration": "4 weeks",
                        "prereqs": ["CY301", "CY202"],
                        "why": "Full-scope enterprise network penetration report and defensive hardening playbook.",
                        "skills": ["Threat Hunting", "Forensics", "Security Architecture"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Cloud & DevOps Engineer",
        "keywords": ("cloud", "devops", "aws", "azure", "docker", "kubernetes", "k8s", "terraform", "ci/cd", "infrastructure"),
        "phases": [
            {
                "phase": "Phase 1: Linux, Containers & GitOps",
                "nodes": [
                    {
                        "id": "DO101",
                        "title": "Docker Containerization & Multi-Stage Builds",
                        "type": "Course",
                        "provider": "Docker Official / Bret Fisher",
                        "duration": "3 weeks",
                        "prereqs": [],
                        "why": "Creating lightweight, secure container images and compose environments.",
                        "skills": ["Docker", "Containers", "Docker Compose", "Image Optimization"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "DO102",
                        "title": "Linux Systems & Shell Automation",
                        "type": "Course",
                        "provider": "Linux Academy / KodeKloud",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Automating server management and system diagnostics with Bash.",
                        "skills": ["Linux", "Bash", "Systemd", "SSH Networking"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Cloud Services & Infrastructure as Code",
                "nodes": [
                    {
                        "id": "DO201",
                        "title": "AWS / Cloud Solutions Architecture",
                        "type": "Course",
                        "provider": "AWS Certified Solutions Architect (Stephane Maarek)",
                        "duration": "4 weeks",
                        "prereqs": ["DO101", "DO102"],
                        "why": "VPC networking, compute scaling (EC2/ECS/Lambda), and resilient database clusters.",
                        "skills": ["AWS VPC", "EC2", "S3", "IAM", "Load Balancing"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "DO202",
                        "title": "Infrastructure as Code with Terraform & GitHub Actions",
                        "type": "Project",
                        "provider": "HashiCorp Learn / GitHub Docs",
                        "duration": "3 weeks",
                        "prereqs": ["DO201"],
                        "why": "Declarative multi-cloud provisioning with automated CI/CD validation pipelines.",
                        "skills": ["Terraform", "HCL", "GitHub Actions", "GitOps"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Kubernetes Orchestration & Observability",
                "nodes": [
                    {
                        "id": "DO301",
                        "title": "Kubernetes Cluster Administration (CKA Curriculum)",
                        "type": "Course",
                        "provider": "Mumshad Mannambeth / CNCF",
                        "duration": "4 weeks",
                        "prereqs": ["DO201", "DO202"],
                        "why": "Deployments, StatefulSets, Ingress controllers, Helm charts, and auto-scaling.",
                        "skills": ["Kubernetes", "Helm", "Ingress", "Cluster Networking"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "DO302",
                        "title": "Enterprise GitOps & Prometheus Observability Capstone",
                        "type": "Project",
                        "provider": "ArgoCD & Prometheus Lab",
                        "duration": "3 weeks",
                        "prereqs": ["DO301"],
                        "why": "Production cluster with ArgoCD continuous deployment, Prometheus metrics, and Grafana dashboards.",
                        "skills": ["ArgoCD", "Prometheus", "Grafana", "Site Reliability"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Musician",
        "keywords": ("guitar", "piano", "music", "sing", "song", "drum", "violin", "flute", "ukulele", "chords"),
        "phases": [
            {
                "phase": "Phase 1: Instrument Setup, Posture & Rhythm",
                "nodes": [
                    {
                        "id": "MU101",
                        "title": "Instrument Fundamentals, Ergonomics & Care",
                        "type": "Course",
                        "provider": "ArtistWorks / JustinGuitar",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Proper hand posture and tuning habits prevent injury and accelerate muscle memory.",
                        "skills": ["Tuning", "Posture", "Instrument Anatomy"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "MU102",
                        "title": "Rhythm, Timing & Beat Subdivision",
                        "type": "Practice",
                        "provider": "Musictheory.net / Metronome Lab",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Internalizing time signatures and metronome practice separates amateurs from musicians.",
                        "skills": ["Metronome", "Timing", "Time Signatures", "Ear Training"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Chords, Scales & Repertoire Building",
                "nodes": [
                    {
                        "id": "MU201",
                        "title": "Core Chords, Transitions & Scale Shapes",
                        "type": "Course",
                        "provider": "JustinGuitar / Simply Piano",
                        "duration": "4 weeks",
                        "prereqs": ["MU101", "MU102"],
                        "why": "Mastering the major/minor chord vocabulary and pentatonic scale opens thousands of songs.",
                        "skills": ["Major/Minor Chords", "Smooth Transitions", "Pentatonic Scale"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "MU202",
                        "title": "Master 5 Complete Songs Across Genres",
                        "type": "Project",
                        "provider": "Songsterr / Ultimate Guitar",
                        "duration": "3 weeks",
                        "prereqs": ["MU201"],
                        "why": "Playing full songs end-to-end tests stamina and musical expression.",
                        "skills": ["Repertoire", "Strumming Patterns", "Dynamics"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Improvisation & Live Performance Capstone",
                "nodes": [
                    {
                        "id": "MU301",
                        "title": "Improvisation, Ear Transcription & Music Theory",
                        "type": "Course",
                        "provider": "Berklee Online / Rick Beato",
                        "duration": "3 weeks",
                        "prereqs": ["MU201"],
                        "why": "Learn to play what you hear by ear without relying solely on chord charts.",
                        "skills": ["Ear Training", "Improvisation", "Harmonic Analysis"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "MU302",
                        "title": "Live Recording & Community Performance Capstone",
                        "type": "Project",
                        "provider": "Open Mic / YouTube Studio",
                        "duration": "2 weeks",
                        "prereqs": ["MU301", "MU202"],
                        "why": "Recording and performing cements confidence and completes the transition to active performer.",
                        "skills": ["Audio Recording", "Stage Presence", "Performance"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Language Learner",
        "keywords": ("language", "spanish", "french", "german", "japanese", "korean", "chinese", "mandarin", "italian", "fluent", "ielts", "toefl"),
        "phases": [
            {
                "phase": "Phase 1: Phonetics & Top 1,000 High-Frequency Words",
                "nodes": [
                    {
                        "id": "LG101",
                        "title": "Phonetic Sound System & Pronunciation Bootcamp",
                        "type": "Course",
                        "provider": "Anki Spaced Repetition / Fluent Forever",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Ear training on native vowel and consonant contrasts prevents fossilized accent errors.",
                        "skills": ["Phonetics", "Accent Training", "Spaced Repetition"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "LG102",
                        "title": "Top 1,000 Core Vocabulary & Sentence Builders",
                        "type": "Practice",
                        "provider": "Duolingo / Clozemaster",
                        "duration": "3 weeks",
                        "prereqs": [],
                        "why": "The top 1,000 words account for ~80% of daily conversational speech.",
                        "skills": ["Core Vocabulary", "High Frequency Phrases"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Grammar Frameworks & Active Conversational Drills",
                "nodes": [
                    {
                        "id": "LG201",
                        "title": "Grammar Structure in Context & Tense Mastery",
                        "type": "Course",
                        "provider": "Language Transfer / Assimil",
                        "duration": "4 weeks",
                        "prereqs": ["LG101", "LG102"],
                        "why": "Pattern-based grammar allows spontaneous sentence creation without mental translation.",
                        "skills": ["Sentence Grammar", "Verb Conjugation", "Tenses"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "LG202",
                        "title": "Live 1-on-1 Native Speaking Exchanges",
                        "type": "Project",
                        "provider": "iTalki / Tandem Community",
                        "duration": "4 weeks",
                        "prereqs": ["LG201"],
                        "why": "Speaking from month one builds real conversational speed and overcomes fear of mistakes.",
                        "skills": ["Conversational Fluency", "Listening Speed", "Spontaneity"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Immersion & Fluency Benchmark",
                "nodes": [
                    {
                        "id": "LG301",
                        "title": "Comprehensible Native Immersion (Podcasts & Media)",
                        "type": "Practice",
                        "provider": "Language Reactor / Native Media",
                        "duration": "4 weeks",
                        "prereqs": ["LG201", "LG202"],
                        "why": "Unlocks natural phrasing, colloquial idioms, and rapid native speech comprehension.",
                        "skills": ["Advanced Listening", "Idioms", "Cultural Context"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "LG302",
                        "title": "30-Minute Unrehearsed Native Conversation Capstone",
                        "type": "Project",
                        "provider": "Official CEFR / iTalki Assessment",
                        "duration": "2 weeks",
                        "prereqs": ["LG301"],
                        "why": "Objective milestone demonstrating B2+ conversational fluency.",
                        "skills": ["Fluency Benchmark", "Presentation", "Debate"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Fitness Enthusiast",
        "keywords": ("fit", "fitness", "gym", "workout", "muscle", "weight loss", "weight gain", "strength", "running", "marathon", "diet", "nutrition", "calisthenics"),
        "phases": [
            {
                "phase": "Phase 1: Mobility Screen & Habit Anchoring",
                "nodes": [
                    {
                        "id": "FT101",
                        "title": "Movement Assessment & Core Stability",
                        "type": "Course",
                        "provider": "Nike Training Club / Squat University",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Screening joint mobility and core bracing ensures safe progressive overload.",
                        "skills": ["Mobility", "Movement Mechanics", "Injury Prevention"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "FT102",
                        "title": "Nutrition Fundamentals & Macronutrient Tracking",
                        "type": "Course",
                        "provider": "Precision Nutrition / MacroFactor",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "Fueling, protein targets, and hydration are 70% of body recomposition.",
                        "skills": ["Macronutrients", "Hydration", "Meal Planning"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Compound Lifts & Hypertrophy Periodization",
                "nodes": [
                    {
                        "id": "FT201",
                        "title": "Compound Strength Fundamentals (Squat, Bench, Deadlift)",
                        "type": "Course",
                        "provider": "Stronger by Science / Barbell Medicine",
                        "duration": "4 weeks",
                        "prereqs": ["FT101", "FT102"],
                        "why": "Progressive overload across multi-joint lifts builds functional power and density.",
                        "skills": ["Compound Lifts", "Progressive Overload", "Form Cueing"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "FT202",
                        "title": "Cardiovascular Engine: Zone 2 & VO2 Max Intervals",
                        "type": "Practice",
                        "provider": "Couch to 5K / Garmin Coach",
                        "duration": "4 weeks",
                        "prereqs": ["FT101"],
                        "why": "Aerobic base expands mitochondrial density and accelerates recovery between sets.",
                        "skills": ["Zone 2 Cardio", "Endurance", "Recovery Optimization"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Peak Performance & Milestone Event",
                "nodes": [
                    {
                        "id": "FT301",
                        "title": "Advanced Periodization, Deloads & Sleep Science",
                        "type": "Course",
                        "provider": "Renaissance Periodization",
                        "duration": "3 weeks",
                        "prereqs": ["FT201"],
                        "why": "Managing fatigue and sleep architecture allows continuous progress without plateauing.",
                        "skills": ["Periodization", "Fatigue Management", "Sleep Optimization"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "FT302",
                        "title": "Milestone Fitness Event (10K Run or Power PR Block)",
                        "type": "Project",
                        "provider": "Local Race / Gym Performance Test",
                        "duration": "2 weeks",
                        "prereqs": ["FT301", "FT202"],
                        "why": "Testing limits in a formal event solidifies months of disciplined habit formation.",
                        "skills": ["Peak Performance", "Testing", "Athleticism"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    },
    {
        "role": "Exam Topper",
        "keywords": ("exam", "jee", "neet", "gate", "upsc", "cat", "sat", "gmat", "gre", "entrance", "study"),
        "phases": [
            {
                "phase": "Phase 1: Syllabus Decomposition & Diagnostic Baseline",
                "nodes": [
                    {
                        "id": "EX101",
                        "title": "Syllabus Weightage Analysis & Study Schedule Design",
                        "type": "Practice",
                        "provider": "Official Syllabus + Past 10-Year Papers",
                        "duration": "1 week",
                        "prereqs": [],
                        "why": "Focusing high-yield topics first yields the highest score improvement per study hour.",
                        "skills": ["Strategic Planning", "Weightage Analysis", "Time Blocking"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "EX102",
                        "title": "Diagnostic Full-Length Mock & Gap Assessment",
                        "type": "Assessment",
                        "provider": "Official Previous Year Papers",
                        "duration": "1 week",
                        "prereqs": [],
                        "why": "A baseline diagnostic highlights weak conceptual areas before study begins.",
                        "skills": ["Diagnostic Testing", "Gap Identification", "Error Logging"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Deep Conceptual Mastery & Spaced Active Recall",
                "nodes": [
                    {
                        "id": "EX201",
                        "title": "Concept Mastery via First-Principles Problem Solving",
                        "type": "Course",
                        "provider": "NPTEL / Khan Academy / Standard Reference Texts",
                        "duration": "6 weeks",
                        "prereqs": ["EX101", "EX102"],
                        "why": "Rigorous first-principles understanding solves non-standard tricky exam questions.",
                        "skills": ["First Principles", "Advanced Problem Solving", "Note Summarization"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "EX202",
                        "title": "Spaced Revision & Active Recall System (Anki)",
                        "type": "Practice",
                        "provider": "Anki / Personal Flashcards",
                        "duration": "Ongoing",
                        "prereqs": ["EX201"],
                        "why": "Combats the Ebbinghaus forgetting curve and keeps formulas at instant recall.",
                        "skills": ["Active Recall", "Spaced Repetition", "Formula Retention"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Full-Length Timed Test Series & Error Sprints",
                "nodes": [
                    {
                        "id": "EX301",
                        "title": "Timed Exam Simulation & Speed Optimization",
                        "type": "Practice",
                        "provider": "All-India Test Series / Allen / IMS",
                        "duration": "4 weeks",
                        "prereqs": ["EX201", "EX202"],
                        "why": "Simulating strict exam timing builds pressure resistance, speed, and question triage skills.",
                        "skills": ["Time Management", "Question Triage", "Exam Temperament"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "EX302",
                        "title": "Master Error Notebook & Final Score Sprint",
                        "type": "Project",
                        "provider": "Personal Mistake Journal",
                        "duration": "2 weeks",
                        "prereqs": ["EX301"],
                        "why": "Systematically eliminating recurring mistake patterns turns good scores into top ranks.",
                        "skills": ["Error Elimination", "Speed & Accuracy", "Peak Mindset"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]
    }
]

def generate_fallback_roadmap(goal: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """Offline domain matching engine.
    
    Matches goal against domain templates or creates a universal adaptive 3-phase DAG.
    Scales durations to the learner's weekly commitment.
    """
    goal_l = f" {goal.lower()} "

    match = next(
        (t for t in DOMAIN_TEMPLATES if any(k in goal_l for k in t["keywords"])),
        None
    )

    if match:
        role = match["role"]
        phases = match["phases"]
    else:
        # Universal adaptive scaffold for any customized subject
        subject = goal.strip().rstrip('.!?,;:') or "Your Custom Learning Goal"
        role = subject if len(subject) <= 40 else subject[:37] + "..."
        phases = [
            {
                "phase": "Phase 1: Orientation & Core Fundamentals",
                "nodes": [
                    {
                        "id": "UN101",
                        "title": f"{subject}: Beginner Fundamentals & Concept Map",
                        "type": "Course",
                        "provider": "Coursera / MIT OCW / YouTube Masterclasses",
                        "duration": "2 weeks",
                        "prereqs": [],
                        "why": "A structured introduction establishes correct principles and mental models from day one.",
                        "skills": ["Core Fundamentals", "Domain Terminology", "Concept Mapping"],
                        "difficulty": "Beginner"
                    },
                    {
                        "id": "UN102",
                        "title": "Tooling Setup & Weekly Practice System",
                        "type": "Practice",
                        "provider": "Self-Directed Frameworks",
                        "duration": "1 week",
                        "prereqs": [],
                        "why": "An organized environment and locked study schedule make progress automatic and consistent.",
                        "skills": ["Habit Design", "Workflow Setup", "Deliberate Practice"],
                        "difficulty": "Beginner"
                    }
                ]
            },
            {
                "phase": "Phase 2: Deliberate Practice & Intermediate Application",
                "nodes": [
                    {
                        "id": "UN201",
                        "title": f"Applied {subject} Practice Drills & Deep Work",
                        "type": "Course",
                        "provider": "Top-Rated Masterclass / Interactive Lab",
                        "duration": "4 weeks",
                        "prereqs": ["UN101"],
                        "why": "Targeted deliberate practice with immediate feedback loops accelerates real competence.",
                        "skills": ["Applied Techniques", "Problem Solving", "Speed & Accuracy"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "id": "UN202",
                        "title": "Community Project & Peer Feedback Loop",
                        "type": "Project",
                        "provider": "Open Community / Peer Review Forum",
                        "duration": "3 weeks",
                        "prereqs": ["UN101", "UN102"],
                        "why": "External peer feedback identifies blind spots that self-study alone cannot reveal.",
                        "skills": ["Collaboration", "Peer Review", "Iterative Refinement"],
                        "difficulty": "Intermediate"
                    }
                ]
            },
            {
                "phase": "Phase 3: Advanced Mastery & Milestone Capstone",
                "nodes": [
                    {
                        "id": "UN301",
                        "title": f"Advanced Techniques & Edge Cases in {subject}",
                        "type": "Course",
                        "provider": "Specialized Advanced Workshops",
                        "duration": "3 weeks",
                        "prereqs": ["UN201"],
                        "why": "Mastering non-standard challenges turns intermediate skills into authoritative competence.",
                        "skills": ["Advanced Theory", "Optimization", "Creative Synthesis"],
                        "difficulty": "Advanced"
                    },
                    {
                        "id": "UN302",
                        "title": f"Public Milestone Showcase: {subject} Capstone",
                        "type": "Project",
                        "provider": "Public Portfolio / Competition / Exam",
                        "duration": "2 weeks",
                        "prereqs": ["UN301", "UN202"],
                        "why": "A tangible capstone cements all prior learning and provides proof of mastery.",
                        "skills": ["Mastery Proof", "Presentation", "Portfolio"],
                        "difficulty": "Advanced"
                    }
                ]
            }
        ]

    # Scale module durations to weekly study commitment
    try:
        hours = int(profile.get("weekly_hours", 10))
    except (TypeError, ValueError):
        hours = 10
    factor = max(0.5, min(2.0, 10 / max(1, hours)))

    scaled_phases = []
    for phase in phases:
        scaled_nodes = []
        for node in phase["nodes"]:
            node_copy = dict(node)
            m = re.match(r"^(\d+)\s*weeks?", str(node_copy.get("duration", "")))
            if m:
                weeks = max(1, round(int(m.group(1)) * factor))
                node_copy["duration"] = f"{weeks} week" + ("s" if weeks != 1 else "")
            scaled_nodes.append(node_copy)
        scaled_phases.append({"phase": phase["phase"], "nodes": scaled_nodes})

    return {
        "goal": goal,
        "role": role,
        "phases": scaled_phases
    }
