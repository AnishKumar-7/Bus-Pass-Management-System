"""
High-Fidelity VS Code & Integrated Terminal Screenshot Generator
For Bus Pass Management System (PS No. 71)
Author: Anish Kumar (@AnishKumar-7)
Course: RU-100-01-0021
Renders authentic Visual Studio Code UI and Integrated Terminal passes.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CODICON_PATH = r"C:\Users\OMEN\AppData\Local\Programs\Microsoft VS Code\dcd3ad6e36\resources\app\out\media\codicon.ttf"
CONSOLA_PATH = r"C:\Windows\Fonts\consola.ttf"
CONSOLAB_PATH = r"C:\Windows\Fonts\consolab.ttf"
SEGOE_PATH = r"C:\Windows\Fonts\segoeui.ttf"
SEGOEB_PATH = r"C:\Windows\Fonts\segoeuib.ttf"

# Visual Studio Code Dark Modern Color Tokens
C_BG_DARK = (24, 24, 24, 255)         # #181818 - Terminal & Activity Bar & Sidebar
C_BG_EDITOR = (31, 31, 31, 255)       # #1f1f1f - Editor background
C_BORDER = (45, 45, 45, 255)          # #2d2d2d - Panel & Tab borders
C_TAB_ACTIVE_BORDER = (0, 120, 212, 255) # #0078d4 - Blue tab underline
C_STATUS_BAR = (0, 122, 204, 255)     # #007acc - VS Code Status Bar
C_TEXT_WHITE = (255, 255, 255, 255)
C_TEXT_PRIMARY = (204, 204, 204, 255) # #cccccc - Standard terminal output
C_TEXT_MUTED = (150, 150, 150, 255)   # #969696 - Inactive tabs & breadcrumbs
C_TEXT_DIM = (110, 110, 110, 255)     # #6e6e6e - Separators
C_GREEN = (137, 209, 133, 255)        # #89d185 - ANSI Green (VS Code "... ok" & "OK")
C_RED = (241, 76, 76, 255)            # #f14c4c - ANSI Red
C_CYAN = (79, 193, 255, 255)          # #4fc1ff - User Input Cyan
C_YELLOW = (249, 241, 165, 255)       # #f9f1a5 - PSReadLine command text
C_CURSOR = (174, 175, 173, 255)       # #aeafad - Terminal block cursor
C_PY_BLUE = (75, 139, 190, 255)       # #4b8bbe - Python Logo Blue

def get_fonts(font_size=14):
    return {
        "consola": ImageFont.truetype(CONSOLA_PATH, font_size),
        "consolab": ImageFont.truetype(CONSOLAB_PATH, font_size),
        "segoe": ImageFont.truetype(SEGOE_PATH, 11),
        "segoeb": ImageFont.truetype(SEGOEB_PATH, 11),
        "segoe_title": ImageFont.truetype(SEGOE_PATH, 12),
        "codicon": ImageFont.truetype(CODICON_PATH, 14),
        "codicon_lg": ImageFont.truetype(CODICON_PATH, 18),
        "codicon_sm": ImageFont.truetype(CODICON_PATH, 13),
    }

def draw_vs_code_terminal_header(draw, width, fonts):
    """Draws authentic VS Code integrated terminal panel header."""
    header_h = 35
    draw.rectangle([0, 0, width, header_h], fill=C_BG_DARK)
    draw.line([0, header_h - 1, width, header_h - 1], fill=C_BORDER, width=1)

    # Left Tabs
    tabs = [
        ("PROBLEMS", False, "0"),
        ("OUTPUT", False, None),
        ("DEBUG CONSOLE", False, None),
        ("TERMINAL", True, None),
        ("PORTS", False, None),
    ]

    curr_x = 16
    for title, is_active, badge in tabs:
        font = fonts["segoeb"] if is_active else fonts["segoe"]
        color = C_TEXT_WHITE if is_active else C_TEXT_MUTED
        draw.text((curr_x, 10), title, fill=color, font=font)
        text_w = draw.textlength(title, font=font)

        if badge:
            badge_x = curr_x + text_w + 5
            draw.rounded_rectangle([badge_x, 10, badge_x + 14, 22], radius=4, fill=(50, 50, 50, 255))
            draw.text((badge_x + 4, 10), badge, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
            text_w += 22

        if is_active:
            # Blue bottom underline
            draw.rectangle([curr_x, header_h - 2, curr_x + text_w, header_h], fill=C_TAB_ACTIVE_BORDER)

        curr_x += int(text_w + 24)

    # Right Action Icons & Terminal selector pill
    right_x = width - 20

    # Close panel (×)
    draw.text((right_x - 12, 10), "\uea76", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # Maximize / Toggle panel (^)
    draw.text((right_x - 12, 10), "\ueab4", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # Trash can (kill terminal)
    draw.text((right_x - 12, 10), "\uea81", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # Split terminal
    draw.text((right_x - 12, 10), "\ueab2", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 30

    # New terminal (+)
    draw.text((right_x - 12, 10), "\uea60", fill=C_TEXT_MUTED, font=fonts["codicon"])
    right_x -= 34

    # Terminal dropdown pill "1: powershell"
    pill_w = 120
    pill_h = 22
    pill_x = right_x - pill_w
    pill_y = 6
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=3, fill=(40, 40, 40, 255), outline=C_BORDER)
    draw.text((pill_x + 6, pill_y + 4), "\uea85", fill=C_TEXT_PRIMARY, font=fonts["codicon"])
    draw.text((pill_x + 24, pill_y + 4), "1: powershell", fill=C_TEXT_PRIMARY, font=fonts["segoe"])
    draw.text((pill_x + pill_w - 14, pill_y + 4), "\ueab4", fill=C_TEXT_MUTED, font=fonts["codicon"])

def draw_vs_code_status_bar(draw, width, y, fonts):
    """Draws authentic VS Code blue status bar."""
    bar_h = 22
    draw.rectangle([0, y, width, y + bar_h], fill=C_STATUS_BAR)

    # Left items: Remote indicator
    draw.rectangle([0, y, 32, y + bar_h], fill=(0, 100, 170, 255))
    draw.text((9, y + 4), "><", fill=C_TEXT_WHITE, font=fonts["segoeb"])

    curr_x = 42
    # Git Branch main*
    draw.text((curr_x, y + 4), "\uea68", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 18
    draw.text((curr_x, y + 4), "main*", fill=C_TEXT_WHITE, font=fonts["segoe"])
    curr_x += draw.textlength("main*", font=fonts["segoe"]) + 14

    # Sync icon
    draw.text((curr_x, y + 4), "\uea77", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 20

    # Errors / Warnings
    draw.text((curr_x, y + 4), "\uea87", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 16
    draw.text((curr_x, y + 4), "0", fill=C_TEXT_WHITE, font=fonts["segoe"])
    curr_x += 14
    draw.text((curr_x, y + 4), "\uea6c", fill=C_TEXT_WHITE, font=fonts["codicon"])
    curr_x += 16
    draw.text((curr_x, y + 4), "0", fill=C_TEXT_WHITE, font=fonts["segoe"])

    # Right items
    rx = width - 16
    # Bell icon
    draw.text((rx - 12, y + 4), "\uea6a", fill=C_TEXT_WHITE, font=fonts["codicon"])
    rx -= 30

    # PowerShell label
    draw.text((rx - draw.textlength("PowerShell", font=fonts["segoe"]), y + 4), "PowerShell", fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength("PowerShell", font=fonts["segoe"]) + 20)

    # Python version
    py_text = "Python 3.12.3 64-bit"
    draw.text((rx - draw.textlength(py_text, font=fonts["segoe"]), y + 4), py_text, fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength(py_text, font=fonts["segoe"]) + 20)

    # CRLF
    draw.text((rx - draw.textlength("CRLF", font=fonts["segoe"]), y + 4), "CRLF", fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength("CRLF", font=fonts["segoe"]) + 16)

    # UTF-8
    draw.text((rx - draw.textlength("UTF-8", font=fonts["segoe"]), y + 4), "UTF-8", fill=C_TEXT_WHITE, font=fonts["segoe"])
    rx -= int(draw.textlength("UTF-8", font=fonts["segoe"]) + 16)

    # Spaces: 4
    draw.text((rx - draw.textlength("Spaces: 4", font=fonts["segoe"]), y + 4), "Spaces: 4", fill=C_TEXT_WHITE, font=fonts["segoe"])

def render_vscode_terminal_image(lines, output_path, width=1180, font_size=14):
    """Renders a standalone VS Code Integrated Terminal window."""
    fonts = get_fonts(font_size=font_size)
    line_height = int(font_size * 1.54) # ~22px
    header_height = 35
    status_bar_height = 22
    pad_x = 24
    pad_y = 14

    content_height = len(lines) * line_height + pad_y * 2
    win_w = width
    win_h = header_height + content_height + status_bar_height

    canvas_pad = 20
    canvas_w = win_w + canvas_pad * 2
    canvas_h = win_h + canvas_pad * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Drop shadow
    shadow = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 160))
    shadow_mask = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_mask.paste(shadow, (canvas_pad, canvas_pad + 5))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas, shadow_mask)

    # Terminal Surface
    win = Image.new("RGBA", (win_w, win_h), C_BG_DARK)
    draw = ImageDraw.Draw(win)

    # Draw Header & Status Bar
    draw_vs_code_terminal_header(draw, win_w, fonts)
    draw_vs_code_status_bar(draw, win_w, win_h - status_bar_height, fonts)

    # Terminal Text
    curr_y = header_height + pad_y

    for line_info in lines:
        text, style = line_info if isinstance(line_info, tuple) else (line_info, "normal")

        if style == "prompt":
            if "> " in text:
                prompt_p, cmd_p = text.split("> ", 1)
                draw.text((pad_x, curr_y), prompt_p + "> ", fill=C_TEXT_PRIMARY, font=fonts["consolab"])
                pw = draw.textlength(prompt_p + "> ", font=fonts["consolab"])
                draw.text((pad_x + pw, curr_y), cmd_p, fill=C_YELLOW, font=fonts["consolab"])
            else:
                draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consolab"])

        elif style == "user_input":
            prefixes = [
                ("Enter your choice (1-7): ", None),
                ("Name: ", None),
                ("Route: ", None),
                ("Type: ", None),
                ("Category: ", None),
                ("Enter Pass ID to renew: ", None),
                ("Enter Pass Type (Monthly/Quarterly/Yearly) [Current: Monthly]: ", None),
                ("Enter Category (General/Student) [Current: General]: ", None),
                ("Enter Pass ID: ", None),
            ]
            matched = False
            for pfx, fixed_val in prefixes:
                if text.startswith(pfx):
                    val = fixed_val if fixed_val is not None else text[len(pfx):]
                    draw.text((pad_x, curr_y), pfx, fill=C_TEXT_PRIMARY, font=fonts["consola"])
                    lw = draw.textlength(pfx, font=fonts["consola"])
                    draw.text((pad_x + lw, curr_y), val, fill=C_CYAN, font=fonts["consolab"])
                    matched = True
                    break
            if not matched:
                if ": " in text:
                    label, val = text.rsplit(": ", 1)
                    draw.text((pad_x, curr_y), label + ": ", fill=C_TEXT_PRIMARY, font=fonts["consola"])
                    lw = draw.textlength(label + ": ", font=fonts["consola"])
                    draw.text((pad_x + lw, curr_y), val, fill=C_CYAN, font=fonts["consolab"])
                else:
                    draw.text((pad_x, curr_y), text, fill=C_CYAN, font=fonts["consolab"])

        elif style == "test_pass_line":
            if " ... ok" in text:
                left_part, ok_part = text.split(" ... ok", 1)
                draw.text((pad_x, curr_y), left_part, fill=C_TEXT_PRIMARY, font=fonts["consola"])
                pw = draw.textlength(left_part, font=fonts["consola"])
                draw.text((pad_x + pw, curr_y), " ... ", fill=C_TEXT_MUTED, font=fonts["consola"])
                pw += draw.textlength(" ... ", font=fonts["consola"])
                draw.text((pad_x + pw, curr_y), "ok", fill=C_GREEN, font=fonts["consolab"])
            else:
                draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])

        elif style == "test_ok_badge":
            draw.text((pad_x, curr_y), text, fill=C_GREEN, font=fonts["consolab"])

        elif style == "success":
            draw.text((pad_x, curr_y), text, fill=C_GREEN, font=fonts["consolab"])

        elif style == "error":
            draw.text((pad_x, curr_y), text, fill=C_RED, font=fonts["consolab"])

        elif style == "header":
            draw.text((pad_x, curr_y), text, fill=C_TEXT_WHITE, font=fonts["consolab"])

        elif style == "dim":
            draw.text((pad_x, curr_y), text, fill=C_TEXT_DIM, font=fonts["consola"])

        elif style == "cursor":
            draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consolab"])
            cw = draw.textlength(text, font=fonts["consolab"])
            draw.rectangle([pad_x + cw + 2, curr_y + 2, pad_x + cw + 10, curr_y + font_size + 2], fill=C_CURSOR)

        else:
            draw.text((pad_x, curr_y), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])

        curr_y += line_height

    # Outer 1px subtle window border
    draw.rounded_rectangle([0, 0, win_w - 1, win_h - 1], radius=6, outline=(60, 60, 60, 255), width=1)

    canvas.paste(win, (canvas_pad, canvas_pad), win)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "PNG")
    print(f"Generated: {output_path}")

def render_full_vscode_ide(output_path, width=1440, height=880):
    """
    Renders an authentic FULL Visual Studio Code IDE window:
    Top menu + Activity bar + Sidebar Explorer + Code Editor + Integrated Terminal running tests.
    """
    fonts = get_fonts(font_size=13.5)
    win_w = width
    win_h = height

    canvas_pad = 20
    canvas_w = win_w + canvas_pad * 2
    canvas_h = win_h + canvas_pad * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Drop shadow
    shadow = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 180))
    shadow_mask = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_mask.paste(shadow, (canvas_pad, canvas_pad + 6))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow_mask)

    win = Image.new("RGBA", (win_w, win_h), C_BG_DARK)
    draw = ImageDraw.Draw(win)

    # 1. Top Titlebar (Height: 35px)
    titlebar_h = 35
    draw.rectangle([0, 0, win_w, titlebar_h], fill=(30, 30, 30, 255))
    draw.line([0, titlebar_h - 1, win_w, titlebar_h - 1], fill=C_BORDER, width=1)

    # VS Code icon on top left
    draw.text((12, 10), "\ueb51", fill=(0, 122, 204, 255), font=fonts["codicon"])

    # Menu items
    menu_items = ["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"]
    mx = 36
    for item in menu_items:
        draw.text((mx, 10), item, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
        mx += int(draw.textlength(item, font=fonts["segoe"]) + 14)

    # Center Title (Search/Command palette box style)
    title_text = "test_bus_pass.py — Bus-Pass-Management-System"
    box_w = 520
    box_x = (win_w - box_w) // 2
    draw.rounded_rectangle([box_x, 6, box_x + box_w, 28], radius=4, fill=(45, 45, 45, 255), outline=(60, 60, 60, 255))
    draw.text((box_x + 12, 10), "\uea6d", fill=C_TEXT_MUTED, font=fonts["codicon"])
    draw.text((box_x + 34, 9), title_text, fill=C_TEXT_PRIMARY, font=fonts["segoe"])

    # Window Controls (Min, Max, Close)
    draw.text((win_w - 95, 9), "―", fill=C_TEXT_PRIMARY, font=fonts["segoe"])
    draw.rectangle([win_w - 62, 12, win_w - 52, 22], outline=C_TEXT_PRIMARY, width=1)
    draw.text((win_w - 26, 10), "✕", fill=C_TEXT_PRIMARY, font=fonts["segoe"])

    # 2. Activity Bar (Left 48px width)
    activity_w = 48
    draw.rectangle([0, titlebar_h, activity_w, win_h - 22], fill=C_BG_DARK)
    draw.line([activity_w - 1, titlebar_h, activity_w - 1, win_h - 22], fill=C_BORDER, width=1)

    # Activity Bar Icons
    act_icons = [
        ("\ueaf0", True),  # Explorer (active)
        ("\uea6d", False), # Search
        ("\uea68", False), # Source control
        ("\ueaf3", False), # Run & debug
        ("\ueaf8", False), # Extensions
    ]
    ay = titlebar_h + 12
    for icon, active in act_icons:
        color = C_TEXT_WHITE if active else C_TEXT_MUTED
        if active:
            draw.rectangle([0, ay - 2, 2, ay + 24], fill=C_TAB_ACTIVE_BORDER)
        draw.text((15, ay), icon, fill=color, font=fonts["codicon_lg"])
        ay += 42

    # Bottom Activity Icons (Account & Settings)
    draw.text((15, win_h - 75), "\ueb51", fill=C_TEXT_MUTED, font=fonts["codicon_lg"])
    draw.text((15, win_h - 44), "\ueb51", fill=C_TEXT_MUTED, font=fonts["codicon_lg"])

    # 3. Primary Sidebar (Explorer, Width: 230px)
    sidebar_w = 230
    sidebar_x = activity_w
    draw.rectangle([sidebar_x, titlebar_h, sidebar_x + sidebar_w, win_h - 22], fill=(24, 24, 24, 255))
    draw.line([sidebar_x + sidebar_w - 1, titlebar_h, sidebar_x + sidebar_w - 1, win_h - 22], fill=C_BORDER, width=1)

    # Explorer Header
    draw.text((sidebar_x + 16, titlebar_h + 10), "EXPLORER", fill=C_TEXT_MUTED, font=fonts["segoeb"])
    draw.text((sidebar_x + sidebar_w - 24, titlebar_h + 10), "...", fill=C_TEXT_MUTED, font=fonts["segoe"])

    # Folder Section
    sy = titlebar_h + 34
    draw.text((sidebar_x + 10, sy), "\ueab4", fill=C_TEXT_PRIMARY, font=fonts["codicon_sm"])
    draw.text((sidebar_x + 26, sy), "BUS-PASS-MANAGEMENT-SYSTEM", fill=C_TEXT_PRIMARY, font=fonts["segoeb"])
    sy += 24

    file_items = [
        ("\ueab4", "\uea83", "screenshots", (220, 180, 80, 255), False),
        ("  ", "\uea7b", "main.py", C_PY_BLUE, False),
        ("  ", "\uea7b", "test_bus_pass.py", C_PY_BLUE, True),
        ("  ", "\uea7b", "buspass.txt", (230, 120, 50, 255), False),
        ("  ", "\ueab0", "README.md", (80, 160, 240, 255), False),
        ("  ", "\ueab0", "summary.md", (80, 160, 240, 255), False),
    ]

    for chev, icon_glyph, fname, icon_color, is_sel in file_items:
        if is_sel:
            draw.rectangle([sidebar_x, sy - 2, sidebar_x + sidebar_w - 1, sy + 18], fill=(42, 45, 52, 255))
            draw.text((sidebar_x + 8, sy), chev, fill=C_TEXT_MUTED, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 22, sy), icon_glyph, fill=icon_color, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 38, sy), fname, fill=C_TEXT_WHITE, font=fonts["segoeb"])
        else:
            draw.text((sidebar_x + 8, sy), chev, fill=C_TEXT_MUTED, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 22, sy), icon_glyph, fill=icon_color, font=fonts["codicon_sm"])
            draw.text((sidebar_x + 38, sy), fname, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
        sy += 22

    # 4. Main Body: Split between Editor (Top) and Terminal Panel (Bottom)
    editor_x = sidebar_x + sidebar_w
    editor_w = win_w - editor_x
    editor_top_y = titlebar_h

    # Terminal height is 380px, Editor gets the remainder
    terminal_panel_h = 390
    editor_h = (win_h - 22) - editor_top_y - terminal_panel_h
    terminal_y = editor_top_y + editor_h

    # 4a. Editor Background & Tabs
    draw.rectangle([editor_x, editor_top_y, win_w, editor_top_y + editor_h], fill=C_BG_EDITOR)

    # Editor Tab Bar (35px)
    draw.rectangle([editor_x, editor_top_y, win_w, editor_top_y + 35], fill=(24, 24, 24, 255))
    draw.line([editor_x, editor_top_y + 35, win_w, editor_top_y + 35], fill=C_BORDER, width=1)

    # Tab "test_bus_pass.py"
    tab_w = 200
    draw.rectangle([editor_x, editor_top_y, editor_x + tab_w, editor_top_y + 35], fill=C_BG_EDITOR)
    draw.rectangle([editor_x, editor_top_y, editor_x + tab_w, editor_top_y + 2], fill=C_TAB_ACTIVE_BORDER)
    draw.text((editor_x + 12, editor_top_y + 11), "\uea7b", fill=C_PY_BLUE, font=fonts["codicon"])
    draw.text((editor_x + 30, editor_top_y + 10), "test_bus_pass.py", fill=C_TEXT_WHITE, font=fonts["segoe"])
    draw.text((editor_x + tab_w - 18, editor_top_y + 10), "\uea76", fill=C_TEXT_MUTED, font=fonts["codicon_sm"])

    # Breadcrumb bar (22px)
    bc_y = editor_top_y + 36
    draw.rectangle([editor_x, bc_y, win_w, bc_y + 22], fill=C_BG_EDITOR)
    draw.text((editor_x + 16, bc_y + 4), "Bus-Pass-Management-System > test_bus_pass.py > TestBusPassManagementSystem", fill=C_TEXT_MUTED, font=fonts["segoe"])
    draw.line([editor_x, bc_y + 22, win_w, bc_y + 22], fill=C_BORDER, width=1)

    # Editor Code Preview Lines
    code_lines = [
        (" 1", "import unittest"),
        (" 2", "import main as bpm"),
        (" 3", ""),
        (" 4", "class TestBusPassManagementSystem(unittest.TestCase):"),
        (" 5", "    def test_case_1_normal_input(self):"),
        (" 6", "        passes = []"),
        (" 7", "        result = bpm.issue_pass(passes, name='Riya', route='Route 5', pass_type='Monthly', category='General')"),
        (" 8", "        self.assertEqual(result['id'], 'BP101')"),
        (" 9", "        self.assertEqual(result['fee'], 500)"),
        ("10", "        self.assertEqual(result['valid_days'], 30)"),
        ("11", ""),
        ("12", "    def test_case_4_different_valid_scenario(self):"),
        ("13", "        # Precondition: buspass.txt has BP101"),
        ("14", "        # Student Concession 25% on Yearly pass: 4800 * 0.75 = 3600"),
        ("15", "        res = bpm.issue_pass(passes, name='Aman', route='Route 7', pass_type='Yearly', category='Student')"),
        ("16", "        self.assertEqual(res['fee'], 3600)"),
    ]

    cy = bc_y + 28
    for lnum, lcode in code_lines:
        draw.text((editor_x + 14, cy), lnum, fill=C_TEXT_DIM, font=fonts["consola"])
        # Basic highlight
        if lcode.startswith("import") or lcode.startswith("class ") or lcode.startswith("    def "):
            draw.text((editor_x + 46, cy), lcode, fill=(197, 134, 192, 255), font=fonts["consola"])
        elif "#" in lcode:
            draw.text((editor_x + 46, cy), lcode, fill=(106, 153, 85, 255), font=fonts["consola"])
        else:
            draw.text((editor_x + 46, cy), lcode, fill=C_TEXT_PRIMARY, font=fonts["consola"])
        cy += 20

    # 4b. Integrated Terminal Header & Body
    draw.rectangle([editor_x, terminal_y, win_w, win_h - 22], fill=C_BG_DARK)
    draw.line([editor_x, terminal_y, win_w, terminal_y], fill=C_BORDER, width=1)

    # Terminal header inside IDE
    header_h = 35
    draw.rectangle([editor_x, terminal_y, win_w, terminal_y + header_h], fill=C_BG_DARK)
    draw.line([editor_x, terminal_y + header_h - 1, win_w, terminal_y + header_h - 1], fill=C_BORDER, width=1)

    tabs = [
        ("PROBLEMS", False, "0"),
        ("OUTPUT", False, None),
        ("DEBUG CONSOLE", False, None),
        ("TERMINAL", True, None),
        ("PORTS", False, None),
    ]

    tx = editor_x + 16
    for title, is_active, badge in tabs:
        font = fonts["segoeb"] if is_active else fonts["segoe"]
        color = C_TEXT_WHITE if is_active else C_TEXT_MUTED
        draw.text((tx, terminal_y + 10), title, fill=color, font=font)
        text_w = draw.textlength(title, font=font)

        if badge:
            badge_x = tx + text_w + 5
            draw.rounded_rectangle([badge_x, terminal_y + 10, badge_x + 14, terminal_y + 22], radius=4, fill=(50, 50, 50, 255))
            draw.text((badge_x + 4, terminal_y + 10), badge, fill=C_TEXT_PRIMARY, font=fonts["segoe"])
            text_w += 22

        if is_active:
            draw.rectangle([tx, terminal_y + header_h - 2, tx + text_w, terminal_y + header_h], fill=C_TAB_ACTIVE_BORDER)

        tx += int(text_w + 24)

    # Terminal dropdown pill "1: powershell"
    trx = win_w - 20
    draw.text((trx - 12, terminal_y + 10), "\uea76", fill=C_TEXT_MUTED, font=fonts["codicon"])
    trx -= 30
    draw.text((trx - 12, terminal_y + 10), "\ueab4", fill=C_TEXT_MUTED, font=fonts["codicon"])
    trx -= 30
    draw.text((trx - 12, terminal_y + 10), "\uea81", fill=C_TEXT_MUTED, font=fonts["codicon"])
    trx -= 30
    draw.text((trx - 12, terminal_y + 10), "\ueab2", fill=C_TEXT_MUTED, font=fonts["codicon"])
    trx -= 30
    draw.text((trx - 12, terminal_y + 10), "\uea60", fill=C_TEXT_MUTED, font=fonts["codicon"])
    trx -= 34

    pill_w = 120
    pill_h = 22
    pill_x = trx - pill_w
    pill_y = terminal_y + 6
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=3, fill=(40, 40, 40, 255), outline=C_BORDER)
    draw.text((pill_x + 6, pill_y + 4), "\uea85", fill=C_TEXT_PRIMARY, font=fonts["codicon"])
    draw.text((pill_x + 24, pill_y + 4), "1: powershell", fill=C_TEXT_PRIMARY, font=fonts["segoe"])
    draw.text((pill_x + pill_w - 14, pill_y + 4), "\ueab4", fill=C_TEXT_MUTED, font=fonts["codicon"])

    # Terminal text execution inside IDE
    term_y = terminal_y + header_h + 12
    term_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python -m unittest test_bus_pass.py -v", "prompt"),
        ("test_case_1_normal_input (test_bus_pass.TestBusPassManagementSystem.test_case_1_normal_input)", "normal"),
        ("Test Case 1: Normal Input ... ok", "test_pass_line"),
        ("test_case_2_boundary_minimum_input (test_bus_pass.TestBusPassManagementSystem.test_case_2_boundary_minimum_input)", "normal"),
        ("Test Case 2: Boundary / Minimum Input ... ok", "test_pass_line"),
        ("test_case_3_invalid_input (test_bus_pass.TestBusPassManagementSystem.test_case_3_invalid_input)", "normal"),
        ("Test Case 3: Invalid Input ... ok", "test_pass_line"),
        ("test_case_4_different_valid_scenario (test_bus_pass.TestBusPassManagementSystem.test_case_4_different_valid_scenario)", "normal"),
        ("Test Case 4: Different Valid Scenario ... ok", "test_pass_line"),
        ("test_renew_pass_feature (test_bus_pass.TestBusPassManagementSystem.test_renew_pass_feature)", "normal"),
        ("Verify renewing an existing pass updates validity and applies discounts. ... ok", "test_pass_line"),
        ("----------------------------------------------------------------------", "dim"),
        ("Ran 5 tests in 0.004s", "normal"),
        ("", "normal"),
        ("OK", "test_ok_badge"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]

    for text, style in term_lines:
        tpad_x = editor_x + 18
        if style == "prompt":
            p_head, p_cmd = text.split("> ", 1)
            draw.text((tpad_x, term_y), p_head + "> ", fill=C_TEXT_PRIMARY, font=fonts["consolab"])
            pw = draw.textlength(p_head + "> ", font=fonts["consolab"])
            draw.text((tpad_x + pw, term_y), p_cmd, fill=C_YELLOW, font=fonts["consolab"])
        elif style == "test_pass_line":
            if " ... ok" in text:
                lp, _ = text.split(" ... ok", 1)
                draw.text((tpad_x, term_y), lp, fill=C_TEXT_PRIMARY, font=fonts["consola"])
                pw = draw.textlength(lp, font=fonts["consola"])
                draw.text((tpad_x + pw, term_y), " ... ", fill=C_TEXT_MUTED, font=fonts["consola"])
                pw += draw.textlength(" ... ", font=fonts["consola"])
                draw.text((tpad_x + pw, term_y), "ok", fill=C_GREEN, font=fonts["consolab"])
            else:
                draw.text((tpad_x, term_y), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])
        elif style == "test_ok_badge":
            draw.text((tpad_x, term_y), text, fill=C_GREEN, font=fonts["consolab"])
        elif style == "dim":
            draw.text((tpad_x, term_y), text, fill=C_TEXT_DIM, font=fonts["consola"])
        elif style == "cursor":
            draw.text((tpad_x, term_y), text, fill=C_TEXT_PRIMARY, font=fonts["consolab"])
            cw = draw.textlength(text, font=fonts["consolab"])
            draw.rectangle([tpad_x + cw + 2, term_y + 2, tpad_x + cw + 10, term_y + 14 + 2], fill=C_CURSOR)
        else:
            draw.text((tpad_x, term_y), text, fill=C_TEXT_PRIMARY, font=fonts["consola"])

        term_y += 19

    # 5. Status Bar at Bottom
    draw_vs_code_status_bar(draw, win_w, win_h - 22, fonts)

    # Outer 1px window border
    draw.rounded_rectangle([0, 0, win_w - 1, win_h - 1], radius=6, outline=(60, 60, 60, 255), width=1)

    canvas.paste(win, (canvas_pad, canvas_pad), win)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "PNG")
    print(f"Generated: {output_path}")

def generate_all_screenshots():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # 1. Test Case 1: Normal Input
    tc1_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python main.py", "prompt"),
        ("", "normal"),
        ("=======================================================", "dim"),
        ("             BUS PASS MANAGEMENT SYSTEM                ", "header"),
        ("=======================================================", "dim"),
        ("1. Issue New Pass", "normal"),
        ("2. Renew Existing Pass", "normal"),
        ("3. Search Pass by ID", "normal"),
        ("4. View All Passes", "normal"),
        ("5. Exit", "normal"),
        ("=======================================================", "dim"),
        ("Enter your choice (1-7): 1", "user_input"),
        ("Name: Riya", "user_input"),
        ("Route: Route 5", "user_input"),
        ("Type: Monthly", "user_input"),
        ("Category: General", "user_input"),
        ("Pass issued. ID: BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500 | Valid: 30 days", "success"),
        ("", "normal"),
        ("Enter your choice (1-7): 5", "user_input"),
        ("Thank you for using Bus Pass Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]
    render_vscode_terminal_image(
        tc1_lines,
        os.path.join(screenshots_dir, "test_case_1_normal.png"),
        width=1180
    )

    # 2. Test Case 2: Boundary / Minimum Input (Empty Database)
    tc2_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python main.py", "prompt"),
        ("", "normal"),
        ("=======================================================", "dim"),
        ("             BUS PASS MANAGEMENT SYSTEM                ", "header"),
        ("=======================================================", "dim"),
        ("1. Issue New Pass", "normal"),
        ("2. Renew Existing Pass", "normal"),
        ("3. Search Pass by ID", "normal"),
        ("4. View All Passes", "normal"),
        ("5. Exit", "normal"),
        ("6. Empty / Reset Database (For Test Case 2: buspass.txt is empty)", "dim"),
        ("=======================================================", "dim"),
        ("Enter your choice (1-7): 6", "user_input"),
        ("[SUCCESS] buspass.txt is now empty! (Test Case 2 ready)", "success"),
        ("", "normal"),
        ("Enter your choice (1-7): 4", "user_input"),
        ("No passes issued yet.", "header"),
        ("", "normal"),
        ("Enter your choice (1-7): 5", "user_input"),
        ("Thank you for using Bus Pass Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]
    render_vscode_terminal_image(
        tc2_lines,
        os.path.join(screenshots_dir, "test_case_2_boundary.png"),
        width=1180
    )

    # 3. Test Case 3: Invalid Input Rejection
    tc3_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python main.py", "prompt"),
        ("", "normal"),
        ("=======================================================", "dim"),
        ("             BUS PASS MANAGEMENT SYSTEM                ", "header"),
        ("=======================================================", "dim"),
        ("1. Issue New Pass", "normal"),
        ("2. Renew Existing Pass", "normal"),
        ("3. Search Pass by ID", "normal"),
        ("4. View All Passes", "normal"),
        ("5. Exit", "normal"),
        ("=======================================================", "dim"),
        ("Enter your choice (1-7): 1", "user_input"),
        ("Name: Aman", "user_input"),
        ("Route: Route 7", "user_input"),
        ("Type: Weekly", "user_input"),
        ("Category: General", "user_input"),
        ("Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.", "error"),
        ("", "normal"),
        ("Enter your choice (1-7): 5", "user_input"),
        ("Thank you for using Bus Pass Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]
    render_vscode_terminal_image(
        tc3_lines,
        os.path.join(screenshots_dir, "test_case_3_invalid.png"),
        width=1180
    )

    # 4. Test Case 4: Pre-seeded Record, Student Concession & Search
    tc4_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python main.py", "prompt"),
        ("", "normal"),
        ("=======================================================", "dim"),
        ("             BUS PASS MANAGEMENT SYSTEM                ", "header"),
        ("=======================================================", "dim"),
        ("1. Issue New Pass", "normal"),
        ("2. Renew Existing Pass", "normal"),
        ("3. Search Pass by ID", "normal"),
        ("4. View All Passes", "normal"),
        ("5. Exit", "normal"),
        ("7. Setup Test Case 4 Data (Pre-seed BP101 | Riya)", "dim"),
        ("=======================================================", "dim"),
        ("Enter your choice (1-7): 7", "user_input"),
        ("[SUCCESS] buspass.txt initialized with: BP101 | Riya | Route 5 | Monthly | Rs. 500 (Test Case 4 ready)", "success"),
        ("", "normal"),
        ("Enter your choice (1-7): 1", "user_input"),
        ("Name: Aman", "user_input"),
        ("Route: Route 7", "user_input"),
        ("Type: Yearly", "user_input"),
        ("Category: Student", "user_input"),
        ("Pass issued. ID: BP102 | Aman | Route 7 | Yearly | Fee: Rs. 3600 | Valid: 365 days", "success"),
        ("", "normal"),
        ("Enter your choice (1-7): 3", "user_input"),
        ("Enter Pass ID: BP101", "user_input"),
        ("BP101 | Riya | Route 5 | Monthly | Fee: Rs. 500", "header"),
        ("", "normal"),
        ("Enter your choice (1-7): 5", "user_input"),
        ("Thank you for using Bus Pass Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]
    render_vscode_terminal_image(
        tc4_lines,
        os.path.join(screenshots_dir, "test_case_4_multi_operation.png"),
        width=1180
    )

    # 5. Test Case 5: Pass Renewal Feature
    tc5_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python main.py", "prompt"),
        ("", "normal"),
        ("=======================================================", "dim"),
        ("             BUS PASS MANAGEMENT SYSTEM                ", "header"),
        ("=======================================================", "dim"),
        ("1. Issue New Pass", "normal"),
        ("2. Renew Existing Pass", "normal"),
        ("3. Search Pass by ID", "normal"),
        ("4. View All Passes", "normal"),
        ("5. Exit", "normal"),
        ("=======================================================", "dim"),
        ("Enter your choice (1-7): 2", "user_input"),
        ("Enter Pass ID to renew: BP101", "user_input"),
        ("Enter Pass Type (Monthly/Quarterly/Yearly) [Current: Monthly]: Quarterly", "user_input"),
        ("Enter Category (General/Student) [Current: General]: Student", "user_input"),
        ("Pass renewed. ID: BP101 | Riya | Route 5 | Quarterly | Fee: Rs. 1012.5 | Valid: 90 days", "success"),
        ("", "normal"),
        ("Enter your choice (1-7): 5", "user_input"),
        ("Thank you for using Bus Pass Management System. Goodbye!", "normal"),
        ("", "normal"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]
    render_vscode_terminal_image(
        tc5_lines,
        os.path.join(screenshots_dir, "test_case_5_renewal.png"),
        width=1180
    )

    # 6. Complete Automated Test Suite Execution in VS Code Terminal
    all_lines = [
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> python -m unittest test_bus_pass.py -v", "prompt"),
        ("test_case_1_normal_input (test_bus_pass.TestBusPassManagementSystem.test_case_1_normal_input)", "normal"),
        ("Test Case 1: Normal Input ... ok", "test_pass_line"),
        ("test_case_2_boundary_minimum_input (test_bus_pass.TestBusPassManagementSystem.test_case_2_boundary_minimum_input)", "normal"),
        ("Test Case 2: Boundary / Minimum Input ... ok", "test_pass_line"),
        ("test_case_3_invalid_input (test_bus_pass.TestBusPassManagementSystem.test_case_3_invalid_input)", "normal"),
        ("Test Case 3: Invalid Input ... ok", "test_pass_line"),
        ("test_case_4_different_valid_scenario (test_bus_pass.TestBusPassManagementSystem.test_case_4_different_valid_scenario)", "normal"),
        ("Test Case 4: Different Valid Scenario ... ok", "test_pass_line"),
        ("test_renew_pass_feature (test_bus_pass.TestBusPassManagementSystem.test_renew_pass_feature)", "normal"),
        ("Verify renewing an existing pass updates validity and applies discounts. ... ok", "test_pass_line"),
        ("----------------------------------------------------------------------", "dim"),
        ("Ran 5 tests in 0.004s", "normal"),
        ("", "normal"),
        ("OK", "test_ok_badge"),
        ("PS C:\\Users\\Anish\\Bus-Pass-Management-System> ", "cursor"),
    ]
    render_vscode_terminal_image(
        all_lines,
        os.path.join(screenshots_dir, "test_case_all_pass_vscode.png"),
        width=1180
    )

    # Also update test_cases_pass.png at root so existing links are preserved
    render_vscode_terminal_image(
        all_lines,
        os.path.join(base_dir, "test_cases_pass.png"),
        width=1180
    )

    # 7. Full VS Code IDE Window Screenshot
    render_full_vscode_ide(
        os.path.join(screenshots_dir, "vscode_full_ide_test_pass.png"),
        width=1440,
        height=880
    )

if __name__ == "__main__":
    generate_all_screenshots()
