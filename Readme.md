# Open Domain Question Answering Chatbot 

This repo contains code to create a open domain question answering (QA) Chatbot using Streamlit and Flask with Google and Wikipedia as knowledge base

## Technology Stack

* Frontend: Streamlit
* Backend: Flask (Python)

## How to run

> Important: Since I did this project long back, I have tested it on conda virtual environment with Python version 3.6.13.

* Step-1: Clone the repo and `cd` into it.

* Step-2: Create a conda virtual environment and activate it

```bash
conda create -n gwqa python=3.6
``` 
* Step-3: Install the frontend dependencies by running the following command 
```bash
pip install -r requirements.txt
```

* Step-4: Install the backend dependencies by `cd` into `backend` folder

```bash
pip install spacy==2.3.0
python -m spacy download en_core_web_sm
pip install -r requirements.txt
```

* Step-5: Start the backend service (Flask)
```bash
python main.py
```

* Step-6: Goto the root folder and run the following command to start streamlit
```bash
streamlit run app.py
```

