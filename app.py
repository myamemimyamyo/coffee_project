import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="서울시 카페 상권분석",
    layout="wide"
)
st.error("디자인 수정 코드가 실행 중입니다.")

# 한글 폰트
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

# =========================
# CSS 디자인
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F7F3EC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero {
    background: linear-gradient(135deg, #4B2E1E 0%, #8B6F47 100%);
    padding: 42px 46px;
    border-radius: 26px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(75, 46, 30, 0.18);
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 18px;
    line-height: 1.7;
    color: #F7F3EC;
}

.section-card {
    background-color: #FFFFFF;
    padding: 30px 34px;
    border-radius: 22px;
    border: 1px solid #E5D8C8;
    box-shadow: 0 6px 20px rgba(43, 33, 24, 0.06);
    margin-bottom: 28px;
}

.section-label {
    display: inline-block;
    background-color: #EFE2D0;
    color: #4B2E1E;
    font-size: 13px;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
}

.insight-box {
    background-color: #F9F4ED;
    border-left: 6px solid #7CA6B8;
    padding: 18px 20px;
    border-radius: 14px;
    margin-top: 18px;
    color: #2B2118;
    font-size: 16px;
    line-height: 1.6;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E5D8C8;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 16px rgba(43, 33, 24, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #6F6258;
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    color: #4B2E1E;
    font-size: 28px;
    font-weight: 800;
}

h1, h2, h3 {
    color: #2B2118;
    letter-spacing: -0.4px;
}

p, li {
    color: #4A4038;
    line-height: 1.7;
}

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 데이터 불러오기
# =========================
cafe_gu = pd.read_csv("cafe_gu.csv")
density_area = pd.read_csv("density_area.csv")
final_df = pd.read_csv("final_df.csv")

# =========================
# 핵심 지표 계산
# =========================
total_cafe = cafe_gu["카페수"].sum()
top_cafe_gu = cafe_gu.sort_values("카페수", ascending=False).iloc[0]["자치구"]
top_shortage_gu = final_df.sort_values("카페1개당생활인구", ascending=False).iloc[0]["자치구"]
top_spending_gu = final_df.sort_values("카페1개당음식지출액", ascending=False).iloc[0]["자치구"]

candidate_df = final_df.copy()

candidate_df["입지점수"] = (
    candidate_df["카페1개당생활인구"].rank(ascending=True)
    + candidate_df["카페1개당음식지출액"].rank(ascending=True)
    + candidate_df["생활인구1인당음식지출액"].rank(ascending=True)
)

recommend = candidate_df.sort_values("입지점수", ascending=False).head(5)
best_gu = recommend.iloc[0]["자치구"]

# =========================
# 그래프 함수
# =========================
def draw_bar_chart(df, x, y, title, ylabel):
    import numpy as np
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(11, 5.8))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # 값 정렬
    df = df.copy()
    values = df[y].values
    labels = df[x].values

    # 커피톤 그라데이션 색상
    colors = [
        "#3E2723", "#4E342E", "#5D4037", "#6D4C41", "#795548",
        "#8D6E63", "#A1887F", "#BCAAA4", "#D7CCC8", "#EFEBE9"
    ]

    # 기본 막대는 숨기고, 둥근 막대를 직접 그림
    bars = ax.bar(labels, values, color="none")

    for i, bar in enumerate(bars):
        x_pos = bar.get_x()
        y_pos = 0
        width = bar.get_width()
        height = bar.get_height()

        rounded_bar = FancyBboxPatch(
            (x_pos, y_pos),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=0,
            facecolor=colors[i % len(colors)],
            alpha=0.95
        )
        ax.add_patch(rounded_bar)

        # 막대 위 숫자 표시
        ax.text(
            x_pos + width / 2,
            height + max(values) * 0.015,
            f"{height:,.0f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#3E2723"
        )

    # 제목/축
    ax.set_title(
        title,
        fontsize=18,
        fontweight="bold",
        color="#2B2118",
        pad=22
    )

    ax.set_ylabel(ylabel, fontsize=11, color="#6F6258")
    ax.set_xlabel("")

    # 축 스타일
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E5D8C8")
    ax.spines["bottom"].set_color("#E5D8C8")

    ax.tick_params(axis="x", labelsize=10, colors="#4A4038")
    ax.tick_params(axis="y", labelsize=10, colors="#6F6258")

    plt.xticks(rotation=35, ha="right")

    # 은은한 그리드
    ax.grid(axis="y", linestyle="--", alpha=0.18)
    ax.set_axisbelow(True)

    # y축 여백
    ax.set_ylim(0, max(values) * 1.15)

    plt.tight_layout()
    st.pyplot(fig)

# =========================
# Hero Section
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">서울시 카페 상권분석 대시보드</div>
    <div class="hero-subtitle">
        카페 공급, 생활인구, 음식 소비 데이터를 결합해<br>
        신규 커피 브랜드의 최적 입지와 타깃 소비자를 도출합니다.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI 카드
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("총 카페 수", f"{total_cafe:,}개")
col2.metric("카페 수 1위", top_cafe_gu)
col3.metric("공급 부족 가능성 1위", top_shortage_gu)
col4.metric("카페당 음식지출액 1위", top_spending_gu)

# =========================
# Executive Summary
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">EXECUTIVE SUMMARY</div>', unsafe_allow_html=True)
st.header("분석 요약")

st.write(f"""
이번 대시보드는 서울시 자치구별 카페 공급 현황과 생활인구, 음식 소비 데이터를 함께 분석하여  
신규 커피 브랜드가 우선적으로 검토할 수 있는 입지 후보를 도출했습니다.

분석 결과, 1차 입지 후보로는 **{best_gu}**를 우선 검토할 수 있습니다.  
이는 단순히 카페 수가 적은 지역이 아니라, 생활인구와 소비력 대비 카페 공급 여지가 있는지를 함께 고려한 결과입니다.
""")

st.markdown(f"""
<div class="insight-box">
<b>핵심 인사이트:</b> 신규 브랜드는 이미 카페가 많은 지역보다, 
생활인구와 소비 여력에 비해 카페 공급이 상대적으로 부족한 지역을 우선 검토하는 것이 유리합니다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 1. 자치구별 카페 수
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">MARKET SUPPLY</div>', unsafe_allow_html=True)
st.header("1. 자치구별 카페 수 분석")

st.write("""
자치구별 카페 수는 서울 내 카페 공급이 어느 지역에 집중되어 있는지를 보여줍니다.  
카페 수가 많은 지역은 이미 상권이 형성되어 있지만, 동시에 경쟁 강도도 높을 가능성이 있습니다.
""")

top_cafe = cafe_gu.sort_values("카페수", ascending=False).head(10)
draw_bar_chart(top_cafe, "자치구", "카페수", "자치구별 카페 수 TOP 10", "카페 수")

st.markdown(f"""
<div class="insight-box">
카페 수가 가장 많은 지역은 <b>{top_cafe_gu}</b>입니다. 
상업 활동과 유동인구가 활발하다는 점을 보여주지만, 신규 브랜드 입장에서는 경쟁이 치열할 수 있습니다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 2. 카페 밀집도
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">COMPETITION DENSITY</div>', unsafe_allow_html=True)
st.header("2. 면적 대비 카페 밀집도 분석")

st.write("""
카페 밀집도는 자치구 면적 1㎢당 카페 수를 의미합니다.  
단순 카페 수보다 공간 대비 경쟁 강도를 더 잘 보여주는 지표입니다.
""")

top_density = density_area.sort_values("면적대비_카페밀집도", ascending=False).head(10)
top_density_gu = top_density.iloc[0]["자치구"]

draw_bar_chart(
    top_density,
    "자치구",
    "면적대비_카페밀집도",
    "면적 대비 카페 밀집도 TOP 10",
    "1㎢당 카페 수"
)

st.markdown(f"""
<div class="insight-box">
면적 대비 카페 밀집도가 가장 높은 지역은 <b>{top_density_gu}</b>입니다. 
좁은 공간 안에 카페가 많이 몰려 있어 경쟁 강도가 높은 상권으로 해석할 수 있습니다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 3. 카페 1개당 생활인구
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">DEMAND GAP</div>', unsafe_allow_html=True)
st.header("3. 카페 공급 부족 가능성 분석")

st.write("""
`카페 1개당 생활인구`는 카페 한 곳이 담당하는 평균 생활인구를 의미합니다.  
값이 높을수록 생활인구에 비해 카페 수가 적어, 공급 부족 가능성이 있는 지역으로 볼 수 있습니다.
""")

top_shortage = final_df.sort_values("카페1개당생활인구", ascending=False).head(10)

draw_bar_chart(
    top_shortage,
    "자치구",
    "카페1개당생활인구",
    "카페 1개당 생활인구 TOP 10",
    "카페 1개당 생활인구"
)

st.markdown(f"""
<div class="insight-box">
생활인구 대비 카페 공급이 가장 부족할 가능성이 높은 지역은 <b>{top_shortage_gu}</b>입니다. 
신규 커피 브랜드 입점 후보로 우선 검토할 수 있습니다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 4. 카페 1개당 음식지출액
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">SPENDING POTENTIAL</div>', unsafe_allow_html=True)
st.header("4. 카페 1개당 음식지출액 분석")

st.write("""
`카페 1개당 음식지출액`은 음식 소비 규모를 카페 수로 나눈 값입니다.  
값이 높을수록 소비 여력은 큰데 카페 공급은 상대적으로 적은 지역으로 해석할 수 있습니다.
""")

top_spending = final_df.sort_values("카페1개당음식지출액", ascending=False).head(10)

draw_bar_chart(
    top_spending,
    "자치구",
    "카페1개당음식지출액",
    "카페 1개당 음식지출액 TOP 10",
    "카페 1개당 음식지출액"
)

st.markdown(f"""
<div class="insight-box">
카페 1개당 음식지출액이 가장 높은 지역은 <b>{top_spending_gu}</b>입니다. 
이는 소비력 대비 카페 공급이 상대적으로 부족할 가능성을 보여줍니다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 5. 생활인구 1인당 음식지출액
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">PREMIUM MARKET</div>', unsafe_allow_html=True)
st.header("5. 생활인구 1인당 음식지출액 분석")

st.write("""
`생활인구 1인당 음식지출액`은 지역의 소비력 수준을 보여주는 지표입니다.  
프리미엄 커피 브랜드 입지를 검토할 때 참고할 수 있습니다.
""")

top_per_person = final_df.sort_values("생활인구1인당음식지출액", ascending=False).head(10)
top_per_person_gu = top_per_person.iloc[0]["자치구"]

draw_bar_chart(
    top_per_person,
    "자치구",
    "생활인구1인당음식지출액",
    "생활인구 1인당 음식지출액 TOP 10",
    "생활인구 1인당 음식지출액"
)

st.markdown(f"""
<div class="insight-box">
생활인구 1인당 음식지출액이 가장 높은 지역은 <b>{top_per_person_gu}</b>입니다. 
프리미엄 또는 스페셜티 커피 브랜드 입지로 검토할 수 있습니다.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 최종 추천
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">FINAL RECOMMENDATION</div>', unsafe_allow_html=True)
st.header("최종 입지 제안")

st.write("""
최종 입지 후보는 다음 세 가지 조건을 함께 고려했습니다.

1. 생활인구 대비 카페 공급이 부족한가  
2. 카페 1개당 음식지출액이 높은가  
3. 생활인구 1인당 음식지출액이 높은가  
""")

st.dataframe(
    recommend[
        [
            "자치구",
            "카페수",
            "총생활인구수",
            "카페1개당생활인구",
            "카페1개당음식지출액",
            "생활인구1인당음식지출액",
            "입지점수"
        ]
    ],
    use_container_width=True
)

st.markdown(f"""
<div class="insight-box">
분석 결과, 신규 커피 브랜드의 1차 입지 후보로는 <b>{best_gu}</b>를 우선 검토할 수 있습니다. 
다만 실제 입점 의사결정에서는 임대료, 역세권 여부, 경쟁 브랜드 위치, 상권 이미지 등을 추가로 고려해야 합니다.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
