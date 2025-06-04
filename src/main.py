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


@rt('/status')
def status():
    return {'status': 'ok'}

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
        H2("Commit Activity (Last 6 Months)"),
        Div(
            Div(id="ex-ghDay", cls="margin-bottom--md"),
            A("← Previous", href="#", cls="button button--sm button--secondary margin-top--sm", **{
                "onclick": "event.preventDefault(); cal.previous();"
            }),
            A("Next →", href="#", cls="button button--sm button--secondary margin-top--sm margin-left--xs", **{
                "onclick": "event.preventDefault(); cal.next();"
            }),
            Div(
                Span("Less", style="color: #768390;"),
                Div(id="ex-ghDay-legend", style="display: inline-block; margin: 0 4px;"),
                Span("More", style="color: #768390; font-size: 12px;"),
                style="float: right; font-size: 12px;",
            ),
            style={
                "background": "#22272d",
                "color": "#adbac7",
                "borderRadius": "3px",
                "padding": "1rem",
                "overflow": "hidden"
            }
        ),
        # Scripts and CSS
        Script(src="https://d3js.org/d3.v7.min.js"),
        Script(src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/cal-heatmap.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/plugins/Tooltip.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/plugins/LegendLite.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/plugins/CalendarLabel.min.js"),
        Link(rel="stylesheet", href="https://unpkg.com/cal-heatmap/dist/cal-heatmap.css"),
        # Heatmap Init
        Script(f"""
        document.addEventListener("DOMContentLoaded", function () {{
            const data = {json.dumps(heatmap_data)};
            const cal = new CalHeatmap();
            window.cal = cal;

            cal.paint({{
                theme: 'dark',
                itemSelector: "#ex-ghDay",
                range: 6,
                date: {{
                    start: new Date(new Date().setDate(new Date().getDate() - 180)),
                }},
                data: {{
                    source: data,
                    x: 'date',
                    y: 'value',
                    groupY: 'max',
                }},
                scale: {{
                    color: {{
                        type: 'threshold',
                        range: ['#14432a', '#166b34', '#37a446', '#4dd05a'],
                        domain: [1, 3, 5],
                    }},
                }},
                domain: {{
                    type: 'month',
                    gutter: 4,
                    label: {{ text: 'MMM', textAlign: 'start', position: 'top' }},
                }},
                subDomain: {{
                    type: 'ghDay',
                    radius: 2,
                    width: 11,
                    height: 11,
                    gutter: 4,
                }},
            }},
            
           );
        }});
        """)
    )
'''
 [
                [
                    Tooltip,
                    {{
                        text: function (date, value, dayjsDate) {{
                            return (value ? value : "No") + " commits on " + dayjsDate.format("dddd, MMMM D, YYYY");
                        }}
                    }}
                ],
                [
                    LegendLite,
                    {{
                        includeBlank: true,
                        itemSelector: "#ex-ghDay-legend",
                        radius: 2,
                        width: 11,
                        height: 11,
                        gutter: 4
                    }}
                ],
                [
                    CalendarLabel,
                    {{
                        width: 30,
                        textAlign: "start",
                        text: () => dayjs.weekdaysShort().map((d, i) => (i % 2 === 0 ? "" : d)),
                        padding: [25, 0, 0, 0]
                    }}
                ]
            ]
'''

def FooterSection():
    return Footer(
        P("© 2025 Mershab Issadien"),
        cls="footer"
    )


serve()
