# Fonts

`M PLUS Rounded 1c`, served locally rather than from Google's CDN. This is an
app for a child on a tablet; a typeface is not something to need a network for,
and the remote copy also meant nobody could screenshot the real thing offline.

| file | weight |
|---|---|
| `mplus-rounded-1c-latin-400.woff2` | 400 |
| `mplus-rounded-1c-latin-700.woff2` | 700 |
| `mplus-rounded-1c-latin-800.woff2` | 800 |
| `mplus-rounded-1c-latin-900.woff2` | 900 |

87 KB in total. Those are the only four weights `index.html` asks for.

## Why only the latin subset

M PLUS Rounded 1c is a Japanese family. Its full webfont runs to megabytes
across roughly 590 subset files. Nothing in the page or in `data/*.csv` uses a
character above U+00FF — checked, not assumed — so no other subset would ever be
requested. The `unicode-range` in the `@font-face` rules is Google's own for the
latin subset, copied unedited.

If a character outside that range ever appears, pull the matching subset the
same way:

```sh
curl -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
  (KHTML, like Gecko) Chrome/120.0 Safari/537.36' \
  'https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800;900&display=swap'
```

The plain-browser User-Agent matters: without it Google returns `.ttf` URLs
instead of `.woff2`. The response is grouped by subset with a `/* latin */`
style comment above each block.

## Licence

SIL Open Font License 1.1.

**`OFL.txt` is missing and needs adding.** The OFL requires its own text to
travel with the font files, and it could not be fetched from the sandbox this
was set up in. Get it from the family's directory in
<https://github.com/google/fonts> (under `ofl/`), or from
<https://openfontlicense.org>, and drop it in beside the `.woff2` files.
