---
title: "Shortcodes"
weight: 40
aliases: ["/wiki/hugo/shortcodes/"]
---

A shortcode is a template callable from inside Markdown. Markdown has no syntax for a figure with a caption, a tabbed panel, or a list of child pages; a shortcode supplies one, keeping the content file readable while the HTML lives in a template where it can be changed once for every page that calls it.

```text
{{</* section */>}}
```

That line, at the bottom of 28 of this wiki's 35 section indexes, renders the list of child pages. The template behind it is `layouts/_shortcodes/section.html` in the [hugo-book theme](/wiki/web/hugo/themes-and-modules), whose first statement is a `warnf` announcing its own deprecation — a shortcode is a template like any other, and a theme can retire one by printing a warning from inside it.

## Two delimiters, two different behaviours

Shortcodes are called with angle brackets or with percent signs, and the difference is what happens to the output afterwards.

`{{</* name */>}}` inserts the template's output into the HTML verbatim.

`{{%/* name */%}}` feeds the template's output back through the Markdown renderer before it lands in the page.

A shortcode template of `**{{ .Inner }}**` makes the distinction concrete:

```text
A {{%/* note */%}}*em*{{%/* /note */%}} B

C {{</* note */>}}*em*{{</* /note */>}} D
```

```html
<p>A <em><strong>em</strong></em> B</p>
<p>C ***em*** D</p>
```

The percent form's asterisks were interpreted; the angle-bracket form's were not. Use the percent form when the shortcode emits Markdown or wraps Markdown the author writes inside it, and the angle-bracket form when it emits HTML. Getting it backwards produces literal asterisks in the page, or, in the other direction, HTML that Goldmark strips because `unsafe` rendering is off.

## Writing one

A shortcode is a template file whose name is the shortcode's name, under `layouts/_shortcodes/`. Parameters arrive positionally or by name, and Hugo does not mix the two styles in one call.

```go-html-template
{{/* layouts/_shortcodes/note.html */}}
<div class="note note--{{ .Get "level" | default "info" }}">
  {{ .Inner | .Page.RenderString }}
</div>
```

```text
{{</* note level="warning" */>}}
Text the author writes, rendered as Markdown by RenderString.
{{</* /note */>}}
```

The context available inside the template:

| Field | What it holds |
| --- | --- |
| `.Get "name"` / `.Get 0` | a named or positional parameter |
| `.Params` | all parameters, as a map or a slice |
| `.Inner` | the raw text between opening and closing tags |
| `.InnerDeindent` | the same, with leading indentation stripped |
| `.Page` | the page the shortcode was called from |
| `.Name` | the shortcode's own name |
| `.Ordinal` | its zero-based position among shortcodes on the page |
| `.Position` | file and line, for error messages |

`.Inner` is raw text, not rendered Markdown. `{{ .Inner | .Page.RenderString }}` renders it; `{{ .Inner | safeHTML }}` passes it through unescaped; using it bare prints the source. A shortcode with an `.Inner` needs a closing tag, and calling it without one is a build error.

Hugo resolves shortcodes the same way it resolves anything else in `layouts/`: the project's `layouts/_shortcodes/note.html` [shadows a theme's](/wiki/web/hugo/themes-and-modules#overriding-means-matching-a-path) file of that name, and a missing shortcode fails the build with the calling file and line.

## Embedded shortcodes

Hugo ships a set that needs no template. `figure` emits a `<figure>` with a caption; `highlight` gives a code block explicit options that a fence cannot express; `param` prints a front matter value into prose; `details` emits a collapsible block; `qr` renders a QR code as an inline image. `ref` and `relref` resolve a page reference to a URL and fail the build if the page does not exist — the subject of [internal links](/wiki/web/hugo/internal-links). `youtube`, `vimeo`, `instagram`, and `x` embed third-party content, at the cost of a request to that third party from every reader's browser.

The set shrinks as well as grows, and Hugo retires a shortcode in two stages. `comment` is deprecated in favour of HTML comments and still works, with a warning naming the file and line. `gist` and `twitter` are past that stage: calling either is a build error reporting the version that deprecated it and the version that removed it. A content file is the worst place for a dependency on something being retired, since nothing about it is typed or compiled, which is why the removal is an error rather than silence.

## Shortcodes expand inside code fences

Hugo processes shortcodes before Markdown, on the raw file, without regard to fenced code blocks. A call to `{{</* section */>}}` inside a ```` ```text ```` fence is executed, and the fence displays the *result*.

Escaping is a comment marker inside the delimiter, and it works in fenced blocks as well as in prose:

```text
{{</*/* note */*/>}}   renders as a literal shortcode call
```

Every shortcode call shown on this page uses that form. The failure it prevents is silent in the ordinary case — a documentation page renders the widget it meant to describe — and a build error in the case where the example was deliberately malformed.

## Shortcode or render hook

Both put a template between Markdown and HTML, and they differ in what triggers them. A shortcode fires where the author writes a call, so it handles the exceptional case: this image needs a caption, this section needs a table of child pages. A [render hook](/wiki/web/hugo/render-hooks) fires on every instance of a Markdown construct, so it handles the systematic case: every image gets `loading="lazy"`, every external link gets `rel="noopener"`.

Reaching for a shortcode where a render hook belongs shows up as the same call repeated on every page, and as content files that stop being portable Markdown.

## External references

- [Hugo: Shortcodes](https://gohugo.io/content-management/shortcodes/)
- [Hugo: Create your own shortcodes](https://gohugo.io/templates/shortcode/)
- [Hugo: Embedded shortcodes](https://gohugo.io/shortcodes/)
