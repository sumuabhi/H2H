import flet as ft  # pyright: ignore[reportMissingImports]
import requests
from datetime import datetime
from quest_view import build_quest_view

# Paste your Firebase Realtime Database URL here (without trailing slash)
FIREBASE_URL = "https://heart2heart-29673-default-rtdb.firebaseio.com"
ROOM_PATH = f"{FIREBASE_URL}/heart2heart_room.json"

# Y2K Color Palette
Y2K_BG = "#FFF0F8"           # Pearl Bubblegum Pink
Y2K_CARD = "#FFFFFF"         # Glossy White
Y2K_PINK = "#FF4DA6"         # Hot Y2K Magenta-Pink
Y2K_PINK_SOFT = "#FFD6EB"    # Pastel Pink Highlight
Y2K_LILAC = "#F3E5FF"        # Cyber Lavender
Y2K_LILAC_BORDER = "#B565FF" # Electric Lilac
Y2K_INK = "#3D0C2E"          # Deep Berry Outline/Text
Y2K_SUBTEXT = "#7D3C68"      # Muted Plum

QUICK_EMOJIS = ["🥳", "🥺", "😞", "🪫", "🫂", "💖", "😭", "😴", "🌸", "🧸", "✨", "💌", "🫶", "🦋", "💿", "🎀"]

DEFAULT_STATE = {
    "Mekuri": {
        "latest_status": {
            "emoji": "💖",
            "phrase": "share your lore with the loml!!",
            "percentage": 100,
            "slider_label": "Intensity",
            "no_reply": False,
            "updated_at": "Just now",
        },
        "slider_config": {
            "label": "Intensity",
            "min": 0,
            "max": 100,
            "step": 5,
        },
        "moods": [
            {"emoji": "💖", "phrase": "share your lore with the loml!!"},
        ],
    },
    "Puwali": {
        "latest_status": {
            "emoji": "💖",
            "phrase": "share your lore with the loml!!",
            "percentage": 100,
            "slider_label": "Intensity",
            "no_reply": False,
            "updated_at": "Just now",
        },
        "slider_config": {
            "label": "Intensity",
            "min": 0,
            "max": 100,
            "step": 5,
        },
        "moods": [
            {"emoji": "💖", "phrase": "share your lore with the loml!!"},
        ],
    },
    "reassurances": [
        {
            "sender": "Puwali",
            "text": "share your lore with the loml!!",
            "time": "Pinned",
        }
    ],
}


def y2k_shadow(color=Y2K_PINK_SOFT):
    return ft.BoxShadow(
        spread_radius=0,
        blur_radius=0,
        color=color,
        offset=ft.Offset(3, 3),
    )


def fetch_cloud_state():
    try:
        res = requests.get(ROOM_PATH, timeout=5)
        if res.status_code == 200 and res.json():
            return res.json()
    except Exception:
        pass
    return DEFAULT_STATE.copy()


def push_cloud_state(state):
    try:
        requests.put(ROOM_PATH, json=state, timeout=5)
        return True
    except Exception:
        return False


