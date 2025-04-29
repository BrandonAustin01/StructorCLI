# 🏗️ StructorCLI

**StructorCLI** is a blazing-fast, professional-grade CLI tool for scaffolding project structures using intelligent, reusable templates.

> "Build the structure. Focus on creation."

---

## 🚀 Features

- 🛠️ Scaffold projects in seconds using interactive or flag-based CLI
- 📦 Supports 30+ templates (Python, Node, Go, Rust, HTML, FastAPI, React, and more)
- 🔍 Intelligent name injection using `{{project_name}}`
- 💡 Dynamic template discovery — just drop in new folders under `templates/`
- 🔄 Retry-friendly loop with error handling and validation
- ✨ Motivational success quotes to keep your build vibe alive
- 🎨 Beautiful `rich` output: tables, trees, panels, progress bars

---

## 📥 Installation

```bash
# Clone the repo
git clone https://github.com/BrandonAustin01/StructorCLI.git
cd StructorCLI

# Install in editable (dev) mode
pip install -e .
```

> Requires Python 3.8+

---

## ⚡ Usage

### 🧭 Interactive Mode

```bash
structor
```

You'll be prompted to enter a project name and select a template visually.

---

### 💻 Flag Mode

```bash
structor --template react --name my-app
```

| Flag         | Description                                 |
|--------------|---------------------------------------------|
| `--template` | Specify template folder name                |
| `--name`     | Set project name without prompt             |
| `--help`     | Show help screen                            |
| `--version`  | Show current StructorCLI version            |
| `--list`, `-l`, `list` | View all available templates    |

---

## 📁 Template Structure

All templates live inside:

```bash
src/structorcli/templates/
```

Each template folder can include any file structure.  
You can use `{{project_name}}` inside any `.md`, `.py`, `.json`, etc.

Example injection:

```json
{
  "name": "{{project_name}}",
  "version": "1.0.0"
}
```

Will become:

```json
{
  "name": "my-app",
  "version": "1.0.0"
}
```

---

## 🛠 Supported Templates (Sample)

- ✅ Python / Flask / FastAPI
- ✅ Node.js / Express
- ✅ Bash
- ✅ Go / Go-WebServer
- ✅ Rust / Rust-CLI
- ✅ HTML / Astro / Vite / Svelte / Vue / React
- ✅ Django / PHP / Java / C++ / C# / Kotlin
- ✅ Discord Bots (Node & Python)
- ✅ GraphQL / Microservice / NestJS

> Add your own by dropping a folder inside `templates/`

---

## 👨‍💻 Author

Created by [**Brandon Austin**](https://github.com/BrandonAustin01)  
Built with 🧠, refined with 💎, powered by [Rich](https://github.com/Textualize/rich)

---

## ⭐ Contribute

If you enjoy StructorCLI:
- Star the repo ⭐
- Add new templates
- Open PRs or issues to help polish the experience

Let’s keep scaffolding smart.

---