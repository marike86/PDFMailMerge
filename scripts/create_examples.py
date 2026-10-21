"""Rebuild the small, local demo shipped with the portable application."""
from pathlib import Path
import csv
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]


def main():
    destination = ROOT / "examples"
    destination.mkdir(exist_ok=True)
    with fitz.open() as doc:
        page = doc.new_page(width=595, height=842)
        page.draw_rect(fitz.Rect(0, 0, 595, 14), fill=(0.06, 0.42, 0.74), color=None)
        page.insert_text((54, 68), "NORTH / STUDIO", fontsize=13, color=(0.06, 0.42, 0.74))
        page.insert_text((54, 124), "项目邀请函", fontsize=28, fontname="china-ss", color=(0.09, 0.14, 0.23))
        page.insert_text((54, 151), "A PERSONAL INVITATION", fontsize=10, color=(0.4, 0.46, 0.55))
        page.draw_line((54, 180), (541, 180), color=(0.85, 0.89, 0.93))
        page.insert_text((54, 225), "致 / TO", fontsize=10, fontname="china-ss", color=(0.4, 0.46, 0.55))
        page.insert_text((54, 260), "{{name}}", fontsize=21, color=(0.09, 0.14, 0.23))
        page.insert_text((54, 320), "诚邀您参与我们的创作计划。", fontsize=13, fontname="china-ss")
        page.insert_text((54, 347), "期待与您一起，把想法变成值得分享的作品。", fontsize=13, fontname="china-ss")
        page.draw_rect(fitz.Rect(54, 397, 541, 551), fill=(0.95, 0.97, 0.99), color=None)
        for y, heading, token in ((430, "所属单位", "{{company}}"), (480, "联系邮箱", "{{email}}")):
            page.insert_text((74, y), heading, fontsize=10, fontname="china-ss", color=(0.4, 0.46, 0.55))
            page.insert_text((74, y + 22), token, fontsize=12, color=(0.09, 0.14, 0.23))
        page.insert_text((54, 635), "欢迎加入，期待相见。", fontsize=13, fontname="china-ss")
        page.insert_text((54, 716), "NORTH STUDIO / CREATIVE PARTNERS", fontsize=10, color=(0.06, 0.42, 0.74))
        page.draw_line((54, 760), (541, 760), color=(0.85, 0.89, 0.93))
        page.insert_text((54, 785), "PDF MAIL MERGE  /  LOCAL DEMO", fontsize=8, color=(0.4, 0.46, 0.55))
        doc.save(destination / "invitation_template.pdf", garbage=4, deflate=True)
    with (destination / "demo_data.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "name", "email", "company"])
        writer.writeheader()
        writer.writerows([
            {"id": "0001", "name": "林晓", "email": "lin@example.com", "company": "山海设计工作室"},
            {"id": "0002", "name": "陈予", "email": "chen@example.com", "company": "远见创意"},
            {"id": "0003", "name": "周然", "email": "zhou@example.com", "company": "澄明科技"},
        ])


if __name__ == "__main__":
    main()
