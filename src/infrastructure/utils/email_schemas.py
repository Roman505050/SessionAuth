def get_verification_email_html_body(code: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="uk">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verification Email</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #131E34;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: #fff;
                }}
                p {{
                    margin-bottom: 20px;
                    color: #ccc;
                }}
                .code {{
                    background-color: #1E2B48;
                    padding: 20px;
                    border-radius: 5px;
                    font-family: Consolas, monospace;
                    font-size: 20px;
                    text-align: center;
                    color: #fff;
                }}
                .instruction {{
                    font-size: 14px;
                    color: #ccc;
                    text-align: center;
                }}
                .regards {{
                    font-size: 14px;
                    text-align: left;
                    color: #ccc;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Verification Email</h1>
                <p>Dear User,</p>
                <p>Thank you for registering on our website. To complete the registration process, please enter the following code:</p>
                <div class="code">{code}</div>
                <p class="instruction">If you did not register on our website, please ignore this email.</p>
                <p class="regards">With best regards,<br>Team</p>
            </div>
        </body>
        </html>
    """
