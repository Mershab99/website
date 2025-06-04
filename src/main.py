import json

from fasthtml.common import *

import service.apiclient

FULL_NAME = "Mershab Issadien"

app, rt = fast_app(hdrs=[
    Script(src="https://cdn.tailwindcss.com"),
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"),
])


@rt('/status')
def status():
    return {'status': 'ok'}


@rt
def index():
    return (
        Title(FULL_NAME),  # page title in browser tab
        Main(
            Div(
                HeroSection(
                    f"Hi, I'm {FULL_NAME}",
                    "Backend engineer specializing in Java, Go & Python, with a passion for Kubernetes, DevOps, and cloud infrastructure. \n"
                ),
                AboutSection(),
                CommitHeatmap(),
                FooterSection(),
                cls="max-w-xl"  # optional max width for content
            ),
            cls="flex flex-col justify-center items-center min-h-screen text-center px-4"
        )
    )


def HeroSection(title, subtitle):
    return Div(
        H1(title, cls="text-4xl font-bold text-base-content"),
        P(subtitle, cls="mt-4 text-lg text-base-content"),
        cls="text-center"
    )


def AboutSection():
    return Section(
        H2("About Me", cls="text-2xl font-semibold text-base-content mb-2"),
        P(
            "I architect and build scalable backend systems using Java and Go, "
            "focusing on cloud-native infrastructure, Kubernetes orchestration, "
            "and DevOps automation. I’m passionate about designing robust, "
            "efficient pipelines and infrastructure that empower teams to deploy "
            "secure and resilient applications.",
            cls="text-base-content text-md leading-relaxed"
        ),
        cls="bg-base-200 p-6 rounded-lg shadow"
    )


def CommitHeatmap():
    heatmap_request = service.apiclient.load_request_data()
    heatmap_data = service.apiclient.fetch_commits_heatmap(heatmap_request)

    return Div(
        H2("Commit Activity", cls="text-xl font-semibold text-base-content mb-4"),
        Div(
            Div(id="ex-ghDay", cls="mb-4 w-full max-w-full overflow-auto rounded-md"),

            Div(
                A("← Previous", href="#", cls="btn btn-sm btn-outline", **{
                    "onclick": "event.preventDefault(); cal.previous();"
                }),
                A("Next →", href="#", cls="btn btn-sm btn-outline ml-2", **{
                    "onclick": "event.preventDefault(); cal.next();"
                }),
                cls="mb-4"
            ),

            Div(
                Span("Less", cls="text-sm text-gray-400"),
                Div(id="ex-ghDay-legend", cls="inline-block mx-2"),
                Span("More", cls="text-sm text-gray-400"),
                cls="text-right text-sm"
            ),

            cls="bg-base-200 text-base-content rounded-lg p-4 shadow-md"
        ),
        # Scripts
        # Core & plugin scripts and styles
        Script(src="https://d3js.org/d3.v7.min.js"),
        Script(src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/cal-heatmap.min.js"),

        # Plugin dependencies and plugins
        Script(src="https://unpkg.com/@popperjs/core@2"),  # Needed for Tooltip
        Script(src="https://unpkg.com/cal-heatmap/dist/plugins/Tooltip.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/plugins/LegendLite.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/plugins/CalendarLabel.min.js"),

        # CSS
        Link(rel="stylesheet", href="https://unpkg.com/cal-heatmap/dist/cal-heatmap.css"),
        # Init
        Script(f"""
        document.addEventListener("DOMContentLoaded", function () {{
            const data = {json.dumps(heatmap_data)};
            const cal = new CalHeatmap();
            window.cal = cal;

            cal.paint({{
                theme: 'dark',
                itemSelector: "#ex-ghDay",
                range: 8,
                date: {{
                    start: new Date(new Date().setDate(new Date().getDate() - 180)),
                }},
                data: {{
                    source: data,
                    x: 'date',
                    y: 'value',
                }},
                scale: {{
                    color: {{
                        type: 'threshold',
                        range: ['#14432a', '#166b34', '#37a446', '#4dd05a'],
                        domain: [1, 3, 7],
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
               
           ]
            
            );
        }});
        """)
    )


def FooterSection():
    return Footer(
        P("© 2025 Mershab Issadien", cls="text-sm text-center text-base-content"),
        cls="mt-12"
    )


serve()
