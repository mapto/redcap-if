INPUT_OPTION = """<input type="radio" id="{name}" name="choice" value="{value}"><label for="{name}">{text}</label>"""
CHARACTER = """<img class="character" src="/static/characters/{character}.png">"""

PAGE = ""
with open("template.html") as fhtml:
    PAGE = fhtml.read()
