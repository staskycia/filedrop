def console_window(title, content):
    title = str(title)
    content = str(content)
    print(f"""
{"#" * 40}
{"#" * int((38 - len(title))/2)} {title} {"#" * int((38 - len(title))/2 + (1 if len(title) % 2 == 1 else 0))}
{"#" * 40}
#{" "*38}#
#{" "*38}#
#{" " * int((38 - len(content))/2)}{content}{" " * int((38 - len(content))/2 + (1 if len(content) % 2 == 1 else 0))}#
#{" "*38}#
#{" "*38}#
{"#" * 40}
""")