import flet as ft
import random
import asyncio
import webbrowser
from datetime import date, datetime




# Y2K Palette matching main.py
Y2K_CARD = "#FFFFFF"
Y2K_PINK = "#FF4DA6"
Y2K_PINK_SOFT = "#FFD6EB"
Y2K_LILAC = "#F3E5FF"
Y2K_LILAC_BORDER = "#B565FF"
Y2K_INK = "#3D0C2E"
Y2K_SUBTEXT = "#7D3C68"

# Put your default background music file in the Heart2Heart folder, or pick one in the app
DEFAULT_BG_MUSIC = "lovequest_bg.mp3"

RIDDLE_BANK = [
    {"q": "I have cities, but no houses; forests, but no trees; and water, but no fish. What am I?", "a": "map", "hint": "Explorers use me to find treasure!"},
    {"q": "The more of me you take, the more you leave behind. What am I?", "a": "footsteps", "hint": "You make them walking through a lavender field."},
    {"q": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "a": "echo", "hint": "Shout in a canyon and I answer back."},
    {"q": "What has keys that open no locks, space, and no room, and you can enter, but not go outside?", "a": "keyboard", "hint": "You're typing on one right now!"},
    {"q": "I am always in front of you, yet you can never see me. What am I?", "a": "future", "hint": "Tomorrow belongs to me."},
    {"q": "What gets wetter the more it dries?", "a": "towel", "hint": "Found in the bathroom after a shower."},
    {"q": "I have hands, a face, and numbers, yet I cannot hold you or smile. What am I?", "a": "clock", "hint": "I measure every second of your quest!"},
    {"q": "What can you catch, but never throw?", "a": "cold", "hint": "Achoo!"},
    {"q": "I'm light as a feather, yet the strongest person can't hold me for five minutes. What am I?", "a": "breath", "hint": "Inhale and exhale."},
    {"q": "What has a heart that doesn't beat?", "a": "artichoke", "hint": "A leafy green vegetable (or a playing card!)."},
    {"q": "I go up, but never come down. What am I?", "a": "age", "hint": "Changes on every birthday."},
    {"q": "What belongs to you, but your friends use it way more than you do?", "a": "name", "hint": "Mekuri and Puwali!"},
]

TREASURE_POOL = [
    {"emoji": "🎶", "name": "Enchanted Y2K Music Box", "desc": "Plays a lullaby written in starlight."},
    {"emoji": "💎", "name": "Starlight Lavender Amethyst", "desc": "Glows softly whenever you miss each other."},
    {"emoji": "👑", "name": "Gilded Pixel Gold Chest", "desc": "Overflowing with chocolate coins & love notes."},
    {"emoji": "🔮", "name": "Moonbeam Wish Orb", "desc": "Grants one cozy date-night wish!"},
    {"emoji": "🧸", "name": "Velvet Ribbon Teddy Charm", "desc": "A pocket-sized guardian of good vibes."},
    {"emoji": "💿", "name": "Holographic Mixtape Disc", "desc": "Contains your eternal theme song."},
]


def y2k_shadow(color=Y2K_PINK_SOFT):
    return ft.BoxShadow(spread_radius=0, blur_radius=0, color=color, offset=ft.Offset(3, 3))


def get_daily_riddles():
    today_str = date.today().isoformat()
    rng = random.Random(today_str)
    return rng.sample(RIDDLE_BANK, 3)


