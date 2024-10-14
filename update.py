from requests import get as rget
import os
import subprocess

# tired of redeploying :(
UPSTREAM_REPO = os.environ.get('UPSTREAM_REPO', 'https://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@github.com/GK-BOTZ/src')
UPSTREAM_BRANCH = os.environ.get('UPSTREAM_BRANCH', 'v4')
try:
    if len(UPSTREAM_REPO) == 0:
       raise TypeError
except:
    UPSTREAM_REPO = None
try:
    if len(UPSTREAM_BRANCH) == 0:
       raise TypeError
except:
    UPSTREAM_BRANCH = 'main'

if UPSTREAM_REPO is not None:
    if os.path.exists('.git'):
        subprocess.run(["rm", "-rf", ".git"])

    update = subprocess.run([f"git init -q \
                     && git config --global user.email yashoswal18@gmail.com \
                     && git config --global user.name mergebot \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

    if update.returncode == 0:
        print('Uᴘᴅᴀᴛᴇ Wᴀs Sᴜᴄᴄᴇsғᴜʟ...✅')
    else:
        print('Oᴘᴇʀᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ...❌')
