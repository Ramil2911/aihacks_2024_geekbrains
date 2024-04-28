FROM pytorch/torchserve as production

#CMD torch-model-archiver --model-name "rubert" --version 1.0 --serialized-file rubert-sentiment/pytorch_model.bin --extra-files "rubert-sentiment/config.json,rubert-sentiment/vocab.txt" --handler "handler.py" --export-path models --force
#CMD torch-model-archiver --model-name "classifier" --version 1.0 --serialized-file classifier/pytorch_model.bin --extra-files "classifier/config.json,classifier/vocab.txt,classifier/special_tokens_map.json,classifier/tokenizer_config.json" --handler "handler_classifier.py" --export-path models --force


RUN pip install transformers[torch] accelerate llama-cpp-python llama-cpp-python[server]

COPY config.properties /home/model-server/config.properties
COPY models /home/model-server/model-store