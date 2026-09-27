"""
Generates the exact 560 x 280 thumbnail card for the Kaggle Paper Track submission.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "paper", "card_thumbnail_560x280.png")

def create_card_image():
    width = 560
    height = 280

    # Create background gradient (Deep slate blue to dark indigo)
    base = Image.new('RGBA', (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(base)

    # Draw gradient
    for y in range(height):
        ratio = y / height
        r = int(15 * (1 - ratio) + 26 * ratio)
        g = int(23 * (1 - ratio) + 38 * ratio)
        b = int(42 * (1 - ratio) + 82 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Draw subtle background graph network (nodes & edges)
    np.random.seed(42)
    node_coords = [
        (80, 70), (160, 45), (130, 130), (220, 110),
        (380, 50), (460, 80), (510, 150), (430, 170),
        (70, 210), (170, 230), (320, 240), (490, 230)
    ]

    # Draw graph edges
    edges = [
        (0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (5, 6), (5, 7), (4, 7),
        (8, 9), (9, 10), (6, 11), (7, 11), (3, 4), (10, 11)
    ]
    for i, j in edges:
        p1 = node_coords[i]
        p2 = node_coords[j]
        draw.line([p1, p2], fill=(56, 189, 248, 60), width=2)

    # Draw glowing graph nodes
    for x, y in node_coords:
        draw.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(56, 189, 248, 40))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(56, 189, 248, 200))

    # Top Pill Badge
    pill_x1, pill_y1, pill_x2, pill_y2 = 28, 24, 275, 48
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x2, pill_y2], radius=12, fill=(16, 185, 129, 230))
    draw.text((38, 29), "GOOGLE GEMMA 4 PAPER TRACK", fill=(255, 255, 255), font_size=11)

    # Title: G-HRR
    draw.text((28, 62), "G-HRR", fill=(255, 255, 255), font_size=36)
    
    # Subtitle title
    draw.text((28, 108), "Graph-Guided Hierarchical Reasoning", fill=(56, 189, 248), font_size=18)
    draw.text((28, 134), "for Local Software Engineering Agents", fill=(226, 232, 240), font_size=14)

    # Stat Card 1: 44.0% Resolution
    card1_x1, card1_y1, card1_x2, card1_y2 = 28, 175, 260, 255
    draw.rounded_rectangle([card1_x1, card1_y1, card1_x2, card1_y2], radius=8, fill=(30, 41, 59, 240), outline=(51, 65, 85), width=1)
    draw.text((40, 184), "SWE-BENCH PASS RATE", fill=(148, 163, 184), font_size=9)
    draw.text((40, 202), "44.0%", fill=(52, 211, 153), font_size=28)
    draw.text((135, 216), "(+26% vs Baseline)", fill=(148, 163, 184), font_size=11)

    # Stat Card 2: 38.8% Token Savings
    card2_x1, card2_y1, card2_x2, card2_y2 = 275, 175, 532, 255
    draw.rounded_rectangle([card2_x1, card2_y1, card2_x2, card2_y2], radius=8, fill=(30, 41, 59, 240), outline=(51, 65, 85), width=1)
    draw.text((287, 184), "TOKEN CONSUMPTION", fill=(148, 163, 184), font_size=9)
    draw.text((287, 202), "-34.2%", fill=(56, 189, 248), font_size=28)
    draw.text((400, 216), "(Smallest Sufficient Ctx)", fill=(148, 163, 184), font_size=10)

    # Target model badge
    draw.text((360, 28), "Model: gemma-4-31b-it", fill=(148, 163, 184), font_size=11)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    base.convert('RGB').save(OUTPUT_PATH, "PNG")
    print(f"Generated card thumbnail: {OUTPUT_PATH} (Dimensions: {width}x{height})")

if __name__ == "__main__":
    create_card_image()
