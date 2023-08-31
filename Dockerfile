FROM python:3.10
WORKDIR /component-snapshot

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt 

# RUN python3 -c "import nltk;nltk.download('stopwords');nltk.download('averaged_perceptron_tagger');nltk.download('omw-1.4');nltk.download('wordnet');"

COPY . .

ENTRYPOINT ["python", "-m", "service.server"]