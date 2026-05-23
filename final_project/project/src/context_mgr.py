def truncate_context(
    messages: list[dict[str, str]], limit_message: int, limit_chars: int
) -> list[dict[str, str]]:
    system_msgs = [m for m in messages if m['role'] == 'system']
    chat_msgs = [m for m in messages if m['role'] != 'system']

    if len(chat_msgs) > limit_message:
        chat_msgs = chat_msgs[-limit_message:]

    while chat_msgs:
        total_chars = sum(len(m['content']) for m in chat_msgs)

        if total_chars <= limit_chars:
            break

        oldest_msg = chat_msgs[0]
        excess = total_chars - limit_chars

        if len(oldest_msg['content']) > excess:
            oldest_msg['content'] = oldest_msg['content'][excess:]
            break
        else:
            chat_msgs.pop(0)

    return system_msgs + chat_msgs
