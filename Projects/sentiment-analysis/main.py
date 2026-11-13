import os
from functools import lru_cache
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from transformers import pipeline

SENTIMENT_MODEL = os.getenv(
    "SENTIMENT_MODEL", "cardiffnlp/twitter-roberta-base-sentiment-latest"
)

app = FastAPI(
    title="Sentiment Analysis API",
    description="Classify text feedback as positive, negative, or neutral.",
    version="1.0.0",
)


class SentimentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Feedback text to classify.",
    )

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text must not be empty or whitespace only.")
        return value


class SentimentResponse(BaseModel):
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    score: float


@lru_cache(maxsize=1)
def get_classifier():
    # The model is loaded once and reused for subsequent requests.
    return pipeline(
        task="text-classification",
        model=SENTIMENT_MODEL,
        truncation=True,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest):
    try:
        prediction = get_classifier()(request.text)[0]
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Sentiment model is unavailable: {exc}",
        ) from exc

    label = str(prediction["label"]).lower()
    # Support model outputs such as LABEL_0 as well as named labels.
    label_map = {"label_0": "negative", "label_1": "neutral", "label_2": "positive"}
    sentiment = label_map.get(label, label)
    if sentiment not in {"positive", "negative", "neutral"}:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected sentiment label returned by model: {label}",
        )

    return SentimentResponse(
        text=request.text,
        sentiment=sentiment,
        score=float(prediction["score"]),
    )
