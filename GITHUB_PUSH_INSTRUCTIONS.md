# GitHub Setup Instructions

## How to Push This Project to GitHub

Follow these steps to push the Workflow Engine project to your GitHub repository.

### Prerequisites
1. Git installed on your machine (download from https://git-scm.com/)
2. GitHub account (https://github.com)
3. This workflow-engine directory

### Steps

#### 1. Initialize Git Repository
```bash
cd workflow-engine
git init
```

#### 2. Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 3. Add All Files
```bash
git add .
```

#### 4. Create Initial Commit
```bash
git commit -m "Initial commit: Workflow engine implementation

- Core workflow engine with Node, Graph, and WorkflowRunner
- Tool registry system for registering Python functions
- FastAPI endpoints for graph creation and execution
- Code Review mini-agent example workflow
- Comprehensive demo script showing all features
- Full API documentation and README"
```

#### 5. Add Remote Repository
Replace YOUR_USERNAME with your actual GitHub username:
```bash
git remote add origin https://github.com/goeltanay2003/workflow-engine.git
```

#### 6. Create and Switch to Main Branch
```bash
git branch -M main
```

#### 7. Push to GitHub
```bash
git push -u origin main
```

### Alternative: Using SSH (Recommended for Future Pushes)

If you have SSH keys configured:
```bash
git remote set-url origin git@github.com:goeltanay2003/workflow-engine.git
git push -u origin main
```

### Verify Upload
Visit: https://github.com/goeltanay2003/workflow-engine

You should see all your files there!

### Future Updates
After the initial push, for future updates:
```bash
git add .
git commit -m "Your commit message"
git push
```

---

**Note**: If you don't have Git installed, download it from: https://git-scm.com/download/win
