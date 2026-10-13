# Changelog

## 0.2.0

### Added
- **Themes:** `light`, `dark`, `ocean`, `sunset`, `forest`, `rose`
- **Backgrounds:** solid colors, gradients (with optional animation), image backgrounds
- **Fonts:** 20+ built-in fonts (English and Arabic) and any Google Font by name, plus `headingfont`
- **Animations:** 8 entrance effects, 8 looping effects, `delay` and `duration`
- **Mac-style motion:** smooth scrolling, spring hover effects, glass blur, staggered reveals inside grids
- **Stickers:** emoji or image stickers, draggable with `drag=yes`
- **New elements:** `subtitle`, `card`, `list`, `hero`, `navbar`, `footer`, `video`, `divider`, `space`
- **Layout:** `box` and `grid` containers closed with `end`
- **Styling options:** `color`, `bg`, `size`, `font`, `weight`, `spacing`, `textgradient`, `radius`, `shadow`, `border`, `padding`, `margin`, `width`, `height`, `gap`, `fit`, `align`, `glass`, `look`, `hover`, `inline`, `id`
- **Page commands:** `page`, `icon`, `lang`, `direction`, `theme`, `textcolor`, `accent`, `background`, `gradient`, `font`, `headingfont`, `width`, `animate`
- Full RTL and Arabic support
- Clear error messages with line numbers
- `demo.nova` showcase

### Changed
- `button` can now link somewhere: `button "Click" "#section"`
- `image` accepts an optional description
- Output is now a responsive page with a mobile-friendly viewport

### Security
- All text is escaped
- CSS values are validated
- `javascript:` and `data:` links are blocked

## 0.1.0

- First release
- Commands: `title`, `paragraph`, `button`, `link`, `image`
- Comments with `#`
