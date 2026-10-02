import streamlit as st
from datetime import datetime
import re

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Trà Sữa HOLI - Đặt món",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# HIỂN THỊ ẢNH
# =========================================================

try:
    st.image("ẢNH TRÀ SỮA.jpg", use_container_width=True)
except:
    pass

# =========================================================
# CSS GIAO DIỆN
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #7B3F20;
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
    background-color: #fff3e8;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 15px;
}

.total-price {
    font-size: 30px;
    font-weight: bold;
    color: #8B4513;
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

.chatbot-title {
    font-size: 24px;
    font-weight: bold;
    color: #7B3F20;
}

.chatbot-box {
    background-color: #fff7ef;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #ead4c0;
}

.menu-card {
    padding: 12px;
    border: 1px solid #eee;
    border-radius: 10px;
    background-color: #fff;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DỮ LIỆU SẢN PHẨM
# =========================================================

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

# ĐỒ ĂN VẶT

snacks = {
    "Khoai tây chiên": 30000,
    "Xúc xích": 25000,
    "Cá viên chiên": 25000,
    "Gà viên chiên": 30000,
    "Phô mai que": 30000
}

# SIZE

size_price = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

# TOPPING

topping_price = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Hạt thủy tinh": 7000
}

# ĐƯỜNG

sugar_levels = [
    "100% đường",
    "70% đường",
    "50% đường",
    "30% đường",
    "0% đường"
]

# ĐÁ

ice_levels = [
    "100% đá",
    "70% đá",
    "50% đá",
    "30% đá",
    "Không đá"
]


# =========================================================
# THÔNG TIN QUÁN
# =========================================================

SHOP_NAME = "TRÀ SỮA HOLI"
SHOP_ADDRESS = "123 Nguyễn Văn Cừ, Quận 5, TP.HCM"
SHOP_PHONE = "0909 123 456"
OPEN_TIME = "08:00 - 22:00 hàng ngày"


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Xin chào! 👋 Mình là **HOLI**, trợ lý ảo của quán Trà Sữa HOLI 🧋\n\n"
                "Mình có thể giúp bạn:\n"
                "• 🧋 Tư vấn đồ uống\n"
                "• 💰 Tư vấn theo ngân sách\n"
                "• 🛒 Nhận đơn trực tiếp\n"
                "• 🎁 Xem khuyến mãi\n"
                "• 🕐 Xem giờ mở cửa và địa chỉ\n"
                "• 📦 Kiểm tra trạng thái đơn hàng\n\n"
                "Bạn muốn HOLI hỗ trợ gì?"
            )
        }
    ]

if "order_status" not in st.session_state:
    st.session_state.order_status = "Chưa có đơn hàng"


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def money(number):
    return f"{number:,} VNĐ"


# =========================================================
# HÀM TÍNH TỔNG
# =========================================================

def get_cart_total():
    return sum(item["total"] for item in st.session_state.cart)


# =========================================================
# HÀM THÊM MÓN VÀO GIỎ
# =========================================================

def add_to_cart(
    drink,
    size="M",
    quantity=1,
    sugar="50% đường",
    ice="50% đá",
    topping="Không topping"
):

    base_price = products.get(drink, 0)
    size_extra = size_price.get(size, 0)
    topping_extra = topping_price.get(topping, 0)

    unit_price = base_price + size_extra + topping_extra
    total = unit_price * quantity

    item = {
        "drink": drink,
        "size": size,
        "quantity": quantity,
        "sugar": sugar,
        "ice": ice,
        "topping": topping,
        "unit_price": unit_price,
        "total": total
    }

    st.session_state.cart.append(item)
    st.session_state.paid = False

    return total


# =========================================================
# CHATBOT - TÌM SẢN PHẨM
# =========================================================

def find_product(message):

    message_lower = message.lower()

    # Tìm trà sữa / đồ uống
    for product in products:

        if product.lower() in message_lower:
            return product

        # Một số từ khóa ngắn
        keyword = product.lower().replace("trà sữa ", "")

        if keyword in message_lower and len(keyword) > 3:
            return product

    return None


