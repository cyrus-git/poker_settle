import streamlit as st


def settle_debts(player_data):
    """
    player_data: [(name, balance), ...]
      balance > 0 : 受け取る金額
      balance < 0 : 支払う金額
    戻り値: [(payer, receiver, amount), ...]
    """
    plus_list = [(n, b) for (n, b) in player_data if b > 0]
    minus_list = [(n, b) for (n, b) in player_data if b < 0]

    # 多い順/小さい順にソート
    plus_list.sort(key=lambda x: x[1], reverse=True)
    minus_list.sort(key=lambda x: x[1])  # balanceがよりマイナスの人から

    results = []
    i, j = 0, 0

    while i < len(plus_list) and j < len(minus_list):
        name_plus, bal_plus = plus_list[i]
        name_minus, bal_minus = minus_list[j]

        # やり取りする金額を算出
        amount = min(bal_plus, abs(bal_minus))

        # 結果を追加
        results.append((name_minus, name_plus, amount))

        # 残高の更新
        bal_plus -= amount
        bal_minus += amount

        # 更新分を反映
        plus_list[i] = (name_plus, bal_plus)
        minus_list[j] = (name_minus, bal_minus)

        # 受取が0になったら次へ
        if plus_list[i][1] == 0:
            i += 1
        # 支払が0になったら次へ
        if minus_list[j][1] == 0:
            j += 1

    return results


def main():
    st.title("ポーカー精算 (シンプル)")

    num_players = st.number_input("プレイヤー数を入力", min_value=1, value=4, step=1)

    st.write("各プレイヤーの名前と損益を入力してください（プラス:勝ち, マイナス:負け）")
    player_data = []
    for i in range(num_players):
        default_name = f"Player{i+1}"
        name = st.text_input(f"プレイヤー {i+1} の名前",
                             value=default_name, key=f"name_{i}")
        balance = st.number_input(
            f"{name} の損益 (例: 300, -200)",
            value=0,
            step=100,
            key=f"balance_{i}"
        )
        player_data.append((name, balance))

    if st.button("精算を計算"):
        results = settle_debts(player_data)

        st.subheader("精算結果")
        if not results:
            st.write("やり取りはありません。全員バランスが取れています。")
        else:
            for payer, receiver, amount in results:
                st.write(f"**{payer}** → **{receiver}** : {amount} 円")


if __name__ == "__main__":
    main()
