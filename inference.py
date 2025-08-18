from gpt4all import GPT4All
import json


with open("config.json", "r") as jsondata:
    LLMconfig = json.load(jsondata)

try:
    model = GPT4All(
        model_name=LLMconfig["modelpath"],
        device=LLMconfig["device"],
        allow_download=False,
        verbose=True,
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None


def LLMInferece(prompt="hi"):
    if model is None:
        return {"message": "Model not loaded. Please check server logs."}

    try:
        print(f"Question : {prompt}")
        with model.chat_session():
            response = model.generate(
                prompt=prompt, **LLMconfig["Modelfinetuningparameters"]
            )

        # clean_response = response.strip().replace("\\n", "\n")
        # print(response)
        return {"message": response}

    except Exception as e:
        print(f"Error during generation: {e}")
        return {"message": f"Error: {e}"}


# if __name__ == "__main__":
#     financial_data = "Explain the concept of general relativity. What is the difference between a neuron and a synapse?"
#     start = time.perf_counter()
#     analysis_result = AnalyzeFinancialData(financial_data)
#     end = time.perf_counter()
#     execution_time = end - start
#     print(f"Ai inference : {analysis_result['message']}")
#     print(f"Suggestion generated in : {execution_time:.4f} seconds")
