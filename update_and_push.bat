
@echo off
cd /d %~dp0
echo [SAMBOT-MIRROR] Updating gmgn live.json from gmgn.ai ...
python update_tokens.py

echo [GIT] Pushing changes to GitHub ...
git add live.json
git commit -m "auto: update gmgn tokens"
git push

echo Done. Press any key to close.
pause