def main(page: ft.Page):
    page.title = "✧ Heart2Heart ✧"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = Y2K_BG
    page.window.width = 435
    page.window.height = 855

    state = fetch_cloud_state()
    current_user = "Mekuri"
    selected_index = 0

    def partner_of(user):
        return "Puwali" if user == "Mekuri" else "Mekuri"

    def get_slider_cfg(user):
        return state.get(user, {}).setdefault(
            "slider_config", {"label": "Intensity", "min": 0, "max": 100, "step": 5}
        )

    # --- PARTNER LIVE STATUS BANNER (Y2K HOLO CARD) ---
    partner_tag = ft.Text("★ PARTNER STATUS ★", size=10, weight=ft.FontWeight.BOLD, color=Y2K_LILAC_BORDER)
    partner_card_text = ft.Text("", size=15, weight=ft.FontWeight.BOLD, color=Y2K_INK)
    partner_card_sub = ft.Text("", size=12, color=Y2K_SUBTEXT)
    feedback_text = ft.Text("", size=13, color=Y2K_PINK, weight=ft.FontWeight.BOLD)

    def update_partner_banner():
        partner = partner_of(current_user)
        p_status = state.get(partner, {}).get("latest_status", {})
        emoji = p_status.get("emoji", "💖")
        phrase = p_status.get("phrase", "share your lore with the loml!!")
        pct = p_status.get("percentage", 100)
        s_label = p_status.get("slider_label", "Intensity")
        time_str = p_status.get("updated_at", "")
        no_rep = " • [🪫 low-battery: no reply needed]" if p_status.get("no_reply") else ""

        # Check if partner recently entered LoveQuest
        ping = state.get("quest", {}).get("active_ping")
        quest_ping_str = ""
        if ping and ping.get("sender") == partner:
            quest_ping_str = f" • 🔔 Entered LoveQuest at {ping.get('time')}!"

        partner_card_text.value = f"{partner}: {emoji} \"{phrase}\" [{s_label}: {pct}%]"
        partner_card_sub.value = f"Updated: {time_str}{no_rep}{quest_ping_str}"

    def sync_from_cloud(e=None):
        nonlocal state
        state = fetch_cloud_state()
        apply_slider_config()
        update_partner_banner()
        refresh_mood_list()
        refresh_notes()
        feedback_text.value = "✧ Synced latest updates! ✧"
        page.update()

    # User Switcher ("Mekuri" vs "Puwali")
    def set_user(user_name):
        nonlocal current_user, selected_index
        current_user = user_name
        selected_index = 0
        mekuri_btn.bgcolor = Y2K_PINK if current_user == "Mekuri" else Y2K_CARD
        mekuri_btn.color = "white" if current_user == "Mekuri" else Y2K_INK
        puwali_btn.bgcolor = Y2K_PINK if current_user == "Puwali" else Y2K_CARD
        puwali_btn.color = "white" if current_user == "Puwali" else Y2K_INK
        apply_slider_config()
        update_partner_banner()
        refresh_mood_list()
        page.update()

    mekuri_btn = ft.Button(
        content="🎀 Mekuri",
        bgcolor=Y2K_PINK,
        color="white",
        on_click=lambda e: set_user("Mekuri"),
    )
    puwali_btn = ft.Button(
        content="💿 Puwali",
        bgcolor=Y2K_CARD,
        color=Y2K_INK,
        on_click=lambda e: set_user("Puwali"),
    )
    user_selector = ft.Row([mekuri_btn, puwali_btn], spacing=6)

    partner_banner = ft.Container(
        bgcolor=Y2K_LILAC,
        border=ft.Border.all(2, Y2K_LILAC_BORDER),
        border_radius=18,
        padding=12,
        shadow=y2k_shadow("#DFBFFF"),
        content=ft.Row(
            [
                ft.Column([partner_tag, partner_card_text, partner_card_sub], expand=True, spacing=2),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_color=Y2K_LILAC_BORDER,
                    tooltip="Sync latest updates",
                    on_click=sync_from_cloud,
                ),
            ]
        ),
    )

    # --- CUSTOMIZABLE PERCENTAGE SLIDER ---
    percent_text = ft.Text("Intensity: 80%", size=15, weight=ft.FontWeight.BOLD, color=Y2K_INK, expand=True)
    no_reply_checkbox = ft.Checkbox(
        label="🪫 Low-battery mode (no reply needed right now)",
        value=False,
        active_color=Y2K_PINK,
    )

    def on_slider_change(e):
        cfg = get_slider_cfg(current_user)
        percent_text.value = f"✦ {cfg['label']}: {int(e.control.value)}%"
        page.update()

    intensity_slider = ft.Slider(
        min=0,
        max=100,
        divisions=20,
        value=80,
        active_color=Y2K_PINK,
        inactive_color=Y2K_PINK_SOFT,
        thumb_color=Y2K_LILAC_BORDER,
        on_change=on_slider_change,
    )

    def apply_slider_config():
        cfg = get_slider_cfg(current_user)
        s_min = int(cfg.get("min", 0))
        s_max = int(cfg.get("max", 100))
        s_step = max(1, int(cfg.get("step", 5)))
        if s_max <= s_min:
            s_max = s_min + 10

        intensity_slider.min = s_min
        intensity_slider.max = s_max
        intensity_slider.divisions = max(1, (s_max - s_min) // s_step)

        clamped_val = min(max(int(intensity_slider.value), s_min), s_max)
        intensity_slider.value = clamped_val
        percent_text.value = f"✦ {cfg.get('label', 'Intensity')}: {clamped_val}%"

    def open_slider_settings(e):
        cfg = get_slider_cfg(current_user)
        label_field = ft.TextField(label="Bar Label (e.g., Intensity, Battery, Love)", value=cfg.get("label", "Intensity"))
        min_field = ft.TextField(label="Min %", value=str(cfg.get("min", 0)), width=95)
        max_field = ft.TextField(label="Max %", value=str(cfg.get("max", 100)), width=95)
        step_field = ft.TextField(label="Step %", value=str(cfg.get("step", 5)), width=95)

        def save_slider_cfg(ev):
            try:
                new_min = int(min_field.value)
                new_max = int(max_field.value)
                new_step = max(1, int(step_field.value))
                if new_max <= new_min:
                    new_max = new_min + 10
            except ValueError:
                return

            state[current_user]["slider_config"] = {
                "label": label_field.value.strip() or "Intensity",
                "min": new_min,
                "max": new_max,
                "step": new_step,
            }
            push_cloud_state(state)
            apply_slider_config()
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("✧ Customize Percentage Bar ✧", color=Y2K_INK),
            content=ft.Column(
                [
                    label_field,
                    ft.Row([min_field, max_field, step_field], spacing=8),
                ],
                tight=True,
                spacing=12,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda ev: setattr(dialog, "open", False) or page.update()),
                ft.Button(content="Save Bar", bgcolor=Y2K_PINK, color="white", on_click=save_slider_cfg),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # --- CUSTOMIZABLE EMOJIS & PHRASES ---
    mood_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=210)

    def open_edit_dialog(index=None):
        user_moods = state[current_user]["moods"]
        is_new = index is None
        emoji_field = ft.TextField(
            label="Emoji",
            value="💖" if is_new else user_moods[index]["emoji"],
            width=85,
            text_align=ft.TextAlign.CENTER,
        )
        phrase_field = ft.TextField(
            label="Custom Phrase",
            value="" if is_new else user_moods[index]["phrase"],
            expand=True,
        )

        def pick_quick_emoji(em):
            emoji_field.value = em
            page.update()

        emoji_picker_row = ft.Row(
            wrap=True,
            spacing=4,
            controls=[
                ft.TextButton(
                    content=ft.Text(em, size=20),
                    style=ft.ButtonStyle(padding=4),
                    on_click=lambda ev, chosen=em: pick_quick_emoji(chosen),
                )
                for em in QUICK_EMOJIS
            ],
        )

        def save_mood(ev):
            if not phrase_field.value.strip():
                return
            entry = {
                "emoji": emoji_field.value.strip() or "💬",
                "phrase": phrase_field.value.strip(),
            }
            if is_new:
                state[current_user]["moods"].append(entry)
            else:
                state[current_user]["moods"][index] = entry
            push_cloud_state(state)
            dialog.open = False
            refresh_mood_list()
            page.update()

        def delete_mood(ev):
            nonlocal selected_index
            if len(state[current_user]["moods"]) <= 1:
                return
            state[current_user]["moods"].pop(index)
            selected_index = 0
            push_cloud_state(state)
            dialog.open = False
            refresh_mood_list()
            page.update()

        actions = [
            ft.TextButton("Cancel", on_click=lambda ev: setattr(dialog, "open", False) or page.update()),
            ft.Button(content="Save", bgcolor=Y2K_PINK, color="white", on_click=save_mood),
        ]
        if not is_new:
            actions.insert(
                0,
                ft.TextButton(
                    "Delete",
                    style=ft.ButtonStyle(color="#C92A2A"),
                    on_click=delete_mood,
                ),
            )

        dialog = ft.AlertDialog(
            title=ft.Text("✧ Add Mood Shortcut ✧" if is_new else "✧ Customize Emoji & Phrase ✧", color=Y2K_INK),
            content=ft.Column(
                [
                    ft.Row([emoji_field, phrase_field]),
                    ft.Text("Tap an emoji below or type any emoji above:", size=12, color=Y2K_SUBTEXT),
                    emoji_picker_row,
                ],
                tight=True,
                spacing=10,
            ),
            actions=actions,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        
    def select_mood(index):
        nonlocal selected_index
        selected_index = index
        refresh_mood_list()
        page.update()

    def refresh_mood_list():
        mood_column.controls.clear()
        user_moods = state[current_user]["moods"]
        for idx, item in enumerate(user_moods):
            is_selected = idx == selected_index
            card = ft.Container(
                bgcolor=Y2K_PINK_SOFT if is_selected else Y2K_CARD,
                border=ft.Border.all(2, Y2K_PINK if is_selected else Y2K_INK),
                border_radius=16,
                padding=8,
                shadow=y2k_shadow(Y2K_PINK if is_selected else Y2K_PINK_SOFT),
                on_click=lambda e, i=idx: select_mood(i),
                content=ft.Row(
                    [
                        ft.Text(item["emoji"], size=22),
                        ft.Text(item["phrase"], size=14, expand=True, weight=ft.FontWeight.W_600, color=Y2K_INK),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=Y2K_PINK,
                            tooltip="Edit emoji or phrase",
                            on_click=lambda e, i=idx: open_edit_dialog(i),
                        ),
                    ]
                ),
            )
            mood_column.controls.append(card)

    def handle_post_status(e):
        mood = state[current_user]["moods"][selected_index]
        cfg = get_slider_cfg(current_user)
        pct = int(intensity_slider.value)
        now_str = datetime.now().strftime("%I:%M %p, %b %d")

        state[current_user]["latest_status"] = {
            "emoji": mood["emoji"],
            "phrase": mood["phrase"],
            "percentage": pct,
            "slider_label": cfg.get("label", "Intensity"),
            "no_reply": no_reply_checkbox.value,
            "updated_at": now_str,
        }
        ok = push_cloud_state(state)
        feedback_text.value = (
            f"✧ Updated: {mood['emoji']} {mood['phrase']} ({cfg.get('label', 'Intensity')}: {pct}%) ✧"
            if ok
            else "Saved locally — paste your Firebase URL to sync across devices!"
        )
        page.update()

    # --- TAB 1: CHECK-IN ---
    apply_slider_config()
    update_partner_banner()
    refresh_mood_list()

    slider_box = ft.Container(
        bgcolor=Y2K_CARD,
        border=ft.Border.all(2, Y2K_INK),
        border_radius=18,
        padding=12,
        shadow=y2k_shadow(Y2K_PINK_SOFT),
        content=ft.Column(
            [
                ft.Row(
                    [
                        percent_text,
                        ft.IconButton(
                            icon=ft.Icons.TUNE,
                            icon_color=Y2K_PINK,
                            tooltip="Customize percentage bar (Min, Max, Step, Label)",
                            on_click=open_slider_settings,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                intensity_slider,
                no_reply_checkbox,
            ],
            spacing=2,
        ),
    )

    checkin_view = ft.Column(
        [
            partner_banner,
            ft.Row(
                [
                    ft.Text("♡ Pick your vibe:", size=15, weight=ft.FontWeight.BOLD, color=Y2K_INK, expand=True),
                    ft.TextButton("+ New Vibe", on_click=lambda e: open_edit_dialog(None)),
                ]
            ),
            mood_column,
            slider_box,
            ft.Button(
                content="✧ Send Heart2Heart Update 💌 ✧",
                bgcolor=Y2K_PINK,
                color="white",
                height=48,
                width=400,
                on_click=handle_post_status,
            ),
            feedback_text,
        ],
        spacing=8,
    )

    # --- TAB 2: REASSURANCE JAR ---
    notes_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=340)
    new_note_input = ft.TextField(
        hint_text="share your lore with the loml!! (｡•́‿•̀｡)",
        bgcolor=Y2K_CARD,
        border_color=Y2K_INK,
        border_radius=14,
        expand=True,
    )

    def refresh_notes():
        notes_column.controls.clear()
        for note in reversed(state.get("reassurances", [])):
            notes_column.controls.append(
                ft.Container(
                    bgcolor=Y2K_CARD,
                    border_radius=16,
                    padding=12,
                    border=ft.Border.all(2, Y2K_INK),
                    shadow=y2k_shadow("#DFBFFF"),
                    content=ft.Column(
                        [
                            ft.Text(note["text"], size=14, color=Y2K_INK),
                            ft.Text(f"♡ {note['sender']} • {note['time']}", size=11, color=Y2K_SUBTEXT),
                        ],
                        spacing=4,
                    ),
                )
            )

    def add_note(e):
        if not new_note_input.value.strip():
            return
        state.setdefault("reassurances", []).append(
            {
                "sender": current_user,
                "text": new_note_input.value.strip(),
                "time": datetime.now().strftime("%I:%M %p"),
            }
        )
        push_cloud_state(state)
        new_note_input.value = ""
        refresh_notes()
        page.update()

    refresh_notes()
    reassurance_view = ft.Column(
        [
            ft.Text("✧ Reassurance Jar 💖 ✧", size=18, weight=ft.FontWeight.BOLD, color=Y2K_INK),
            ft.Row([new_note_input, ft.Button(content="Post 💌", bgcolor=Y2K_PINK, color="white", on_click=add_note)]),
            notes_column,
        ],
        spacing=10,
    )

    # --- TAB 3: LOVEQUEST TREASURE HUNT ---
    treasure_view, on_enter_quest, on_leave_quest = build_quest_view(
        page, state, push_cloud_state, lambda: current_user
    )

    body_container = ft.Container(content=checkin_view, padding=6)

    def on_tab_change(e):
        idx = e.control.selected_index
        body_container.content = [checkin_view, reassurance_view, treasure_view][idx]
        if idx == 2:
            on_enter_quest()
        else:
            on_leave_quest()
        page.update()

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("✧ Heart2Heart ✧", size=24, weight=ft.FontWeight.BOLD, color=Y2K_PINK),
                        ft.Text("two-way digital diary (｡･ω･｡)ﾉ♡", size=11, color=Y2K_SUBTEXT),
                    ],
                    spacing=0,
                    expand=True,
                ),
                user_selector,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        body_container,
    )
    page.navigation_bar = ft.NavigationBar(
        bgcolor=Y2K_CARD,
        indicator_color=Y2K_PINK_SOFT,
        on_change=on_tab_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Check-In"),
            ft.NavigationBarDestination(icon=ft.Icons.CHAT_BUBBLE, label="Reassurance"),
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Quest"),
        ],
)
ft.run(main, view=ft.AppView.WEB_BROWSER, port=8000)
