import math
import time
from datetime import date, datetime, timedelta

import importlib

try:
    go = importlib.import_module("plotly.graph_objects")
except ModuleNotFoundError as exc:
    if exc.name not in {"plotly", "plotly.graph_objects"}:
        raise
    go = None

try:
    st = importlib.import_module("streamlit")
except ModuleNotFoundError as exc:
    if exc.name != "streamlit":
        raise
    raise SystemExit(
        "Streamlit is required. Install it with: python -m pip install streamlit"
    ) from exc

MAX_COORDINATE_DISTANCE = math.sqrt(2)
OASIS_PLANET = "オアシス惑星"
GHOST_PLANET = "ゴースト惑星"
LEGACY_CATEGORY_NAMES = {
    "いいこと": OASIS_PLANET,
    "悪いこと": GHOST_PLANET,
}

st.set_page_config(
    page_title="Beyond Earth",
    page_icon="◉",
    layout="wide",
)

st.html(
    """
    <style>
    .stApp {
        background-color: #0b1020;
        background-image:
            radial-gradient(circle at 13% 27%, rgba(255, 255, 255, 0.95) 0 1px, rgba(102, 211, 255, 0.55) 2px, transparent 7px),
            radial-gradient(ellipse 1px 7px at 13% 27%, rgba(206, 245, 255, 0.85), transparent 90%),
            radial-gradient(ellipse 7px 1px at 13% 27%, rgba(206, 245, 255, 0.85), transparent 90%),
            radial-gradient(circle at 37% 68%, rgba(255, 255, 255, 0.95) 0 1px, rgba(180, 147, 255, 0.55) 2px, transparent 7px),
            radial-gradient(ellipse 1px 6px at 37% 68%, rgba(232, 220, 255, 0.85), transparent 90%),
            radial-gradient(ellipse 6px 1px at 37% 68%, rgba(232, 220, 255, 0.85), transparent 90%),
            radial-gradient(circle at 64% 39%, rgba(255, 255, 255, 0.95) 0 1px, rgba(102, 211, 255, 0.55) 2px, transparent 7px),
            radial-gradient(ellipse 1px 8px at 64% 39%, rgba(206, 245, 255, 0.85), transparent 90%),
            radial-gradient(ellipse 8px 1px at 64% 39%, rgba(206, 245, 255, 0.85), transparent 90%),
            radial-gradient(circle at 84% 73%, rgba(255, 255, 255, 0.95) 0 1px, rgba(180, 147, 255, 0.55) 2px, transparent 7px),
            radial-gradient(ellipse 1px 6px at 84% 73%, rgba(232, 220, 255, 0.85), transparent 90%),
            radial-gradient(ellipse 6px 1px at 84% 73%, rgba(232, 220, 255, 0.85), transparent 90%),
            radial-gradient(1.5px 1.5px at 8% 17%, rgba(255, 255, 255, 0.82) 45%, transparent 70%),
            radial-gradient(1px 1px at 19% 73%, rgba(176, 215, 255, 0.72) 45%, transparent 70%),
            radial-gradient(2px 2px at 31% 38%, rgba(255, 255, 255, 0.75) 45%, transparent 70%),
            radial-gradient(1px 1px at 43% 88%, rgba(255, 255, 255, 0.72) 45%, transparent 70%),
            radial-gradient(1.5px 1.5px at 56% 21%, rgba(220, 205, 255, 0.78) 45%, transparent 70%),
            radial-gradient(1px 1px at 67% 63%, rgba(255, 255, 255, 0.78) 45%, transparent 70%),
            radial-gradient(2px 2px at 79% 34%, rgba(177, 225, 255, 0.7) 45%, transparent 70%),
            radial-gradient(1px 1px at 92% 78%, rgba(255, 255, 255, 0.78) 45%, transparent 70%),
            radial-gradient(ellipse at 18% 12%, rgba(28, 94, 150, 0.2), transparent 43%),
            radial-gradient(ellipse at 85% 74%, rgba(91, 49, 143, 0.17), transparent 42%),
            repeating-linear-gradient(30deg, rgba(100, 160, 190, 0.025) 0 1px, transparent 1px 72px),
            repeating-linear-gradient(150deg, rgba(100, 160, 190, 0.025) 0 1px, transparent 1px 72px);
        background-attachment: fixed;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: transparent;
    }

    [data-testid="stAppViewContainer"] h1 {
        color: #f3f8ff;
        letter-spacing: 0.045em;
        text-shadow:
            0 2px 0 rgba(26, 43, 74, 0.95),
            0 5px 12px rgba(34, 128, 180, 0.55),
            0 12px 30px rgba(17, 26, 54, 0.9);
    }

    [data-testid="stAppViewContainer"] h1::after {
        content: "";
        display: block;
        width: 4.5rem;
        height: 3px;
        margin-top: 0.55rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #54d6df, #a68aff);
        box-shadow: 0 0 14px rgba(84, 214, 223, 0.7);
    }
    </style>
    """
)


