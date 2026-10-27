"""
generate_pdf.py - Generates the complete 28-page Investigation Memo PDF
for DEEPTANSH NAGAR (Student ID: 500121033, Project Code: DF-PBL-026).
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Running header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, 755, "IoT Device Forensic Plan: Investigation Memo (SYNTHETIC Case)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(40, 750, 572, 750)
            
        # Running footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 25, page_text)
        self.drawString(40, 25, "IoT Device Forensic Plan: Investigation Memo (SYNTHETIC Case) - Deeptansh Nagar (500121033)")
        self.restoreState()

def build_pdf(filename="IoT_Device_Forensic_Plan_Deeptansh_Nagar.pdf"):
    # Margins: 40pt left/right, top 55pt (for header), bottom 40pt (for footer)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A202C"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1A202C"),
        spaceBefore=12,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    italic_style = ParagraphStyle(
        'ItalicDark',
        parent=body_style,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor("#4A5568")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2D3748")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#2D3748")
    )

    story = []

    def make_table(data, col_widths, is_header=True):
        formatted_data = []
        for r_idx, row in enumerate(data):
            formatted_row = []
            for c_idx, cell in enumerate(row):
                if isinstance(cell, str):
                    if r_idx == 0 and is_header:
                        formatted_row.append(Paragraph(cell, table_header_style))
                    else:
                        formatted_row.append(Paragraph(cell, table_cell_style))
                else:
                    formatted_row.append(cell)
            formatted_data.append(formatted_row)
        t = Table(formatted_data, colWidths=col_widths)
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F7FAFC")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#1A202C")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ]
        if is_header:
            t_style.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EDF2F7")))
        t.setStyle(TableStyle(t_style))
        return t

    # -------------------------------------------------------------------------
    # PAGE 1: Overview & Rubric Map
    # -------------------------------------------------------------------------
    story.append(Paragraph("IoT Device Forensic Plan: Investigation Memo<br/>(SYNTHETIC Case)", title_style))
    story.append(Paragraph("Oct 27, 2026 &nbsp;|&nbsp; <b>DEEPTANSH NAGAR</b> (500121033) &nbsp;|&nbsp; Project Code: <b>DF-PBL-026</b>", subtitle_style))
    
    story.append(Paragraph("Overview", h1_style))
    story.append(Paragraph(
        "This report plans and tests the forensic acquisition and analysis of a fictional smart camera, "
        "and concludes that the available evidence cannot yet separate four competing explanations. "
        "All data is SYNTHETIC, and every real tool output is recorded from the student's local machine execution.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Seven sections visual chevron table
    chevron_data = [
        ["1\nProblem", "2\nEvidence", "3\nMethod", "4\nResult", "5\nTest", "6\nLimits", "7\nConclusion"],
        ["Scenario and\n4 hypotheses", "Architecture\nmap, 6 items", "Acquisition\nplan, risks", "Evidence\nmatrix", "Python tool,\nevidence log", "Scope, access,\nclocks, tool", "Qualified,\nlow confidence"]
    ]
    t_chev = Table([
        [Paragraph(f"<b>{c[0]}</b>", table_header_style) for c in chevron_data],
        [Paragraph(f"<font size=6.5 color='#4A5568'>{c[1]}</font>", table_cell_style) for c in chevron_data]
    ], colWidths=[76]*7)
    t_chev.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EBF8FF")),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#F7FAFC")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#BEE3F8")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#90CDF4")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_chev)
    story.append(Spacer(1, 12))

    # Callout boxes
    c1 = Table([[Paragraph("<b>Defense Prep:</b> 7.5-minute structured talk, controlled terminal demo script, and model answers.", callout_style)]], colWidths=[532])
    c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(c1)
    story.append(Spacer(1, 6))

    c2 = Table([[Paragraph("<b>Rules followed:</b> all data SYNTHETIC; observation, interpretation, inference kept strictly apart.", callout_style)]], colWidths=[532])
    c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(c2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>report map · 7 sections, defense prep in summary</b>", italic_style))
    story.append(Spacer(1, 4))

    rubric_data = [
        ["Rubric criterion", "Weight", "Where it is addressed"],
        ["Problem framing", "20%", "Section 1: scenario, forensic question, four hypotheses"],
        ["Technical execution", "25%", "Sections 3 and 5: acquisition plan, decision tree, Python tool"],
        ["Evidence integrity", "15%", "Sections 3.1, 3.4, and 5: hashing, chain of custody, evidence log"],
        ["Analysis and limitations", "20%", "Sections 4 and 6: evidence matrix, residual risks"],
        ["Deliverable quality", "10%", "Whole report: architecture map, decision tree, heat map, call chain"],
        ["Defense and originality", "10%", "Sections 7, 9, and Defense Prep plan"]
    ]
    story.append(make_table(rubric_data, [130, 60, 342]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 2: 1. Problem Statement
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Problem Statement", h1_style))
    story.append(Paragraph(
        "This memo asks what best explains a camera's setting change and three video uploads on one night, "
        "using only evidence that could lawfully be collected from a fictional device.<br/>"
        "<b>Data statement:</b> every device, vendor, account, domain, IP address, and time in this report is <b>SYNTHETIC</b>. "
        "No real third-party device or account was investigated.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.1 Scenario (SYNTHETIC)", h2_style))
    story.append(Paragraph(
        "An office owner reports that a smart camera uploaded three clips between 02:14 and 02:31 while the office was empty. "
        "The owner says motion alerts had been turned off.",
        body_style
    ))
    story.append(Spacer(1, 6))

    spec_data = [
        ["Item", "Detail (SYNTHETIC)"],
        ["Device", "\"LumiCam C2\", fictional vendor Brightwave Labs"],
        ["Hardware", "Fictional ARM processor, 128 MB RAM, 16 MB SPI NOR flash, microSD slot"],
        ["Interfaces", "Wi-Fi, Bluetooth LE (setup only), UART header (3.3V), no JTAG"],
        ["Firmware", "Version 2.3.1, Linux-based"],
        ["Companion app", "\"LumiView\" mobile app"],
        ["Cloud", "api.lumicam.example, storage.lumicam.example (RFC 2606)"],
        ["Cloud account", "owner-synth-01@example.org"],
        ["Network", "Office network 192.0.2.0/24, camera at 192.0.2.45 (RFC 5737)"]
    ]
    story.append(make_table(spec_data, [130, 402]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 3: Timeline & Forensic Question
    # -------------------------------------------------------------------------
    timeline_data = [
        ["Time (SYNTHETIC)", "Event"],
        ["Day 1, 18:40", "Office closes, camera armed"],
        ["Day 1, 23:55", "Cloud login from a new app session"],
        ["Day 2, 02:10", "Motion alert setting changed to OFF through the cloud API"],
        ["Day 2, 02:14 to 02:31", "Three clips uploaded"],
        ["Day 2, 09:05", "Owner reports the problem; camera still powered on"]
    ]
    story.append(make_table(timeline_data, [150, 382]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Uploads began 4 min after the setting change, 2 h 15 min after a new login</b>", italic_style))
    story.append(Paragraph("<font size=7.5 color='#718096'>SYNTHETIC timeline, Day 1 18:40 to Day 2 09:05, assuming one clock and timezone (risk R8)</font>", body_style))
    story.append(Spacer(1, 4))

    # ASCII Scale Box
    timeline_box = (
        "+--------------------------------------------------------------------------------------------------+\n"
        "| Day 1 18:40          Day 1 23:55          Day 2 02:10      Day 2 02:14-02:31       Day 2 09:05   |\n"
        "| [Camera armed] ----> [New session] -----> [Alert to OFF] -> [Three uploads] -----> [Owner reports]|\n"
        "|  (mode=night)         (S-0002 known=false) (via cloud API)   (17-min cluster)       (camera ON)  |\n"
        "+--------------------------------------------------------------------------------------------------+"
    )
    story.append(Preformatted(timeline_box, code_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>incident timeline, to scale · 5 events</b>", italic_style))
    story.append(Paragraph(
        "Drawn to scale, the three uploads sit in one 17-minute cluster, far from the earlier login. "
        "The setting change at 02:10 is the central event every hypothesis must explain.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2 Forensic question", h2_style))
    story.append(Paragraph(
        "Based on the evidence that can be lawfully acquired from the synthetic LumiCam C2, its companion app, "
        "and its cloud account, what best explains the change of the motion-alert setting to OFF at 02:10 "
        "and the three video uploads between 02:14 and 02:31 on Day 2, and with what confidence?<br/><br/>"
        "<b>In scope:</b> the camera, local network state, the LumiView app, and the cloud account records.<br/>"
        "<b>Out of scope:</b> naming a person, proving intent, or investigating any real device.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 4: 1.3 Hypotheses & 1.4 Separation Evidence
    # -------------------------------------------------------------------------
    story.append(Paragraph("1.3 Hypotheses", h2_style))
    
    hyp_data = [
        ["ID", "Hypothesis", "Description"],
        ["H1", "Device compromise", "The camera's software or configuration was changed by an unauthorized party, locally or remotely."],
        ["H2", "Cloud-account misuse", "Someone used the owner's credentials or a stolen session to change the setting and trigger uploads; the device was not altered."],
        ["H3", "Benign malfunction", "A software or cloud synchronization fault changed the setting or caused uploads without any person acting."],
        ["H4", "Authorized user action", "A legitimate user made the change and forgot, or did not report it."]
    ]
    story.append(make_table(hyp_data, [35, 125, 372]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<i>Hypotheses can overlap (for example H2 and H4 if a password was shared), so the analysis does not force a single answer.</i>", italic_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.4 Evidence that would separate them (expected patterns, not findings)", h2_style))
    
    sep_data_1 = [
        ["Evidence source", "Supports H1 if...", "Supports H2 if...", "Supports H3 if...", "Supports H4 if..."],
        ["Device logs", "Unknown processes or config changes with no matching cloud command", "Normal command received from the cloud", "Errors or repeated retries around 02:10 to 02:31", "Normal command matching a known app session"],
        ["Firmware image", "Hash differs from vendor version 2.3.1", "Firmware matches", "Firmware matches; known fault pattern", "Firmware matches"],
        ["Network records", "Connections to unexpected destinations", "Only vendor cloud domains", "Vendor domains with sync retries", "Only vendor domains"]
    ]
    story.append(make_table(sep_data_1, [75, 114, 114, 114, 115]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 5: 1.4 cont & 2. Evidence Inventory
    # -------------------------------------------------------------------------
    sep_data_2 = [
        ["Evidence source", "Supports H1 if...", "Supports H2 if...", "Supports H3 if...", "Supports H4 if..."],
        ["Companion app data", "No related app activity", "Shows the unknown 23:55 session", "No related app activity", "Shows activity from a known device or user"],
        ["Cloud account records", "No matching cloud command for the change", "Unfamiliar login followed by the API call", "System-generated event, no user call", "Login and call from a known device"]
    ]
    story.append(make_table(sep_data_2, [75, 114, 114, 114, 115]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("2. Evidence Inventory", h1_style))
    story.append(Paragraph(
        "Evidence sits in six places, from the camera's memory (lost at power-off) to the vendor's cloud "
        "(kept, but subject to retention and legal limits). The architecture map below shows where each item lives; "
        "the tables give specifications and volatility. Items marked \"assumed\" are assumptions of the synthetic design.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 6: 2.1 Architecture Map & 2.2 Components
    # -------------------------------------------------------------------------
    story.append(Paragraph("2.1 Architecture map", h2_style))
    story.append(Paragraph("<b>Evidence sits in six places; camera RAM (E1) is lost at power-off</b>", italic_style))
    story.append(Spacer(1, 4))

    arch_box = (
        "+----------------------------------------------------------------------------------------------------+\n"
        "|  LumiCam C2 (SYNTHETIC)                      Router (E2)               Vendor cloud (E6)           |\n"
        "|  +-----------------------+              D1   DHCP leases and      D3   Cloud storage               |\n"
        "|  | RAM 128 MB (E1)       | ----------------> connection logs --------> storage.lumicam.example     |\n"
        "|  | *Lost at power-off*   |                   (Logs may rotate)    D2   Cloud API                   |\n"
        "|  +-----------------------+                                        ---> api.lumicam.example         |\n"
        "|  | SPI flash 16 MB (E3)  |                                                        ^                |\n"
        "|  | Firmware v2.3.1       |                                                        | D4             |\n"
        "|  +-----------------------+                                             Phone app (E5)              |\n"
        "|  | microSD card (E4)     |                                             LumiView app logs & session |\n"
        "|  +-----------------------+                                                                         |\n"
        "|  | UART 3.3V header      |                                                                         |\n"
        "|  +-----------+-----------+                                                                         |\n"
        "|              | D6                                                                                  |\n"
        "|              v                                                                                     |\n"
        "|  Examiner workstation (Read-only console capture)                                                  |\n"
        "+----------------------------------------------------------------------------------------------------+"
    )
    story.append(Preformatted(arch_box, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>architecture map · camera, router, phone app, cloud</b>", italic_style))
    story.append(Paragraph(
        "The camera's RAM is the most volatile item. The router and cloud hold copies of what crossed the network (D1 to D3), "
        "the phone app reaches the cloud API (D4), and the examiner reads the camera only through the UART header (D6). "
        "D5, the Bluetooth setup link, is left out because it is likely unused in this incident.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Components (SYNTHETIC)", h2_style))
    comp_data_1 = [
        ["Component", "Specification", "Evidence it may hold", "Volatility", "Access"],
        ["SoC", "Fictional ARM CPU", "Running processes, runtime state", "High", "UART console (assumed)"]
    ]
    story.append(make_table(comp_data_1, [65, 110, 157, 80, 120]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 7: Components Table Continued
    # -------------------------------------------------------------------------
    comp_data_2 = [
        ["Component", "Specification", "Evidence it may hold", "Volatility", "Access"],
        ["RAM", "128 MB", "Live logs, network connections, command history", "High (lost at power-off)", "UART, if still powered"],
        ["Flash", "16 MB SPI NOR", "Firmware v2.3.1, configuration, persistent logs", "Low", "UART, chip reader, or SPI (assumed)"],
        ["microSD", "Removable card", "Local clips, possible local logs", "Low", "Card reader with write blocker"],
        ["UART", "3.3V header", "Boot and console output (a path, not storage)", "Not applicable", "Serial adapter"],
        ["JTAG", "Not exposed", "None", "Not applicable", "Not available"],
        ["Wi-Fi / BLE", "2.4 GHz / setup only", "Connection and pairing details", "Low to medium", "Via router records"],
        ["Companion app", "LumiView", "App logs, session data, setting history", "Medium", "Phone backup (with authorization)"],
        ["Cloud API", "api.lumicam.example", "Login records, source IPs, API call history", "Medium (retention limits)", "Vendor export (with authorization)"],
        ["Cloud storage", "storage.lumicam.example", "Uploaded clips and metadata", "Medium", "Vendor export (with authorization)"],
        ["Router", "Office network", "DHCP leases, connection logs", "Medium", "Admin export (with authorization)"]
    ]
    story.append(make_table(comp_data_2, [65, 110, 157, 80, 120]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 8: 2.3 Order of Volatility & 2.4 Data Flows
    # -------------------------------------------------------------------------
    story.append(Paragraph("2.3 Evidence items, ordered by volatility", h2_style))
    
    vol_data = [
        ["Order", "ID", "Location", "Survives power-off?", "Risk if delayed"],
        ["1", "E1", "Camera RAM and live logs", "No", "Lost if power is removed"],
        ["2", "E2", "Network and live state (router records, active connections)", "Partly", "Logs may rotate or overwrite"],
        ["3", "E3", "Camera flash and firmware", "Yes", "Low, but careless extraction can alter data"],
        ["4", "E4", "microSD card", "Yes", "Low, but can be overwritten while the camera runs"],
        ["5", "E5", "Companion app data", "Yes", "Medium; app may sync or update"],
        ["6", "E6", "Cloud records", "Yes (retention limits)", "Medium; remote changes or deletion possible"]
    ]
    story.append(make_table(vol_data, [35, 30, 177, 110, 180]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.4 Data flows", h2_style))
    flow_data = [
        ["ID", "From", "To", "Content", "Why it matters"],
        ["D1", "Camera", "Router", "All camera traffic (Wi-Fi)", "When and where the camera connected"],
        ["D2", "Router", "Cloud API", "Status, commands, setting changes (HTTPS)", "Whether the 02:10 change reached the camera"],
        ["D3", "Router", "Cloud storage", "Clip uploads (HTTPS)", "The 02:14 to 02:31 uploads"],
        ["D4", "App", "Cloud API", "Login, setting changes (HTTPS)", "Who or what logged in at 23:55"],
        ["D5", "App", "Camera", "Setup only (BLE)", "Likely unused in this incident (assumed)"]
    ]
    story.append(make_table(flow_data, [30, 55, 75, 172, 200]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 9: D6, Assumptions & 3. Method
    # -------------------------------------------------------------------------
    flow_d6 = [
        ["ID", "From", "To", "Content", "Why it matters"],
        ["D6", "Examiner", "Camera", "Read-only console (UART)", "Planned way to collect volatile data"]
    ]
    story.append(make_table(flow_d6, [30, 55, 75, 172, 200]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Assumptions:</b> the UART header gives a read-only console; the camera is still powered on, "
        "so E1 may exist; device and cloud clocks may differ; cloud retention periods are not defined in the scenario.",
        italic_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Method", h1_style))
    story.append(Paragraph(
        "The method collects evidence in order of volatility, works only on verified copies, and records a SHA-256 hash, "
        "tool, version, command, and timestamp for every step. This is a plan: no physical hardware collection was performed, "
        "so every planned tool is explicitly designated as \"Planned tool, not run (SYNTHETIC case)\".",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.1 Planning rules", h2_style))
    rules_data = [
        ["Rule", "Reason"],
        ["Collect in order of volatility (E1 to E6)", "Fast-disappearing evidence is lost first"],
        ["Work on verified copies; keep originals untouched", "Preserves the original evidence"],
        ["Hash every artifact with SHA-256 right after collection", "Proves a copy has not changed"],
        ["Record tool, version, command, and time for every action", "Allows another person to repeat the work"],
        ["Record the examiner clock and device clock at the start", "Prevents timestamp and timezone errors"],
        ["Read-only access by default", "Avoids changing the device"],
        ["Collect only with written (SYNTHETIC) authorization", "Legal and ethical requirement"]
    ]
    story.append(make_table(rules_data, [200, 332]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 10: 3.2 Decision Tree
    # -------------------------------------------------------------------------
    story.append(Paragraph("3.2 Decision tree: device on or off", h2_style))
    story.append(Paragraph("<b>Power state decides whether E1 can still be captured live</b>", italic_style))
    story.append(Spacer(1, 4))

    dtree_box = (
        "+--------------------------------------------------------------------------------------------------+\n"
        "|                           [ Authorization confirmed; photograph setup ]                          |\n"
        "|                                                 |                                                |\n"
        "|                                     [ Camera powered on? ]                                       |\n"
        "|                                    /                      \\                                      |\n"
        "|                            YES    /                        \\   NO                                |\n"
        "|                                  v                          v                                    |\n"
        "|                 [ Do not power off or unplug ]        [ Do not power on; E1 is lost; ]           |\n"
        "|                 [ Record clocks discrepancy  ]        [ record it as a limitation    ]           |\n"
        "|                                  |                                  |                            |\n"
        "|                   [ Read-only UART access? ]                        |                            |\n"
        "|                         /          \\                                |                            |\n"
        "|                 YES    /            \\   NO                          |                            |\n"
        "|                       v              v                              |                            |\n"
        "|             +--------------------+  [ Note limitation, continue E2] |                            |\n"
        "|             | E1: Capture RAM    |                  |               |                            |\n"
        "|             +---------+----------+                  |               |                            |\n"
        "|                       |                             |               |                            |\n"
        "|                       +--------------+--------------+               |                            |\n"
        "|                                      |                              |                            |\n"
        "|                                      v                              |                            |\n"
        "|                      [ E2: Network and live state ]                 |                            |\n"
        "|                                      |                              |                            |\n"
        "|                      [ Risk of remote wipe / sync? ]                |                            |\n"
        "|                                    /        \\                       |                            |\n"
        "|                            YES    /          \\   NO                 |                            |\n"
        "|                                  v            v                     |                            |\n"
        "|                     [ Isolate at router ]     |                     |                            |\n"
        "|                                  \\            /                     |                            |\n"
        "|                                   v          v                      |                            |\n"
        "|                     [ Controlled shutdown / power removal ]         |                            |\n"
        "|                                      |                              |                            |\n"
        "|                                      +------------------------------+                            |\n"
        "|                                      v                                                           |\n"
        "|   Then, on every path, in this order:                                                            |\n"
        "|   E3 flash image (read twice, compare hashes), then E4 microSD image through a write blocker,    |\n"
        "|   E5 companion app data (authorized), then E6 cloud records (authorized export or request).      |\n"
        "|   Hash every item and update the evidence log and chain of custody.                              |\n"
        "+--------------------------------------------------------------------------------------------------+"
    )
    story.append(Preformatted(dtree_box, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>decision tree · camera on or off, 3 decisions</b>", italic_style))
    story.append(Paragraph(
        "The scenario states the camera is still powered on, so the left path applies; the right path is the case "
        "where it was already powered off. Isolating the network protects against remote changes but also changes device "
        "behaviour, so the decision, its reason, and its time must be written down.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 11: 3.3 Acquisition Plan (E1 to E4)
    # -------------------------------------------------------------------------
    story.append(Paragraph("3.3 Acquisition plan", h2_style))
    
    acq_data_1 = [
        ["ID", "Source", "Method", "Tool (version)", "Expected artifact"],
        ["E1", "Camera RAM and live state", "Connect a serial adapter to the UART header and capture the console to a file. Run only a fixed list of read-only commands (date, uptime, process list, connections, kernel messages, mounts) and log each one. Assumes console available.", "Serial terminal (picocom or minicom) [Planned tool, not run (SYNTHETIC case)]; USB-serial adapter [Planned tool, not run]", "Console capture text file (SYNTHETIC)"],
        ["E2", "Network and live state", "Export DHCP and connection records from the router; optionally capture traffic from a mirror port.", "Router export, tcpdump or Wireshark [Planned tool, not run (SYNTHETIC case)]", "Router log export, optional capture file (SYNTHETIC)"],
        ["E3", "Camera flash and firmware", "After shutdown, read the SPI flash with an in-circuit clip. Read twice and compare hashes.", "flashrom or equivalent [Planned tool, not run (SYNTHETIC case)]; SPI clip", "Flash image (SYNTHETIC)"],
        ["E4", "microSD card", "Remove after shutdown, connect through a hardware write blocker, create an image.", "Write blocker [Planned tool, not run (SYNTHETIC case)]; dd, dc3dd, or FTK Imager [Planned tool, not run]", "microSD image, local clips (SYNTHETIC)"]
    ]
    story.append(make_table(acq_data_1, [25, 75, 172, 140, 120]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 12: 3.3 Acquisition Plan (E5, E6) & Requirements
    # -------------------------------------------------------------------------
    acq_data_2 = [
        ["ID", "Source", "Method", "Tool (version)", "Expected artifact"],
        ["E5", "Companion app (LumiView)", "With consent, obtain a phone backup or app export; record app version and phone model.", "Phone backup or lawful extraction tool [Planned tool, not run (SYNTHETIC case)]", "App logs, sessions, setting history (SYNTHETIC)"],
        ["E6", "Cloud records", "Request an account export or vendor records for owner-synth-01@example.org, Day 1 to Day 2.", "Vendor export or legal request (SYNTHETIC process)", "Login log, API call log, clip metadata (SYNTHETIC)"]
    ]
    story.append(make_table(acq_data_2, [25, 75, 172, 140, 120]))
    story.append(Spacer(1, 10))

    acq_req = [
        ["ID", "Hash step", "Authorization requirement", "Chain-of-custody entry"],
        ["E1", "SHA-256 of the capture file as soon as the session ends", "Owner consent covering physical access and cable connection", "Item, description, collector, date/time, source, SHA-256, location"],
        ["E2", "SHA-256 of each export or capture", "Network owner consent", "Same fields"],
        ["E3", "SHA-256 of both reads; they must match before use", "Owner consent for opening the device and chip reading", "Same fields, plus programmer used"],
        ["E4", "SHA-256 of the image (and of source via write blocker, where tool allows)", "Owner consent", "Same fields, plus write-blocker model"],
        ["E5", "SHA-256 of the backup or export", "Phone owner consent; data beyond the app is out of scope", "Same fields, plus phone model and app version"],
        ["E6", "SHA-256 of each export", "Account owner consent or vendor legal process; no unauthorized cloud access", "Same fields, plus how and when the export arrived"]
    ]
    story.append(make_table(acq_req, [25, 150, 177, 180]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 13: 3.4 Chain-of-Custody Template & 3.5 Risk Register Intro
    # -------------------------------------------------------------------------
    story.append(Paragraph("3.4 Chain-of-custody template", h2_style))
    
    coc_data = [
        ["Field", "Entry"],
        ["Evidence ID", "E1 to E6 (Assigned per item)"],
        ["Description", "Console capture / router log / flash image / microSD raw / app export / cloud JSON"],
        ["Source", "LumiCam C2 (fictional), Router, Smartphone, Cloud API"],
        ["Collected by", "DEEPTANSH NAGAR (500121033)"],
        ["Date and time, with timezone", "2026-10-27T12:00:00Z (UTC reference)"],
        ["Tool and version", "Planned tool, not run (SYNTHETIC case)"],
        ["Command or procedure", "Planned procedure, not run (SYNTHETIC case)"],
        ["SHA-256", "ad1d0c5f2b7c80aff2ff6739173e5f14369561eb020b51d2476fdc495fe8ec4a (Log A baseline)"],
        ["Storage location", "Evidence Locker #2 / Secure Digital Repository"],
        ["Transferred to", "[Lead Examiner / Custodian, Pending Transfer]"]
    ]
    story.append(make_table(coc_data, [150, 382]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<i>Template only, no real physical collection performed (SYNTHETIC case).</i><br/>"
        "<b>Clock handling:</b> at the start, record the examiner's clock and the device's clock side by side, "
        "write the difference as an offset in the evidence log, note the timezone of each source, and convert all analysis times to UTC while keeping the original value.",
        italic_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.5 Risk register", h2_style))
    story.append(Paragraph(
        "Score = likelihood × impact, each rated 1 (low) to 3 (high); 6 or more is a priority. "
        "Ratings are judgement-based for this SYNTHETIC case.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 14: Risk Heat Map & R1, R2
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>Only R5 and R8 reach the top score of 9</b>", italic_style))
    story.append(Paragraph("<font size=7.5 color='#718096'>Risks by likelihood and impact, SYNTHETIC case, judgement-based ratings</font>", body_style))
    story.append(Spacer(1, 4))

    # ASCII Risk Matrix
    risk_box = (
        "+--------------------------------------------------------------------------------------------------+\n"
        "| Likelihood |                                                                                     |\n"
        "|   High (3) |                                       | R5 (Cloud Auth), R8 (Clock Drift) [Score 9] |\n"
        "|            |---------------------------------------+---------------------------------------------|\n"
        "|   Med  (2) |                   | R6 (Tool fault),  | R1 (RAM lost), R2 (Remote wipe),            |\n"
        "|            |                   | R9 (Doc gap) [4]  | R4 (Encryption), R7 (Contamination) [6]     |\n"
        "|            |-------------------+-------------------+---------------------------------------------|\n"
        "|   Low  (1) |                   |                   | R3 (Firmware mod), R10 (Copy loss),         |\n"
        "|            |                   |                   | R11 (UART electrical damage) [Score 3]      |\n"
        "|            +-------------------+-------------------+---------------------------------------------|\n"
        "|            |      Low (1)      |    Medium (2)     |                  High (3)                   |\n"
        "|                                         Impact                                                   |\n"
        "+--------------------------------------------------------------------------------------------------+"
    )
    story.append(Preformatted(risk_box, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>risk heat map · 11 risks on likelihood and impact</b>", italic_style))
    story.append(Paragraph(
        "Most risks cluster at high impact: losing volatile data, a remote wipe, a locked bootloader, and contamination all score 6. "
        "The two that reach 9 are about authorization and clocks, not about the device itself.",
        body_style
    ))
    story.append(Spacer(1, 8))

    risk_data_1 = [
        ["ID", "Risk", "Likelihood", "Impact", "Score", "Mitigation", "Owner", "Residual risk"],
        ["R1", "Volatile data lost at power-off", "Medium", "High", "6", "Do not power off before E1 is captured; label \"Do not unplug\"; collect E1 first", "Examiner", "Medium: data may already have changed"],
        ["R2", "Remote wipe or cloud sync overwrite", "Medium", "High", "6", "Capture E1 and E2 first, then isolate network path at router and record time and reason; request cloud data early", "Examiner", "Medium: isolation changes behaviour; cloud data may already be altered"]
    ]
    story.append(make_table(risk_data_1, [22, 90, 48, 40, 30, 142, 50, 110]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 15: Risk Register R3 to R8
    # -------------------------------------------------------------------------
    risk_data_2 = [
        ["ID", "Risk", "Likelihood", "Impact", "Score", "Mitigation", "Owner", "Residual risk"],
        ["R3", "Firmware modified during extraction", "Low", "High", "3", "Read-only commands only; never write to flash; read flash twice and compare hashes; log every command", "Examiner", "Low"],
        ["R4", "Encryption or locked bootloader", "Medium", "High", "6", "Check for a console first; if blocked, record it and rely on E2, E4, E5, E6; no bypass without authorization", "Examiner", "High: device evidence may be unavailable"],
        ["R5", "Cloud authorization and legal limits", "High", "High", "9", "Written authorization first; use official export or legal process; record scope and retention limit", "Authorizing party and Examiner", "Medium: vendor may refuse or delete data"],
        ["R6", "Tool unreliability", "Medium", "Medium", "4", "Record versions; test tools on a known SYNTHETIC file; read flash twice; spot-check with a second tool", "Examiner", "Low to Medium"],
        ["R7", "Evidence contamination", "Medium", "High", "6", "Hardware write blocker; work on verified copies; seal originals; label items", "Examiner and custodian", "Low"],
        ["R8", "Timestamp and timezone errors", "High", "High", "9", "Record both clocks and the offset; note each source's timezone; convert to UTC and keep originals", "Examiner", "Medium: device clock may have drifted"]
    ]
    story.append(make_table(risk_data_2, [22, 90, 48, 40, 30, 142, 50, 110]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 16: Risk Register R9 to R11 & 4. Result
    # -------------------------------------------------------------------------
    risk_data_3 = [
        ["ID", "Risk", "Likelihood", "Impact", "Score", "Mitigation", "Owner", "Residual risk"],
        ["R9", "Documentation gaps", "Medium", "Medium", "4", "Chain-of-custody template; fill evidence log at time of each action; use Section 5 script", "Examiner", "Low"],
        ["R10", "Loss or corruption of evidence copies", "Low", "High", "3", "Two copies in separate locations; re-check SHA-256 before each use", "Custodian", "Low"],
        ["R11", "Physical damage to the device", "Low", "High", "3", "Check 3.3V before connecting; photograph before and after; practise on a spare board", "Examiner", "Low to Medium"]
    ]
    story.append(make_table(risk_data_3, [22, 90, 48, 40, 30, 142, 50, 110]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "R5 and R8 carry the highest score because authorization limits and timestamp errors can weaken the whole conclusion. "
        "R4 and R5 may remove the evidence needed to separate H1 from H2, and R8 affects every hypothesis.",
        italic_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Result", h1_style))
    story.append(Paragraph(
        "With only the SYNTHETIC scenario facts, the four hypotheses cannot be separated; the facts lean weakly toward "
        "a cloud-side explanation (H2 or H4) over a device-level one (H1). Observation, interpretation, and inference are kept "
        "in separate columns, and confidence is a judgement, not a probability. No new log lines, hashes, or tool output were invented for this matrix.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 17: 4.1 Evidence Matrix (M1 to M5)
    # -------------------------------------------------------------------------
    story.append(Paragraph("4.1 Evidence matrix", h2_style))
    
    matrix_data = [
        ["ID", "Artifact (SYNTHETIC)", "Observation", "Interpretation", "Inference", "Supports / contradicts", "Confidence", "Limitation"],
        ["M1", "Cloud login record, Day 1, 23:55 (E6)", "A login from a new app session is recorded.", "A session not seen before was created on the account.", "Someone or some device new to the account logged in; does not show who.", "Weakly supports H2 and H4; neutral for H1 and H3", "Low", "\"New\" is vendor's label. No device ID, IP, or location; timezone not stated."],
        ["M2", "Cloud API record, Day 2, 02:10 (E6)", "The motion alert setting was changed to OFF through cloud API.", "Change requested through cloud, not physical control.", "Change can be explained without device compromise; which session sent it is unknown.", "Consistent with H2, H4, and H3 (if system-generated); does not require H1 but does not exclude it", "Low to Medium", "Scenario does not say which session made call; linking to M1 is an assumption."],
        ["M3", "Cloud storage metadata, Day 2, 02:14 to 02:31 (E6)", "Three clips were uploaded.", "Camera, or something using credentials, sent video to cloud storage.", "Uploads began 4 min after setting change: timing relationship only.", "Compatible with all four; does not separate them", "Low", "Not stated whether setting controls recording or uploading; clip content not examined."],
        ["M4", "Owner report (statement)", "Owner says office was empty and motion alerts were off.", "Owner believes no one was present and did not expect uploads.", "Weak indication owner did not knowingly cause uploads.", "Weakly contradicts H4", "Low", "A statement, not a technical artifact; unverified."],
        ["M5", "Device state at 09:05", "Camera was still powered on when reported.", "Volatile data (E1) may still exist.", "Affects what can be collected, not which hypothesis is true.", "Neutral", "Medium (as reported)", "Reported by owner; condition of RAM unknown."]
    ]
    story.append(make_table(matrix_data, [20, 68, 74, 74, 74, 80, 50, 92]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 18: Matrix at a Glance & 4.2 Evidence Still Needed
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>No single artifact separates the four hypotheses</b>", italic_style))
    story.append(Paragraph("<font size=7.5 color='#718096'>Evidence matrix at a glance, SYNTHETIC scenario facts, confidence low to medium</font>", body_style))
    story.append(Spacer(1, 4))

    mat_glance = [
        ["", "H1\nDevice comp", "H2\nCloud misuse", "H3\nMalfunction", "H4\nAuthorized"],
        ["M1 New session login", "none", "weak support", "none", "weak support"],
        ["M2 Setting change", "none", "fits", "fits", "fits"],
        ["M3 Three uploads", "fits", "fits", "fits", "fits"],
        ["M4 Owner statement", "none", "none", "none", "weak contra"],
        ["M5 Device still on", "none", "none", "none", "none"]
    ]
    t_glance = Table([
        [Paragraph(f"<b>{c}</b>", table_header_style) for c in mat_glance[0]],
        *[ [Paragraph(c, table_cell_style) for c in row] for row in mat_glance[1:] ]
    ], colWidths=[120, 103, 103, 103, 103])
    t_glance.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (2, 1), (2, 1), colors.HexColor("#EBF8FF")), # weak support
        ('BACKGROUND', (4, 1), (4, 1), colors.HexColor("#EBF8FF")), # weak support
        ('BACKGROUND', (4, 4), (4, 4), colors.HexColor("#FFF5F5")), # weak contra
    ]))
    story.append(t_glance)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>evidence matrix at a glance · 5 artifacts by 4 hypotheses</b>", italic_style))
    story.append(Paragraph(
        "The drawing condenses the matrix above. Only two cells lean at all (the new login weakly supports H2 and H4, "
        "and the owner's statement weakly contradicts H4); everything else fits several hypotheses or none, which is why the conclusion stays open.<br/>"
        "Time gaps from the SYNTHETIC timeline (assuming one clock and timezone, see R8): login to setting change 2 h 15 min; "
        "setting change to first upload 4 min; first to last upload 17 min.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 Evidence still needed", h2_style))
    story.append(Paragraph("These items are planned in Section 3 but no data exists for them; they are not invented here.", italic_style))
    story.append(Spacer(1, 4))

    need_data_1 = [
        ["ID", "Pending artifact", "Question it answers", "Separates"],
        ["P1", "Cloud login details (IP, device ID, location)", "Was the 23:55 session from a known device?", "H2 vs H4"],
        ["P2", "Cloud API call details for 02:10 (session or token)", "Which session changed the setting?", "H2 vs H4 vs H3"],
        ["P3", "Camera console and log capture (E1)", "Did the camera receive a normal command at 02:10? Any unknown process or error?", "H1 vs H3 vs H2"]
    ]
    story.append(make_table(need_data_1, [25, 177, 210, 120]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 19: 4.2 Pending Artifacts (P4 to P6) & 4.3 Analysis
    # -------------------------------------------------------------------------
    need_data_2 = [
        ["ID", "Pending artifact", "Question it answers", "Separates"],
        ["P4", "Firmware hash against the vendor's v2.3.1 (E3)", "Was the firmware altered?", "H1 vs others"],
        ["P5", "Router connection records (E2)", "Did the camera contact non-vendor destinations?", "H1 vs others"],
        ["P6", "Companion app session data (E5)", "Does the app show activity for the 23:55 session?", "H2 vs H4"]
    ]
    story.append(make_table(need_data_2, [25, 177, 210, 120]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("4.3 Analysis", h2_style))
    
    ana_data = [
        ["Hypothesis", "Status with current data", "Reason"],
        ["H1 Device compromise", "Untested, not ruled out", "No device-level evidence yet (P3, P4, P5). M2 means it is not required to explain the setting change, but it could still explain the uploads."],
        ["H2 Cloud-account misuse", "Slightly more consistent than H1", "M1 and M2 fit, but both also fit a legitimate user."],
        ["H3 Benign malfunction", "Not excluded", "No fault evidence either way."],
        ["H4 Authorized user action", "Not excluded", "M4 weakens it slightly, but it is only a statement; M1 may be a new legitimate phone."]
    ]
    story.append(make_table(ana_data, [130, 140, 262]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<i>How later evidence would change the result:</i>", italic_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 20: How Pending Evidence Moves the Result
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>Four kinds of pending evidence would each move the result</b>", italic_style))
    story.append(Spacer(1, 4))

    shift_box = (
        "+--------------------------------------------------------------------------------------------------+\n"
        "|  P1, P6: session recognised                       --- stronger --->  H4 (Authorized user action) |\n"
        "|  (The 23:55 session is from a recognised device)  --- weaker   --->  H2 (Cloud-account misuse)   |\n"
        "|                                                                                                  |\n"
        "|  P2: change from that session                     --- stronger --->  H2 (Cloud-account misuse)   |\n"
        "|  (The 02:10 change came from unrecognised 23:55)                                                 |\n"
        "|                                                                                                  |\n"
        "|  P4, P5: device-level signs                       --- stronger --->  H1 (Device compromise)      |\n"
        "|  (Firmware hash differs, or non-vendor dest used)                                                |\n"
        "|                                                                                                  |\n"
        "|  P3, P2: fault, no user call                      --- stronger --->  H3 (Benign malfunction)     |\n"
        "|  (Device log shows faults with no user call)                                                     |\n"
        "+--------------------------------------------------------------------------------------------------+"
    )
    story.append(Preformatted(shift_box, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>what would move each hypothesis · pending evidence P1 to P6</b>", italic_style))
    story.append(Paragraph(
        "Green arrows strengthen a hypothesis and red arrows weaken it. The table below says the same thing in words.",
        body_style
    ))
    story.append(Spacer(1, 6))

    move_table = [
        ["If later evidence shows...", "Then..."],
        ["The 23:55 session is from a device the owner recognises (P1, P6)", "H4 stronger, H2 weaker"],
        ["The 02:10 change came from the unrecognised 23:55 session (P2)", "H2 stronger"],
        ["Firmware hash differs, or the camera contacted non-vendor destinations (P4, P5)", "H1 stronger"],
        ["Device log shows faults or retries with no matching user call (P3, P2)", "H3 stronger"]
    ]
    story.append(make_table(move_table, [260, 272]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 21: 5. Reproducible Test
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Reproducible Test", h1_style))
    story.append(Paragraph(
        "A small Python tool (<code>evidence_tool.py</code>, standard library only) hashes evidence files with SHA-256, "
        "writes an evidence log with a UTC timestamp and the exact command for every action, verifies hashes on rerun, "
        "and parses a SYNTHETIC log. The tool, the two SYNTHETIC logs (A and B), and a README with full run instructions "
        "are in the <code>iot_forensic_demo</code> folder submitted with this report.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.1 Commands", h2_style))
    
    cmd_data = [
        ["Command", "Purpose"],
        ["init", "Hash every file in evidence/ and save a baseline in evidence_log.json; refuses to overwrite an existing baseline without --force"],
        ["verify", "Re-hash and report OK, MISMATCH, MISSING, or UNLISTED for each file; exit code 0 only on a full pass"],
        ["parse", "Check the file's hash first, refuse to parse on a mismatch, then print a UTC timeline, the gap between setting change and first upload, and observation flags"]
    ]
    story.append(make_table(cmd_data, [80, 452]))
    story.append(Spacer(1, 10))

    py_cmds = (
        "python evidence_tool.py init\n"
        "python evidence_tool.py verify\n"
        "python evidence_tool.py parse --file evidence/camera_console_synthetic_A.log\n"
        "python evidence_tool.py parse --file evidence/camera_console_synthetic_B.log"
    )
    story.append(Preformatted(py_cmds, code_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 22: Call Chain & Real Outputs
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>Every command hashes first and records itself in the evidence log</b>", italic_style))
    story.append(Spacer(1, 4))

    call_chain_box = (
        "+--------------------------------------------------------------------------------------------------+\n"
        "|  init: hash every file in evidence/ and save the baseline                                        |\n"
        "|  cmd_init ----> list_files ----> sha256_file ----> record_action                                 |\n"
        "|                                                                                                  |\n"
        "|  verify: re-hash every file and compare with the baseline                                        |\n"
        "|  cmd_verify ----> check_files ----> sha256_file ----> record_action                              |\n"
        "|                                                                                                  |\n"
        "|  parse: check the file hash first, then analyse the log                                          |\n"
        "|  cmd_parse ----> sha256_file ----> [Hash OK?] -- YES --> parse_log_file -> analyse -> record_act |\n"
        "|                                           \\                                                      |\n"
        "|                                            NO ---> Refuse, log it                                |\n"
        "|                                                                                                  |\n"
        "|  evidence_log.json, written by save_log (Baseline SHA-256 per file plus entry per command)       |\n"
        "+--------------------------------------------------------------------------------------------------+"
    )
    story.append(Preformatted(call_chain_box, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>call chain of the three commands · hash gate before analysis</b>", italic_style))
    story.append(Paragraph(
        "All three commands call <code>sha256_file</code> and end by calling <code>record_action</code>. "
        "In <code>parse</code>, the hash gate sits before any analysis: a file that no longer matches its baseline "
        "is refused and the refusal is logged.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Python version:</b> <code>Python 3.11.9</code> (Windows PowerShell)", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Output of init:</b>", body_style))
    init_out = (
        "HASHED  camera_console_synthetic_A.log  ad1d0c5f2b7c80aff2ff6739173e5f14369561eb020b51d2476fdc495fe8ec4a\n"
        "HASHED  camera_console_synthetic_B.log  36f1c40006de149f172b7a9ae8c70911aadc02f3713e3c2e7aa6183dd590a583\n"
        "Baseline written to evidence_log.json"
    )
    story.append(Preformatted(init_out, code_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Output of verify:</b>", body_style))
    ver_out = (
        "OK        camera_console_synthetic_A.log\n"
        "OK        camera_console_synthetic_B.log\n"
        "OVERALL: PASS - all hashes match"
    )
    story.append(Preformatted(ver_out, code_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 Expected parse results", h2_style))
    story.append(Paragraph("These are what the supplied SYNTHETIC files produced on the student's machine:", body_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 23: 5.2 Parse Results, 5.3 Live Demo, 5.4 Functions
    # -------------------------------------------------------------------------
    parse_sum = [
        ["Input", "Parsed events", "Malformed lines", "Gap, setting change to first upload", "Flags (consistent-with only, not proof)"],
        ["Log A", "11", "1 (line 14, deliberate)", "4 min 4 s", "Unrecognised session (H2, H4)"],
        ["Log B", "9", "0", "4 min 4 s", "Unlisted process (H1); config change without a cloud command (H1, H3); three non-vendor destinations (H1)"]
    ]
    story.append(make_table(parse_sum, [45, 65, 80, 110, 232]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.3 Live demonstration", h2_style))
    story.append(Paragraph(
        "<b>1. Change the input.</b> Parse log B after log A. The same code gives different flags because the log content differs.<br/>"
        "<b>2. Change a file.</b> Add one line to log A, then run <code>verify</code>: expected <code>MISMATCH</code>, <code>OVERALL: FAIL</code>. "
        "Running <code>parse</code> on it is refused. Remove the line and verify passes again.<br/>"
        "<b>3. Add a file.</b> Create any new file in evidence/ and run <code>verify</code>: expected <code>UNLISTED</code>.<br/>"
        "Every step is recorded in <code>evidence_log.json</code>.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.4 What the functions do", h2_style))
    fn_data_1 = [
        ["Function", "Purpose"],
        ["sha256_file()", "Reads a file in 64 KB pieces and returns its SHA-256 fingerprint"],
        ["record_action()", "Appends UTC time, the exact command line, and the result to the evidence log"],
        ["cmd_init()", "Creates the baseline and protects it from accidental overwrite"],
        ["check_files() / cmd_verify()", "Compare current hashes with the baseline and report a pass or fail"],
        ["parse_line() / parse_log_file()", "Split each log line into time, component, event, and fields; reject malformed lines and times without a timezone; sort events by UTC time"]
    ]
    story.append(make_table(fn_data_1, [150, 382]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 24: 5.4 cont, 5.5 Limits of Artefact & 6. Limitations
    # -------------------------------------------------------------------------
    fn_data_2 = [
        ["Function", "Purpose"],
        ["analyse()", "Applies four fixed rules (unrecognised session, config change with no command in the previous 60 s, unlisted process, non-vendor destination) and returns observation flags"],
        ["cmd_parse()", "Verifies the hash before analysis, then prints the timeline, gap, and flags"]
    ]
    story.append(make_table(fn_data_2, [150, 382]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<i>The flags are observations from fixed rules. They are not conclusions and never name a person or intent.</i>", italic_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.5 Limits of the artefact", h2_style))
    story.append(Paragraph(
        "• The log format is invented; real device logs need their own parser.<br/>"
        "• The four rules are simple and can miss real problems or flag harmless events.<br/>"
        "• A matching hash shows a file is unchanged since it was hashed, not that it was correct when collected.<br/>"
        "• The JSON evidence log is not tamper-proof; a real case would store the baseline hashes separately.<br/>"
        "• Logs A and B are test inputs created for this demonstration. They are not the Step 1 scenario evidence and do not change the Section 4 matrix.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("6. Limitations", h1_style))
    story.append(Paragraph(
        "The biggest limitation is that all data is synthetic and no device-level evidence was available, "
        "so H1 stays untested rather than rejected.",
        body_style
    ))
    story.append(Spacer(1, 6))

    lim_data_1 = [
        ["Area", "Limitation", "Effect on the conclusion"],
        ["Scope", "One device, one account, one night. Other devices and accounts are out of scope.", "Causes outside the scope are not examined"],
        ["Synthetic data", "All facts, logs, and timings are invented. No real device, vendor, or attacker behaviour is tested.", "Findings show the method, not real-world results"]
    ]
    story.append(make_table(lim_data_1, [90, 220, 222]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 25: Limitations Table Continued
    # -------------------------------------------------------------------------
    lim_data_2 = [
        ["Area", "Limitation", "Effect on the conclusion"],
        ["Limited evidence", "The matrix uses high-level scenario facts only. No console, firmware, network, app, or detailed cloud artifacts are available.", "Confidence stays low; hypotheses cannot be separated"],
        ["Statements", "The owner's report and the vendor's \"new session\" label are unverified.", "These items carry low weight"],
        ["Model-specific", "The plan assumes a Linux camera with a UART header, a removable microSD card, and a particular cloud design.", "It cannot be applied unchanged to other devices, such as a locked-down smart plug"],
        ["Technical access", "A readable UART console, readable flash, and unencrypted storage are assumed. Encryption or a locked bootloader could block device evidence (R4).", "H1 might remain untestable"],
        ["Volatile data", "Running commands changes the device slightly, and some RAM data may already be lost (R1, R3).", "Device observations may be incomplete"],
        ["Authorization and legal", "Cloud and phone data need consent or legal process; vendor retention and privacy rules may limit access (R5). Authorization here is SYNTHETIC.", "Cloud evidence may be incomplete in a real case"],
        ["Time and clocks", "Scenario times are assumed to share one clock and timezone; real device clocks drift (R8).", "Event order could be wrong if clocks are not corrected"],
        ["Network isolation", "Blocking the camera's network to prevent remote changes also changes its behaviour (R2).", "The decision must be documented and may affect later observations"],
        ["Technical artefact", "Invented log format, four simple rules, and a plain JSON log that is not tamper-proof.", "Supports integrity checks but is not a complete forensic tool"]
    ]
    story.append(make_table(lim_data_2, [90, 220, 222]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 26: Method Limit & 7. Conclusion
    # -------------------------------------------------------------------------
    lim_data_3 = [
        ["Area", "Limitation", "Effect on the conclusion"],
        ["Method", "Confidence levels and risk ratings are judgement-based.", "Another examiner might rate them differently"]
    ]
    story.append(make_table(lim_data_3, [90, 220, 222]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "Using only the SYNTHETIC scenario facts in the Section 4 matrix, the four hypotheses cannot yet be separated. "
        "The setting change reached the camera through the cloud API, and a new session appeared on the account earlier that night. "
        "These facts are slightly more consistent with a cloud-side explanation (H2 cloud-account misuse or H4 authorized user action) "
        "than with a device-level one (H1 device compromise). Confidence in this leaning is <b>low</b>. H3 (benign malfunction) is not excluded.<br/><br/>"
        "The data does not show who acted, why, or whether the setting change caused the uploads. It does not name a person, give a motive, "
        "or claim guilt, and it does not claim the device is safe or compromised.",
        body_style
    ))
    story.append(Spacer(1, 8))

    conc_points = [
        ["Point", "Basis in the matrix"],
        ["A device compromise is not required to explain setting change", "M2: the change was made through the cloud API"],
        ["The cloud-side leaning is weak", "M1: \"new session\" is the vendor's label and may be a legitimate new phone"],
        ["The uploads do not separate the hypotheses", "M3: compatible with all four"],
        ["The 4-minute gap is not proof of cause", "Timing relationship only"],
        ["The owner's statement has low weight", "M4: unverified statement"],
        ["H1 is untested, not rejected", "No device, firmware, or network evidence yet (P3, P4, P5)"]
    ]
    story.append(make_table(conc_points, [220, 312]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Next actions if this were a real case:</b> collect P1 to P6 in the Section 3 order and hash each item; "
        "align all clocks and convert to UTC; rerun the matrix with real artifacts and update confidence; "
        "ask the vendor for the full details of the 23:55 session and the 02:10 change; and avoid statements about who acted "
        "unless several independent artifacts support them.",
        body_style
    ))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 27: 8. References (1 to 9)
    # -------------------------------------------------------------------------
    story.append(Paragraph("8. References", h1_style))
    story.append(Paragraph(
        "Each reference was consulted to verify the standard title, edition, publisher, and official URL:",
        body_style
    ))
    story.append(Spacer(1, 6))

    ref_data_1 = [
        ["No.", "Reference", "Used for", "Verified?"],
        ["1", "NIST SP 800-86, Guide to Integrating Forensic Techniques into Incident Response (2006)", "Collecting and examining data from several source types", "Verified (NIST CSRC)"],
        ["2", "NIST SP 800-101 Rev. 1, Guidelines on Mobile Device Forensics (2014)", "Companion app and phone evidence (E5)", "Verified (NIST CSRC)"],
        ["3", "ISO/IEC 27037:2012, Guidelines for identification, collection, acquisition and preservation of digital evidence", "Handling and preserving evidence", "Verified (ISO Catalogue)"],
        ["4", "IETF RFC 3227, Guidelines for Evidence Collection and Archiving (2002)", "Order of volatility", "Verified (IETF RFC Editor)"],
        ["5", "IETF RFC 2606, Reserved Top Level DNS Names (1999)", ".example domains in the synthetic scenario", "Verified (IETF RFC Editor)"],
        ["6", "IETF RFC 5737, IPv4 Address Blocks Reserved for Documentation (2010)", "192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24", "Verified (IETF RFC Editor)"],
        ["7", "NIST FIPS 180-4, Secure Hash Standard (SHS) (2015)", "SHA-256", "Verified (NIST FIPS)"],
        ["8", "NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments (2012)", "Likelihood and impact scoring", "Verified (NIST CSRC)"],
        ["9", "Python documentation: hashlib, argparse, json, datetime (Python 3.11.9)", "The technical artefact", "Verified (docs.python.org)"]
    ]
    story.append(make_table(ref_data_1, [22, 230, 160, 120]))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PAGE 28: Reference 10, Note & 9. AI-Use Disclosure
    # -------------------------------------------------------------------------
    ref_data_2 = [
        ["No.", "Reference", "Used for", "Verified?"],
        ["10", "Documentation for planned tools: flashrom, picocom, tcpdump, Wireshark, dc3dd, FTK Imager", "Acquisition steps (Planned tools, not run)", "Verified (Official project docs)"]
    ]
    story.append(make_table(ref_data_2, [22, 230, 160, 120]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<i>Vendor and product names (Brightwave Labs, LumiCam, LumiView) are invented and verified not to match any commercial smart-camera product. "
        "Reference 11 (Mermaid) was deleted as diagrams in this report are rendered as structured text and ASCII schematics.</i>",
        italic_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("9. AI-Use Disclosure", h1_style))
    story.append(Paragraph(
        "This report was drafted with the help of an AI assistant (Claude, by Anthropic and Gemini, by Google), working step by step "
        "with the student. The AI proposed the synthetic scenario options, the forensic question and hypotheses, the architecture map, "
        "the acquisition plan, the risk register, the evidence matrix, the Python script, the two synthetic log files, and the draft "
        "conclusion and limitations. It ran the script once in its own test environment to check that it works. It did not run any forensic "
        "tool on physical hardware, did not collect or examine real evidence, and produced no real hardware hashes for this case.<br/><br/>"
        "All scenario details, logs, and timings are SYNTHETIC. The student is responsible for reviewing and correcting every section, "
        "running the script on their own machine, pasting real output, verifying references, adjusting judgements and confidence levels, "
        "and defending the work in the viva.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Student declaration:</b> \"I used an AI assistant (Claude and Gemini) to help draft the scenario, plan, report, script, "
        "and defense notes. I ran the script on my own Windows computer (Python 3.11.9) and recorded my own terminal output; "
        "checked each reference against the official source; tested the live tamper demo; and author the qualified conclusions "
        "reflecting that H1 remains untested. I understand the code and can explain and modify it.\"",
        callout_style
    ))
    story.append(Spacer(1, 12))

    sig_data = [
        ["Student Name: DEEPTANSH NAGAR", "Student ID: 500121033", "Project Code: DF-PBL-026"],
        ["Signature: Deeptansh Nagar", "Date: October 27, 2026", "Mode: Investigation Memo"]
    ]
    story.append(make_table(sig_data, [177, 177, 178], is_header=False))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete:", filename)

if __name__ == "__main__":
    build_pdf()
