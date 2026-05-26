# Singapore Semiconductor Profiler

This repository contains the Codex plugin for turning one Singapore semiconductor or semiconductor-adjacent company URL into one validated row in a project-local workbook:

```text
data/companies.xlsx
```

The plugin is intentionally small. The AI researches the website and returns one
JSON object. The bundled Python script validates the JSON, prevents duplicate
domains, and writes the Excel row.

## Install

1. Open Codex and click the "Plugins" tab. ![plugins](screenshots/plugins.jpg)

2. Click "Add more". ![addmore](screenshots/addmore.jpg)

3. Paste the GitHub URL into the "Source" and click "Add marketplace". ![addmarketplace](screenshots/addmarketplace.jpg)

4. Start using the plugin. For this plugin, GPT-5.5 medium or above is recommended.