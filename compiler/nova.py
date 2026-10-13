import sys
import shlex
import html

def compile_line(line, num):
    parts = shlex.split(line)
    cmd, args = parts[0], parts[1:]

    if cmd == "title" and len(args) == 1:
        return f"<h1>{html.escape(args[0])}</h1>"
    if cmd == "paragraph" and len(args) == 1:
        return f"<p>{html.escape(args[0])}</p>"
    if cmd == "button" and len(args) == 1:
        return f"<button>{html.escape(args[0])}</button>"
    if cmd == "link" and len(args) == 2:
        return f'<a href="{html.escape(args[1])}">{html.escape(args[0])}</a>'
    if cmd == "image" and len(args) == 1:
        return f'<img src="{html.escape(args[0])}" style="max-width:100%">'

    raise SyntaxError(f"سطر {num}: امر غير صحيح -> {line}")

def build(path):
    body = []
    with open(path, encoding="utf-8") as f:
        for num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            body.append(compile_line(line, num))

    page = (
        "<!DOCTYPE html>\n<html>\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Nova Site</title>\n</head>\n<body>\n"
        + "\n".join(body)
        + "\n</body>\n</html>\n"
    )

    out = path.rsplit(".", 1)[0] + ".html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("تم! الملف:", out)

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "index.nova")