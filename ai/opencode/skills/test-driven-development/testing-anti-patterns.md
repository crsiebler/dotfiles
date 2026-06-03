# Testing Anti-Patterns

**Load this reference when:** writing or changing tests, adding mocks, tempted to monkey patch, or tempted to add test-only methods to production code.

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested. Monkey patching is usually a sign that production code is too coupled to object creation or global imports.

**Core principle:** Test what the code does, not what the mocks do.

**Following strict TDD prevents these anti-patterns.**

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
4. NEVER monkey patch when dependency injection, interfaces, factories, adapters, or fakes can provide a clean seam
5. NEVER test declarative infrastructure by asserting raw source text
```

## Anti-Pattern 1: Testing Mock Behavior

**The violation:**
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**Why this is wrong:**
- You're verifying the mock works, not that the component works
- Test passes when mock is present, fails when it's not
- Tells you nothing about real behavior

**your human partner's correction:** "Are we testing the behavior of a mock?"

**The fix:**
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// OR if sidebar must be mocked for isolation:
// Don't assert on the mock - test Page's behavior with sidebar present
```

### Gate Function

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

## Anti-Pattern 2: Test-Only Methods in Production

**The violation:**
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// In tests
afterEach(() => session.destroy());
```

**Why this is wrong:**
- Production class polluted with test-only code
- Dangerous if accidentally called in production
- Violates YAGNI and separation of concerns
- Confuses object lifecycle with entity lifecycle

**The fix:**
```typescript
// ✅ GOOD: Test utilities handle test cleanup
// Session has no destroy() - it's stateless in production

// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

### Gate Function

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
```

## Anti-Pattern 3: Mocking Without Understanding

**The violation:**
```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate server', () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**Why this is wrong:**
- Mocked method had side effect test depended on (writing config)
- Over-mocking to "be safe" breaks actual behavior
- Test passes for wrong reason or fails mysteriously

**The fix:**
```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate server', () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### Gate Function

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## Anti-Pattern 4: Monkey Patching Instead of Testable Design

**The violation:**
```python
# BAD: Production code hardcodes the imported client.
import api_client

def get_user_profile(user_id):
    return api_client.fetch_user(user_id)

# BAD: Test must patch the import path to replace behavior.
@patch("app.user_service.api_client.fetch_user")
def test_get_user_profile(mock_fetch_user):
    mock_fetch_user.return_value = {"id": 42, "name": "Ada"}

    result = get_user_profile(42)

    assert result["name"] == "Ada"
```

```typescript
// BAD: Module mock replaces implementation globally.
vi.mock('../apiClient', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 42, name: 'Ada' })
}));
```

**Why this is wrong:**
- Global patching hides real dependencies instead of making them explicit
- Tests become coupled to import paths and module loading behavior
- Patch cleanup failures can leak state into later tests
- Refactors break tests even when behavior is unchanged
- Hardcoded object creation remains hard to test and hard to change

**The fix: dependency injection or an interface:**
```python
class UserClient:
    def fetch_user(self, user_id: int) -> dict: ...

def get_user_profile(user_id: int, client: UserClient) -> dict:
    return client.fetch_user(user_id)

class FakeUserClient:
    def fetch_user(self, user_id: int) -> dict:
        return {"id": user_id, "name": "Ada"}

def test_get_user_profile():
    result = get_user_profile(42, FakeUserClient())

    assert result["name"] == "Ada"
```

```typescript
type UserClient = {
  fetchUser(userId: number): Promise<{ id: number; name: string }>;
};

async function getUserProfile(userId: number, client: UserClient) {
  return client.fetchUser(userId);
}

test('returns the user profile', async () => {
  const fakeClient: UserClient = {
    async fetchUser(userId) {
      return { id: userId, name: 'Ada' };
    }
  };

  await expect(getUserProfile(42, fakeClient)).resolves.toEqual({
    id: 42,
    name: 'Ada'
  });
});
```

### Gate Function

```
BEFORE using patch(), monkeypatch, jest.mock(), vi.mock(), or module mocks:
  STOP - Do not patch yet

  Ask:
    1. Can this dependency be passed as an argument or constructor parameter?
    2. Can this third-party SDK be wrapped in an adapter?
    3. Can production code use an interface/protocol and tests use a fake?
    4. Can object creation move to a factory selected by environment/config?

  IF yes to any:
    Redesign the code and test through the seam

  IF no:
    Explain why patching is unavoidable and keep the patch at the lowest level
