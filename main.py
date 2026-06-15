import os
import flet as ft
import flet_video as fv
import webbrowser
import threading

def main(page: ft.Page):

    # =========================================================
    # PAGE SETTINGS (Optimized for Fixed Header Layout)
    # =========================================================
    page.title = "Metarere Kavakuru - Civil Engineering Portfolio"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#faf5ff"
    page.scroll = None

    # =========================================================
    # CIVIL ENGINEERING LIGHT BROWN PALETTE
    # =========================================================
    PRIMARY_BROWN = "#8B5A2B"      # Warm brown
    ACCENT_TAN = "#D2B48C"         # Tan/light brown
    DEEP_CLAY = "#A0522D"          # Sienna/deep brown
    LIGHT_BG = "#FFF8F0"           # Warm off-white
    SECTION_BG = "#FDF5E6"         # Old lace
    SECTION_DEEP = "#FAEBD7"       # Antique white
    BG_WHITE = "#FFFFFF"
    TEXT_GREY = "#5C4033"          # Dark brown-grey
    AVATAR_BG = "#F5DEB3"          # Wheat
    SUBTEXT_GREY = "#A0522D"       # Sienna
    CARD_BG = "#FFFFFF"
    BORDER_COLOR = "#DEB887"       # Burlywood
    
    DARK_CARD_BG = "#8B5A2B"       # Warm brown
    DARK_TEXT_WHITE = "#FFFFFF"
    NAV_INACTIVE = "#D2B48C"       # Tan
    OVERLAY_BROWN = "#CD853F"      # Peru
    PROGRESS_TRACK = "#F5DEB3"     # Wheat
    SHADOW_BROWN = "#D2B48C"       # Tan
    CERT_HINT = "#FAEBD7"          # Antique white

    def open_certificate_zoom(title: str, image_file: str):
        zoom_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, color=PRIMARY_BROWN, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=900,
                height=620,
                bgcolor=BG_WHITE,
                padding=10,
                border_radius=8,
                content=ft.Image(src=f"/images/{image_file}", fit="contain"),
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_certificate_zoom(zoom_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(zoom_dialog)

    def close_certificate_zoom(dialog):
        page.close(dialog)

    def get_uniform_border(width: int, color: str):
        return ft.Border(
            top=ft.BorderSide(width, color),
            bottom=ft.BorderSide(width, color),
            left=ft.BorderSide(width, color),
            right=ft.BorderSide(width, color),
        )

    # =========================================================
    # PREMIUM COMPONENT BUILDERS
    # =========================================================
    def create_section_header(title: str, subtitle: str):
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    title, 
                    size=28, 
                    weight=ft.FontWeight.BOLD, 
                    color=PRIMARY_BROWN, 
                    style=ft.TextStyle(letter_spacing=1.2)
                ),
                ft.Text(subtitle, size=15, color=TEXT_GREY),
                ft.Container(height=4, width=60, bgcolor=ACCENT_TAN, border_radius=2),
                ft.Container(height=15)
            ]
        )

    def create_skill_chip(label: str, level: float):
        return ft.Container(
            bgcolor=BG_WHITE,
            padding=ft.Padding(16, 12, 16, 12),
            border_radius=8,
            border=get_uniform_border(1, BORDER_COLOR),
            content=ft.Column([
                ft.Row([
                    ft.Text(label, weight=ft.FontWeight.W_600, color=DEEP_CLAY, size=14),
                    ft.Text(f"{int(level*100)}%", weight=ft.FontWeight.BOLD, color=PRIMARY_BROWN, size=12)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=6),
                ft.Stack([
                    ft.Container(height=4, bgcolor=PROGRESS_TRACK, border_radius=2, expand=True),
                    ft.Container(height=4, bgcolor=PRIMARY_BROWN, border_radius=2, width=120 * level)
                ])
            ])
        )

    def create_info_card(title: str, body: str, icon=ft.Icons.CHECK_CIRCLE):
        return ft.Container(
            bgcolor=BG_WHITE,
            padding=20,
            border_radius=8,
            border=get_uniform_border(1, BORDER_COLOR),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row([
                        ft.Icon(icon, color=PRIMARY_BROWN, size=24),
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                    ]),
                    ft.Text(body, color=TEXT_GREY, size=13),
                ],
            ),
        )

    def create_stat_card(value: str, label: str, icon: str, sublabel: str = ""):
        return ft.Container(
            bgcolor=BG_WHITE,
            padding=ft.Padding(16, 12, 16, 12),
            border_radius=10,
            border=get_uniform_border(1, BORDER_COLOR),
            content=ft.Column(
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, color=PRIMARY_BROWN, size=32),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                    ft.Text(label, size=12, weight=ft.FontWeight.W_500, color=DEEP_CLAY),
                    ft.Text(sublabel, size=10, color=SUBTEXT_GREY) if sublabel else ft.Container(),
                ]
            )
        )

    # =========================================================
    # NAVIGATION SYSTEM
    # =========================================================
    current_page_key = {"value": "overview"}
    nav_buttons = {}

    def build_page_view(section_control, page_key):
        return ft.Column(
            key=f"page-{page_key}",
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            spacing=0,
            controls=[section_control],
        )

    def navigate_to(page_key):
        current_page_key["value"] = page_key
        page_switcher.content = build_page_view(portfolio_pages[page_key], page_key)
        for key, button in nav_buttons.items():
            button.style = ft.ButtonStyle(
                color=BG_WHITE if key == page_key else NAV_INACTIVE,
                overlay_color=OVERLAY_BROWN,
            )
        page.update()

    # =========================================================
    # SECTIONS DEFINITIONS
    # =========================================================
    
    # 1. Overview Section
    hero_section = ft.Container(
        key="overview",
        bgcolor=LIGHT_BG,
        padding=ft.Padding(50, 60, 50, 60),
        content=ft.Column([
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        col={"sm": 12, "md": 7},
                        spacing=20,
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "CIVIL ENGINEERING STUDENT @ UNAM", 
                                    size=12, 
                                    weight=ft.FontWeight.W_600, 
                                    color=ACCENT_TAN, 
                                    style=ft.TextStyle(letter_spacing=1.5)
                                ),
                                bgcolor=BG_WHITE,
                                padding=ft.Padding(12, 6, 12, 6),
                                border_radius=20,
                            ),
                            ft.Text("Metarere Kavakuru", size=44, weight=ft.FontWeight.BOLD, color=PRIMARY_BROWN),
                            ft.Text(
                                "Dedicated civil engineering student specializing in structural analysis, geotechnical engineering, and sustainable infrastructure development. Passionate about creating resilient and eco-friendly construction solutions for modern challenges.",
                                size=16, color=TEXT_GREY,
                            ),
                            ft.Divider(color=BORDER_COLOR, thickness=1),
                            ft.Row(
                                spacing=20,
                                controls=[
                                    ft.Column(spacing=5, controls=[
                                        ft.Text("PHONE", size=10, color=SUBTEXT_GREY, weight=ft.FontWeight.BOLD),
                                        ft.Text("+264 81 811 0602", size=14, weight=ft.FontWeight.W_500, color=DEEP_CLAY),
                                    ]),
                                    ft.Column(spacing=5, controls=[
                                        ft.Text("EMAIL", size=10, color=SUBTEXT_GREY, weight=ft.FontWeight.BOLD),
                                        ft.Text("kavakurum@gmail.com", size=14, weight=ft.FontWeight.W_500, color=DEEP_CLAY),
                                    ]),
                                    ft.Column(spacing=5, controls=[
                                        ft.Text("GITHUB", size=10, color=SUBTEXT_GREY, weight=ft.FontWeight.BOLD),
                                        ft.Text("@Kavakuru-Metarere7", size=14, weight=ft.FontWeight.W_500, color=DEEP_CLAY),
                                    ]),
                                ]
                            ),
                            ft.Row(
                                spacing=15,
                                controls=[
                                    ft.ElevatedButton(
                                        "Download CV",
                                        icon=ft.Icons.DOWNLOAD,
                                        bgcolor=PRIMARY_BROWN,
                                        color=BG_WHITE,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    ),
                                    ft.OutlinedButton(
                                        "GitHub Portfolio",
                                        icon=ft.Icons.CODE,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            side=ft.BorderSide(1, PRIMARY_BROWN),
                                            color=PRIMARY_BROWN,
                                        ),
                                        url="https://github.com/Kavakuru-Metarere7",
                                    ),
                                    ft.OutlinedButton(
                                        "SiteSpy Project",
                                        icon=ft.Icons.BUILD,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            side=ft.BorderSide(1, ACCENT_TAN),
                                            color=ACCENT_TAN,
                                        ),
                                        url="https://github.com/Kavakuru-Metarere7/KavakuruMetarerePortfolio",
                                    ),
                                ]
                            ),
                        ],
                    ),
                    ft.Column(
                        col={"sm": 12, "md": 5},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=220,
                                height=220,
                                border_radius=110,
                                bgcolor=AVATAR_BG,
                                border=get_uniform_border(4, PRIMARY_BROWN),
                                content=ft.Image(src="/images/Profile.jpeg", width=220, height=220, border_radius=110, fit="cover"),
                            ),
                        ],
                    ),
                ]
            ),
            ft.Container(height=20),
            # Stats Row
            ft.ResponsiveRow(
                spacing=15,
                controls=[
                    ft.Container(col={"sm": 6, "md": 3}, content=create_stat_card("12+", "MATLAB Certificates", ft.Icons.SCHOOL, "MathWorks Certified")),
                    ft.Container(col={"sm": 6, "md": 3}, content=create_stat_card("35+", "GitHub Commits", ft.Icons.COMMIT, "Active Contributor")),
                    ft.Container(col={"sm": 6, "md": 3}, content=create_stat_card("6", "Major Projects", ft.Icons.ENGINEERING, "Completed")),
                    ft.Container(col={"sm": 6, "md": 3}, content=create_stat_card("3", "Research Papers", ft.Icons.DESCRIPTION, "Under Review")),
                ]
            ),
            ft.Container(height=20),
            # Professional Highlights Row
            ft.ResponsiveRow(
                spacing=15,
                controls=[
                    ft.Container(
                        col={"sm": 12, "md": 4},
                        bgcolor=BG_WHITE,
                        padding=18,
                        border_radius=10,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.STAR, color=ACCENT_TAN, size=28),
                                ft.Text("Top Student", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Structural Design", size=12, color=TEXT_GREY),
                                ft.Container(height=2, width=40, bgcolor=ACCENT_TAN),
                                ft.Text("Awarded for outstanding performance in advanced structural analysis and design.", size=11, color=SUBTEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 4},
                        bgcolor=BG_WHITE,
                        padding=18,
                        border_radius=10,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.SCIENCE, color=ACCENT_TAN, size=28),
                                ft.Text("Research Assistant", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Sustainable Materials", size=12, color=TEXT_GREY),
                                ft.Container(height=2, width=40, bgcolor=ACCENT_TAN),
                                ft.Text("Investigating alternative eco-friendly construction materials for low-cost housing.", size=11, color=SUBTEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 4},
                        bgcolor=BG_WHITE,
                        padding=18,
                        border_radius=10,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.VOLUNTEER_ACTIVISM, color=ACCENT_TAN, size=28),
                                ft.Text("Community Service", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Engineering Outreach", size=12, color=TEXT_GREY),
                                ft.Container(height=2, width=40, bgcolor=ACCENT_TAN),
                                ft.Text("Led a team of 10 students in a community bridge assessment and repair project.", size=11, color=SUBTEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    ),
                ]
            ),
            ft.Container(height=20),
            # About Me Section
            ft.Container(
                bgcolor=BG_WHITE,
                padding=25,
                border_radius=12,
                border=get_uniform_border(1, BORDER_COLOR),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Text("📖 About Me", size=20, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                        ft.Text(
                            "I am a dedicated Civil Engineering student at the University of Namibia, passionate about developing sustainable infrastructure and innovative construction solutions. "
                            "My academic journey has equipped me with strong fundamentals in structural design, geotechnical analysis, and construction management, while my technical skills in AutoCAD, Revit, and Python enable me to create data-driven solutions for real-world engineering challenges.",
                            size=14, color=TEXT_GREY,
                        ),
                        ft.Text(
                            "I am actively seeking internship opportunities and research collaborations in the civil engineering industry, particularly in areas of structural engineering, geotechnical investigations, and sustainable construction practices.",
                            size=14, color=TEXT_GREY,
                        ),
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Container(
                                    content=ft.Text("🏆 Top Performer - Structural Design", size=12, color=DEEP_CLAY),
                                    bgcolor=LIGHT_BG,
                                    padding=ft.Padding(12, 6, 12, 6),
                                    border_radius=15,
                                ),
                                ft.Container(
                                    content=ft.Text("🎓 Dean's List 2024", size=12, color=DEEP_CLAY),
                                    bgcolor=LIGHT_BG,
                                    padding=ft.Padding(12, 6, 12, 6),
                                    border_radius=15,
                                ),
                                ft.Container(
                                    content=ft.Text("📐 AutoCAD Certified", size=12, color=DEEP_CLAY),
                                    bgcolor=LIGHT_BG,
                                    padding=ft.Padding(12, 6, 12, 6),
                                    border_radius=15,
                                ),
                            ]
                        ),
                    ]
                )
            ),
            ft.Container(height=20),
            # Core Competencies Section
            ft.Container(
                bgcolor=SECTION_BG,
                padding=25,
                border_radius=12,
                border=get_uniform_border(1, BORDER_COLOR),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Row([
                            ft.Icon(ft.Icons.APP_REGISTRATION, color=PRIMARY_BROWN, size=24),
                            ft.Text("Core Competencies", size=20, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                        ]),
                        ft.ResponsiveRow(
                            spacing=10,
                            controls=[
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("🏗️ Structural Analysis", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("📐 AutoCAD/Revit", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("🌱 Sustainable Design", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("📊 Project Management", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("🧪 Material Testing", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("📈 Cost Estimation", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("🔬 Soil Mechanics", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                                ft.Container(col={"sm": 6, "md": 3}, content=ft.Container(
                                    content=ft.Text("📋 Site Supervision", size=13, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                                    bgcolor=BG_WHITE, padding=10, border_radius=8, border=get_uniform_border(1, BORDER_COLOR)
                                )),
                            ]
                        )
                    ]
                )
            ),
            ft.Container(height=20),
            # Core Values Section
            ft.ResponsiveRow(
                spacing=15,
                controls=[
                    ft.Container(
                        col={"sm": 12, "md": 4},
                        bgcolor=BG_WHITE,
                        padding=20,
                        border_radius=10,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.LIGHTBULB, color=ACCENT_TAN, size=32),
                                ft.Text("Innovation", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Applying cutting-edge technology to solve traditional civil engineering challenges.", size=12, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 4},
                        bgcolor=BG_WHITE,
                        padding=20,
                        border_radius=10,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.FAVORITE, color=ACCENT_TAN, size=32),
                                ft.Text("Sustainability", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Committed to environmentally responsible infrastructure development and construction.", size=12, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 4},
                        bgcolor=BG_WHITE,
                        padding=20,
                        border_radius=10,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.TRENDING_UP, color=ACCENT_TAN, size=32),
                                ft.Text("Excellence", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Striving for the highest standards in academic and professional engineering work.", size=12, color=TEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    ),
                ]
            ),
            ft.Container(height=20),
            # Call to Action Section
            ft.Container(
                bgcolor=PRIMARY_BROWN,
                padding=30,
                border_radius=12,
                content=ft.Column(
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Ready to Build the Future Together?", size=22, weight=ft.FontWeight.BOLD, color=BG_WHITE),
                        ft.Text("I'm always open to discussing new projects, research opportunities, or internships.", size=14, color=CERT_HINT, text_align=ft.TextAlign.CENTER),
                        ft.Row(
                            spacing=15,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    "Contact Me",
                                    icon=ft.Icons.EMAIL,
                                    bgcolor=BG_WHITE,
                                    color=PRIMARY_BROWN,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                    on_click=lambda e: navigate_to("contact"),
                                ),
                                ft.OutlinedButton(
                                    "View My Work",
                                    icon=ft.Icons.WORK,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        side=ft.BorderSide(1, BG_WHITE),
                                        color=BG_WHITE,
                                    ),
                                    on_click=lambda e: navigate_to("projects"),
                                ),
                            ]
                        )
                    ]
                )
            ),
        ])
    )

    # 2. Skills Section
    skills_section = ft.Container(
        key="skills",
        bgcolor=SECTION_BG,
        padding=40,
        content=ft.Column([
            create_section_header("CORE CIVIL ENGINEERING & TECHNICAL MATRIX", "Integrated expertise across structural, geotechnical, and construction management."),
            ft.ResponsiveRow([
                ft.Column(col={"sm": 12, "md": 4}, spacing=10, controls=[
                    ft.Text("Structural Engineering", weight=ft.FontWeight.BOLD, color=ACCENT_TAN, size=16),
                    create_skill_chip("Structural Analysis", 0.88),
                    create_skill_chip("Reinforced Concrete Design", 0.85),
                    create_skill_chip("Steel Structure Design", 0.82),
                ]),
                ft.Column(col={"sm": 12, "md": 4}, spacing=10, controls=[
                    ft.Text("Geotechnical Engineering", weight=ft.FontWeight.BOLD, color=ACCENT_TAN, size=16),
                    create_skill_chip("Soil Mechanics", 0.85),
                    create_skill_chip("Foundation Design", 0.80),
                    create_skill_chip("Slope Stability", 0.78),
                ]),
                ft.Column(col={"sm": 12, "md": 4}, spacing=10, controls=[
                    ft.Text("Digital & Construction Tools", weight=ft.FontWeight.BOLD, color=ACCENT_TAN, size=16),
                    create_skill_chip("AutoCAD & Revit", 0.88),
                    create_skill_chip("Civil 3D", 0.82),
                    create_skill_chip("Project Management", 0.80),
                ]),
            ], spacing=20)
        ])
    )

    # 3. Individual Portfolio Reflection Section
    contribution_section = ft.Container(
        key="contribution",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("INDIVIDUAL CONTRIBUTION PORTFOLIO", "Reflection, evidence, lessons learned, challenges, and showcase material."),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "Semester Project Contribution (SiteSpy)",
                                "I contributed to the authentication screens and flow between login, registration, and password recovery for the SiteSpy construction support app. My work focused on presenting a clear split-layout case study without implementation clutter.",
                                ft.Icons.ENGINEERING,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "Evidence of Work",
                                "This portfolio includes authentication flow documentation, design system notes, implementation notes, and clear explanations of how the entry screens build trust for the construction support application.",
                                ft.Icons.FACT_CHECK,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "What I Learned",
                                "I learned how entry screens shape user trust and how clear account flows support a practical mobile app for construction professionals. I strengthened my ability to translate design requirements into functional UI flows.",
                                ft.Icons.LIGHTBULB,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=create_info_card(
                                "Challenges Addressed",
                                "The main challenge was presenting authentication flow without implementation clutter. The solution was a clear split-layout case study that focuses on user experience and flow clarity.",
                                ft.Icons.TROUBLESHOOT,
                            ),
                        ),
                    ],
                ),
                ft.Container(
                    bgcolor=LIGHT_BG,
                    padding=20,
                    border_radius=8,
                    border=get_uniform_border(1, BORDER_COLOR),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column([
                                ft.Text("Individual Contribution Video", size=18, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Watch the final showcase recording of my individual contribution to the SiteSpy project.", color=TEXT_GREY, size=13),
                            ]),
                            ft.TextButton("Watch Video", icon=ft.Icons.VIDEO_LIBRARY, url="https://drive.google.com/drive/folders/1m2OSdE8WwZKpmWNR-2WS2pAwwpySQRk1?usp=sharing", style=ft.ButtonStyle(color=ACCENT_TAN)),
                        ],
                    ),
                ),
            ],
        ),
    )

    # 4. Project Timeline Section
    timeline_section = ft.Container(
        key="timeline",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("PROJECT TIMELINE", "Weekly log of my specific contributions to the semester group project."),
                ft.Container(
                    bgcolor=BG_WHITE,
                    padding=25,
                    border_radius=10,
                    border=get_uniform_border(1, BORDER_COLOR),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Text("Week 1-2 - Requirements Analysis and Authentication Research", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ft.Text("Reviewed the SiteSpy project brief, analyzed user requirements for authentication, researched best practices for login/registration flows, and documented the screen structure I would implement. Initial project setup and design system planning.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Week 3-4 - Wireframing and Split-Layout Design", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ft.Text("Designed wireframes for authentication screens and created a split-layout approach that separates visual branding from form inputs. Established consistent spacing and typography guidelines.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Week 5-6 - Login Screen Implementation", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ft.Text("Implemented the login screen with email/phone input, password field, remember me functionality, and proper validation handling. Integrated visual assets and maintained responsive behavior.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Week 7-8 - Registration Flow and Password Recovery", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ft.Text("Built complete registration flow with multi-step form handling and password recovery interface with email reset functionality. Ensured smooth transitions between auth states.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Week 9-10 - User Testing and Flow Optimization", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ft.Text("Conducted user testing sessions, gathered feedback on authentication experience, and optimized flow based on usability findings. Fixed edge cases and improved error messaging.", color=TEXT_GREY),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Text("Final Week - Documentation and Portfolio Integration", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ft.Text("Finalized all authentication components, documented design decisions, and integrated everything into the project portfolio. Prepared case study materials and final presentation.", color=TEXT_GREY),
                        ],
                    ),
                ),
            ],
        ),
    )

    # 5. Projects Section
    project_section = ft.Container(
        key="projects",
        bgcolor=BG_WHITE,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("CIVIL ENGINEERING PROJECTS", "Advanced design and analysis tools for infrastructure development."),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=CARD_BG,
                            padding=25,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row([ft.Icon(ft.Icons.BUILD, color=PRIMARY_BROWN, size=24), ft.Text("SiteSpy - Construction Support App", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN)]),
                                    ft.Text("A construction support mobile application that keeps project records, helps with wall measurements and material estimation, and prepares information for later review. The app streamlines on-site data collection and reporting.", color=TEXT_GREY, size=14),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=12,
                                        border_radius=6,
                                        content=ft.Column([
                                            ft.Text("SITESPY CORE FEATURES:", size=11, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                            ft.Text("• Authentication with login, registration, and password recovery", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Wall measurement tools for accurate material estimation", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Project record keeping with cloud synchronization", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Data preparation for later review and reporting", size=12, font_family="monospace", color=ACCENT_TAN),
                                        ])
                                    ),
                                    ft.Text("As a key contributor to this project, I focused on the authentication screens and flow between login, registration, and password recovery. The split-layout approach creates a clear, user-friendly experience.", color=TEXT_GREY, size=12),
                                    ft.Row([
                                        ft.Container(content=ft.Text("React Native", size=11, color=BG_WHITE), bgcolor=PRIMARY_BROWN, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("Firebase Auth", size=11, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("Expo", size=11, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=5, border_radius=4),
                                    ]),
                                    ft.Row(alignment=ft.MainAxisAlignment.START, controls=[
                                        ft.TextButton("View Live Portfolio", icon=ft.Icons.WEB, url="https://Kavakuru-Metarere7.github.io/KavakuruMetarerePortfolio/", style=ft.ButtonStyle(color=ACCENT_TAN)),
                                        ft.TextButton("View Repository", icon=ft.Icons.CODE, url="https://github.com/Kavakuru-Metarere7/KavakuruMetarerePortfolio", style=ft.ButtonStyle(color=ACCENT_TAN)),
                                    ])
                                ],
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=CARD_BG,
                            padding=25,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("1. Structural Load Calculator", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                                    ft.Text("Web-based structural load calculator for determining dead loads, live loads, and load combinations according to building codes.", color=TEXT_GREY, size=14),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=12,
                                        border_radius=6,
                                        content=ft.Column([
                                            ft.Text("STRUCTURAL CORE FORMULAS:", size=11, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                            ft.Text("• Dead Load: DL = γ × Volume", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Live Load: LL = occupancy × area factor", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Ultimate Load: UL = 1.2DL + 1.6LL", size=12, font_family="monospace", color=ACCENT_TAN),
                                        ])
                                    ),
                                    ft.Text("Helps structural engineers quickly compute loads for beams, columns, and foundations, ensuring code-compliant designs.", color=TEXT_GREY, size=12),
                                    ft.Row([
                                        ft.Container(content=ft.Text("JavaScript", size=11, color=BG_WHITE), bgcolor=PRIMARY_BROWN, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("HTML/CSS", size=11, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=5, border_radius=4),
                                    ])
                                ],
                            ),
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=CARD_BG,
                            padding=25,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("2. Foundation Design Tool", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                                    ft.Text("Geotechnical analysis tool for shallow foundation design, including bearing capacity calculations and settlement predictions based on soil properties.", color=TEXT_GREY, size=14),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=12,
                                        border_radius=6,
                                        content=ft.Column([
                                            ft.Text("FOUNDATION CORE EQUATIONS:", size=11, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                            ft.Text("• Terzaghi's Bearing Capacity: q_ult = cN_c + γDN_q + 0.5γBN_γ", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Settlement: S = qB(1-μ²) I / E", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Safety Factor: FS = q_ult / q_app", size=12, font_family="monospace", color=ACCENT_TAN),
                                        ])
                                    ),
                                    ft.Text("Assists geotechnical engineers in determining foundation dimensions and verifying safety against bearing failure and excessive settlement.", color=TEXT_GREY, size=12),
                                    ft.Row([
                                        ft.Container(content=ft.Text("Python", size=11, color=BG_WHITE), bgcolor=PRIMARY_BROWN, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("NumPy", size=11, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=5, border_radius=4),
                                    ])
                                ],
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=CARD_BG,
                            padding=25,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("3. Material Estimation Suite", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                                    ft.Text("Comprehensive material quantity calculator for concrete, steel reinforcement, and formwork based on structural drawings and dimensions.", color=TEXT_GREY, size=14),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=12,
                                        border_radius=6,
                                        content=ft.Column([
                                            ft.Text("ESTIMATION FORMULAS:", size=11, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                            ft.Text("• Concrete Volume: V = Length × Width × Depth", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Rebar Weight: W = (A_s × L) × ρ_steel", size=12, font_family="monospace", color=ACCENT_TAN),
                                            ft.Text("• Formwork Area: A = 2 × (L + W) × D", size=12, font_family="monospace", color=ACCENT_TAN),
                                        ])
                                    ),
                                    ft.Text("Helps construction estimators and civil engineers calculate accurate material quantities for cost estimation and procurement planning.", color=TEXT_GREY, size=12),
                                    ft.Row([
                                        ft.Container(content=ft.Text("React", size=11, color=BG_WHITE), bgcolor=PRIMARY_BROWN, padding=5, border_radius=4),
                                        ft.Container(content=ft.Text("Node.js", size=11, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=5, border_radius=4),
                                    ])
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    # 6. Technical Blog Section - WITH VIDEO
    blog_section = ft.Container(
        key="blog",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("TECHNICAL BLOG: CONFIDENCE IN CONCEPTS", "Written technical explanations with embedded video showcase."),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=22,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("Reinforced Concrete Beam Design", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                                    ft.Text("The design of reinforced concrete beams involves calculating the required steel reinforcement to resist bending moments and shear forces while satisfying serviceability requirements.", color=TEXT_GREY, size=13),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=14,
                                        border_radius=6,
                                        content=ft.Text("M_n = A_s × f_y × (d - a/2)", font_family="monospace", size=14, color=PRIMARY_BROWN),
                                    ),
                                    ft.Text("Where M_n is the nominal moment capacity, A_s is the area of steel reinforcement, f_y is the yield strength, d is the effective depth, and a is the depth of the compression block.", color=TEXT_GREY, size=13),
                                    ft.TextButton("Watch Explanation", icon=ft.Icons.PLAY_CIRCLE, style=ft.ButtonStyle(color=ACCENT_TAN)),
                                ],
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=22,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Text("Soil Bearing Capacity and Settlement", size=18, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                                    ft.Text("The bearing capacity of soil determines how much load the ground can safely support. Terzaghi's bearing capacity equation is fundamental for shallow foundation design.", color=TEXT_GREY, size=13),
                                    ft.Container(
                                        bgcolor=LIGHT_BG,
                                        padding=14,
                                        border_radius=6,
                                        content=ft.Text("q_ult = cN_c + γDN_q + 0.5γBN_γ", font_family="monospace", size=14, color=PRIMARY_BROWN),
                                    ),
                                    ft.Text("q_ult is the ultimate bearing capacity, c is cohesion, γ is unit weight, D is depth, B is width, and N_c, N_q, N_γ are bearing capacity factors.", color=TEXT_GREY, size=13),
                                    ft.TextButton("Watch Explanation", icon=ft.Icons.PLAY_CIRCLE, style=ft.ButtonStyle(color=ACCENT_TAN)),
                                ],
                            ),
                        ),
                    ],
                ),
                
                # Video Showcase Section
                ft.Container(
                    bgcolor=BG_WHITE,
                    padding=25,
                    border_radius=10,
                    border=get_uniform_border(1, BORDER_COLOR),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Row([
                                ft.Icon(ft.Icons.VIDEO_LIBRARY, color=PRIMARY_BROWN, size=32),
                                ft.Text("Project Showcase Video", size=20, weight=ft.FontWeight.BOLD, color=ACCENT_TAN),
                            ]),
                            ft.Divider(color=BORDER_COLOR),
                            ft.Container(
                                height=400,
                                width=None,
                                bgcolor="#000000",
                                border_radius=8,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=fv.Video(
                                    expand=True,
                                    playlist=[fv.VideoMedia("/video/video.mp4")],
                                    playlist_mode=fv.PlaylistMode.LOOP,
                                    fill_color=PRIMARY_BROWN,
                                    aspect_ratio=16/9,
                                    volume=100,
                                    autoplay=False,
                                    show_controls=True,
                                    filter_quality=ft.FilterQuality.HIGH,
                                    muted=False,
                                    wakelock=True,
                                ),
                            ),
                            ft.Text(
                                "Watch this video to see my individual contribution to the SiteSpy project, including key features, technical challenges, and team collaboration highlights.",
                                size=13,
                                color=TEXT_GREY,
                                italic=True,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    # 7. Experience / Leadership Section
    leadership_section = ft.Container(
        key="experience",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("CIVIL ENGINEERING LEADERSHIP & FIELD EXPERIENCE", "Active contributions to the civil engineering community and practical construction exposure."),
                ft.Text("Bridging academic civil engineering theory with practical construction industry applications while mentoring aspiring engineers.", size=15, color=TEXT_GREY),
                ft.ResponsiveRow(
                    spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column([
                                ft.Icon(ft.Icons.GROUP, color=PRIMARY_BROWN, size=28),
                                ft.Text("Civil Engineering Society Member", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Contributing to student-led workshops, industry guest lectures, and site visit coordination with local construction and engineering firms.", color=TEXT_GREY, size=13),
                            ])
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=8,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column([
                                ft.Icon(ft.Icons.BUILD, color=PRIMARY_BROWN, size=28),
                                ft.Text("Intern - Construction Site", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                ft.Text("Site surveying, material testing, quality control, concrete sampling, and assisting senior engineers with project documentation and site supervision.", color=TEXT_GREY, size=13),
                            ])
                        ),
                    ]
                )
            ]
        )
    )

    # 8. Certificate Section
    certificate_data = [
        {"title": "Calculations with Vectors and Matrices", "file": "Calculations with Vectors and Matrices.jpeg"},
        {"title": "Explore Data with MATLAB Plots", "file": "Explore Data with MATLAB Plots.jpeg"},
        {"title": "Machine Learning Onramp", "file": "Machine Learning Onramp.jpeg"},
        {"title": "Make and Manipulate Matrices", "file": "Make and Manipulate Matrices.jpeg"},
        {"title": "MATLAB Desktop Tools and Troubleshooting Scripts", "file": "MATLAB Desktop Tools and Troubleshooting Scripts.jpeg"},
        {"title": "MATLAB Onramp", "file": "MATLAB Onramp.jpeg"},
        {"title": "Simulink Onramp", "file": "Simulink Onramp.jpeg"},
        {"title": "The How and Why of Writing Functions", "file": "The How and Why of Writting Functions.jpeg"},
    ]

    cert_cards = []
    for cert in certificate_data:
        img_control = ft.Image(
            src=f"/images/{cert['file']}",
            height=150,
            fit="contain", 
            scale=1.0,
            animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
        )

        card_design = ft.Container(
            bgcolor=DARK_CARD_BG,
            padding=15,
            border_radius=10,
            border=get_uniform_border(1, ACCENT_TAN),
            on_click=lambda e, title=cert["title"], file=cert["file"]: open_certificate_zoom(title, file),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=150,
                        width=320,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        border_radius=6,
                        bgcolor=BG_WHITE,
                        content=img_control,
                    ),
                    ft.Container(height=6),
                    ft.Text(cert["title"], weight=ft.FontWeight.BOLD, color=DARK_TEXT_WHITE, text_align=ft.TextAlign.CENTER, size=13, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text("Click to zoom", color=CERT_HINT, size=11, text_align=ft.TextAlign.CENTER),
                ],
            ),
        )

        hover_stack = ft.Stack(
            height=230,
            controls=[
                ft.Container(top=10, left=0, right=0, animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT), content=card_design)
            ]
        )

        def make_hover_handler(stack_wrapper, target_img):
            inner_move_container = stack_wrapper.controls[0]
            def handle_hover(e):
                if e.data == "true":
                    inner_move_container.top = 0  
                    inner_move_container.shadow = ft.BoxShadow(blur_radius=12, color=ACCENT_TAN)
                    target_img.scale = 1.05  
                else:
                    inner_move_container.top = 10  
                    inner_move_container.shadow = None
                    target_img.scale = 1.0
                inner_move_container.update()
                target_img.update()
            return handle_hover

        card_design.on_hover = make_hover_handler(hover_stack, img_control)
        cert_cards.append(ft.Container(col={"sm": 12, "md": 6, "lg": 4}, content=hover_stack))

    certification_section = ft.Container(
        key="certificates",
        bgcolor=SECTION_DEEP,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                create_section_header("MATLAB ACHIEVEMENT HUB", "Proof of completion for short self-paced courses from the MathWorks Learning Center."),
                ft.Text("Click any certificate to zoom in and inspect the completion proof clearly.", size=13, color=SUBTEXT_GREY),
                ft.ResponsiveRow(spacing=20, run_spacing=10, controls=cert_cards),
            ],
        ),
    )

    # 9. GitHub Evidence & Documentation Section
    github_section = ft.Container(
        key="github",
        bgcolor=LIGHT_BG,
        padding=40,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("GITHUB EVIDENCE & DOCUMENTATION", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_BROWN),
                            ft.Text("Verifiable individual contribution records for the SiteSpy semester project.", size=15, color=TEXT_GREY),
                        ]),
                        ft.IconButton(icon=ft.Icons.CODE, icon_color=PRIMARY_BROWN, tooltip="GitHub Evidence")
                    ]
                ),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=create_info_card(
                                "Commit History",
                                "Authentication screens implementation commits showing login, registration, and password recovery components with clear commit messages and timestamps.",
                                ft.Icons.COMMIT,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=create_info_card(
                                "Repository Structure",
                                "Well-organized portfolio repository with clear documentation, implementation notes, and case study materials for the SiteSpy authentication flow.",
                                ft.Icons.FOLDER_SPECIAL,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=create_info_card(
                                "Impact Summary",
                                "My authentication screens provide a clean, user-friendly entry point that builds trust and supports the practical needs of construction professionals using the app.",
                                ft.Icons.INSIGHTS,
                            ),
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row([ft.Icon(ft.Icons.FOLDER_SPECIAL, color=PRIMARY_BROWN), ft.Text("KavakuruMetarerePortfolio", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY)]),
                                    ft.Text("This portfolio showcases my work on the SiteSpy construction support app, with a focus on authentication screens and user flow design. It demonstrates my ability to create clean, usable interfaces.", size=13, color=TEXT_GREY),
                                    ft.Row(wrap=True, spacing=5, controls=[
                                        ft.Container(content=ft.Text("HTML/CSS", size=10, color=BG_WHITE), bgcolor=PRIMARY_BROWN, padding=4, border_radius=4),
                                        ft.Container(content=ft.Text("JavaScript", size=10, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=4, border_radius=4),
                                        ft.Container(content=ft.Text("GitHub Pages", size=10, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=4, border_radius=4),
                                    ]),
                                    ft.Divider(color=BORDER_COLOR),
                                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                        ft.Text("Live Portfolio", size=11, color=SUBTEXT_GREY),
                                        ft.TextButton("View Live", url="https://Kavakuru-Metarere7.github.io/KavakuruMetarerePortfolio/", style=ft.ButtonStyle(color=ACCENT_TAN))
                                    ])
                                ]
                            )
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            bgcolor=BG_WHITE,
                            padding=20,
                            border_radius=10,
                            border=get_uniform_border(1, BORDER_COLOR),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row([ft.Icon(ft.Icons.CODE, color=PRIMARY_BROWN), ft.Text("Authentication Flow Demo", size=16, weight=ft.FontWeight.BOLD, color=DEEP_CLAY)]),
                                    ft.Text("Interactive demonstration of the authentication flow including login, registration, and password recovery screens with smooth transitions and validation.", size=13, color=TEXT_GREY),
                                    ft.Row(wrap=True, spacing=5, controls=[
                                        ft.Container(content=ft.Text("React Native", size=10, color=BG_WHITE), bgcolor=PRIMARY_BROWN, padding=4, border_radius=4),
                                        ft.Container(content=ft.Text("Expo", size=10, color=DEEP_CLAY), bgcolor=LIGHT_BG, padding=4, border_radius=4),
                                    ]),
                                    ft.Divider(color=BORDER_COLOR),
                                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                        ft.Text("Case Study", size=11, color=SUBTEXT_GREY),
                                        ft.TextButton("View Demo", style=ft.ButtonStyle(color=ACCENT_TAN))
                                    ])
                                ]
                            )
                        ),
                    ],
                ),
            ],
        ),
    )

    # 10. Contact Section
    name_field = ft.TextField(
        label="Your Full Name", 
        border_color=PRIMARY_BROWN, 
        focused_border_color=ACCENT_TAN,
        bgcolor=BG_WHITE,
        prefix_icon=ft.Icons.PERSON,
    )
    email_field = ft.TextField(
        label="Email Address", 
        border_color=PRIMARY_BROWN, 
        focused_border_color=ACCENT_TAN,
        bgcolor=BG_WHITE,
        prefix_icon=ft.Icons.EMAIL,
    )
    subject_field = ft.TextField(
        label="Subject", 
        border_color=PRIMARY_BROWN, 
        focused_border_color=ACCENT_TAN,
        bgcolor=BG_WHITE,
        prefix_icon=ft.Icons.CHAT,
    )
    message_field = ft.TextField(
        label="Your Message", 
        multiline=True, 
        min_lines=5, 
        border_color=PRIMARY_BROWN, 
        focused_border_color=ACCENT_TAN,
        bgcolor=BG_WHITE,
        prefix_icon=ft.Icons.MESSAGE,
    )

    def handle_submit_message(e):
        if not name_field.value or not email_field.value:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Please fill out your Name and Email fields before submitting."), bgcolor=ACCENT_TAN))
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"✨ Thank you {name_field.value}! Your message has been sent successfully. I'll get back to you soon! ✨"), bgcolor=PRIMARY_BROWN))
            name_field.value = ""
            email_field.value = ""
            subject_field.value = ""
            message_field.value = ""
            page.update()

    contact_section = ft.Container(
        key="contact",
        bgcolor=SECTION_DEEP,
        padding=ft.Padding(40, 60, 40, 60),
        content=ft.Column([
            create_section_header("LET'S CONNECT", "Have a project in mind? Let's collaborate!"),
            
            ft.ResponsiveRow(
                spacing=30,
                controls=[
                    # Left Column - Contact Info & Social
                    ft.Column(
                        col={"sm": 12, "md": 5},
                        spacing=25,
                        controls=[
                            ft.Container(
                                bgcolor=BG_WHITE,
                                padding=30,
                                border_radius=20,
                                border=get_uniform_border(1, BORDER_COLOR),
                                content=ft.Column(
                                    spacing=20,
                                    controls=[
                                        ft.Text("📬 Contact Information", size=20, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                        ft.Divider(color=BORDER_COLOR),
                                        ft.Row([ft.Icon(ft.Icons.LOCATION_ON, color=ACCENT_TAN, size=24), ft.Text("Ongwediva, Namibia", color=TEXT_GREY, size=15)]),
                                        ft.Row([ft.Icon(ft.Icons.EMAIL, color=ACCENT_TAN, size=24), ft.Text("kavakurum@gmail.com", color=TEXT_GREY, size=15)]),
                                        ft.Row([ft.Icon(ft.Icons.PHONE, color=ACCENT_TAN, size=24), ft.Text("+264 81 811 0602", color=TEXT_GREY, size=15)]),
                                        ft.Row([ft.Icon(ft.Icons.CODE, color=ACCENT_TAN, size=24), ft.Text("github.com/Kavakuru-Metarere7", color=TEXT_GREY, size=15)]),
                                    ]
                                )
                            ),
                            ft.Container(
                                bgcolor=BG_WHITE,
                                padding=30,
                                border_radius=20,
                                border=get_uniform_border(1, BORDER_COLOR),
                                content=ft.Column(
                                    spacing=15,
                                    controls=[
                                        ft.Text("🌟 Connect With Me", size=18, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                        ft.Divider(color=BORDER_COLOR),
                                        ft.Row(
                                            spacing=20,
                                            controls=[
                                                ft.IconButton(icon=ft.Icons.CODE, icon_size=32, icon_color=PRIMARY_BROWN, on_click=lambda e: webbrowser.open("https://github.com/Kavakuru-Metarere7")),
                                                ft.IconButton(icon=ft.Icons.MAIL, icon_size=32, icon_color=PRIMARY_BROWN, on_click=lambda e: webbrowser.open("mailto:kavakurum@gmail.com")),
                                                ft.IconButton(icon=ft.Icons.CHAT, icon_size=32, icon_color=PRIMARY_BROWN, on_click=lambda e: webbrowser.open("https://linkedin.com")),
                                            ]
                                        ),
                                        ft.Container(height=10),
                                        ft.Text("Available for:", size=14, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                        ft.Row(
                                            wrap=True,
                                            spacing=8,
                                            controls=[
                                                ft.Container(content=ft.Text("🏗️ Structural Design", size=12), bgcolor=LIGHT_BG, padding=8, border_radius=15),
                                                ft.Container(content=ft.Text("🏭 Site Inspection", size=12), bgcolor=LIGHT_BG, padding=8, border_radius=15),
                                                ft.Container(content=ft.Text("📊 Cost Estimation", size=12), bgcolor=LIGHT_BG, padding=8, border_radius=15),
                                                ft.Container(content=ft.Text("🎓 Peer Tutoring", size=12), bgcolor=LIGHT_BG, padding=8, border_radius=15),
                                            ]
                                        ),
                                    ]
                                )
                            ),
                        ]
                    ),
                    # Right Column - Contact Form
                    ft.Container(
                        col={"sm": 12, "md": 7},
                        bgcolor=BG_WHITE,
                        padding=35,
                        border_radius=20,
                        border=get_uniform_border(1, BORDER_COLOR),
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(ft.Icons.CHAT, color=ACCENT_TAN, size=28),
                                        ft.Text("Send Me a Message", size=24, weight=ft.FontWeight.BOLD, color=DEEP_CLAY),
                                    ]
                                ),
                                ft.Divider(color=BORDER_COLOR),
                                name_field, 
                                email_field, 
                                subject_field, 
                                message_field,
                                ft.Container(height=5),
                                ft.ElevatedButton(
                                    "Send Message →", 
                                    icon=ft.Icons.SEND, 
                                    bgcolor=PRIMARY_BROWN, 
                                    color=BG_WHITE, 
                                    on_click=handle_submit_message, 
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=15,
                                    )
                                ),
                                ft.Text("✨ I'll respond within 24-48 hours", size=11, color=SUBTEXT_GREY, text_align=ft.TextAlign.CENTER),
                            ]
                        )
                    )
                ]
            )
        ])
    )

    portfolio_pages = {
        "overview": hero_section,
        "skills": skills_section,
        "contribution": contribution_section,
        "timeline": timeline_section,
        "projects": project_section,
        "blog": blog_section,
        "experience": leadership_section,
        "certificates": certification_section,
        "github": github_section,
        "contact": contact_section,
    }

    page_switcher = ft.AnimatedSwitcher(
        content=build_page_view(hero_section, "overview"),
        duration=220,
        reverse_duration=160,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
        transition=ft.AnimatedSwitcherTransition.FADE,
        expand=True,
    )

    def make_nav_button(label, page_key):
        button = ft.TextButton(
            label,
            style=ft.ButtonStyle(
                color=BG_WHITE if page_key == current_page_key["value"] else NAV_INACTIVE,
                overlay_color=OVERLAY_BROWN,
            ),
            on_click=lambda e, target=page_key: navigate_to(target),
        )
        nav_buttons[page_key] = button
        return button

    # =========================================================
    # STICKY NAVBAR PANEL
    # =========================================================
    header_navbar = ft.Container(
        bgcolor=PRIMARY_BROWN,
        padding=ft.Padding(40, 15, 40, 15),
        border=ft.Border(bottom=ft.BorderSide(1, ACCENT_TAN)),
        shadow=ft.BoxShadow(blur_radius=10, color=SHADOW_BROWN, offset=ft.Offset(0, 2)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=BG_WHITE, border_radius=6),
                    ft.Text("METARERE KAVAKURU", weight=ft.FontWeight.BOLD, size=16, color=BG_WHITE, style=ft.TextStyle(letter_spacing=1.1))
                ], spacing=10),
                ft.Row([
                    make_nav_button("Overview", "overview"),
                    make_nav_button("Skills", "skills"),
                    make_nav_button("Portfolio", "contribution"),
                    make_nav_button("Timeline", "timeline"),
                    make_nav_button("Projects", "projects"),
                    make_nav_button("Blog", "blog"),
                    make_nav_button("Experience", "experience"),
                    make_nav_button("MATLAB Hub", "certificates"),
                    make_nav_button("GitHub", "github"),
                    make_nav_button("Contact", "contact"),
                ], spacing=10, wrap=True)
            ]
        )
    )

    # =========================================================
    # RENDER DIRECT TO MAIN PAGE WINDOW
    # =========================================================
    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header_navbar,
                page_switcher
            ]
        )
    )

# =========================================================
# MAIN ENTRY POINT - READY FOR RENDER DEPLOYMENT
# =========================================================
if __name__ == "__main__":
    # Get port from environment variable for Render deployment
    port = int(os.environ.get("PORT", 8551))
    
    # For Render deployment - use 0.0.0.0 to bind to all interfaces
    try:
        ft.run(
            main, 
            host="0.0.0.0", 
            port=port, 
            assets_dir="assets",
            view=None  # No browser view for headless deployment
        )
    except Exception as e:
        print(f"Error starting the app: {e}")
        print(f"Attempting to run on port {port} with assets at assets/")
        # Fallback for Render
        ft.run(
            main, 
            host="0.0.0.0", 
            port=port, 
            assets_dir="assets",
            web_renderer=ft.WebRenderer.CANVAS_KIT
        )