# =========================================================
# CHATBOT - XỬ LÝ CÂU HỎI
# =========================================================

def chatbot_response(message):

    msg = message.lower().strip()

    # -----------------------------------------------------
    # CHÀO HỎI
    # -----------------------------------------------------

    if any(word in msg for word in [
        "xin chào",
        "hello",
        "hi",
        "chào"
    ]):

        return (
            "Xin chào bạn 👋🧋\n\n"
            "Mình là HOLI. Bạn có thể hỏi mình về:\n"
            "• Menu và giá\n"
            "• Topping\n"
            "• Đồ ăn vặt\n"
            "• Khuyến mãi\n"
            "• Đặt món\n"
            "• Địa chỉ và giờ mở cửa\n"
            "• Thanh toán\n"
            "• Trạng thái đơn hàng"
        )

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    if any(word in msg for word in [
        "menu",
        "thực đơn",
        "có món gì",
        "đồ uống",
        "trà sữa"
    ]):

        result = "🧋 **MENU TRÀ SỮA HOLI**\n\n"

        for name, price in products.items():
            result += f"• {name}: **{money(price)}**\n"

        result += "\n🍟 **ĐỒ ĂN VẶT**\n"

        for name, price in snacks.items():
            result += f"• {name}: **{money(price)}**\n"

        return result

    # -----------------------------------------------------
    # TOPPING
    # -----------------------------------------------------

    if "topping" in msg:

        result = "🧋 **TOPPING TẠI HOLI**\n\n"

        for name, price in topping_price.items():

            if price == 0:
                result += f"• {name}\n"
            else:
                result += f"• {name}: **+{money(price)}**\n"

        return result

    # -----------------------------------------------------
    # ĐỒ ĂN VẶT
    # -----------------------------------------------------

    if any(word in msg for word in [
        "đồ ăn",
        "ăn vặt",
        "snack",
        "đồ ăn vặt"
    ]):

        result = "🍟 **ĐỒ ĂN VẶT HOLI**\n\n"

        for name, price in snacks.items():
            result += f"• {name}: **{money(price)}**\n"

        return result

    # -----------------------------------------------------
    # KHUYẾN MÃI
    # -----------------------------------------------------

    if any(word in msg for word in [
        "khuyến mãi",
        "ưu đãi",
        "giảm giá",
        "voucher",
        "sale"
    ]):

        return (
            "🎁 **CHƯƠNG TRÌNH KHUYẾN MÃI HOLI**\n\n"
            "🥤 Mua từ 2 ly trà sữa: giảm 5.000 VNĐ.\n"
            "👥 Đơn từ 100.000 VNĐ: tặng 1 topping.\n"
            "🎂 Khách hàng sinh nhật: giảm 10% hóa đơn.\n\n"
            "Bạn có thể hỏi mình: **'Đơn 100k được ưu đãi gì?'**"
        )

    # -----------------------------------------------------
    # GIỜ MỞ CỬA
    # -----------------------------------------------------

    if any(word in msg for word in [
        "giờ mở cửa",
        "mở cửa",
        "đóng cửa",
        "mấy giờ"
    ]):

        return (
            f"🕐 **Giờ mở cửa HOLI:**\n\n"
            f"{OPEN_TIME}."
        )

    # -----------------------------------------------------
    # ĐỊA CHỈ
    # -----------------------------------------------------

    if any(word in msg for word in [
        "địa chỉ",
        "ở đâu",
        "cửa hàng",
        "địa điểm"
    ]):

        return (
            f"📍 **Địa chỉ HOLI:**\n\n"
            f"{SHOP_ADDRESS}\n\n"
            f"☎️ Hotline: {SHOP_PHONE}"
        )

    # -----------------------------------------------------
    # THANH TOÁN
    # -----------------------------------------------------

    if any(word in msg for word in [
        "thanh toán",
        "trả tiền",
        "thanh toán bằng gì",
        "payment"
    ]):

        return (
            "💳 **PHƯƠNG THỨC THANH TOÁN**\n\n"
            "• 💵 Tiền mặt\n"
            "• 🏦 Chuyển khoản\n"
            "• 📱 MoMo\n"
            "• 💳 Thẻ ngân hàng"
        )

    # -----------------------------------------------------
    # KIỂM TRA ĐƠN
    # -----------------------------------------------------

    if any(word in msg for word in [
        "trạng thái đơn",
        "đơn hàng của tôi",
        "đơn tới đâu",
        "kiểm tra đơn",
        "đơn hàng"
    ]):

        if len(st.session_state.cart) == 0:

            return (
                "📦 Hiện tại bạn chưa có đơn hàng nào.\n\n"
                "Bạn có thể nhắn:\n"
                "**'Cho tôi 1 trà sữa matcha'**"
            )

        total = get_cart_total()

        return (
            "📦 **TRẠNG THÁI ĐƠN HÀNG**\n\n"
            f"Trạng thái: **{st.session_state.order_status}**\n\n"
            f"Số món: **{len(st.session_state.cart)}**\n"
            f"Tổng tiền: **{money(total)}**"
        )

    # -----------------------------------------------------
    # NGÂN SÁCH
    # -----------------------------------------------------

    numbers = re.findall(r"\d+", msg)

    if "ngân sách" in msg or "budget" in msg:

        if numbers:

            budget = int(numbers[0])

            # Nếu người dùng nhập 50k
            if "k" in msg:
                budget = budget * 1000

            affordable = []

            for name, price in products.items():

                if price <= budget:
                    affordable.append(
                        f"• {name}: **{money(price)}**"
                    )

            if affordable:

                return (
                    f"💰 Với ngân sách khoảng **{money(budget)}**, "
                    "HOLI gợi ý:\n\n"
                    + "\n".join(affordable[:6])
                )

            return "💰 Ngân sách này hơi thấp so với menu hiện tại. Bạn có thể tăng ngân sách một chút nhé!"

        return (
            "💰 Bạn cho HOLI biết ngân sách nhé.\n\n"
            "Ví dụ:\n"
            "👉 'Tư vấn cho tôi đồ uống dưới 40k'\n"
            "👉 'Tôi có ngân sách 50k'"
        )

    # -----------------------------------------------------
    # TƯ VẤN THEO SỞ THÍCH
    # -----------------------------------------------------

    if any(word in msg for word in [
        "ngọt",
        "thanh",
        "béo",
        "matcha",
        "trái cây",
        "chua",
        "ít ngọt"
    ]):

        if "matcha" in msg:
            return (
                "🍵 Nếu bạn thích vị trà thơm, hơi đắng nhẹ và béo, "
                "HOLI gợi ý **Trà sữa matcha – 35.000 VNĐ**.\n\n"
                "Bạn có thể chọn 50% đường + 50% đá để vị matcha cân bằng hơn."
            )

        if "trái cây" in msg or "thanh" in msg:
            return (
                "🍑 Nếu bạn thích vị thanh mát, HOLI gợi ý:\n\n"
                "• Trà đào – 30.000 VNĐ\n"
                "• Trà vải – 30.000 VNĐ\n"
                "• Trà chanh – 25.000 VNĐ"
            )

        if "ngọt" in msg:
            return (
                "🍯 Nếu bạn thích vị ngọt đậm, HOLI gợi ý:\n\n"
                "• Trà sữa trân châu đường đen\n"
                "• Trà sữa socola\n"
                "• Trà sữa truyền thống"
            )

        if "béo" in msg:
            return (
                "🥛 Nếu bạn thích vị béo, HOLI gợi ý "
                "**Trà sữa khoai môn** hoặc thêm **kem cheese +10.000 VNĐ**."
            )

        if "ít ngọt" in msg:
            return (
                "🌿 Nếu bạn thích ít ngọt, hãy chọn mức **30% hoặc 0% đường**.\n\n"
                "HOLI gợi ý Trà đào, Trà vải hoặc Trà sữa ô long."
            )

    # -----------------------------------------------------
    # ĐẶT MÓN TRỰC TIẾP
    # -----------------------------------------------------

    product = find_product(msg)

    if product:

        quantity = 1

        if numbers:
            quantity = int(numbers[0])

            if quantity > 20:
                quantity = 20

        size = "M"

        if "xl" in msg:
            size = "XL"
        elif re.search(r"\bl\b", msg):
            size = "L"

        sugar = "50% đường"

        if "100% đường" in msg:
            sugar = "100% đường"
        elif "70% đường" in msg:
            sugar = "70% đường"
        elif "30% đường" in msg:
            sugar = "30% đường"
        elif "0% đường" in msg:
            sugar = "0% đường"

        ice = "50% đá"

        if "không đá" in msg:
            ice = "Không đá"
        elif "30% đá" in msg:
            ice = "30% đá"
        elif "70% đá" in msg:
            ice = "70% đá"
        elif "100% đá" in msg:
            ice = "100% đá"

        topping = "Không topping"

        for topping_name in topping_price:

            if topping_name.lower() in msg:
                topping = topping_name
                break

        total = add_to_cart(
            drink=product,
            size=size,
            quantity=quantity,
            sugar=sugar,
            ice=ice,
            topping=topping
        )

        st.session_state.order_status = "Đã nhận đơn"

        return (
            f"✅ HOLI đã thêm vào đơn hàng:\n\n"
            f"🧋 **{quantity} ly {product}**\n"
            f"📏 Size: **{size}**\n"
            f"🍬 Đường: **{sugar}**\n"
            f"🧊 Đá: **{ice}**\n"
            f"🧋 Topping: **{topping}**\n\n"
            f"💰 Thành tiền: **{money(total)}**\n\n"
            f"Bạn có thể nhắn **'xác nhận đơn'** để kiểm tra lại đơn."
        )

    # -----------------------------------------------------
    # XÁC NHẬN ĐƠN
    # -----------------------------------------------------

    if any(word in msg for word in [
        "xác nhận đơn",
        "xác nhận",
        "đặt đơn"
    ]):

        if len(st.session_state.cart) == 0:
            return "🛒 Đơn hàng hiện đang trống."

        total = get_cart_total()

        result = "✅ **XÁC NHẬN ĐƠN HÀNG**\n\n"

        for index, item in enumerate(
            st.session_state.cart,
            start=1
        ):

            result += (
                f"{index}. {item['drink']} - "
                f"{item['quantity']} ly - "
                f"{money(item['total'])}\n"
            )

        result += (
            f"\n💰 **TỔNG CỘNG: {money(total)}**\n\n"
            "Nếu thông tin chính xác, bạn có thể bấm nút "
            "**THANH TOÁN** ở khu vực Đơn hàng."
        )

        return result

    # -----------------------------------------------------
    # TỔNG TIỀN
    # -----------------------------------------------------

    if any(word in msg for word in [
        "tổng tiền",
        "bao nhiêu tiền",
        "hết bao nhiêu",
        "tính tiền"
    ]):

        total = get_cart_total()

        if total == 0:
            return "🛒 Bạn chưa có món nào trong đơn hàng."

        return (
            f"🧮 Tổng tiền hiện tại của đơn hàng là:\n\n"
            f"# **{money(total)}**"
        )

    # -----------------------------------------------------
    # CÂU HỎI MẶC ĐỊNH
    # -----------------------------------------------------

    return (
        "😊 HOLI chưa hiểu rõ câu hỏi của bạn.\n\n"
        "Bạn có thể thử:\n"
        "👉 **Menu có những món gì?**\n"
        "👉 **Tư vấn đồ uống dưới 40k**\n"
        "👉 **Tôi thích vị ngọt**\n"
        "👉 **Cho tôi 1 trà sữa matcha**\n"
        "👉 **Topping có gì?**\n"
        "👉 **Hôm nay có khuyến mãi gì?**\n"
        "👉 **Quán mở cửa mấy giờ?**\n"
        "👉 **Địa chỉ quán ở đâu?**\n"
        "👉 **Kiểm tra đơn hàng**"
    )


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">🧋 TRÀ SỮA HOLI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ứng dụng đặt món - Chatbot tư vấn - Tính hóa đơn</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHIA GIAO DIỆN THÀNH 2 CỘT
# =========================================================

