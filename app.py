import streamlit as st
import math

st.set_page_config(page_title="建築断面計算 Web", layout="wide")

st.title("🏗️ 建築断面性能計算 WebApp")

# --- サイドバー ---
st.sidebar.header("設定")
shape = st.sidebar.selectbox("断面形状を選択", ["H形鋼", "角形鋼管", "円形鋼管"])

# --- メインレイアウト ---
col_input, col_view, col_res = st.columns([1, 1.2, 1.2])

with col_input:
    st.subheader("📏 寸法入力")
    if shape == "H形鋼":
        H = st.number_input("H (全高) [mm]", value=400.0, step=10.0)
        B = st.number_input("B (幅) [mm]", value=200.0, step=10.0)
        tw = st.number_input("tw (ウェブ厚) [mm]", value=8.0, step=1.0)
        tf = st.number_input("tf (フランジ厚) [mm]", value=13.0, step=1.0)
        
        # 計算ロジック
        A = (B * H) - (B - tw) * (H - 2 * tf)
        Ix = (B * H**3 / 12) - ((B - tw) * (H - 2 * tf)**3 / 12)
        Iy = (2 * tf * B**3 / 12) + ((H - 2 * tf) * tw**3 / 12)
        Zx, Zy = Ix / (H / 2), Iy / (B / 2)

    elif shape == "角形鋼管":
        H = st.number_input("H (全高) [mm]", value=200.0, step=10.0)
        B = st.number_input("B (全幅) [mm]", value=200.0, step=10.0)
        t = st.number_input("t (肉厚) [mm]", value=6.0, step=1.0)
        
        A = (B * H) - (B - 2*t) * (H - 2*t)
        Ix = (B * H**3 / 12) - ((B - 2*t) * (H - 2*t)**3 / 12)
        Iy = (H * B**3 / 12) - ((H - 2*t) * (B - 2*t)**3 / 12)
        Zx, Zy = Ix / (H / 2), Iy / (B / 2)

    elif shape == "円形鋼管":
        D = st.number_input("D (外径) [mm]", value=216.3, step=0.1)
        t = st.number_input("t (肉厚) [mm]", value=5.8, step=0.1)
        
        inner_d = D - 2*t
        A = math.pi * (D**2 - inner_d**2) / 4
        Ix = Iy = math.pi * (D**4 - inner_d**4) / 64
        Zx = Zy = Ix / (D / 2)

    ix, iy = math.sqrt(Ix / A), math.sqrt(Iy / A)

with col_view:
    st.subheader("🖼️ 凡例と計算式")
    if shape == "H形鋼":
        st.code("""
      B
   <------>
   +------+  ^
   |      |  | tf
   +--+ +--+  v
      | |     
    H | | tw  
      | |     
   +--+ +--+  ^
   |      |  | tf
   +------+  v
        """)
        st.latex(r"I_x = \frac{BH^3 - (B-t_w)(H-2t_f)^3}{12}")
    elif shape == "角形鋼管":
        st.code("""
      B
   <------>
   +------+  ^
   | +--+ |  |
   | |  | |  | H
   | +--+ |  |
   +------+  v
    <-> t
        """)
        st.latex(r"I_x = \frac{BH^3 - (B-2t)(H-2t)^3}{12}")
    elif shape == "円形鋼管":
        st.code("""
     /---\ 
    |  +  | D
     \---/ 
      <-> t
        """)
        st.latex(r"I = \frac{\pi(D^4 - d^4)}{64}")

with col_res:
    st.subheader("📊 計算結果")
    st.metric("断面積 A", f"{A:,.1f} mm²")
    
    st.write("**強軸 (X-X軸)**")
    st.info(f"Ix: {Ix:.2e} mm⁴ / Zx: {Zx:.2e} mm³ / ix: {ix:.2f} mm")

    st.write("**弱軸 (Y-Y軸)**")
    st.success(f"Iy: {Iy:.2e} mm⁴ / Zy: {Zy:.2e} mm³ / iy: {iy:.2f} mm")
