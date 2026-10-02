import streamlit as st
from datetime import datetime

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .total-box {
        padding: 18px;
        border-radius: 12px;
        background-color: #f5f5f5;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .total-price {
        font-size: 30px;
        font-weight: bold;
    }

    .invoice {
        border: 2px solid #333;
        border-radius: 10px;
        padding: 25px;
        background-color: white;
        color: black;
    }

    .invoice-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
    }

    .invoice-center {
        text-align: center;
    }

    .thank-you {
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# DỮ LIỆU SẢN PHẨM
# =========================
products = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa ô long": 32000,
    "Trà sữa trân châu đường đen": 40000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000
}

size_price = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

topping_price = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Hạt thủy tinh": 7000
}

sugar_levels = [
    "100% đường",
    "70% đường",
    "50% đường",
    "30% đường",
    "0% đường"
]

ice_levels = [
    "100% đá",
    "70% đá",
    "50% đá",
    "30% đá",
    "Không đá"
]

# =========================
# SESSION STATE
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<div class="main-title">🧋 QUÁN TRÀ SỮA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ứng dụng đặt món và tính hóa đơn</div>',
    unsafe_allow_html=True
)

# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

st.divider()

# =========================
# CHỌN MÓN
# =========================
st.header("🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / đồ uống",
        list(products.keys())
    )

    size = st.selectbox(
        "Size ly",
        list(size_price.keys())
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

with col2:
    sugar = st.selectbox(
        "Mức độ đường",
        sugar_levels
    )

    ice = st.selectbox(
        "Mức độ đá",
        ice_levels
    )

    topping = st.selectbox(
        "Topping",
        list(topping_price.keys())
    )

# =========================
# TÍNH GIÁ
# =========================
base_price = products[drink]
size_extra = size_price[size]
topping_extra = topping_price[topping]

unit_price = base_price + size_extra + topping_extra
item_total = unit_price * quantity

st.markdown("### 💰 Chi tiết giá")

price_col1, price_col2, price_col3, price_col4 = st.columns(4)

with price_col1:
    st.metric("Giá đồ uống", f"{base_price:,} VNĐ")

with price_col2:
    st.metric("Size", f"+{size_extra:,} VNĐ")

with price_col3:
    st.metric("Topping", f"+{topping_extra:,} VNĐ")

with price_col4:
    st.metric("Thành tiền", f"{item_total:,} VNĐ")

# =========================
# THÊM MÓN
# =========================
if st.button("➕ Thêm món vào đơn", use_container_width=True):

    if not customer_name.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước!")
    else:
        item = {
            "drink": drink,
            "size": size,
            "quantity": quantity,
            "sugar": sugar,
            "ice": ice,
            "topping": topping,
            "unit_price": unit_price,
            "total": item_total
        }

        st.session_state.cart.append(item)
        st.session_state.paid = False

        st.success(f"✅ Đã thêm {quantity} ly {drink} vào đơn hàng!")

# =========================
# HIỂN THỊ GIỎ HÀNG
# =========================
st.divider()

st.header("🛒 Đơn hàng")

if len(st.session_state.cart) == 0:

    st.info("Chưa có món nào trong đơn hàng.")

else:

    grand_total = 0

    for index, item in enumerate(st.session_state.cart):

        grand_total += item["total"]

        with st.container(border=True):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.subheader(
                    f"{index + 1}. {item['drink']}"
                )

                st.write(
                    f"Size: **{item['size']}** | "
                    f"Đường: **{item['sugar']}** | "
                    f"Đá: **{item['ice']}**"
                )

                st.write(
                    f"Topping: **{item['topping']}**"
                )

            with col2:
                st.write(
                    f"Số lượng: **{item['quantity']}**"
                )

                st.write(
                    f"Đơn giá: **{item['unit_price']:,} VNĐ**"
                )

                st.write(
                    f"Thành tiền: **{item['total']:,} VNĐ**"
                )

            with col3:
                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{index}"
                ):
                    st.session_state.cart.pop(index)
                    st.rerun()

    # =========================
    # TỔNG TIỀN
    # =========================
    st.markdown(
        f"""
        <div class="total-box">
            <div>TỔNG THANH TOÁN</div>
            <div class="total-price">
                {grand_total:,} VNĐ
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # THANH TOÁN
    # =========================
    if st.button(
        "💳 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):
        st.session_state.paid = True
        st.balloons()

# =========================
# HÓA ĐƠN
# =========================
if st.session_state.paid and len(st.session_state.cart) > 0:

    grand_total = sum(
        item["total"]
        for item in st.session_state.cart
    )

    invoice_time = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    st.divider()

    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    invoice_html = f"""
    <div class="invoice">

        <div class="invoice-title">
            🧋 QUÁN TRÀ SỮA
        </div>

        <div class="invoice-center">
            <p>HÓA ĐƠN THANH TOÁN</p>
            <p>Thời gian: {invoice_time}</p>
        </div>

        <hr>

        <p>
            <b>Khách hàng:</b> {customer_name}
        </p>

        <hr>

        <table style="width:100%; border-collapse:collapse;">
            <tr>
                <th style="text-align:left;">Món</th>
                <th>SL</th>
                <th>Đơn giá</th>
                <th style="text-align:right;">Thành tiền</th>
            </tr>
    """

    for item in st.session_state.cart:

        invoice_html += f"""
            <tr>
                <td style="padding:8px 0;">
                    {item['drink']}<br>
                    <small>
                        Size {item['size']} -
                        {item['topping']}
                    </small>
                </td>

                <td style="text-align:center;">
                    {item['quantity']}
                </td>

                <td style="text-align:center;">
                    {item['unit_price']:,}
                </td>

                <td style="text-align:right;">
                    {item['total']:,} VNĐ
                </td>
            </tr>
        """

    invoice_html += f"""
        </table>

        <hr>

        <div style="
            text-align:right;
            font-size:20px;
            font-weight:bold;
        ">
            TỔNG CỘNG:
            {grand_total:,} VNĐ
        </div>

        <p class="thank-you">
            CẢM ƠN QUÝ KHÁCH! 🧋❤️
        </p>

    </div>
    """

    st.markdown(
        invoice_html,
        unsafe_allow_html=True
    )

    # =========================
    # NÚT ĐƠN HÀNG MỚI
    # =========================
    st.write("")

    if st.button(
        "🔄 Tạo đơn hàng mới",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.paid = False
        st.rerun()