chat_col, main_col = st.columns([1, 2.4])


# =========================================================
# CHATBOT
# =========================================================

with chat_col:

    st.markdown(
        '<div class="chatbot-title">🤖 Chat với HOLI</div>',
        unsafe_allow_html=True
    )

    st.caption("Trợ lý ảo của Trà Sữa HOLI")

    # Hiển thị lịch sử chat

    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Nút gợi ý

    st.markdown("### 💡 Gợi ý nhanh")

    quick1 = st.button(
        "🧋 Xem menu",
        use_container_width=True
    )

    quick2 = st.button(
        "🎁 Khuyến mãi",
        use_container_width=True
    )

    quick3 = st.button(
        "💰 Tư vấn dưới 40k",
        use_container_width=True
    )

    quick4 = st.button(
        "🕐 Giờ mở cửa",
        use_container_width=True
    )

    quick5 = st.button(
        "📦 Kiểm tra đơn",
        use_container_width=True
    )

    quick_message = None

    if quick1:
        quick_message = "Xem menu"

    elif quick2:
        quick_message = "Khuyến mãi"

    elif quick3:
        quick_message = "Tư vấn đồ uống dưới 40k"

    elif quick4:
        quick_message = "Giờ mở cửa"

    elif quick5:
        quick_message = "Kiểm tra đơn hàng"

    # Ô nhập chat

    user_message = st.chat_input(
        "Nhập tin nhắn cho HOLI..."
    )

    # Nếu bấm nút nhanh

    if quick_message:
        user_message = quick_message

    if user_message:

        # Hiển thị tin nhắn người dùng

        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_message
        })

        # Xử lý chatbot

        answer = chatbot_response(user_message)

        # Lưu câu trả lời

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()


