FROM pytorch/torchserve as production

RUN pip install transformers[torch] accelerate

COPY config.properties /home/model-server/config.properties
COPY models/rubert.mar /home/model-server/model-store