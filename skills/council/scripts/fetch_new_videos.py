#!/usr/bin/env python3
"""
Find new videos from council channels and optionally pull their transcripts.

Uses YouTube's public RSS feeds (no API key needed) to detect new uploads, tracks
what's already been seen in a local state file, and fetches transcripts via
youtube-transcript-api.

Usage:
    python3 fetch_new_videos.py                 # list new videos as JSON
    python3 fetch_new_videos.py --transcripts   # also fetch transcript text
    python3 fetch_new_videos.py --member nate-b-jones
    python3 fetch_new_videos.py --since 7       # only videos from last 7 days
    python3 fetch_new_videos.py --mark-seen     # record these as processed
    python3 fetch_new_videos.py --reset         # clear seen-state (re-pull everything)

Output is JSON on stdout so a Claude session can consume it directly.
Diagnostics go to stderr.

Requires: youtube-transcript-api  (pip install youtube-transcript-api)
Only needed for --transcripts; listing new videos works with the stdlib alone.

IMPORTANT — where this runs matters:
  YouTube blocks caption requests from datacenter IPs. Transcript fetching therefore
  fails from a cloud session (RequestBlocked) but works fine from a normal home or
  office connection. Run with --transcripts on your own machine.

  Video descriptions come from the RSS feed and always work regardless of IP. For
  these particular creators the descriptions are substantive enough to triage
  relevance, so the weekly digest runs on descriptions and only pulls full
  transcripts when a video actually warrants the depth.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path(os.path.expanduser("~/.claude/council-data"))
STATE_FILE = DATA_DIR / "seen_videos.json"
CHANNELS_FILE = Path(__file__).parent / "channels.json"
RSS = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def log(msg):
    print(msg, file=sys.stderr)


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def fetch_feed(channel_id, attempts=4):
    """Return list of video dicts from a channel's RSS feed (~15 most recent).

    YouTube throttles bursts from datacenter IPs and signals it with spurious
    404/500 responses rather than 429. Retry with exponential backoff — a polite
    poll of five feeds is well under the limit, but a burst is not.
    """
    req = urllib.request.Request(
        RSS.format(channel_id),
        headers={"User-Agent": "Mozilla/5.0 (council-skill)"},
    )
    last = None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                root = ET.fromstring(resp.read())
            break
        except Exception as e:
            last = e
            if i < attempts - 1:
                wait = 5 * (2 ** i)
                log(f"   throttled ({type(e).__name__}), retrying in {wait}s")
                time.sleep(wait)
    else:
        raise last

    videos = []
    for entry in root.findall("atom:entry", NS):
        vid = entry.findtext("yt:videoId", namespaces=NS)
        if not vid:
            continue
        group = entry.find("media:group", NS)
        desc = ""
        if group is not None:
            desc = group.findtext("media:description", default="", namespaces=NS) or ""
        videos.append({
            "video_id": vid,
            "title": entry.findtext("atom:title", default="", namespaces=NS),
            "published": entry.findtext("atom:published", default="", namespaces=NS),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "description": desc[:2500],
        })
    return videos


HASHTAG_RE = re.compile(r"#\w+")


def classify(video, cfg=None, min_desc=400):
    """Guess whether a video is substantive or a clip/short/promo.

    RSS gives no duration, so this is heuristic. It is deliberately tuned to be
    permissive — it flags the obvious noise (shorts, clips) and leaves anything
    ambiguous marked 'unknown' for the reasoning layer to judge from the title
    and description. Better to pass a borderline case through than to silently
    drop a real video.
    """
    cfg = cfg or {}
    title = video.get("title", "")
    desc = video.get("description", "")
    tags = len(HASHTAG_RE.findall(title))
    signals = []

    # Per-channel rules beat generic heuristics. An All-In clip has a long,
    # substantive description and would otherwise sail through as a real video,
    # even though it's an excerpt of that week's flagship episode.
    clip_re = cfg.get("clip_title_regex")
    if clip_re and re.search(clip_re, title):
        video["kind"] = "noise"
        video["kind_signals"] = ["matches channel clip pattern"]
        return video

    flag_re = cfg.get("flagship_title_regex")
    if flag_re and re.search(flag_re, title):
        video["kind"] = "flagship"
        video["kind_signals"] = []
        return video

    # Shorts are near-universally hashtag-stuffed in the title.
    if tags >= 2:
        signals.append("hashtag-stuffed title")
    # Clips and shorts carry thin descriptions; real uploads get a writeup.
    if len(desc.strip()) < min_desc:
        signals.append("thin description")
    if len(title) < 30 and tags >= 1:
        signals.append("short title + tag")
    if re.search(r"\b(shorts?|clip|teaser|trailer|preview)\b", title, re.I):
        signals.append("clip keyword")

    if len(signals) >= 2:
        kind = "noise"
    elif signals:
        kind = "unknown"
    else:
        kind = "substantive"

    video["kind"] = kind
    video["kind_signals"] = signals
    return video


def get_transcript(video_id):
    """Return transcript segments with timestamps, or None if unavailable."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        log("!! youtube-transcript-api not installed. "
            "Run: pip install youtube-transcript-api")
        return None

    try:
        # API shape has changed across versions; try new instance-based form first.
        try:
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
            raw = fetched.to_raw_data()
        except AttributeError:
            raw = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except Exception as e:
        log(f"   no transcript for {video_id}: {type(e).__name__}")
        return None

    return [
        {"t": int(s["start"]), "text": s["text"]}
        for s in raw
        if s.get("text", "").strip()
    ]


