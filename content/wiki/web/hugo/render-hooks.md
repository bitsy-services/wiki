---
title: "Render Hooks"
weight: 50
aliases: ["/wiki/hugo/render-hooks/"]
---

A render hook is a template that replaces Goldmark's output for one kind of Markdown construct, everywhere it appears. Write `layouts/_markup/render-image.html` and every image on the site — in every page, from every author, past and future — renders through it. The content files do not change and do not learn anything about the site's HTML.

```go-html-template
{{/* layouts/_markup/render-image.html */}}
<figure>
  <img src="{{ .Destination | safeURL }}" alt="{{ .PlainText }}" loading="lazy">
  {{ with .Title }}<figcaption>{{ . }}</figcaption>{{ end }}
</figure>
```

## The hooks

| File | Fires on |
| --- | --- |
| `render-link.html` | inline links |
| `render-image.html` | images |
| `render-heading.html` | headings |
| `render-blockquote.html` | blockquotes, including alert syntax |
| `render-codeblock.html` | fenced code blocks |
| `render-codeblock-<lang>.html` | fenced blocks with that language tag |
| `render-table.html` | tables |
| `render-passthrough.html` | passthrough snippets, typically math |

All of them live in `layouts/_markup/`, in the project or in a theme, and follow the same lookup rules as any other template — a project file at the same path shadows the theme's.

The per-language code block hook dispatches on the fence's language tag. `layouts/_markup/render-codeblock-mermaid.html` catches ```` ```mermaid ```` fences and emits a `<div class="mermaid">` plus whatever the diagram library needs, leaving every other fence to normal syntax highlighting. The hugo-book theme ships that file and a `render-codeblock-katex.html` beside it, which is why a fenced block in this wiki can be a diagram or an equation without any shortcode in the content.

## What the template receives

Each hook gets a context shaped for its construct. The common fields:

| Field | Available on | Holds |
| --- | --- | --- |
| `.Destination` | link, image | the raw target, exactly as written |
| `.Text` | link, image, heading | the rendered inner Markdown |
| `.PlainText` | link, image, heading | the same with markup stripped |
| `.Title` | link, image | the optional quoted title |
| `.Anchor` | heading | the generated `id` |
| `.Level` | heading | 1 to 6 |
| `.Type` | codeblock | the language tag on the fence |
| `.Inner` | codeblock, blockquote | the block's contents |
| `.Attributes` | all | Markdown attributes on the construct |
| `.Page` | all | the page being built |
| `.PageInner` | all | the page the content came from, when it was included from elsewhere |
| `.Position` | all | file and line, for error messages |

`.Destination` is the string the author typed, not a resolved URL. Turning `beta.md` into `/docs/guide/beta/` is work the hook does, usually with `.Page.GetPage`, and a hook that forgets to do it emits a link to a file that is not there.

## The embedded link and image hooks

Hugo carries built-in link and image hooks that resolve relative destinations against the page. With them active, `[beta](beta.md)` in `content/docs/guide/alpha.md` renders as `/docs/guide/beta/`, and `[b](../bundle/)` renders as `/docs/bundle/`. When they run is controlled per hook:

```toml
[markup.goldmark.renderHooks.link]
  useEmbedded = 'fallback'
```

| Value | Behaviour |
| --- | --- |
| `auto` | the default; embedded hooks only for multilingual single-host projects |
| `never` | embedded hooks off; a custom hook still runs if one exists |
| `fallback` | embedded hooks whenever no custom hook exists |
| `always` | embedded hooks regardless, overriding any custom hook |

The default reads as "off" on an ordinary single-language site, which surprises people who expect `beta.md` links to resolve out of the box. A theme with its own `render-link.html` makes the setting moot in any case: `fallback` yields to the theme, and hugo-book ships one.

What the embedded hook does not do is complain. A destination it cannot resolve — `nope.md`, or an absolute `/docs/guide/nope` — is written into the HTML unchanged, the build exits zero, and nothing is logged. Resolution and validation are separate problems, and Hugo only solves the first; [internal links](/wiki/web/hugo/internal-links) is the second.

## Reach and limits

A render hook fires on Markdown, so anything not parsed as Markdown escapes it. Inline HTML in a content file is passed through by Goldmark untouched — an `<img>` tag written by hand gets no `loading="lazy"` from the hook above. Output from an angle-bracket [shortcode](/wiki/web/hugo/shortcodes) also escapes, because that output is inserted after Markdown rendering; the percent form's output goes back through the parser and does hit the hooks.

Heading anchors come from Goldmark rather than from a hook. `markup.goldmark.parser.autoHeadingID` generates them and `autoIDType` selects the algorithm — the [rules and their consequences for links](/wiki/web/hugo/internal-links#the-other-route-check-the-output) are on the internal links page. A `render-heading.html` hook receives the result in `.Anchor` and can print it, wrap it, or hang a permalink off it, but does not decide it.

## External references

- [Hugo: Markdown render hooks](https://gohugo.io/render-hooks/)
- [Hugo: Configure markup](https://gohugo.io/configuration/markup/)
- [GitHub alert syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts) — what a blockquote hook reads `.AlertType` from
