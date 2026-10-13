# Nova

**Nova** is a small programming language for building modern websites.
You write simple English commands, and Nova compiles them into a single, smooth, Mac-style HTML page: colors, fonts, images, stickers and animations included.

**Current version: 0.2.0**

```
theme dark
font Poppins
accent #00d4ff

hero "Hello, Nova" "A website in a few lines" glass=yes animate=blur
button "Get started" "#features" align=center
```

## Features

- 🎨 **Colors**: 6 ready themes, custom colors, gradients (even animated), image backgrounds
- 🔤 **Fonts**: 20+ built-in fonts (English and Arabic) plus any Google Font by name
- 🖼️ **Images and video**: with rounded corners, shadows, fit and hover effects
- 😀 **Stickers**: emoji or image stickers, with animation, and draggable with the mouse or finger
- ✨ **Animations**: 8 entrance effects and 8 looping effects
- 🍎 **Mac-smooth motion**: smooth scrolling, spring hover effects, glass blur, staggered reveals, sticky glass navbar
- 🌍 **RTL support**: full Arabic and right-to-left layout
- ♿ **Accessible**: respects the "reduce motion" setting
- 🔒 **Safe output**: all text is escaped, CSS values are validated, `javascript:` links are blocked

## Requirements

Python 3.8 or newer. No other packages needed.

## Quick start

```
python compiler/nova.py examples/demo.nova
```

This creates `examples/demo.html`. Open it in any browser.

You can also choose the output file:

```
python compiler/nova.py site.nova output.html
```

## Project structure

```
nova/
├── compiler/
│   └── nova.py        the compiler
├── examples/
│   └── demo.nova      showcase of every feature
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## Language basics

- One command per line.
- Text goes in `"quotes"`.
- Options come after the text, written as `name=value`.
- If an option value has spaces, quote it: `font="Playfair Display"`.
- Lines starting with `#` are comments.
- Use `\n` inside text for a line break.

```
# comment
title "My site" color=#ff3366 size=56 animate=zoom
paragraph "Line one\nLine two" align=center
```

## Global commands

Write these anywhere in the file. They affect the whole page.

| Command | Example | What it does |
|---|---|---|
| `page` | `page "My Site"` | Page title |
| `icon` | `icon "🚀"` | Emoji used as the tab icon |
| `lang` | `lang ar` | Page language |
| `direction` | `direction rtl` | `rtl` or `ltr` |
| `theme` | `theme dark` | `light`, `dark`, `ocean`, `sunset`, `forest`, `rose` |
| `textcolor` | `textcolor #ffffff` | Text color |
| `accent` | `accent #ff3366` | Main color (buttons, links, glow) |
| `background` | `background #111` or `background wall.jpg` | Color or image background |
| `gradient` | `gradient #667eea #764ba2 135 animated=yes` | Gradient background (angle optional) |
| `font` | `font Poppins` | Page font |
| `headingfont` | `headingfont "Playfair Display"` | Font for titles |
| `width` | `width 1000` | Maximum content width in px |
| `animate` | `animate slide-up` | Default entrance animation, or `none` |

## Elements

| Command | Example |
|---|---|
| `title` | `title "Hello"` |
| `subtitle` | `subtitle "Welcome"` |
| `paragraph` | `paragraph "Some text"` |
| `button` | `button "Click" "#section"` (link is optional) |
| `link` | `link "Google" "https://google.com"` |
| `image` | `image "photo.jpg" "description"` (description is optional) |
| `sticker` | `sticker "🚀" size=80 animate=float` (emoji or image file) |
| `card` | `card "Title" "Text" "🎨"` (icon is optional) |
| `list` | `list "One" "Two" "Three"` |
| `hero` | `hero "Big title" "Subtitle"` (subtitle is optional) |
| `navbar` | `navbar "Brand" "Home\|#top" "About\|#about"` |
| `footer` | `footer "Made with Nova"` |
| `video` | `video "clip.mp4"` |
| `divider` | `divider` |
| `space` | `space 40` |
| `box` ... `end` | A container for grouping elements |
| `grid 3` ... `end` | A responsive grid, 1 to 6 columns |

