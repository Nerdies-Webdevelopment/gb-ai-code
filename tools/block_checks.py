"""Bounded static HTML/CSS checks, without third-party dependencies.

CSS comparison covers explicit declarations, media/supports contexts and common
box shorthands. It is not a browser cascade or a complete CSS equivalence proof.
"""
from __future__ import annotations

from html.parser import HTMLParser
import re


class Markup(HTMLParser):
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
    OPTIONAL = set('html head body li dt dd p rt rp optgroup option colgroup thead tbody tfoot tr td th'.split())

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.tags = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag not in self.VOID:
            if self.stack and self.stack[-1] == tag and tag in {'li', 'p', 'dt', 'dd', 'option', 'tr', 'td', 'th'}:
                self.stack.pop()
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_endtag(self, tag):
        while self.stack and self.stack[-1] != tag and self.stack[-1] in self.OPTIONAL:
            self.stack.pop()
        if not self.stack:
            self.errors.append(f'saved HTML closing </{tag}> without matching opener')
        elif self.stack[-1] != tag:
            self.errors.append(f'saved HTML closes </{tag}> while <{self.stack[-1]}> is open')
            if tag in self.stack:
                del self.stack[self.stack.index(tag):]
        else:
            self.stack.pop()


# Core class contracts are evidenced by installed block sources and references.
# Pro classes are not guessed from the block name (some have no unique class).
CORE_CLASSES = {
    name: 'gb-' + name.split('/')[1] + '-'
    for name in ('generateblocks/element', 'generateblocks/text', 'generateblocks/media',
                 'generateblocks/shape', 'generateblocks/button', 'generateblocks/query',
                 'generateblocks/looper', 'generateblocks/loop-item', 'generateblocks/query-page-numbers')
}


def first_markup(fragment, block_name, attrs):
    parser = Markup()
    parser.feed(fragment)
    if not parser.tags:
        return None
    if block_name == 'generateblocks/media' and attrs.get('linkHtmlAttributes'):
        return next((item for item in parser.tags if item[0] == attrs.get('tagName', 'img')), None)
    return parser.tags[0]


def split_top(text, delimiter):
    """Split outside strings, comments, functions and brackets."""
    result, start, depth, quote, escaped = [], 0, 0, '', False
    for i, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ''
        elif char in "\"'":
            quote = char
        elif char in '([':
            depth += 1
        elif char in ')]':
            depth -= 1
        elif depth == 0 and (char == delimiter or (delimiter == ' ' and char.isspace())):
            if text[start:i].strip():
                result.append(text[start:i].strip())
            start = i + 1
    if text[start:].strip():
        result.append(text[start:].strip())
    return result


def normalize(value):
    # Do not remove whitespace within quoted content or custom-property tokens.
    parts = re.split(r'''("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')''', str(value).strip())
    for i in range(0, len(parts), 2):
        part = re.sub(r'\s+', ' ', parts[i])
        part = re.sub(r'\s*([,:()])\s*', r'\1', part)
        part = re.sub(r'(?<![\w.-])0\.(\d+)', r'.\1', part)
        part = re.sub(r'#([0-9a-fA-F])\1([0-9a-fA-F])\2([0-9a-fA-F])\3\b', r'#\1\2\3', part)
        parts[i] = part
    return ''.join(parts)


def expand(prop, value):
    value = normalize(value)
    values = split_top(value, ' ')
    if prop in ('border', 'border-top', 'border-right', 'border-bottom', 'border-left') and len(values) == 3:
        width, style, color = values
        if style in {'none', 'hidden', 'dotted', 'dashed', 'solid', 'double', 'groove', 'ridge', 'inset', 'outset'}:
            sides = ('top', 'right', 'bottom', 'left') if prop == 'border' else (prop[7:],)
            return {f'border-{side}-{kind}': val for side in sides for kind, val in zip(('width', 'style', 'color'), (width, style, color))}
    suffixes = None
    if prop in ('margin', 'padding', 'border-width', 'border-style', 'border-color'):
        suffixes = ['top', 'right', 'bottom', 'left']
    elif prop == 'border-radius' and '/' not in value:
        suffixes = ['top-left', 'top-right', 'bottom-right', 'bottom-left']
    if suffixes and 1 <= len(values) <= 4 and 'var(' not in value:
        a = values[0]; b = values[1] if len(values) > 1 else a
        c = values[2] if len(values) > 2 else a
        d = values[3] if len(values) > 3 else b
        result = {}
        for side, val in zip(suffixes, (a, b, c, d)):
            key = f'border-{side}-{prop[7:]}' if prop.startswith('border-') else f'{prop}-{side}'
            result[key] = val
        return result
    return {prop: value}


def declarations(body):
    result = {}
    for declaration in split_top(body, ';'):
        if ':' not in declaration:
            raise ValueError(f'invalid CSS declaration: {declaration}')
        prop, value = declaration.split(':', 1)
        result.update(expand(prop.strip(), value))
    return result


