from gpt4all import GPT4All
import json
import time


with open("llmconfig.json", "r") as jsondata:
    LLMconfig = json.load(jsondata)

try:
    start = time.perf_counter()

    model = GPT4All(
        model_name=LLMconfig["modelpath"],
        device=LLMconfig["device"],
        allow_download=False,
        verbose=True,
        n_ctx=LLMconfig["contextsize"],
    )
    print("Model loaded successfully!")
    end = time.perf_counter()
    ModelLoadTime = end - start
    print(f"Model Loaded in : {ModelLoadTime:.4f} seconds")

except Exception as e:
    print(f"Failed to load model: {e}")
    model = None


def LLMInferece(prompt="hi", verbose: bool = False):
    if model is None:
        return {"message": "Model not loaded. Please check server logs."}

    try:
        if verbose:
            print(f"Question : {prompt}")
            print("-" * 100)

        start = time.perf_counter()
        with model.chat_session():
            response = model.generate(
                prompt=prompt, **LLMconfig["Modelfinetuningparameters"]
            )
        end = time.perf_counter()
        execution_time = end - start
        print(f"Suggestion generated in : {execution_time:.4f} seconds")
        return {"message": response}

    except Exception as e:
        print(f"Error during generation: {e}")
        return {"message": f"Error: {e}"}