In `navbar`, each item is written as `Text|#id`, where `#id` matches the `id=` of an element.

## Options

Options can be added to any element.

| Option | Example | Description |
|---|---|---|
| `color` | `color=#ff3366` | Text color |
| `bg` | `bg=#222` or `bg=photo.jpg` | Background color or image |
| `size` | `size=48` | Font size (px) |
| `font` | `font=Cairo` | Font |
| `weight` | `weight=bold` | `normal`, `bold`, or 100 to 900 |
| `spacing` | `spacing=2` | Letter spacing |
| `textgradient` | `textgradient=#00d4ff,#7b61ff` | Gradient text (use hex or color names) |
| `radius` | `radius=28` | Rounded corners |
| `shadow` | `shadow=big` | `none`, `soft`, `medium`, `big` |
| `border` | `border="2px solid red"` | Border |
| `padding` `margin` | `padding=32` | Spacing |
| `width` `height` | `width=300` | Size |
| `gap` | `gap=30` | Space between grid items |
| `fit` | `fit=cover` | Image fit: `cover`, `contain`, `fill` |
| `align` | `align=center` | `left`, `center`, `right` |
| `inline` | `inline=yes` | Place elements side by side (inside a `box`) |
| `glass` | `glass=yes` | Frosted glass effect |
| `look` | `look=outline` | Button style: `solid`, `outline`, `soft` |
| `hover` | `hover=lift` | `lift`, `grow`, `shrink`, `glow`, `tilt`, `none` |
| `animate` | `animate=zoom,float` | One or more animations |
| `delay` | `delay=0.3` | Animation delay (seconds) |
| `duration` | `duration=1.2` | Animation duration (seconds) |
| `drag` | `drag=yes` | Make a sticker draggable |
| `autoplay` | `autoplay=yes` | Video autoplay (muted, looping) |
| `id` | `id=features` | Anchor name for links |

## Animations

**Entrance** (play when the element scrolls into view):
`fade` `slide-up` `slide-down` `slide-left` `slide-right` `zoom` `flip` `blur`

**Looping:**
`float` `pulse` `spin` `bounce` `shake` `glow` `wiggle` `rainbow`

You can combine one of each: `animate=slide-down,float`.
Elements inside a `grid` appear one after another automatically.
Use `animate=none` to turn off the entrance effect for one element.

## Fonts

| Type | Names |
|---|---|
| System | `mac` `system` `serif` `mono` |
| English | `inter` `poppins` `montserrat` `roboto` `opensans` `playfair` `lobster` `pacifico` `bebas` `orbitron` `caveat` `fira` |
| Arabic | `cairo` `tajawal` `almarai` `amiri` `changa` |

Any other [Google Font](https://fonts.google.com) works by its name: `font="Dancing Script"`.
Fonts that load from Google need an internet connection; offline pages fall back to the system font.

## Themes

`light` `dark` `ocean` `sunset` `forest` `rose`

Override any theme color with `textcolor`, `accent`, `background` or `gradient`.

## Full example

```
page "My Studio"
icon "🚀"
theme dark
font Poppins
gradient #0f2027 #2c5364 135 animated=yes
accent #00d4ff

navbar "Studio" "Home|#top" "Features|#features"

sticker "🚀" size=90 animate=slide-down,float align=center drag=yes
hero "We build things" "Smooth, modern and simple" id=top glass=yes animate=blur

title "Features" id=features align=center textgradient=#00d4ff,#7b61ff
grid 3
card "Colors" "Themes and gradients" "🎨"
card "Motion" "Smooth animations" "✨"
card "Fonts" "Latin and Arabic" "🔤"
end

footer "Made with Nova"
```

## Error messages

Nova tells you the line number and what is wrong:

```
Nova error - line 4: unknown animation 'boom'. Available: fade, slide-up, ...
```

## Roadmap

- [ ] Multi-page sites
- [ ] Forms and inputs
- [ ] Variables and reusable components
- [ ] Live preview (`--watch`)
- [ ] VS Code syntax highlighting

## Contributing

Issues and pull requests are welcome.

## License

MIT, see [LICENSE](LICENSE).
