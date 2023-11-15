import torch
from transformers import pipeline


class SemanticaSummarizer:
    def __init__(self) -> None:
        self.summarizer = pipeline("summarization")

    def summarize_files(self, paths: str):
        texts = []
        result = []
        for path in paths:
            with open(path, "r", encoding="utf-8") as f:
                texts.append(f.read())
        for text in texts:
            query = "summarize: " + text
            summary = self.summarizer(query, truncation=True)
            result.append(summary[0]["summary_text"])
        return result

    def summarize_texts(self, text: str):
        query = "summarize: " + text
        summary = self.summarizer(query, truncation=True)
        return summary[0]["summary_text"]
