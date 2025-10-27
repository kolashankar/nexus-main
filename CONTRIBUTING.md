# Contributing to Karma Nexus 2.0

Thank you for your interest in contributing to Karma Nexus! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Our Standards

**Examples of behavior that contributes to a positive environment:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 5.0+
- Redis 5.0+
- Yarn package manager
- Git

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/karma-nexus.git
   cd karma-nexus
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/karma-nexus.git
   ```

3. **Install dependencies**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   yarn install
   ```

4. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   # Edit the .env files with your configuration
   ```

## Development Workflow

### Branch Naming Convention

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes for production
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Adding or updating tests

**Examples:**
- `feature/add-guild-wars`
- `bugfix/fix-karma-calculation`
- `docs/update-api-documentation`

### Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(combat): add turn-based combat system

fix(karma): correct karma calculation for edge cases

docs(readme): update installation instructions
```

### Development Process

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow coding standards (see below)
   - Add tests for new features
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   yarn test
   yarn test:e2e
   ```

4. **Lint your code**
   ```bash
   # Backend
   cd backend
   ruff check .
   
   # Frontend
   cd frontend
   yarn lint
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): your commit message"
   ```

6. **Keep your fork up to date**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for function arguments and return values
- Maximum line length: 100 characters
- Use docstrings for classes and functions
- Use `ruff` for linting

**Example:**
```python
def calculate_karma(action: str, target: Player) -> int:
    """Calculate karma change based on action and target.
    
    Args:
        action: Type of action performed
        target: Target player object
        
    Returns:
        Karma change amount
    """
    # Implementation
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components and React Hooks
- Maximum line length: 100 characters
- Use ESLint for linting

**Example:**
```typescript
interface PlayerProps {
  username: string;
  karma: number;
}

export const PlayerCard: React.FC<PlayerProps> = ({ username, karma }) => {
  // Implementation
  return (
    <div className="player-card">
      <h3>{username}</h3>
      <p>Karma: {karma}</p>
    </div>
  );
};
```

### General Guidelines

- **DRY (Don't Repeat Yourself)**: Avoid code duplication
- **KISS (Keep It Simple, Stupid)**: Write simple, understandable code
- **YAGNI (You Aren't Gonna Need It)**: Don't add functionality until needed
- **Comments**: Write self-documenting code; use comments to explain "why", not "what"
- **Error Handling**: Always handle errors gracefully
- **Performance**: Consider performance implications, especially for frequently called code

## Testing

### Testing Requirements

- **All new features** must include tests
- **Bug fixes** should include a test that would have caught the bug
- Maintain **minimum 60% code coverage**
- Tests should be **fast** and **isolated**

### Backend Testing

**Unit Tests:**
```python
import pytest
from services.karma import calculate_karma

def test_karma_calculation():
    result = calculate_karma("help", mock_player)
    assert result > 0
```

**Integration Tests:**
```python
@pytest.mark.asyncio
async def test_player_action_flow(client, auth_headers):
    response = await client.post(
        "/api/actions/help",
        json={"target_id": "player_123"},
        headers=auth_headers
    )
    assert response.status_code == 200
```

### Frontend Testing

**Component Tests:**
```typescript
import { render, screen } from '@testing-library/react';
import { PlayerCard } from './PlayerCard';

test('renders player card', () => {
  render(<PlayerCard username="Test" karma={100} />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

**E2E Tests:**
```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Pull Request Process

### Before Submitting

1. ✅ All tests pass
2. ✅ Code is linted with no errors
3. ✅ Documentation is updated
4. ✅ Commit messages follow convention
5. ✅ Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] All tests pass locally
```

### Review Process

1. **Submit PR** with clear title and description
2. **Automated checks** run (CI/CD)
3. **Code review** by maintainers
4. **Address feedback** if any
5. **Approval** and merge

### After Merge

- Delete your feature branch
- Update your local main branch
- Close related issues

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Browser: [e.g. Chrome 120]
- Version: [e.g. 2.0.0]

**Additional context**
Any other information about the problem
```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
A clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Any alternative solutions

**Additional context**
Any other context or screenshots
```

## Questions?

If you have questions:

1. Check the [documentation](./docs/)
2. Search [existing issues](https://github.com/OWNER/karma-nexus/issues)
3. Create a new issue with the `question` label
4. Join our community chat (if available)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Karma Nexus! 🎮✨**