def timestamped_url(video_id, seconds):
    return f"https://www.youtube.com/watch?v={video_id}&t={int(seconds)}s"


def to_paragraphs(segments, chunk_seconds=90):
    """Group raw caption segments into timestamped paragraphs for easier reading."""
    if not segments:
        return []
    chunks, cur, start = [], [], segments[0]["t"]
    for seg in segments:
        if seg["t"] - start >= chunk_seconds and cur:
            chunks.append({"t": start, "text": " ".join(cur)})
            cur, start = [], seg["t"]
        cur.append(seg["text"])
    if cur:
        chunks.append({"t": start, "text": " ".join(cur)})
    return chunks


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--transcripts", action="store_true",
                   help="fetch transcript text for each new video")
    p.add_argument("--member", help="only this member slug")
    p.add_argument("--since", type=int, default=14,
                   help="only videos published in the last N days (default 14)")
    p.add_argument("--mark-seen", action="store_true",
                   help="record returned videos as processed")
    p.add_argument("--reset", action="store_true",
                   help="clear the seen-state file and exit")
    p.add_argument("--max-per-channel", type=int, default=10)
    p.add_argument("--keep-noise", action="store_true",
                   help="don't filter out likely clips/shorts")
    p.add_argument("--delay", type=float, default=2.0,
                   help="seconds between channel fetches (default 2)")
    args = p.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if args.reset:
        STATE_FILE.unlink(missing_ok=True)
        log("seen-state cleared")
        return

    channels = load_json(CHANNELS_FILE, {})
    if not channels:
        log(f"!! no channels found at {CHANNELS_FILE}")
        sys.exit(1)

    seen = load_json(STATE_FILE, {})
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.since)
    results = {}

    for slug, info in channels.items():
        if args.member and slug != args.member:
            continue

        log(f"-> {info['name']}")
        try:
            videos = fetch_feed(info["channel_id"])
        except Exception as e:
            log(f"   FAILED: {type(e).__name__}: {e}")
            results[slug] = {"error": str(e), "videos": []}
            continue

        already = set(seen.get(slug, []))
        fresh = []
        for v in videos:
            if v["video_id"] in already:
                continue
            try:
                pub = datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
                if pub < cutoff:
                    continue
            except ValueError:
                pass
            fresh.append(v)

        fresh = [classify(v, info) for v in fresh]
        noise = [v for v in fresh if v["kind"] == "noise"]
        if not args.keep_noise:
            fresh = [v for v in fresh if v["kind"] != "noise"]
        if noise:
            log(f"   filtered {len(noise)} clip/short")

        fresh = fresh[: args.max_per_channel]

        if args.transcripts:
            for v in fresh:
                segs = get_transcript(v["video_id"])
                if segs:
                    v["transcript"] = to_paragraphs(segs)
                    v["transcript_available"] = True
                else:
                    v["transcript_available"] = False

        results[slug] = {
            "name": info["name"],
            "handle": info["handle"],
            "new_count": len(fresh),
            "filtered_noise": len(noise),
            "videos": fresh,
        }
        log(f"   {len(fresh)} kept")

        # Be polite between channels — bursts get throttled.
        time.sleep(args.delay)

        if args.mark_seen and fresh:
            seen[slug] = list(already | {v["video_id"] for v in fresh})[-400:]

    if args.mark_seen:
        with open(STATE_FILE, "w") as f:
            json.dump(seen, f, indent=2)
        log(f"state written to {STATE_FILE}")

    json.dump(results, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
