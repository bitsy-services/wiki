---
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
weight: 10
---

{{/*
  Start the body at ## — layouts/single.html renders the title as the page h1.

  Deliberately no `draft: true`: the production build (`hugo`) drops drafts, so a
  page created from this archetype would build locally under `hugo server -D` and
  then silently fail to publish.
*/}}