# =========================================================
# KHU VỰC ĐẶT MÓN
# =========================================================

with main_col:

    # =====================================================
    # THÔNG TIN KHÁCH HÀNG
    # =====================================================

    st.header("👤 Thông tin khách hàng")

    customer_name = st.text_input(
        "Tên khách hàng",
        placeholder="Nhập tên khách hàng..."
    )

    st.divider()

    # =====================================================
    # CHỌN MÓN
    # =====================================================

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

    # =====================================================
    # TÍNH GIÁ
    # =====================================================

    base_price = products[drink]
    size_extra = size_price[size]
    topping_extra = topping_price[topping]

    unit_price = (
        base_price
        + size_extra
        + topping_extra
    )

    item_total = unit_price * quantity

    st.markdown("### 💰 Chi tiết giá")

    price_col1, price_col2, price_col3, price_col4 = st.columns(4)

    with price_col1:
        st.metric(
            "Giá đồ uống",
            money(base_price)
        )

    with price_col2:
        st.metric(
            "Size",
            f"+{money(size_extra)}"
        )

    with price_col3:
        st.metric(
            "Topping",
            f"+{money(topping_extra)}"
        )

    with price_col4:
        st.metric(
            "Thành tiền",
            money(item_total)
        )

    # =====================================================
    # THÊM MÓN
    # =====================================================

    if st.button(
        "➕ Thêm món vào đơn",
        use_container_width=True
    ):

        if not customer_name.strip():

            st.warning(
                "⚠️ Vui lòng nhập tên khách hàng trước!"
            )

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

            st.session_state.order_status = "Đã nhận đơn"

            st.success(
                f"✅ Đã thêm {quantity} ly {drink} vào đơn hàng!"
            )

    # =====================================================
    # ĐƠN HÀNG
    # =====================================================

    st.divider()

    st.header("🛒 Đơn hàng")

    if len(st.session_state.cart) == 0:

        st.info(
            "Chưa có món nào trong đơn hàng."
        )

    else:

        grand_total = 0

        for index, item in enumerate(
            st.session_state.cart
        ):

            grand_total += item["total"]

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [4, 2, 1]
                )

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
                        f"Đơn giá: "
                        f"**{money(item['unit_price'])}**"
                    )

                    st.write(
                        f"Thành tiền: "
                        f"**{money(item['total'])}**"
                    )

                with col3:

                    if st.button(
                        "🗑️ Xóa",
                        key=f"delete_{index}"
                    ):

                        st.session_state.cart.pop(
                            index
                        )

                        st.rerun()

        # =================================================
        # TỔNG TIỀN
        # =================================================

        st.markdown(
            f"""
            <div class="total-box">
                <div>TỔNG THANH TOÁN</div>
                <div class="total-price">
                    {money(grand_total)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # THANH TOÁN
        # =================================================

        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True
        ):

            st.session_state.paid = True

            st.session_state.order_status = (
                "Đã thanh toán - Đang chuẩn bị"
            )

            st.balloons()


# =========================================================
# HÓA ĐƠN
# =========================================================

if (
    st.session_state.paid
    and len(st.session_state.cart) > 0
):

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
            🧋 TRÀ SỮA HOLI
        </div>

        <div class="invoice-center">
            <p>HÓA ĐƠN THANH TOÁN</p>
            <p>Thời gian: {invoice_time}</p>
        </div>

        <hr>

        <p>
            <b>Khách hàng:</b>
            {customer_name}
        </p>

        <p>
            <b>Trạng thái:</b>
            Đã thanh toán
        </p>

        <hr>

        <table style="width:100%; border-collapse:collapse;">

            <tr>
                <th style="text-align:left;">
                    Món
                </th>

                <th>
                    SL
                </th>

                <th>
                    Đơn giá
                </th>

                <th style="text-align:right;">
                    Thành tiền
                </th>
            </tr>
    """

    for item in st.session_state.cart:

        invoice_html += f"""
            <tr>

                <td style="padding:8px 0;">

                    {item['drink']}<br>

                    <small>
                        Size {item['size']} -
                        {item['topping']} -
                        {item['sugar']} -
                        {item['ice']}
                    </small>

                </td>

                <td style="text-align:center;">
                    {item['quantity']}
                </td>

                <td style="text-align:center;">
                    {money(item['unit_price'])}
                </td>

                <td style="text-align:right;">
                    {money(item['total'])}
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
            {money(grand_total)}

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

    st.write("")

    # =====================================================
    # ĐƠN HÀNG MỚI
    # =====================================================

    if st.button(
        "🔄 Tạo đơn hàng mới",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.session_state.paid = False

        st.session_state.order_status = (
            "Chưa có đơn hàng"
        )

        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content":
                    "Xin chào! 👋 Đơn hàng mới đã được tạo. "
                    "HOLI sẵn sàng hỗ trợ bạn 🧋"
            }
        ]

        st.rerun()


# =========================================================
# THÔNG TIN CUỐI TRANG
# =========================================================

st.divider()

footer1, footer2, footer3 = st.columns(3)

with footer1:

    st.markdown(
        f"""
        🕐 **Giờ mở cửa**

        {OPEN_TIME}
        """
    )

with footer2:

    st.markdown(
        f"""
        📍 **Địa chỉ**

        {SHOP_ADDRESS}
        """
    )

with footer3:

    st.markdown(
        """
        💳 **Thanh toán**

        Tiền mặt | Chuyển khoản | MoMo | Thẻ
        """
    )

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        🧋 <b>HOLI</b> - Ngon từng vị, vui từ tâm ❤️
    </div>
    """,
    unsafe_allow_html=True
)