def save_post(content, category, satisfaction, social, intensity):
    posts = st.session_state.setdefault("posts", [])
    posts.append(
        {
            "id": len(posts) + 1,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "content": content,
            "category": category,
            "satisfaction": satisfaction,
            "social": social,
            "intensity": intensity,
        }
    )


def submit_daily_entries():
    entries = [
        (
            OASIS_PLANET,
            st.session_state["good_content"],
            st.session_state["good_satisfaction"],
            st.session_state["good_social"],
        ),
        (
            GHOST_PLANET,
            st.session_state["bad_content"],
            st.session_state["bad_satisfaction"],
            st.session_state["bad_social"],
        ),
    ]
    entries = [
        (category, content.strip(), satisfaction, social)
        for category, content, satisfaction, social in entries
        if content.strip()
    ]
    if not entries:
        st.session_state["post_form_result"] = ("warning", 0)
        return

    for category, content, satisfaction, social in entries:
        save_post(content, category, satisfaction, social, 3)

    st.session_state["good_content"] = ""
    st.session_state["good_satisfaction"] = 0.0
    st.session_state["good_social"] = 0.0
    st.session_state["bad_content"] = ""
    st.session_state["bad_satisfaction"] = 0.0
    st.session_state["bad_social"] = 0.0
    st.session_state["transition_deadline"] = time.monotonic() + 3
    st.session_state["post_form_result"] = ("success", len(entries))


def set_entry_template(field, text):
    st.session_state[field] = text


def display_category_name(category):
    return LEGACY_CATEGORY_NAMES.get(category, category)


def cancel_pending_transition():
    st.session_state.pop("transition_deadline", None)


def select_view(view):
    cancel_pending_transition()
    st.session_state["active_view"] = view


@st.fragment(run_every=0.25)
def finish_save_transition():
    deadline = st.session_state.get("transition_deadline")
    if deadline is not None and time.monotonic() >= deadline:
        st.session_state.pop("transition_deadline", None)
        st.session_state["active_view"] = "analysis"
        st.session_state["scroll_analysis_to_top"] = True
        st.rerun()


def reset_history():
    if st.session_state.get("confirm_reset", False):
        clear_posts()
        st.session_state["confirm_reset"] = False
        st.session_state["reset_history_expander"] = False
        st.session_state["reset_form_result"] = "success"
    else:
        st.session_state["reset_form_result"] = "warning"


def toggle_post_history():
    st.session_state["show_post_history"] = not st.session_state.get(
        "show_post_history",
        False,
    )


def load_posts():
    return sorted(
        st.session_state.setdefault("posts", []),
        key=lambda post: (post["created_at"], post["id"]),
        reverse=True,
    )


def clear_posts():
    st.session_state.setdefault("posts", []).clear()


def average_coordinate_distance(posts):
    if not posts:
        return 0.0
    return sum(
        math.hypot(post["satisfaction"], post["social"]) for post in posts
    ) / len(posts)


