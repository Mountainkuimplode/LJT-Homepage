"""Validate the rendered homepage without adding any public pages."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            assert attrs["id"] not in self.ids, f"Duplicate id: {attrs['id']}"
            self.ids.add(attrs["id"])
        for attribute in ("href", "src"):
            if attrs.get(attribute):
                self.references.append(attrs[attribute])

    def handle_data(self, data):
        self.text.append(data)


site = Path("_site")
pages = sorted(str(path.relative_to(site)) for path in site.rglob("*.html"))
assert pages == ["index.html"], f"Unexpected published HTML pages: {pages}"
html = (site / "index.html").read_text(encoding="utf-8")
page = Page()
page.feed(html)
text = " ".join(" ".join(page.text).split())

for heading in (
    "about", "research-interests", "education", "research-experience",
    "publications", "awards", "contact",
):
    assert heading in page.ids, f"Missing homepage section: {heading}"

publications = (
    "SynLogic: Synthesizing Verifiable Reasoning Data at Scale for Learning Logical Reasoning and Beyond",
    "On the Perception Bottleneck of VLMs for Chart Understanding",
    "On the Universal Truthfulness Hyperplane Inside LLMs",
    "In-Context Sharpness as Alerts: An Inner Representation Perspective for Hallucination Mitigation",
    "C-Eval: A Multi-Level Multi-Discipline Chinese Evaluation Suite for Foundation Models",
    "Composing Parameter-Efficient Modules with Arithmetic Operations",
)
for title in publications:
    assert title in text, f"Publication missing from About: {title}"

for detail in (
    "Junteng Liu", "first-year PhD candidate at HKUST NLP Group",
    "Professor Junxian He", "Ph.D. in Computer Science", "B.Eng.",
    "Shanghai Jiao Tong University", "MINIMAX", "Tencent WXG", "Shanghai AI Lab",
    "Zifei Shan", "Prof. Yu Cheng", "Zhiyuan Honor Scholarship",
    "EMNLP 2024", "ICML 2024", "NeurIPS 2023",
):
    assert detail in text, f"Missing remembered detail: {detail}"

contacts = (
    "mailto:jliugi@connect.ust.hk",
    "https://github.com/Vicent0205",
    "https://scholar.google.com/citations?hl=en&user=tbK9jl4AAAAJ&view_op=list_works&sortby=pubdate",
    "https://x.com/junteng88716710",
)
for contact in contacts:
    assert contact in page.references, f"Missing contact link: {contact}"

for placeholder in (
    "Your Name", "Your Sidebar Name", "Red Brick University", "none@example.org",
    "profile.png", "og-image.png", "PS_CX0AAAAAJ", "yourorcidurl",
    "Academic Pages is a ready-to-fork",
):
    assert placeholder not in html, f"Template placeholder remains: {placeholder}"

origin = "https://mountainkuimplode.github.io"
baseurl = "/LJT-Homepage"
for reference in page.references:
    url = urlsplit(urljoin(origin + baseurl + "/", reference))
    if url.scheme not in ("http", "https") or url.netloc.lower() != urlsplit(origin).netloc:
        continue
    assert url.path.startswith(baseurl + "/"), f"Missing project baseurl: {reference}"
    relative_path = unquote(url.path[len(baseurl) + 1:])
    destination = site / relative_path
    if url.path.endswith("/"):
        destination /= "index.html"
    assert destination.is_file(), f"Broken internal link or asset: {reference}"
    if url.fragment and destination.name == "index.html":
        assert unquote(url.fragment) in page.ids, f"Broken section anchor: {reference}"

css = (site / "assets/css/main.css").read_text(encoding="utf-8")
assert "<html" not in css, "A page layout was incorrectly applied to the stylesheet"
assert not (site / "feed.xml").exists(), "Unexpected feed generated"
assert not (site / "sitemap.xml").exists(), "Unexpected sitemap generated"
print("Validated one homepage, six publications, remembered profile details, contact links, and project-site asset paths.")