def build_doodle_avatar(name, hair_color, shirt_color, is_girl=True):
    glasses = ft.Row(
        [
            ft.Container(
                width=13,
                height=11,
                border=ft.Border.all(2, Y2K_INK),
                border_radius=6,
                bgcolor="#FFFFFFAA",
            ),
            ft.Container(width=3, height=2, bgcolor=Y2K_INK),
            ft.Container(
                width=13,
                height=11,
                border=ft.Border.all(2, Y2K_INK),
                border_radius=6,
                bgcolor="#FFFFFFAA",
            ),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    head = ft.Container(
        width=36,
        height=34,
        bgcolor="#FFE5D9",
        border=ft.Border.all(2, Y2K_INK),
        border_radius=18,
        content=ft.Column(
            [
                ft.Container(height=6, bgcolor=hair_color, border_radius=8),
                glasses,
                ft.Text("‿", size=11, weight=ft.FontWeight.BOLD, color=Y2K_INK),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    body = ft.Container(
        width=28,
        height=20,
        bgcolor=shirt_color,
        border=ft.Border.all(2, Y2K_INK),
        border_radius=8,
        content=ft.Text("🎀" if is_girl else "★", size=9, text_align=ft.TextAlign.CENTER),
    )

    return ft.Column(
        [
            head,
            body,
            ft.Container(
                bgcolor="#FFFFFFCC",
                padding=ft.Padding.symmetric(horizontal=6, vertical=1),
                border_radius=8,
                content=ft.Text(name, size=10, weight=ft.FontWeight.BOLD, color=Y2K_INK),
            ),
        ],
        spacing=1,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def build_quest_view(page: ft.Page, state: dict, push_cloud_state, get_current_user):
    today_key = date.today().isoformat()
    daily_riddles = get_daily_riddles()

    quest_data = state.setdefault(
        "quest",
        {
            "date": today_key,
            "keys_found": 0,
            "completed": False,
            "reward": None,
            "spotify_url": "",
            "bg_music_path": DEFAULT_BG_MUSIC,
            "active_ping": None,
            "hall_of_fame": [],
        },
    )

    if quest_data.get("date") != today_key:
        quest_data["date"] = today_key
        quest_data["keys_found"] = 0
        quest_data["completed"] = False
        quest_data["reward"] = None
        push_cloud_state(state)

    # --- BACKGROUND MUSIC CONTROLLER ---
       # --- BROWSER / MOBILE AUDIO PLAYER ---
  # --- BROWSER / MOBILE AUDIO PLAYER (NO EXTERNAL PLUGIN NEEDED) ---
music_status = ft.Text("🎵 Tap below to play LoveQuest theme", size=11, color=Y2K_SUBTEXT)

def start_bg_music():
    page.launch_url("/lovequest_bg.mp3")
    music_status.value = "🎵 LoveQuest theme launched!"

def stop_bg_music():
    music_status.value = "🔇 Theme paused for round (pick Spotify or play quiet)"


    # --- PARTNER QUEST PING BANNER ---
    ping_banner_text = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color=Y2K_INK, expand=True)
    ping_banner = ft.Container(
        bgcolor=Y2K_PINK_SOFT,
        border=ft.Border.all(2, Y2K_PINK),
        border_radius=12,
        padding=8,
        visible=False,
        content=ft.Row(
            [
                ping_banner_text,
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=16,
                    icon_color=Y2K_PINK,
                    on_click=lambda e: setattr(ping_banner, "visible", False) or page.update(),
                ),
            ]
        ),
    )

    def refresh_ping_banner():
        ping = state.get("quest", {}).get("active_ping")
        me = get_current_user()
        if ping and ping.get("sender") != me:
            ping_banner_text.value = f"🔔 {ping.get('sender')} entered LoveQuest at {ping.get('time')}!"
            ping_banner.visible = True
        else:
            ping_banner.visible = False

    # --- STOPWATCH STATE ---
    timer_running = False
    elapsed_seconds = 0
    timer_text = ft.Text("⏱️ 00:00", size=14, weight=ft.FontWeight.BOLD, color=Y2K_INK)

    async def stopwatch_loop():
        nonlocal elapsed_seconds
        while timer_running:
            await asyncio.sleep(1)
            if not timer_running:
                break
            elapsed_seconds += 1
            mins, secs = divmod(elapsed_seconds, 60)
            timer_text.value = f"⏱️ {mins:02d}:{secs:02d}"
            page.update()

    def start_timer():
        nonlocal timer_running
        if not timer_running and not quest_data.get("completed"):
            timer_running = True
            page.run_task(stopwatch_loop)

    def stop_timer():
        nonlocal timer_running
        timer_running = False

    # --- SPOTIFY PLAYLIST & CO-OP CALL BAR ---
    spotify_input = ft.TextField(
        hint_text="Paste Spotify playlist link (or leave blank for silence)...",
        value=quest_data.get("spotify_url", ""),
        bgcolor=Y2K_CARD,
        border_color=Y2K_INK,
        border_radius=12,
        text_size=12,
        height=38,
        expand=True,
    )

    def play_spotify(e):
        url = spotify_input.value.strip()
        if not url:
            return
        quest_data["spotify_url"] = url
        push_cloud_state(state)
        webbrowser.open(url)

    def join_coop_call(e):
        safe_date = today_key.replace("-", "")
        domain = "meet.jit.si"
        room = f"Heart2HeartMekuriPuwali{safe_date}"
        webbrowser.open("https://" + domain + "/" + room)


    media_bar = ft.Container(
        bgcolor=Y2K_CARD,
        border=ft.Border.all(2, Y2K_INK),
        border_radius=16,
        padding=8,
        shadow=y2k_shadow("#DFBFFF"),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Button(
                            content="📞 Voice / Video Call",
                            bgcolor=Y2K_LILAC_BORDER,
                            color="white",
                            on_click=join_coop_call,
                        ),
                        timer_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        spotify_input,
                        ft.Button(
                            content="🎵 Spotify",
                            bgcolor="#1DB954",
                            color="white",
                            on_click=play_spotify,
                        ),
                    ],
                    spacing=6,
                ),
            ],
            spacing=6,
        ),
    )

    # --- LILY & LAVENDER FIELD SCENE WITH 2 BESPECTACLED DOODLES ---
    mekuri_doodle = build_doodle_avatar("Mekuri", "#4A2511", "#FF85C0", is_girl=True)
    puwali_doodle = build_doodle_avatar("Puwali", "#2B1B17", "#A2D2FF", is_girl=False)

    doodle_spacer = ft.Container(width=10)
    door_icon = ft.Text("🚪🔒", size=34)
    keys_display = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=Y2K_INK)

    scene_card = ft.Container(
        border=ft.Border.all(2, Y2K_INK),
        border_radius=18,
        padding=12,
        shadow=y2k_shadow(Y2K_PINK_SOFT),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#FFD6EB", "#E8D5FF", "#D8F3DC"],
        ),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("☁️ ✨ 🌸 Lavender & Lily Meadow ☁️", size=11, weight=ft.FontWeight.BOLD, color=Y2K_SUBTEXT),
                        keys_display,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        doodle_spacer,
                        mekuri_doodle,
                        puwali_doodle,
                        ft.Container(expand=True),
                        door_icon,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Text(
                    "🪻 🤍 🪻 🌷 🪻 🤍 🪻 🌷 🪻 🤍 🪻 🌷 🪻 🤍 🪻",
                    size=13,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=4,
        ),
    )

    # --- RIDDLE & DOOR INTERACTION AREA ---
    riddle_title = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=Y2K_PINK)
    riddle_prompt = ft.Text("", size=13, color=Y2K_INK)
    riddle_feedback = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color=Y2K_LILAC_BORDER)
    answer_input = ft.TextField(
        hint_text="Type your answer...",
        bgcolor=Y2K_CARD,
        border_color=Y2K_INK,
        border_radius=12,
        expand=True,
    )

    hall_column = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, height=110)

    def refresh_hall_of_fame():
        hall_column.controls.clear()
        records = quest_data.get("hall_of_fame", [])
        if not records:
            hall_column.controls.append(
                ft.Text("No treasures unlocked yet — solve today's 3 riddles!", size=12, color=Y2K_SUBTEXT)
            )
            return
        for rec in reversed(records):
            hall_column.controls.append(
                ft.Container(
                    bgcolor=Y2K_CARD,
                    border=ft.Border.all(1.5, Y2K_INK),
                    border_radius=12,
                    padding=8,
                    content=ft.Row(
                        [
                            ft.Text(rec.get("emoji", "🏆"), size=20),
                            ft.Column(
                                [
                                    ft.Text(rec.get("name", "Treasure"), size=12, weight=ft.FontWeight.BOLD, color=Y2K_INK),
                                    ft.Text(f"📅 {rec.get('date')} • ⏱️ {rec.get('time')}", size=10, color=Y2K_SUBTEXT),
                                ],
                                expand=True,
                                spacing=1,
                            ),
                        ]
                    ),
                )
            )

    def update_quest_ui():
        keys = quest_data.get("keys_found", 0)
        completed = quest_data.get("completed", False)

        keys_display.value = f"Keys: {'🗝️' * keys}{'⚪' * (3 - keys)}"
        doodle_spacer.width = 10 + (keys * 45)
        door_icon.value = "🚪✨" if completed else ("🚪🔓" if keys == 3 else "🚪🔒")

        if completed:
            reward = quest_data.get("reward") or random.choice(TREASURE_POOL)
            riddle_title.value = f"🎉 Door Unlocked! You found: {reward['emoji']} {reward['name']}!"
            riddle_prompt.value = reward["desc"]
            answer_input.visible = False
            submit_btn.visible = False
            hint_btn.visible = False
            open_door_btn.visible = False
        elif keys < 3:
            current_riddle = daily_riddles[keys]
            riddle_title.value = f"✧ Riddle {keys + 1} of 3 ✧"
            riddle_prompt.value = current_riddle["q"]
            answer_input.visible = True
            submit_btn.visible = True
            hint_btn.visible = True
            open_door_btn.visible = False
        else:
            riddle_title.value = "🗝️ All 3 Keys Collected!"
            riddle_prompt.value = "Mekuri & Puwali reached the door! Tap below to unlock your treasure!"
            answer_input.visible = False
            submit_btn.visible = False
            hint_btn.visible = False
            open_door_btn.visible = True

    def check_riddle_answer(e):
        keys = quest_data.get("keys_found", 0)
        if keys >= 3:
            return
        user_ans = answer_input.value.strip().lower()
        correct_ans = daily_riddles[keys]["a"].lower()

        if correct_ans in user_ans and user_ans != "":
            quest_data["keys_found"] = keys + 1
            answer_input.value = ""
            riddle_feedback.value = f"✨ Correct! You earned Key #{keys + 1} 🗝️!"
            push_cloud_state(state)
            update_quest_ui()
        else:
            riddle_feedback.value = "Not quite! Try again or tap Hint 💡"
        page.update()

    def show_hint(e):
        keys = quest_data.get("keys_found", 0)
        if keys < 3:
            riddle_feedback.value = f"💡 Hint: {daily_riddles[keys]['hint']}"
            page.update()

    def open_final_door(e):
        stop_timer()
        mins, secs = divmod(elapsed_seconds, 60)
        time_taken = f"{mins:02d}:{secs:02d}"
        reward = random.choice(TREASURE_POOL)

        quest_data["completed"] = True
        quest_data["reward"] = reward
        quest_data.setdefault("hall_of_fame", []).append(
            {
                "date": today_key,
                "emoji": reward["emoji"],
                "name": reward["name"],
                "time": time_taken,
            }
        )
        push_cloud_state(state)
        riddle_feedback.value = f"🏆 Added to Hall of Fame ({time_taken})! LoveQuest theme resumed 🎵"
        update_quest_ui()
        refresh_hall_of_fame()
        # Resume background music after the round ends
        start_bg_music()
        page.update()

    submit_btn = ft.Button(content="Unlock 🗝️", bgcolor=Y2K_PINK, color="white", on_click=check_riddle_answer)
    hint_btn = ft.TextButton("💡 Hint", on_click=show_hint)
    open_door_btn = ft.Button(
        content="✨ Use 3 Keys & Open Door! ✨",
        bgcolor=Y2K_LILAC_BORDER,
        color="white",
        visible=False,
        on_click=open_final_door,
    )

    riddle_box = ft.Container(
        bgcolor=Y2K_LILAC,
        border=ft.Border.all(2, Y2K_LILAC_BORDER),
        border_radius=16,
        padding=12,
        shadow=y2k_shadow(Y2K_PINK_SOFT),
        content=ft.Column(
            [
                ft.Row([riddle_title, hint_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                riddle_prompt,
                ft.Row([answer_input, submit_btn], spacing=6),
                open_door_btn,
                riddle_feedback,
            ],
            spacing=6,
        ),
    )

    # --- OPENING "LOVEQUEST" SPLASH SCREEN ---
    def begin_round(e):
        stop_bg_music()  # Stop opening bg music so you can use Spotify or silence
        opening_screen.visible = False
        gameplay_screen.visible = True
        start_timer()
        page.update()

    opening_screen = ft.Container(
        border=ft.Border.all(2.5, Y2K_INK),
        border_radius=22,
        padding=20,
        shadow=y2k_shadow(Y2K_PINK),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#FFD6EB", "#E8D5FF", "#FFF0F8"],
        ),
        content=ft.Column(
            [
                ft.Text("✧･ﾟ: ✧･ﾟ: :･ﾟ✧:･ﾟ✧", size=14, color=Y2K_LILAC_BORDER),
                ft.Text("💖 LoveQuest 💖", size=30, weight=ft.FontWeight.BOLD, color=Y2K_PINK),
                ft.Text("Mekuri & Puwali's Daily Meadow Adventure", size=13, color=Y2K_SUBTEXT),
                ft.Row(
                    [
                        build_doodle_avatar("Mekuri", "#4A2511", "#FF85C0", is_girl=True),
                        ft.Text("🌸 🗝️ 🚪 🪻", size=22),
                        build_doodle_avatar("Puwali", "#2B1B17", "#A2D2FF", is_girl=False),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=14,
                ),
                ft.Button(
                    content="▶ Start Today's Round ✧",
                    bgcolor=Y2K_PINK,
                    color="white",
                    height=48,
                    width=260,
                    on_click=begin_round,
                ),
                            ft.TextButton(
                    "🎵 Play / Resume Opening Theme Song",
                    on_click=lambda e: (start_bg_music(), page.update()),
                ),

                music_status,
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    gameplay_screen = ft.Column(
        visible=False,
        spacing=8,
        controls=[
            media_bar,
            scene_card,
            riddle_box,
            ft.Row(
                [
                    ft.Text("🏆 Hall of Fame", size=14, weight=ft.FontWeight.BOLD, color=Y2K_INK, expand=True),
                    music_status,
                ]
            ),
            hall_column,
        ],
    )

    update_quest_ui()
    refresh_hall_of_fame()

    root_column = ft.Column(
        [
            ping_banner,
            opening_screen,
            gameplay_screen,
        ],
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    # Triggered whenever Mekuri or Puwali switches to the Quest tab
    def on_enter_quest():
        sender = get_current_user()
        state.setdefault("quest", {})["active_ping"] = {
            "sender": sender,
            "time": datetime.now().strftime("%I:%M %p"),
        }
        push_cloud_state(state)
        refresh_ping_banner()
        opening_screen.visible = True
        gameplay_screen.visible = False
        start_bg_music()
        page.update()

    # Triggered when leaving the Quest tab so music doesn't keep playing on Check-In
    def on_leave_quest():
        stop_bg_music()
        stop_timer()

    return root_column, on_enter_quest, on_leave_quest
