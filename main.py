name: Auto Post and Index
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with: {python-version: '3.x'}
      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4
      - name: Run Auto Script
        env:
          GCLOUD_KEY: ${{ secrets.GCLOUD_KEY }}
        run: |
          echo "$GCLOUD_KEY" > service-account.json
          python main.py
      - name: Commit and push changes
        run: |
          git config --global user.name 'github-actions'
          git config --global user.email 'github-actions@github.com'
          git add news.json
          git commit -m "Update news content"
          git push
