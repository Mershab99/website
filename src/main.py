import json

from fasthtml.common import *

import service.apiclient

FULL_NAME = "Mershab Issadien"

app, rt = fast_app()


@rt('/status')
def status():
    return {'status': 'ok'}


def task_load_heatmap():
    req = service.apiclient.load_request_data()
    data = service.apiclient.fetch_commits_heatmap(req)
    return data


@rt('/load-heatmap')
def load_heatmap():
    data = task_load_heatmap()
    print(data)
    return CommitHeatmap(data)


def header_scripts():
    return (
        Script(src="https://cdn.tailwindcss.com"),
        Script(src="https://unpkg.com/htmx.org@1.9.10"),
        Script(src="https://d3js.org/d3.v7.min.js"),
        Script(src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/cal-heatmap.min.js"),
        Script(src="https://unpkg.com/@popperjs/core@2"),
        Script(src="https://unpkg.com/cal-heatmap/dist/plugins/Tooltip.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/plugins/LegendLite.min.js"),
        Script(src="https://unpkg.com/cal-heatmap/dist/plugins/CalendarLabel.min.js"),
        Link(rel="stylesheet", href="https://unpkg.com/cal-heatmap/dist/cal-heatmap.css"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"),
    )


@rt
def index():
    return (
        header_scripts(),
        ThemeToggleScript(),
        Title(FULL_NAME),
        Main(
            Div(
                ThemeToggleButton(),
                HeroSection(
                    f"Hi, I'm {FULL_NAME}",
                    "Backend engineer specializing in Java, Go & Python, with a passion for Kubernetes, DevOps, and cloud infrastructure.\n"
                ),
                Div(
                    H2("Commit Heatmap", cls="text-2xl font-bold mb-4"),
                    Span(
                        id="heatmap-spinner",
                        cls="loading loading-dots loading-xl",
                        hx_post=load_heatmap,
                        hx_target="#heatmap-spinner",
                        hx_trigger="load delay:1s",
                        hx_swap="outerHTML"
                    ),
                ),
                AboutSection(),
                FooterSection(),
                cls="w-full max-w-4xl px-4 sm:px-6 lg:px-8"
            ),
            cls="flex flex-col justify-center items-center min-h-screen text-center"
        )
    )


def HeroSection(title, subtitle):
    return Div(
        Div(
            H1(title, cls="text-5xl font-bold text-base-content"),
            P(subtitle, cls="mt-4 text-lg text-base-content max-w-xl"),
            cls="hero-content text-center"
        ),
        cls="hero min-h-[60vh] bg-base-100"
    )


def AboutSection():
    return Section(
        Div(
            H2("About Me", cls="text-2xl font-semibold text-base-content mb-2"),
            P(
                "I architect and build scalable backend systems using Java and Go, "
                "focusing on cloud-native infrastructure, Kubernetes orchestration, "
                "and DevOps automation. I’m passionate about designing robust, "
                "efficient pipelines and infrastructure that empower teams to deploy "
                "secure and resilient applications.",
                cls="text-base-content text-md leading-relaxed"
            ),
            cls="card-body"
        ),
        cls="card bg-base-200 shadow-md my-6"
    )


def CommitHeatmap(heatmap_data):
    return Div(
        Div(
            # Heatmap container
            Div(
                id="commit-heatmap",
                cls=(
                    "flex justify-center mb-4 w-full overflow-x-auto "
                    "rounded-md"
                )
            ),

            # Prev/Next buttons
            Div(
                A("← Previous", href="#", cls="btn btn-sm btn-outline", **{
                    "onclick": "event.preventDefault(); window.cal?.previous();"
                }),
                A("Next →", href="#", cls="btn btn-sm btn-outline ml-2", **{
                    "onclick": "event.preventDefault(); window.cal?.next();"
                }),
                cls="flex justify-center gap-4 mb-4"
            ),

            # Legend
            Div(
                Span("Less", cls="text-sm text-gray-400"),
                Div(id="commit-legend", cls="inline-block mx-2"),
                Span("More", cls="text-sm text-gray-400"),
                cls="flex justify-center items-center gap-2 text-sm"
            ),

            cls="card bg-base-200 text-base-content shadow-md p-6 flex flex-col items-center"
        ),

        # Heatmap render script
        Script(f"""
        (function () {{
            const data = {json.dumps(heatmap_data)};
            const cal = new CalHeatmap();
            window.cal = cal;

            cal.paint({{
                theme: document.documentElement.getAttribute('data-theme') || 'dark',
                itemSelector: "#commit-heatmap",
                range: 8,
                date: {{
                    start: new Date(new Date().setDate(new Date().getDate() - 210)),
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
                        itemSelector: "#commit-legend",
                        radius: 2,
                        width: 11,
                        height: 11,
                        gutter: 4
                    }}
                ]
            ]);
        }})();
        """)
    )


def FooterSection():
    return Footer(
        Div(
            P("© 2025 Mershab Issadien", cls="text-sm text-base-content text-center"),
            cls="w-full text-center"
        ),
        cls="mt-12 p-4 bg-base-100"
    )


def ThemeToggleButton():
    return Div(
        Div(
            Label(
                Span("🌞", cls="label-text"),
                Input(type="checkbox", cls="toggle theme-controller", **{
                    "onchange": "document.documentElement.setAttribute('data-theme', this.checked ? 'light' : 'dark')"
                }),
                Span("🌚", cls="label-text"),
                cls="flex gap-2 items-center"
            ),
            cls="form-control"
        ),
        cls="w-full flex justify-end py-2"
    )


def ThemeToggleScript():
    return Script("""
    (() => {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        if (!document.documentElement.hasAttribute('data-theme')) {
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        }
    })();
    """)


serve()
