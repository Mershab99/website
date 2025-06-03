from collections import defaultdict
from datetime import datetime

from fasthtml.common import *
import json

import service.apiclient

FULL_NAME = "Mershab Issadien"

custom_styles = Style("""
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                     Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        background-color: #f9fafb;
        color: #1f2937;
    }
    .container {
        max-width: 700px;
        width: 100%;
        padding: 2rem;
        box-sizing: border-box;
        text-align: center;
    }
    .hero {
        margin-bottom: 2rem;
    }
    h1 {
        font-weight: 700;
        color: #111827;
    }
    h2 {
        font-weight: 600;
        color: #111827;
    }
    p {
        font-weight: 500;
        line-height: 1.6;
        color: #374151;
    }
    .about {
        margin-bottom: 2rem;
    }
    .footer {
        font-size: 0.9rem;
        color: #4b5563;
    }
""")

app, rt = fast_app(hdrs=[custom_styles])


@rt
def index():
    return Titled(
        FULL_NAME,
        Div(
            HeroSection(
                f"Hi, I'm {FULL_NAME}",
                "Backend engineer specializing in Java, Go & Python, with a passion for Kubernetes, DevOps, and cloud infrastructure."
            ),
            AboutSection(),
            CommitHeatmap(service.apiclient.GetHeatmapData(service.apiclient.GetCommits())),
            FooterSection(),
            cls="container"
        )
    )


def HeroSection(title, subtitle, cta=None):
    elements = [H1(title), P(subtitle)]
    if cta:
        elements.append(cta)
    return Div(*elements, cls="hero")


def AboutSection():
    return Section(
        H2("About Me"),
        P(
            "I architect and build scalable backend systems using Java and Go, "
            "focusing on cloud-native infrastructure, Kubernetes orchestration, "
            "and DevOps automation. I’m passionate about designing robust, "
            "efficient pipelines and infrastructure that empower teams to deploy "
            "secure and resilient applications."
        ),
        cls="about"
    )


def CommitHeatmap(heatmap_data):
    return Div(
        H2("Commit Activity (Last 30 Days)"),
        Div(id="cal-heatmap"),
        Script(src="https://d3js.org/d3.v7.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/cal-heatmap.min.js"),
        Link(rel="stylesheet", href="https://unpkg.com/cal-heatmap/dist/cal-heatmap.css"),
        Script(f"""
        document.addEventListener("DOMContentLoaded", function () {{
            const data = {json.dumps(heatmap_data)};
            const cal = new CalHeatmap();

            cal.paint({{
                itemSelector: "#cal-heatmap",
                range: 6,
                
                domain: {{ type: 'month', gutter: 15 }},
                subDomain: {{ type: 'day'}}, 
                
                date: {{
                    start: new Date(new Date().setDate(new Date().getDate() - 180)),
                }},
                data: {{
                    source: data,
                    x: 'date',
                    y: 'value'
                }},
                scale: {{
                  color: {{
                    type: 'threshold',
                    range: ['#14432a', '#166b34', '#37a446', '#4dd05a'],
                    domain: [10, 20, 30],
                  }},
                }},
                domain: {{
                  type: 'month',
                  gutter: 4,
                  label: {{ text: 'MMM', textAlign: 'start', position: 'top' }},
                }},
            }},
            );
        }});
        """)

    )


def FooterSection():
    return Footer(
        P("© 2025 Mershab Issadien"),
        cls="footer"
    )


serve()
