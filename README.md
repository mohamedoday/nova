# Nova

Nova is a simple programming language for building websites.
It compiles `.nova` files into HTML.

## Example

```
title "My First Site"
paragraph "Written in Nova"
button "Click me"
link "Google" "https://google.com"
image "photo.png"
```

## Usage

Requires Python 3.

```
python compiler/nova.py examples/index.nova
```

This creates `examples/index.html`.

## Commands

| Command | Description |
|---|---|
| `title "text"` | Big heading |
| `paragraph "text"` | Paragraph |
| `button "text"` | Button |
| `link "text" "url"` | Link |
| `image "path"` | Image |

Lines starting with `#` are comments.
