from fasthtml.common import *

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
        color: #1f2937;  /* Darker text color */
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
        font-weight: 700;  /* Bold heading */
        color: #111827;    /* Even darker heading */
    }
    h2 {
        font-weight: 600;
        color: #111827;
    }
    p {
        font-weight: 500;
        line-height: 1.6;
        color: #374151;  /* Dark gray for paragraphs */
    }
    .about {
        margin-bottom: 2rem;
    }
    .footer {
        font-size: 0.9rem;
        color: #4b5563;  /* Medium gray footer */
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
                "Backend engineer specializing in Java, Go & Python, with a passion for Kubernetes, DevOps, and cloud infrastructure.",
                # Button("View Projects", hx_get="/projects", cls="primary")  # To be implemented
            ),
            AboutSection(),
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


def FooterSection():
    return Footer(
        P("© 2025 Mershab Issadien"),
        cls="footer"
    )


serve()
