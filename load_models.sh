#!/bin/bash

ollama serve &

sleep 5

MODEL_FILE="/ollama_models.txt"

if [ ! -f "$MODEL_FILE" ]; then
  echo "Model file not found at $MODEL_FILE"
  exit 1
fi

while IFS= read -r model; do
  if [ -n "$model" ]; then
    if [ ! -f "/root/.ollama/models/${model}" ]; then
      echo "Pulling model: $model"
      ollama pull "$model"
    else
      echo "Model $model already exists, skipping."
    fi
  fi
done < "$MODEL_FILE"

wait