def summarize_coordinates(posts, days):
    start_date = date.today() - timedelta(days=days - 1)
    period_posts = [
        post
        for post in posts
        if start_date <= datetime.fromisoformat(post["created_at"]).date() <= date.today()
    ]
    if not period_posts:
        return None

    satisfaction = sum(post["satisfaction"] for post in period_posts) / len(period_posts)
    social = sum(post["social"] for post in period_posts) / len(period_posts)
    mean_coordinate_distance = average_coordinate_distance(period_posts)
    distance_ratio = mean_coordinate_distance / MAX_COORDINATE_DISTANCE
    categories = {}
    for post in period_posts:
        categories[post["category"]] = categories.get(post["category"], 0) + 1
    top_category = max(categories, key=categories.get)

    observations = []
    if satisfaction <= -0.25:
        observations.append(
            "満足度が低めです。何が負担になったかを一つ特定し、"
            "休息や相談など、すぐできる対処を優先しましょう。"
        )
    elif satisfaction >= 0.25:
        observations.append(
            "満足度が高めです。よかった条件や行動を振り返り、"
            "再現できる形で続けましょう。"
        )
    else:
        observations.append(
            "満足度は中間です。出来事ごとの差に注目すると、"
            "調子を左右する条件が見つかりそうです。"
        )

    if social >= 0.25:
        observations.append(
            "社会・制度との結びつきが強めです。個人だけの責任にせず、"
            "状況やルールを整理して、信頼できる人への相談も検討しましょう。"
        )
    elif social <= -0.25:
        observations.append(
            "個人的な要因が強めです。自分で変えられる行動や伝え方を"
            "一つ選んで試しましょう。"
        )
    else:
        observations.append(
            "個人と環境の両方が関係していそうです。自分で変えられることと、"
            "周囲の協力が必要なことを分けて考えましょう。"
        )

    if distance_ratio < 1 / 3:
        distance_observation = (
            "原点距離は最大距離の約"
            f"{distance_ratio:.0%}で、記録は中立に近い傾向です。"
        )
    elif distance_ratio < 2 / 3:
        distance_observation = (
            "原点距離は最大距離の約"
            f"{distance_ratio:.0%}で、中立からある程度離れた記録もある中間的な傾向です。"
        )
    else:
        distance_observation = (
            "原点距離は最大距離の約"
            f"{distance_ratio:.0%}で、満足度または社会・個人の座標に"
            "はっきりした傾向が出ている記録が多めです。"
        )
    observations.append(
        distance_observation
        + "距離は良し悪しを表さず、方向は各軸の傾向と合わせて見てください。"
    )

    return {
        "count": len(period_posts),
        "satisfaction": satisfaction,
        "social": social,
        "mean_coordinate_distance": mean_coordinate_distance,
        "distance_ratio": distance_ratio,
        "top_category": top_category,
        "observations": observations,
    }


st.session_state.setdefault("posts", [])

st.title("Beyond Earth")
st.caption("Personal feelings → Social patterns")
st.info(
    "投稿履歴はこのブラウザーセッション中だけ保持され、終了後は消えます。"
    "個人情報や、他人に知られたくない内容は入力しないでください。"
)
st.write("Create Your Planet")
st.caption("毎日書いて、星を増やしましょう。")

st.session_state.setdefault("active_view", "journal")
view_col1, view_col2 = st.columns(2)
view_col1.button(
    "Journal / 投稿",
    type="primary" if st.session_state["active_view"] == "journal" else "secondary",
    on_click=select_view,
    args=("journal",),
    width="stretch",
)
view_col2.button(
    "Social Lens / 分析",
    type="primary" if st.session_state["active_view"] == "analysis" else "secondary",
    on_click=select_view,
    args=("analysis",),
    width="stretch",
)

