import time
import typer

app = typer.Typer()


@app.command()
def main(userprompt: str):
    if userprompt is None or "":
        print("fhvbfh")
    from inference import LLMInferece

    start = time.perf_counter()
    print(LLMInferece(prompt=userprompt)["message"])
    end = time.perf_counter()
    execution_time = end - start
    print(f"Suggestion generated in : {execution_time:.4f} seconds")


if __name__ == "__main__":
    app()
