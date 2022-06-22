mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"jagdish.damania@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
primaryColor = """#E694FF"""\n\
backgroundColor = """#00172B"""\n\
secondaryBackgroundColor = """#008388"""\n\
textColor = """#FFF"""\n\
font = """sans serif"""\n\
"  >> ~/.streamlit/config.toml
