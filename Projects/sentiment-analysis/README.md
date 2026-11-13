# Sentiment Analysis API

A text-classification API that uses Hugging Face Transformers to classify feedback as **positive**, **negative**, or **neutral**.

## Features

- Uses a Hugging Face Transformer model for three-class sentiment classification.
- Validates incoming requests with Pydantic, including strict string typing, length limits, and rejection of empty or whitespace-only text.
- Exposes a FastAPI endpoint that returns the original text, predicted sentiment, and confidence score.
- Caches the model pipeline so it is loaded once and reused across requests.

## API

### `GET /health`

Returns a basic service health response.

### `POST /predict`

Request:

```json
{
  "text": "The support team was helpful and resolved my issue quickly."
}
```

Example response:

```json
{
  "text": "The support team was helpful and resolved my issue quickly.",
  "sentiment": "positive",
  "score": 0.98
}
```

The score shown is illustrative; the actual value is returned by the model.

## Run locally

Use Python 3.10 or newer:

```bash
python -m venv .venv
```

Activate the environment, then install and launch:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Model

The default model is `cardiffnlp/twitter-roberta-base-sentiment-latest`. Override it by setting the `SENTIMENT_MODEL` environment variable to another compatible three-class sentiment model.

Model weights are downloaded by Transformers on first use and cached by the Hugging Face tooling. The first prediction may therefore take longer than subsequent requests.
