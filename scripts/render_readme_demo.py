#!/usr/bin/env python3
"""Render the README demo GIF from deterministic frames."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "demo.gif"
WIDTH = 960
HEIGHT = 540
BG = "#0F171A"
PANEL = "#14232B"
PANEL_2 = "#1B3139"
TEXT = "#F7FAF9"
MUTED = "#B8C8C4"
GOLD = "#F8D66D"
TEAL = "#5DB7C3"
GREEN = "#A2D2A4"
ORANGE = "#F0B67F"
RED = "#EF7B7B"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(38, bold=True)
FONT_SUBTITLE = font(20)
FONT_LABEL = font(18, bold=True)
FONT_BODY = font(18)
FONT_MONO = font(18)
FONT_MONO_SMALL = font(16)


def rounded(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2 if outline else 1)


def draw_header(draw: ImageDraw.ImageDraw) -> None:
    rounded(draw, (32, 28, 928, 106), 20, PANEL, "#2F4752")
    rounded(draw, (58, 48, 104, 88), 10, "#E9F3F0")
    draw.polygon([(81, 55), (99, 63), (99, 76), (81, 87), (63, 76), (63, 63)], fill="#16697A")
    draw.rectangle((69, 73, 74, 82), fill=GOLD)
    draw.rectangle((79, 65, 84, 82), fill=GOLD)
    draw.rectangle((89, 75, 94, 82), fill=GOLD)
    draw.text((122, 45), "Signal Harbor", fill=TEXT, font=FONT_TITLE)
    draw.text((124, 83), "Signal ingestion -> cached risk summary -> CI/CD deploy readiness", fill=MUTED, font=FONT_SUBTITLE)


def draw_footer(draw: ImageDraw.ImageDraw, active: int) -> None:
    labels = ["POST signal", "GET risk", "Operate"]
    colors = [TEAL, GOLD, GREEN]
    x = 248
    for idx, label in enumerate(labels):
        fill = colors[idx] if idx == active else "#35505A"
        rounded(draw, (x, 486, x + 142, 518), 16, fill)
        draw.text((x + 18, 493), label, fill="#101820" if idx == active else MUTED, font=FONT_LABEL)
        x += 158


def draw_terminal(draw: ImageDraw.ImageDraw, lines: list[tuple[str, str]], title: str) -> None:
    rounded(draw, (50, 132, 584, 468), 16, "#091113", "#2F4752")
    draw.rectangle((50, 132, 584, 172), fill=PANEL_2)
    draw.ellipse((70, 146, 82, 158), fill=RED)
    draw.ellipse((91, 146, 103, 158), fill=ORANGE)
    draw.ellipse((112, 146, 124, 158), fill=GREEN)
    draw.text((144, 144), title, fill=MUTED, font=FONT_LABEL)
    y = 194
    for text, color in lines:
        draw.text((72, y), text, fill=color, font=FONT_MONO)
        y += 28


def draw_metric_card(draw: ImageDraw.ImageDraw, title: str, value: str, detail: str, color: str, xy: tuple[int, int]) -> None:
    x, y = xy
    rounded(draw, (x, y, x + 286, y + 96), 16, PANEL, "#2F4752")
    draw.text((x + 18, y + 16), title, fill=MUTED, font=FONT_LABEL)
    draw.text((x + 18, y + 42), value, fill=color, font=font(28, bold=True))
    draw.text((x + 18, y + 74), detail, fill=TEXT, font=FONT_MONO_SMALL)


def frame_one() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_terminal(
        draw,
        [
            ("$ curl -X POST /api/v1/signals", TEAL),
            ('  -H "X-API-Key: dev-api-key"', MUTED),
            ('  -d {"signalType":"SECURITY_ALERT",', MUTED),
            ('      "severity":"CRITICAL",', MUTED),
            ('      "serviceName":"automation-api"}', MUTED),
            ("HTTP/1.1 201 Created", GREEN),
            ('{"serviceName":"automation-api",', TEXT),
            (' "severity":"CRITICAL"}', TEXT),
        ],
        "ingest operational signal",
    )
    draw_metric_card(draw, "API Boundary", "201 Created", "validated + authenticated", GREEN, (622, 146))
    draw_metric_card(draw, "Persistence", "PostgreSQL", "JPA entity stored", TEAL, (622, 258))
    draw_metric_card(draw, "Cache Policy", "Evict", "summary refreshed on write", GOLD, (622, 370))
    draw_footer(draw, 0)
    return img


def frame_two() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_terminal(
        draw,
        [
            ("$ curl /api/v1/services/automation-api/risk-summary", TEAL),
            ('  -H "X-API-Key: dev-api-key"', MUTED),
            ("HTTP/1.1 200 OK", GREEN),
            ('{"signalCount":1,', TEXT),
            (' "riskScore":5,', TEXT),
            (' "riskLevel":"ELEVATED",', GOLD),
            (' "signalsByType":{"SECURITY_ALERT":1}}', TEXT),
        ],
        "read cached risk summary",
    )
    draw_metric_card(draw, "Risk Score", "5", "weighted deterministic policy", GOLD, (622, 146))
    draw_metric_card(draw, "Risk Level", "ELEVATED", "explainable output", ORANGE, (622, 258))
    draw_metric_card(draw, "Read Path", "Redis", "cacheable incident view", TEAL, (622, 370))
    draw_footer(draw, 1)
    return img


def frame_three() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_terminal(
        draw,
        [
            ("$ ./mvnw test", TEAL),
            ("BUILD SUCCESS", GREEN),
            ("$ docker build -t signal-harbor:$BUILD_NUMBER .", TEAL),
            ("tests already ran outside Docker", MUTED),
            ("$ DEPLOY_TARGET=aws-eks | azure-aks | onprem", TEAL),
            ("kubeconfig copied to .kubeconfig.ci", GOLD),
            ("container listens on port 80", GREEN),
        ],
        "ci/cd readiness",
    )
    draw_metric_card(draw, "Jenkins", "mvn test", "separate from image build", GREEN, (622, 146))
    draw_metric_card(draw, "Kubernetes", "Port 80", "ingress TLS 443 -> service", TEAL, (622, 258))
    draw_metric_card(draw, "Cloud Targets", "AWS Azure On-Prem", "credential-specific stages", GOLD, (622, 370))
    draw_footer(draw, 2)
    return img


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [frame_one(), frame_two(), frame_three()]
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=[1800, 1800, 2200],
        loop=0,
        optimize=True,
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
