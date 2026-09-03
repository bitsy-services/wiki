---
name: global-attached-images-are-in-the-transcript
description: Images the user attaches to a message are recoverable as base64 from the session .jsonl — never substitute generated art for a supplied asset
metadata:
  type: feedback
---

When the user attaches an image and asks for it to be used, the file usually
does not exist on disk. It *is* in the session transcript at
`~/.claude/projects/<project-slug>/<session-id>.jsonl`, as a base64 `image`
block inside the user message. Extract it:

```python
for line in open(TRANSCRIPT):
    rec = json.loads(line)
    if rec.get("type") == "user" and isinstance(rec["message"].get("content"), list):
        for b in rec["message"]["content"]:
            if isinstance(b, dict) and b.get("type") == "image":
                raw = base64.b64decode(b["source"]["data"])
```

The user message carrying the real attachment has both `image` and `text`
blocks; my own renders come back as `tool_result` blocks, so filter on message
type to avoid picking up the wrong one.

**Why:** Asked to install a supplied logo as a favicon, I searched the repo,
/tmp and Downloads, found nothing, and reconstructed the mark parametrically
from looking at it. The redraw added an inner hexagon the original did not
have. The reaction was "What the hell did you do? You added webbing! I want
the original image that I gave you!" — recreating a brand asset is never an
acceptable substitute for the asset, and the substitution was avoidable
because the bytes were on disk the whole time.

**How to apply:** For any supplied asset — image, logo, data file, document —
retrieve the real bytes from the transcript before doing anything else. If
retrieval genuinely fails, stop and ask; do not generate a stand-in and ship
it. Flagging a substitution in the summary does not make it okay, because the
user has to notice the flag to catch it. Applies well beyond this repo.
