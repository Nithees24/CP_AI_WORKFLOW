-------------------------------------PROJECT WORKFLOW---------------------------------------
PDF Document
   ↓
Text + Layout Extraction
   ↓
Chunking (line / paragraph / block) #Given the choice to the user
   ↓
Pre-processing Rules
   ↓
Confidence Scoring
   ↓w
LLM 
   ↓
Step-wise Structured Output

----------------------------------------------------------------------------------------------

----------------------------------PROJECT DIRECTOARY DETAILS---------------------------------

project/
│
├── data/
│   └── input.pdf
│
├── extractor/
│   └── pdf_parser.py
│
├── preprocessing/
│   └── chunker.py
│
├── classifier/
│   ├── rules.py
│   └── llm_classifier.py
│
├── postprocessing/
│   └── step_builder.py
│
└── output/
    └── structured.json
-----------------------------------------------------------------------------------------------

-------------------------------------PROJECT CONFIGURATION-------------------------------------
pymupdf==1.23.8
pandas>=1.5.0
openai>=1.0.0
langchain>=0.1.0
----------------------------------------------------------------------------------------------
