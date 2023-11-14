# run a client of gradio
from gradio import Interface


def run(name: str):
    return "Hello" + name + "!"


if __name__ == "__main__":
    interface = Interface(fn=run, inputs="text", outputs="text")
