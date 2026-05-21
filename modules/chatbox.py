from pythonosc import udp_client

osc = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)


def send_chatbox(text):

    try:

        if len(text) > 140:
            text = text[:140] + "..."

        osc.send_message(
            "/chatbox/input",
            [text, True, False]
        )

    except Exception as e:
        print(f"[CHATBOX ERROR] {e}")