if st.session_state["active_view"] == "journal":
    st.subheader("惑星の記録")
    for slider_key in (
        "good_satisfaction",
        "good_social",
        "bad_satisfaction",
        "bad_social",
    ):
        st.session_state.setdefault(slider_key, 0.0)
    for content_key in ("good_content", "bad_content"):
        st.session_state.setdefault(content_key, "")

    st.markdown(f"#### {OASIS_PLANET}")
    st.caption("奇跡的な星。今日のいいことを記録します。")
    st.text_area(
        "今日のいいこと（1つ）",
        placeholder="小さなことでも大丈夫です",
        height=80,
        key="good_content",
    )
    st.caption("例を押すと記述欄に入ります。あとから自由に編集できます。")
    good_examples = (
        "馬券が当たった",
        "好きなものを食べた",
        "人に感謝された",
        "やりたいことができた",
    )
    good_example_columns = st.columns(4)
    for column, example in zip(good_example_columns, good_examples):
        column.button(
            example,
            key=f"good_example_{example}",
            on_click=set_entry_template,
            args=("good_content", example),
            width="stretch",
        )
    st.slider(
        "満足度",
        min_value=-1.0,
        max_value=1.0,
        step=0.1,
        help="-1 = 不満、0 = どちらでもない、+1 = 満足",
        key="good_satisfaction",
    )
    st.slider(
        "個人と社会、どちらの影響？",
        min_value=-1.0,
        max_value=1.0,
        step=0.1,
        help="-1 = 自分や身近な人のこと、0 = 両方、+1 = 社会の仕組みや環境のこと",
        key="good_social",
    )

    st.markdown(f"#### {GHOST_PLANET}")
    st.caption("静まり返った不気味な星。今日の悪いことを記録します。")
    st.text_area(
        "今日の悪いこと（1つ）",
        placeholder="気になったこと、つらかったことなど",
        height=80,
        key="bad_content",
    )
    st.caption("例を押すと記述欄に入ります。あとから自由に編集できます。")
    bad_examples = (
        "馬券が外れた",
        "予定がうまくいかなかった",
        "疲れがたまった",
        "人間関係で悩んだ",
    )
    bad_example_columns = st.columns(4)
    for column, example in zip(bad_example_columns, bad_examples):
        column.button(
            example,
            key=f"bad_example_{example}",
            on_click=set_entry_template,
            args=("bad_content", example),
            width="stretch",
        )
    st.slider(
        "満足度",
        min_value=-1.0,
        max_value=1.0,
        step=0.1,
        help="-1 = 不満、0 = どちらでもない、+1 = 満足",
        key="bad_satisfaction",
    )
    st.slider(
        "個人と社会、どちらの影響？",
        min_value=-1.0,
        max_value=1.0,
        step=0.1,
        help="-1 = 自分や身近な人のこと、0 = 両方、+1 = 社会の仕組みや環境のこと",
        key="bad_social",
    )
    st.button(
        "今日の記録を保存",
        type="primary",
        on_click=submit_daily_entries,
    )

    post_form_result = st.session_state.pop("post_form_result", None)
    if post_form_result:
        result_type, count = post_form_result
        if result_type == "warning":
            st.warning("いいことか悪いことを入力してください。")
        elif result_type == "success":
            st.success(f"{count}件の記録を保存しました。")

    if st.session_state.get("transition_deadline") is not None:
        st.markdown(
            """
            <div class="save-loader" role="status" aria-live="polite">
                <span class="save-loader__spinner" aria-hidden="true"></span>
                <span>違和感を模索中</span>
            </div>
            <style>
            .save-loader {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                width: fit-content;
                padding: 0.85rem 1.1rem;
                border: 1px solid rgba(133, 190, 255, 0.28);
                border-radius: 0.9rem;
                background: rgba(15, 25, 52, 0.82);
                color: #eef6ff;
                box-shadow: 0 8px 26px rgba(0, 0, 0, 0.28);
                font-weight: 600;
            }
            .save-loader__spinner {
                width: 1.2rem;
                height: 1.2rem;
                border: 2px solid rgba(205, 224, 255, 0.25);
                border-top-color: #70dcff;
                border-right-color: #b6a0ff;
                border-radius: 50%;
                animation: save-loader-spin 0.8s linear infinite;
            }
            @keyframes save-loader-spin {
                to { transform: rotate(360deg); }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        finish_save_transition()

elif st.session_state["active_view"] == "analysis":
    if st.session_state.pop("scroll_analysis_to_top", False):
        st.html(
            """
            <script>
            const scrollAnalysisToTop = () => {
                window.scrollTo({ top: 0, behavior: "smooth" });
                document.querySelectorAll(
                    'section[data-testid="stMain"], [data-testid="stAppViewContainer"]'
                ).forEach((element) => {
                    element.scrollTo({ top: 0, behavior: "smooth" });
                });
            };
            scrollAnalysisToTop();
            setTimeout(scrollAnalysisToTop, 150);
            </script>
            """,
            unsafe_allow_javascript=True,
        )

    with st.expander(
        "履歴をリセット",
        expanded=False,
        key="reset_history_expander",
    ):
        st.warning("保存した投稿履歴をすべて削除します。この操作は取り消せません。")
        with st.form("reset_history_form"):
            st.checkbox(
                "すべての投稿履歴を削除することを確認しました",
                key="confirm_reset",
            )
            st.form_submit_button(
                "履歴をリセット",
                on_click=reset_history,
            )

    reset_form_result = st.session_state.pop("reset_form_result", None)
    if reset_form_result == "success":
        st.success("投稿履歴をすべて削除しました。")
    elif reset_form_result == "warning":
        st.warning("削除するには確認欄にチェックしてください。")

    df = load_posts()

    st.subheader("座標から傾向と対策を確認")

    today_posts = [
        post
        for post in df
        if datetime.fromisoformat(post["created_at"]).date() == date.today()
    ]
    today_categories = {display_category_name(post["category"]) for post in today_posts}
    if {OASIS_PLANET, GHOST_PLANET}.issubset(today_categories):
        kind_message = (
            "今日も一日お疲れ様でした。今が何時であれ、"
            "これからはリラックスしましょう。"
        )
    elif GHOST_PLANET in today_categories:
        kind_message = (
            "大変だったことを言葉にできたあなたへ。無理をせず、"
            "自分をいたわってください。"
        )
    elif OASIS_PLANET in today_categories:
        kind_message = (
            "今日のよかったことに気づいて記録できたのは、すてきなことです。"
            "その気づきを大切にしてください。"
        )
    else:
        kind_message = (
            "今日はまだ記録がありません。書けるときに、あなたのペースで"
            "振り返れば大丈夫です。"
        )
    st.subheader("今日のあなたへ")
    st.info(kind_message)

    if not df:
        st.info("まずはJournalで投稿を作成してください。")
    else:
        col1, col2 = st.columns(2)

        col1.metric("惑星の数", len(df))
        col2.metric(
            "あなたの惑星は地球からどれぐらい離れている？",
            f"{average_coordinate_distance(df) / MAX_COORDINATE_DISTANCE:.0%}",
            help=(
                "0%は中心、100%は座標範囲の端までの距離です。"
                "記録ごとの距離を平均しています。良し悪しではなく、"
                "どちら向きかはグラフの軸で確認できます。"
            ),
        )

        if go is None:
            st.info(
                "グラフを表示するには Plotly をインストールしてください: "
                "python -m pip install plotly"
            )
        else:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=[
                        coordinate
                        for post in df
                        for coordinate in (0, post["satisfaction"], None)
                    ],
                    y=[
                        coordinate
                        for post in df
                        for coordinate in (0, post["social"], None)
                    ],
                    mode="lines",
                    line={"color": "rgba(190, 210, 255, 0.24)", "width": 1},
                    hoverinfo="skip",
                    showlegend=False,
                    name="地球からの距離",
                )
            )
            for category_name in dict.fromkeys(
                display_category_name(post["category"]) for post in df
            ):
                category_posts = [
                    post
                    for post in df
                    if display_category_name(post["category"]) == category_name
                ]
                star_color = "#b8ff88" if category_name == OASIS_PLANET else "#b8a5ff"
                fig.add_trace(
                    go.Scatter(
                        x=[post["satisfaction"] for post in category_posts],
                        y=[post["social"] for post in category_posts],
                        mode="markers",
                        marker={
                            "symbol": "diamond",
                            "size": [
                                30 + (max(-1, min(1, post["satisfaction"])) + 1) * 8
                                for post in category_posts
                            ],
                            "color": star_color,
                            "opacity": 0.2,
                            "line": {"width": 0},
                        },
                        hoverinfo="skip",
                        showlegend=False,
                        name=f"{category_name}の光",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=[post["satisfaction"] for post in category_posts],
                        y=[post["social"] for post in category_posts],
                        mode="markers",
                        name=category_name,
                        marker={
                            "symbol": "diamond",
                            "size": [
                                8 + (max(-1, min(1, post["satisfaction"])) + 1) * 11
                                for post in category_posts
                            ],
                            "color": star_color,
                            "line": {"color": "#ffffff", "width": 1.2},
                            "sizemode": "diameter",
                        },
                        text=[
                            f"{post['content']}<br>{post['created_at']}<br>"
                            f"地球（原点）からの距離: "
                            f"{math.hypot(post['satisfaction'], post['social']):.2f}"
                            for post in category_posts
                        ],
                        hovertemplate=(
                            "満足度: %{x:.2f}<br>"
                            "個人 ← → 社会の影響: %{y:.2f}<br>"
                            "%{text}<extra>%{fullData.name}</extra>"
                        ),
                    )
                )
            fig.add_trace(
                go.Scatter(
                    x=[0],
                    y=[0],
                    mode="markers",
                    marker={
                        "symbol": "circle",
                        "size": 42,
                        "color": "rgba(74, 222, 128, 0.22)",
                        "line": {"width": 0},
                    },
                    hoverinfo="skip",
                    showlegend=False,
                    name="地球の光",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[0],
                    y=[0],
                    mode="markers+text",
                    name="地球（原点）",
                    marker={
                        "symbol": "circle",
                        "size": 28,
                        "color": "#39a96b",
                        "line": {"color": "#b8ffd2", "width": 2},
                    },
                    text=["地球"],
                    textposition="bottom center",
                    textfont={"color": "#ffffff", "size": 13},
                    hovertemplate="地球（原点）<extra></extra>",
                )
            )

            fig.update_layout(
                title="地球から広がる記録",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                plot_bgcolor="rgba(20, 32, 55, 0.86)",
                xaxis={
                    "title": "満足度（不満 ← → 満足）",
                    "range": [-1.1, 1.1],
                    "zeroline": False,
                    "showgrid": False,
                    "showline": True,
                    "linecolor": "rgba(114, 185, 255, 0.3)",
                },
                yaxis={
                    "title": "個人 ← → 社会の影響",
                    "range": [-1.1, 1.1],
                    "zeroline": False,
                    "scaleanchor": "x",
                    "scaleratio": 1,
                    "showgrid": False,
                    "showline": True,
                    "linecolor": "rgba(114, 185, 255, 0.3)",
                },
            )

            for orbit_radius in (0.5, 1.0):
                fig.add_shape(
                    type="circle",
                    xref="x",
                    yref="y",
                    x0=-orbit_radius,
                    y0=-orbit_radius,
                    x1=orbit_radius,
                    y1=orbit_radius,
                    line={
                        "color": "rgba(114, 185, 255, 0.3)",
                        "width": 1,
                        "dash": "dot",
                    },
                    layer="below",
                )

            fig.add_vrect(
                x0=-1.1,
                x1=-0.5,
                fillcolor="rgba(255, 82, 110, 0.16)",
                line_width=0,
                layer="below",
                annotation_text="Red Zone",
                annotation_position="top left",
                annotation_font_color="#ffb5c2",
                annotation_font_size=12,
            )
            fig.add_hline(
                y=0,
                line_dash="solid",
                line_color="#72b9ff",
                line_width=1.5,
                opacity=0.42,
            )
            fig.add_vline(
                x=0,
                line_dash="solid",
                line_color="#72b9ff",
                line_width=1.5,
                opacity=0.42,
            )
            fig.update_layout(height=600)

            st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "地球が原点です。記録は星で表し、地球から星へ伸びる線が距離を示します。"
            "星をポイントすると、地球からの距離を確認できます。"
            "赤く色付けした範囲は、満足度が低い側（-0.5以下）のRed Zoneです。"
        )
        periods = [
            ("一日", 1, "今日"),
            ("一週間", 7, "直近7日"),
            ("一か月", 30, "直近30日"),
            ("一年", 365, "直近365日"),
        ]
        for label, days, period_name in periods:
            summary = summarize_coordinates(df, days)
            with st.expander(
                f"{label}単位の傾向と対策（{period_name}）",
                expanded=days == 1,
            ):
                if summary is None:
                    st.info(f"{period_name}の投稿はまだありません。")
                    continue

                st.write(
                    f"対象投稿: {summary['count']}件 / "
                    f"多い記録: {display_category_name(summary['top_category'])}"
                )
                st.metric(
                    "あなたの惑星は地球からどれぐらい離れている？",
                    f"{summary['distance_ratio']:.0%}",
                    help=(
                        "0%は中心、100%は座標範囲の端までの距離です。"
                        "記録ごとの距離を平均しています。良し悪しではなく、"
                        "どちら向きかはグラフの軸で確認できます。"
                    ),
                )
                for observation in summary["observations"]:
                    st.write(f"- {observation}")

                if days == 1:
                    st.write(
                        "**今日の対策:** 気になったことを一つだけ選び、"
                        "休息・小さな行動・相談のいずれかを試してみましょう。"
                    )
                elif days == 7:
                    st.write(
                        f"**今週の対策:** {OASIS_PLANET}・{GHOST_PLANET}のどちらが多かったかを振り返り、"
                        "来週試す行動を"
                        "一つ決め、週末に変化を振り返りましょう。"
                    )
                elif days == 30:
                    st.write(
                        "**今月の対策:** 繰り返す負担の原因と助けになる条件を整理し、"
                        "環境調整や相談先を一つ具体化しましょう。"
                    )
                else:
                    st.write(
                        "**今年の対策:** 長く続くテーマを振り返り、"
                        "自分の工夫と周囲に働きかける課題に分けて、"
                        "次の一年の目標を一つ決めましょう。"
                    )

        st.session_state.setdefault("show_post_history", False)
        st.button(
            "投稿履歴を閉じる"
            if st.session_state["show_post_history"]
            else "投稿履歴を見る",
            on_click=toggle_post_history,
        )
        if st.session_state["show_post_history"]:
            st.subheader("投稿履歴")
            st.dataframe(
                [
                    {
                        "created_at": post["created_at"],
                        "category": display_category_name(post["category"]),
                        "satisfaction": post["satisfaction"],
                        "social": post["social"],
                        "content": post["content"],
                    }
                    for post in df
                ],
                use_container_width=True,
                hide_index=True,
            )