def css_rules(css, context=()):
    """Read balanced rule blocks; braces inside strings/functions are data."""
    result = {}
    css = re.sub(r'''("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|/\*.*?\*/''', lambda m: m[1] or '', css, flags=re.S)
    start, opening, depth, parens, quote, escaped = 0, None, 0, 0, '', False
    for i, char in enumerate(css):
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = ''
            continue
        if char in "\"'":
            quote = char
        elif char in '([':
            parens += 1
        elif char in ')]':
            parens -= 1
        elif not parens and char == '{':
            if depth == 0:
                opening = i
            depth += 1
        elif not parens and char == '}':
            depth -= 1
            if depth < 0:
                raise ValueError('unbalanced CSS closing brace')
            if depth == 0:
                selector, body = css[start:opening].strip(), css[opening + 1:i]
                if selector.startswith(('@media', '@supports', '@container', '@layer')):
                    nested = css_rules(body, context + (normalize(selector),))
                    for key, values in nested.items():
                        result.setdefault(key, {}).update(values)
                elif selector.startswith('@'):
                    raise ValueError(f'unsupported CSS at-rule: {selector}')
                else:
                    for sel in split_top(selector, ','):
                        result.setdefault((context, selector_key(sel)), {}).update(declarations(body))
                start = i + 1
    if depth or quote or parens or css[start:].strip():
        raise ValueError('incomplete CSS rule')
    return result


def selector_key(selector):
    return re.sub(r'\s*([>+~])\s*', r'\1', normalize(selector))


def style_rules(styles, selector, context=()):
    result = {(context, selector_key(selector)): {}}
    for prop, value in styles.items():
        if isinstance(value, dict):
            if prop.startswith('@'):
                nested = style_rules(value, selector, context + (normalize(prop),))
            else:
                nested = {}
                for part in split_top(prop, ','):
                    child = part.replace('&', selector) if '&' in part else selector + ' ' + part
                    for key, values in style_rules(value, child, context).items():
                        nested.setdefault(key, {}).update(values)
            for key, values in nested.items():
                result.setdefault(key, {}).update(values)
        elif isinstance(value, (str, int, float)) and not isinstance(value, bool):
            css_prop = prop if prop.startswith('--') else re.sub(r'[A-Z]', lambda m: '-' + m[0].lower(), prop)
            result[(context, selector_key(selector))].update(expand(css_prop, value))
        else:
            raise ValueError(f'unsupported structured style: {prop}')
    return result


def equivalent(prop, a, b):
    """Conservative equivalence; custom properties and strings stay literal."""
    if a == b:
        return True
    if prop.startswith('--'):
        return False
    if re.fullmatch(r'[+-]?0(?:\.0+)?(?:px|em|rem|vh|vw|vmin|vmax|cm|mm|in|pt|pc)?', a) and re.fullmatch(r'[+-]?0(?:\.0+)?(?:px|em|rem|vh|vw|vmin|vmax|cm|mm|in|pt|pc)?', b):
        return True
    if prop == 'color' or prop.endswith('-color'):
        def color(value):
            value = value.lower()
            value = {'black':'#000', 'white':'#fff', 'red':'#f00', 'blue':'#00f', 'lime':'#0f0', 'transparent':'#0000'}.get(value, value)
            if re.fullmatch(r'#[0-9a-f]{3,4}', value):
                value = '#' + ''.join(c * 2 for c in value[1:])
            if re.fullmatch(r'#[0-9a-f]{6}(?:[0-9a-f]{2})?', value):
                return tuple(int(value[i:i+2], 16) for i in (1,3,5)) + (int(value[7:9],16)/255 if len(value) == 9 else 1,)
            match = re.fullmatch(r'rgba?\((\d+),(\d+),(\d+)(?:,([01]|0?\.\d+))?\)', value)
            if match and all(int(match[i]) <= 255 for i in (1,2,3)):
                return tuple(int(match[i]) for i in (1,2,3)) + (float(match[4]) if match[4] else 1,)
            return value
        return color(a) == color(b)
    return False


def compare_styles(styles, css, selector):
    expected, actual = style_rules(styles, selector), css_rules(css)
    findings = []
    for key, properties in expected.items():
        present = actual.get(key, {})
        for prop, value in properties.items():
            if prop in present and not equivalent(prop, value, present[prop]):
                findings.append(('ERROR', f'styles/css mismatch at {key}: {prop}: {value!r} vs {present[prop]!r}'))
            elif prop not in present:
                # Other shorthands may express a longhand, e.g. border, font.
                possible = any(prop.startswith(short + '-') for short in present)
                level = 'WARN' if possible else 'ERROR'
                findings.append((level, f'styles property missing or not comparable in css at {key}: {prop}'))
    for key, properties in actual.items():
        present = expected.get(key, {})
        extra = sorted(properties.keys() - present.keys())
        if extra:
            # CSS-only additions can be intentional custom CSS. Flag them for
            # review; --strict rejects these warnings for new block exports.
            findings.append(('WARN', f'css properties missing or not comparable in styles at {key}: {", ".join(extra)}'))
    return findings
