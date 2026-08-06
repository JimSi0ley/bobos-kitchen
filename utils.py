def format_cook_time(total_minutes):
    if total_minutes is None:
        return "Not specified"

    try:
        total_minutes = int(total_minutes)
    except (TypeError, ValueError):
        return "Not specified"

    hours, minutes = divmod(total_minutes, 60)

    if hours > 0 and minutes > 0:
        hour_word = "hr" if hours == 1 else "hrs"
        return f"{hours} {hour_word} {minutes} min"

    if hours > 0:
        hour_word = "hr" if hours == 1 else "hrs"
        return f"{hours} {hour_word}"

    return f"{minutes} min"
