#!/usr/bin/python3
"""Redcap-IF
Written for the Interact-IF game jam
"""
from typing import Optional

import uvicorn  # type: ignore
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from yarnrunner_python import YarnRunner  # type: ignore

from config import debug, host, port, story
from templates import PAGE, INPUT_OPTION, CHARACTER

__version__ = "0.0.1"

app = FastAPI(
    version=__version__,
    title="Redcap-IF",
    description=__doc__,
    docs_url="/",
    debug=debug,
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# runner: YarnRunner = None


# @app.on_event("startup")
def init(log: str = "") -> YarnRunner:
    print("init")

    # Open the compiled story and strings CSV.
    story_f = open(story + ".yarnc", "rb")
    strings_f = open(story + ".csv", "r")

    # Create the runner
    r = YarnRunner(story_f, strings_f, autostart=False)

    for choice in log.split(","):
        if choice and choice.strip():
            try:
                v = int(choice.strip())
                print(f"making a choice: {v}")
                choose(r, v)
            except ValueError:
                print(f"not a choice: {choice}")


    # # Register any command handlers
    # # (see https://yarnspinner.dev/docs/writing/nodes-and-content/#commands)
    # def custom_command(arg1, arg2):
    #     pass

    # runner.add_command_handler("customCommand", custom_command)

    return r


def get_choices(r: YarnRunner) -> str:
    """Returns the HTML for the choice"""
    result = []
    # Access the choices
    for choice in r.get_choices():
        print(choice)
        result += [
            INPUT_OPTION.format(
                name=choice["choice"], value=choice["index"], text=choice["text"]
            )
        ]

    return "<br/>".join(result)


def get_text(r: YarnRunner) -> str:
    result = "<br/>".join(r.get_lines())
    # Access the lines printed from the story
    print(result)
    return result


def choose(r: YarnRunner, opt: int):
    print(opt)

    # Access the choices
    for choice in r.get_choices():
        print(choice)


    if r.has_line():
        print(f"Skipping: {get_text(r)}")        

    # Make a choice and run until the next choice point or the end
    if opt in r.get_choices():
        r.choose(opt)
    else:
        print("Unable to make choice")

    # # Access the new lines printed from the last run
    # print('\n'.join(runner.get_lines()))

    # # Are we done?
    # if r.finished:
    #     print("Woohoo! Our story is over!")


char_map = {"forest": ["redcap", "wolf"], "house": ["redcap", "wolfasgranny"]}


@app.get("/scene", response_class=HTMLResponse)
# @app.get("/scene/{scene}", response_class=HTMLResponse)
def show(scene: Optional[str] = None, log: Optional[str] = None, choice: Optional[int] = None):
    print("start")
    if not scene:
        scene = "forest"

    if not log:
        log = ""

    chars = "".join(CHARACTER.format(character=name) for name in char_map[scene])

    runner = init(log)

    runner.resume()

    # if choice:
    #     choose(runner, int(choice))

    opts = get_choices(runner)
    txt = get_text(runner)

    print("end")
    return PAGE.format(scene=scene, log=log, characters=chars, options=opts, text=txt)


if __name__ == "__main__":
    uvicorn.run("main:app", host=host, port=port, reload=debug, debug=debug, reload_dirs=["."])
