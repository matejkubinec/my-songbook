#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import pathlib
import re
import sys
import urllib.parse


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    index_path = repo_root / "index.html"
    songs_root = repo_root / "songs"

    if not index_path.is_file():
        print("error: root index.html not found", file=sys.stderr)
        return 1

    pair_map: dict[pathlib.Path, set[str]] = {}
    for path in songs_root.rglob("*"):
        if not path.is_file() or path.suffix not in {".cho", ".pdf"}:
            continue
        pair_map.setdefault(path.with_suffix(""), set()).add(path.suffix)

    title_pattern = re.compile(r"^\{title:\s*(.*?)\s*\}$", re.IGNORECASE)
    artist_pattern = re.compile(r"^\{artist:\s*(.*?)\s*\}$", re.IGNORECASE)
    x_list_pattern = re.compile(r"^\{x_list:\s*(.*?)\s*\}$", re.IGNORECASE)
    entries: list[tuple[str, str, str, str]] = []
    song_data: list[dict[str, object]] = []

    for stem in sorted(pair_map):
        if pair_map[stem] != {".cho", ".pdf"}:
            continue

        cho_path = stem.with_suffix(".cho")
        pdf_path = stem.with_suffix(".pdf")
        title = stem.name
        artist = ""
        lists: list[str] = []
        cho_content = cho_path.read_text(encoding="utf-8")

        for line in cho_content.splitlines():
            stripped_line = line.strip()
            title_match = title_pattern.match(stripped_line)
            if title_match:
                title = title_match.group(1)
            artist_match = artist_pattern.match(stripped_line)
            if artist_match:
                artist = artist_match.group(1)
            x_list_match = x_list_pattern.match(stripped_line)
            if x_list_match:
                raw_items = (item.strip() for item in x_list_match.group(1).split(","))
                lists.extend(item for item in raw_items if item)

        cho_href = urllib.parse.quote(cho_path.relative_to(repo_root).as_posix(), safe="/")
        pdf_href = urllib.parse.quote(pdf_path.relative_to(repo_root).as_posix(), safe="/")
        entries.append((artist, title, cho_href, pdf_href))
        song_data.append(
            {
                "artist": artist,
                "title": title,
                "lists": lists,
                "content": cho_content,
                "_sort_key": (artist.casefold(), title.casefold(), cho_href),
            }
        )

    entries.sort(key=lambda item: (item[0].casefold(), item[1].casefold(), item[2]))

    list_lines = ["<ul id=\"songs\">"]
    for artist, title, cho_href, pdf_href in entries:
        display_label = f"{artist} - {title}" if artist else title
        list_lines.append(
            '  <li>{title} <a href="{cho}" target="_blank" rel="noopener noreferrer">(cho)</a> <a href="{pdf}" target="_blank" rel="noopener noreferrer">(pdf)</a></li>'.format(
                title=html.escape(display_label),
                cho=html.escape(cho_href, quote=True),
                pdf=html.escape(pdf_href, quote=True),
            )
        )
    list_lines.append("</ul>")
    generated_list = "\n".join(list_lines)

    original_html = index_path.read_text(encoding="utf-8")
    pattern = re.compile(r"(?ms)^(?P<indent>[ \t]*)<ul id=\"songs\">.*?</ul>")
    matches = list(pattern.finditer(original_html))
    if len(matches) != 1:
        print(f"error: expected exactly one <ul id=\"songs\"> in index.html, found {len(matches)}", file=sys.stderr)
        return 1

    match = matches[0]
    indent = match.group("indent")
    replacement = "\n".join(f"{indent}{line}" for line in generated_list.splitlines())
    updated_html = original_html[: match.start()] + replacement + original_html[match.end() :]
    index_path.write_text(updated_html, encoding="utf-8")

    songs_json_path = repo_root / "songs.json"
    sorted_song_data = sorted(song_data, key=lambda item: item["_sort_key"])
    output_song_data = [
        {
            "artist": item["artist"],
            "title": item["title"],
            "lists": item["lists"],
            "content": item["content"],
        }
        for item in sorted_song_data
    ]
    songs_json_path.write_text(
        json.dumps(output_song_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
