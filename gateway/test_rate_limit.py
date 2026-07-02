from rate_limiter import check_rate_limit

for i in range(7):

    allowed = check_rate_limit("jiyanshee")

    print(
        f"Request {i+1}:",
        "Allowed" if allowed else "Blocked"
    )