```

## Anti-Pattern 5: Testing Declarative Infrastructure as Text

**The violation:**
```typescript
// BAD: This only proves text exists in a file.
test('defines orders queue', () => {
  const terraform = readFileSync('infra/queue.tf', 'utf8');

  expect(terraform).toContain('aws_sqs_queue');
  expect(terraform).toContain('orders_queue');
});
```

**Why this is wrong:**
- It tests spelling, not infrastructure behavior
- It duplicates Terraform, CloudFormation, Kubernetes, or framework validation poorly
- It passes even when the declaration is invalid, unsafe, or unusable
- It creates false confidence and noisy maintenance burden

**The fix:**
```bash
terraform fmt -check
terraform validate
```

Use a safe `terraform plan`, schema validation, policy check, linter, or framework-native validator when credentials and CI environment allow it.

**When tests are valid:**
- Code renders Terraform, CloudFormation, Helm, Kubernetes, or config files from inputs
- Code chooses resources or settings based on runtime conditions
- Code maps environment variables into behavior
- Code wraps a cloud API, datastore, queue, or SDK client

For those cases, test the generator or runtime behavior, not static file text.

### Gate Function

```
BEFORE testing infrastructure/configuration:
  Ask: "Is this test asserting behavior or only source text?"

  IF only source text:
    STOP - Delete the test
    Run tool validation instead

  IF testing code that generates or selects config:
    Use TDD and assert parsed output or behavior

  IF testing external infrastructure behavior:
    Prefer integration tests only when CI has safe access
```

## Anti-Pattern 6: Incomplete Mocks

**The violation:**
```typescript
// ❌ BAD: Partial mock - only fields you think you need
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};

// Later: breaks when code accesses response.metadata.requestId
```

**Why this is wrong:**
- **Partial mocks hide structural assumptions** - You only mocked fields you know about
- **Downstream code may depend on fields you didn't include** - Silent failures
- **Tests pass but integration fails** - Mock incomplete, real API complete
- **False confidence** - Test proves nothing about real behavior

**The Iron Rule:** Mock the COMPLETE data structure as it exists in reality, not just fields your immediate test uses.

**The fix:**
```typescript
// ✅ GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields real API returns
};
```

### Gate Function

```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"

  Actions:
    1. Examine actual API response from docs/examples
    2. Include ALL fields system might consume downstream
    3. Verify mock matches real response schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: Include all documented fields
```

## Anti-Pattern 7: Integration Tests as Afterthought

**The violation:**
```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```

**Why this is wrong:**
- Testing is part of implementation, not optional follow-up
- TDD would have caught this
- Can't claim complete without tests

**The fix:**
```
TDD cycle:
1. Write failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

## When Mocks Become Too Complex

**Warning signs:**
- Mock setup longer than test logic
- Mocking everything to make test pass
- Mocks missing methods real components have
- Test breaks when mock changes

**your human partner's question:** "Do we need to be using a mock here?"

**Consider:** Integration tests with real components often simpler than complex mocks

## TDD Prevents These Anti-Patterns

**Why TDD helps:**
1. **Write test first** → Forces you to think about what you're actually testing
2. **Watch it fail** → Confirms test tests real behavior, not mocks
3. **Minimal implementation** → No test-only methods creep in
4. **Real dependencies** → You see what the test actually needs before mocking

**If you're testing mock behavior, you violated TDD** - you added mocks without watching test fail against real code first.

## Quick Reference

| Anti-Pattern                    | Fix                                                   |
| ------------------------------- | ----------------------------------------------------- |
| Assert on mock elements         | Test real component or unmock it                      |
| Test-only methods in production | Move to test utilities                                |
| Mock without understanding      | Understand dependencies first, mock minimally         |
| Monkey patching dependencies    | Use dependency injection, interfaces, factories, fakes |
| Infrastructure text assertions  | Run tool validation or test the generator             |
| Incomplete mocks                | Mirror real API completely                            |
| Tests as afterthought           | TDD - tests first                                     |
| Over-complex mocks              | Consider integration tests                            |

## Red Flags

- Assertion checks for `*-mock` test IDs
- Methods only called in test files
- Mock setup is >50% of test
- Test fails when you remove mock
- Can't explain why mock is needed
- Mocking "just to be safe"
- Using `patch`, `monkeypatch`, `jest.mock`, `vi.mock`, or module mocks because dependencies are hardcoded
- Asserting that Terraform, Kubernetes, CloudFormation, YAML, or config files contain specific text
- Tests break when an import path changes but behavior does not

## The Bottom Line

**Mocks are tools to isolate, not things to test.**

If TDD reveals you're testing mock behavior, you've gone wrong.

Fix: Test real behavior or question why you're mocking at all.
