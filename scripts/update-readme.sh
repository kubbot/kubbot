#!/bin/bash
# update-readme.sh - Auto-update README with latest GitHub activity

set -e

USERNAME="kubbot"
README="README.md"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "🔄 Updating README for @$USERNAME..."

# Generate README with timestamp
cat > "$README" <<EOF
<p align="center">
  <img src="./assets/icon/blue 透明.png" alt="kubbot" width="180" />
</p>

<h1 align="center">kubbot</h1>

<p align="center">
  <em>🤖 Automated Builder · Cloud Native Guardian · AI Enabler</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/followers/kubbot?style=flat&logo=github&label=Followers&color=24292f" />
  <img src="https://img.shields.io/github/stars/kubbot?style=flat&logo=github&color=24292f" />
  <img src="https://img.shields.io/github/repo-size/kubbot/kubbot?style=flat&color=24292f" />
</p>

---

## ▍Identity

\`\`\`yaml
name: kubbot
role: Automation & CI/CD Agent
focus: CloudNative · AI · Developer Tools
mission: Win or Learn
\`\`\`

---

## ▍Active Projects

<!-- recent contributions auto-injected -->

## ▍Repositories

<!-- recent repos auto-injected -->

## ▍Contributions

<!-- recent PRs auto-injected -->

---

<p align="center">
  <em>🌟 You never lose — you win or you learn.</em>
</p>

<p align="center">
  <sub>Last updated: <code>$TIMESTAMP</code></sub>
</p>
EOF

echo "✅ README updated at $TIMESTAMP"
