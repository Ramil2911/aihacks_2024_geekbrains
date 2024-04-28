import logging
import os
from abc import ABC

import torch
from llama_cpp import Llama

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)


class LlamaCppHandler(BaseHandler, ABC):
    def __init__(self):
        super(LlamaCppHandler, self).__init__()
        self.initialized = False
        logger.info("Init done")

    def initialize(self, ctx):
        """In this initialize function, the HF large model is loaded and
        partitioned using DeepSpeed.
        Args:
            ctx (context): It is a JSON Object containing information
            pertaining to the model artifacts parameters.
        """
        logger.info("Start initialize")
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_path = properties.get("model_dir")
        if not os.path.exists(model_path):
            model_path = os.environ["LLAMA2_Q4_MODEL"]
        torch.manual_seed(42)

        self.model = Llama(model_path=model_path+"/model-q4_K.gguf")

    def preprocess(self, data):
        print("User's request: ", data)
        text = data[0].get("data")
        if text is None:
            text = data[0].get("body")
        sentences = text.decode('utf-8')
        return sentences

    def inference(self, data, **kwargs):
        result = self.model.create_completion(
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n<|start_header_id|>user<|end_header_id|>" + "Тебя зовут Инна, ты русскоговорящий методический ассистент, созданный для помощи людям в обработке чатов студенческих занятий в команиий GeekBrains. Используя свои знания, помоги пользователю улучшить качество образовательного процесса.<|eot_id|>\n" + data +"<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
            max_tokens=1024,
            top_p=5,
            temperature=0.05,
            stop=["Q:", "<|eot_id|>"],
            echo=True,
        )
        return result

    def postprocess(self, output):
        logger.info(output)
        result = [output["choices"][0]["text"]]
        return result