import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(
    page_title="서울시 카페 상권분석",
    layout="wide"
)

st.title("서울시 카페 상권분석 대시보드")
st.write(
    """
    서울시 자치구별 카페 공급, 생활인구, 음식 소비 데이터를 결합하여  
    신규 커피 브랜드의 입지 가능성을 분석한 대시보드입니다.
    """
)

# 데이터 불러오기
cafe_gu = pd.read_csv("cafe_gu.csv")
density_area = pd.read_csv("density_area.csv")
final_df = pd.read_csv("final_df.csv")

# 핵심 지표
total_cafe = cafe_gu["카페수"].sum()
top_cafe_gu = cafe_gu.sort_values("카페수", ascending=False).iloc[0]["자치구"]
top_shortage_gu = final_df.sort_values("카페1개당생활인구", ascending=False).iloc[0]["자치구"]
top_spending_gu = final_df.sort_values("카페1개당음식지출액", ascending=False).iloc[0]["자치구"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("총 카페 수", f"{total_cafe:,}개")
col2.metric("카페 수 1위", top_cafe_gu)
col3.metric("공급 부족 가능성 1위", top_shortage_gu)
col4.metric("카페당 음식지출액 1위", top_spending_gu)

st.divider()

# 1. 자치구별 카페 수
st.header("1. 자치구별 카페 수 분석")
st.write(
    """
    자치구별 카페 수는 서울 내 카페 공급이 어느 지역에 집중되어 있는지를 보여줍니다.  
    카페 수가 많은 지역은 이미 상권이 형성되어 있지만, 동시에 경쟁 강도도 높을 가능성이 있습니다.
    """
)

top_cafe = cafe_gu.sort_values("카페수", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_cafe["자치구"], top_cafe["카페수"])
ax.set_title("자치구별 카페 수 TOP 10")
ax.set_xlabel("자치구")
ax.set_ylabel("카페 수")
plt.xticks(rotation=45)
st.pyplot(fig)

st.info(
    f"카페 수가 가장 많은 지역은 **{top_cafe_gu}**입니다. "
    "이는 해당 지역의 상업 활동과 유동인구가 활발하다는 점을 보여주지만, 신규 브랜드 입장에서는 경쟁이 치열할 수 있습니다."
)

st.divider()

# 2. 카페 밀집도
st.header("2. 면적 대비 카페 밀집도 분석")
st.write(
    """
    카페 밀집도는 자치구 면적 1㎢당 카페 수를 의미합니다.  
    단순 카페 수보다 공간 대비 경쟁 강도를 더 잘 보여주는 지표입니다.
    """
)

top_density = density_area.sort_values("면적대비_카페밀집도", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_density["자치구"], top_density["면적대비_카페밀집도"])
ax.set_title("면적 대비 카페 밀집도 TOP 10")
ax.set_xlabel("자치구")
ax.set_ylabel("1㎢당 카페 수")
plt.xticks(rotation=45)
st.pyplot(fig)

top_density_gu = top_density.iloc[0]["자치구"]

st.info(
    f"면적 대비 카페 밀집도가 가장 높은 지역은 **{top_density_gu}**입니다. "
    "이 지역은 좁은 공간 안에 카페가 많이 몰려 있어 경쟁 강도가 높은 상권으로 해석할 수 있습니다."
)

st.divider()

# 3. 카페 1개당 생활인구
st.header("3. 카페 공급 부족 가능성 분석")
st.write(
    """
    `카페 1개당 생활인구`는 카페 한 곳이 담당하는 평균 생활인구를 의미합니다.  
    값이 높을수록 생활인구에 비해 카페 수가 적어, 공급 부족 가능성이 있는 지역으로 볼 수 있습니다.
    """
)

top_shortage = final_df.sort_values("카페1개당생활인구", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_shortage["자치구"], top_shortage["카페1개당생활인구"])
ax.set_title("카페 1개당 생활인구 TOP 10")
ax.set_xlabel("자치구")
ax.set_ylabel("카페 1개당 생활인구")
plt.xticks(rotation=45)
st.pyplot(fig)

st.success(
    f"생활인구 대비 카페 공급이 가장 부족할 가능성이 높은 지역은 **{top_shortage_gu}**입니다. "
    "신규 커피 브랜드 입점 후보로 우선 검토할 수 있습니다."
)

st.divider()

# 4. 카페 1개당 음식지출액
st.header("4. 카페 1개당 음식지출액 분석")
st.write(
    """
    `카페 1개당 음식지출액`은 음식 소비 규모를 카페 수로 나눈 값입니다.  
    값이 높을수록 소비 여력은 큰데 카페 공급은 상대적으로 적은 지역으로 해석할 수 있습니다.
    """
)

top_spending = final_df.sort_values("카페1개당음식지출액", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_spending["자치구"], top_spending["카페1개당음식지출액"])
ax.set_title("카페 1개당 음식지출액 TOP 10")
ax.set_xlabel("자치구")
ax.set_ylabel("카페 1개당 음식지출액")
plt.xticks(rotation=45)
st.pyplot(fig)

st.success(
    f"카페 1개당 음식지출액이 가장 높은 지역은 **{top_spending_gu}**입니다. "
    "이는 소비력 대비 카페 공급이 상대적으로 부족할 가능성을 보여줍니다."
)

st.divider()

# 5. 생활인구 1인당 음식지출액
st.header("5. 생활인구 1인당 음식지출액 분석")
st.write(
    """
    `생활인구 1인당 음식지출액`은 지역의 소비력 수준을 보여주는 지표입니다.  
    프리미엄 커피 브랜드 입지를 검토할 때 참고할 수 있습니다.
    """
)

top_per_person = final_df.sort_values("생활인구1인당음식지출액", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_per_person["자치구"], top_per_person["생활인구1인당음식지출액"])
ax.set_title("생활인구 1인당 음식지출액 TOP 10")
ax.set_xlabel("자치구")
ax.set_ylabel("생활인구 1인당 음식지출액")
plt.xticks(rotation=45)
st.pyplot(fig)

top_per_person_gu = top_per_person.iloc[0]["자치구"]

st.info(
    f"생활인구 1인당 음식지출액이 가장 높은 지역은 **{top_per_person_gu}**입니다. "
    "프리미엄 또는 스페셜티 커피 브랜드 입지로 검토할 수 있습니다."
)

st.divider()

# 최종 추천
st.header("최종 입지 제안")

candidate_df = final_df.copy()

candidate_df["입지점수"] = (
    candidate_df["카페1개당생활인구"].rank(ascending=True)
    + candidate_df["카페1개당음식지출액"].rank(ascending=True)
    + candidate_df["생활인구1인당음식지출액"].rank(ascending=True)
)

recommend = candidate_df.sort_values("입지점수", ascending=False).head(5)

st.write(
    """
    최종 입지 후보는 다음 세 가지 조건을 함께 고려했습니다.
    
    1. 생활인구 대비 카페 공급이 부족한가  
    2. 카페 1개당 음식지출액이 높은가  
    3. 생활인구 1인당 음식지출액이 높은가  
    """
)

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

best_gu = recommend.iloc[0]["자치구"]

st.success(
    f"분석 결과, 신규 커피 브랜드의 1차 입지 후보로는 **{best_gu}**를 우선 검토할 수 있습니다. "
    "다만 실제 입점 의사결정에서는 임대료, 역세권 여부, 경쟁 브랜드 위치, 상권 이미지 등을 추가로 고려해야 합니다."
)
