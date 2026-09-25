# Testing Anti-Patterns

Use this reference when writing or reviewing tests, choosing test doubles, or
adding test utilities. Examples illustrate design decisions; adapt them to the
project's test framework and contracts rather than copying them mechanically.

Test observable behavior and meaningful contracts. Mocks isolate dependencies;
they are not the behavior being tested. A failing test first helps expose bad
assumptions, but TDD alone does not guarantee useful assertions or realistic
integration coverage.

## Quick reference

| Anti-pattern | Prefer |
| --- | --- |
| Assert that a mock rendered or returned its configured value | Assert the application's observable result |
| Add production methods solely for test cleanup | Fixtures and test utilities, unless production owns the lifecycle |
| Mock away behavior the test depends on | Isolate the actual external or nondeterministic boundary |
| Patch globals because dependencies are hidden | A small explicit seam, or carefully scoped patching when justified |
| Assert spelling in declarative configuration | Native validation, parsed contract checks, or generator tests |
| Use unrealistic or incomplete response fixtures | Contract-valid examples and deliberate optional/error cases |
| Treat unit tests as proof of integration compatibility | Relevant boundary tests in an authorized environment |
| Build elaborate mock systems or indiscriminate snapshots | Real components where practical and focused assertions |

## 1. Testing mock behavior

**Weak test:** the test double renders a marker, and the test only checks that
marker. It can pass even if the surrounding application is broken.

```typescript
test('renders sidebar', () => {
  render(<Page />); // Sidebar is replaced by a stub rendering sidebar-mock.
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**Better test:** keep the relevant component real and check its public behavior.

```typescript
test('provides navigation to settings', () => {
  render(<Page />);
  const navigation = screen.getByRole('navigation');
  expect(within(navigation).getByRole('link', { name: 'Settings' }))
    .toHaveAttribute('href', '/settings');
});
```

If the requirement is successful navigation, also exercise the click and resulting
route. Finding a link alone does not establish that the destination works.

Interaction assertions are legitimate when the interaction is the contract, such
as publishing a correctly addressed message. Assert the meaningful destination
and payload. Use call counts or ordering only when those properties matter, such
as preventing duplicate submissions. Avoid asserting internal helper calls solely
because that is how today's implementation works.

**Review questions:** Would breaking the requirement make this test fail? Does
the assertion check application behavior or merely repeat the mock's setup?

## 2. Test-only methods in production

**Weak design:** adding a destructive method to a production class only so tests
can clean up an external resource.

```typescript
class Session {
  async destroy() { // Introduced only for afterEach in the test suite.
    await this.workspaceManager.destroyWorkspace(this.workspaceId);
  }
}
```

This exposes a new production operation and may put resource ownership in the
wrong class. It can be dangerous if another caller later uses it.

**Better design:** the fixture records and cleans up the resource it creates.

```typescript
let workspaceId: string;

beforeEach(async () => {
  workspaceId = await testWorkspaceManager.createWorkspace();
});

afterEach(async () => {
  await testWorkspaceManager.destroyWorkspace(workspaceId);
});
```

Use an isolated test manager/environment. Ensure cleanup also handles partial
setup failure; do not delete resources that the fixture did not create.

A production `close`, `dispose`, or `destroy` method is appropriate when resource
cleanup is genuinely part of the production lifecycle. Its use in tests is not
itself an anti-pattern. Likewise, a useful injectable dependency is not test-only
pollution merely because tests use it first.

**Review questions:** Who owns the resource? Would this operation belong in the
production API without the test? Can fixture cleanup perform it safely instead?

## 3. Mocking without understanding dependencies

**Weak test:** replacing the method that writes configuration while trying to
test duplicate detection based on that configuration.

```typescript
test('rejects duplicate server registration', async () => {
  catalog.discoverAndCacheTools = async () => undefined; // Also removed persistence.

  await registry.addServer(config);
  await expect(registry.addServer(config)).rejects.toThrow('duplicate');
});
```

The test removed the state change it needs. It may fail misleadingly or, with
additional stubbing, pass without exercising duplicate detection at all.

**Better test:** replace slow server discovery, preserve registration/persistence,
and use a temporary configuration store owned by the test.

```typescript
test('rejects duplicate server registration', async () => {
  const registry = new Registry({
    store: testConfigStore,
    discoverTools: async () => [],
  });

  await registry.addServer(config);
  await expect(registry.addServer(config)).rejects.toThrow('duplicate');
});
```

Before replacing a dependency, identify its reads, writes, callbacks, errors, and
other side effects. Preserve the effects that are part of the behavior under test.
Prefer a real local component when it is cheap and deterministic. Do not launch
a production integration just to discover which effects it has; inspect its
implementation or use an authorized isolated environment.

**Review questions:** Which state makes the second operation different? Is that
state real in this test? Am I mocking an external boundary or the feature itself?

## 4. Monkey patching instead of a clear seam

**Brittle design:** production code hides a client dependency in a global import,
and every test has to know the exact import location.

```python
import api_client

def get_user_name(user_id):
    return api_client.fetch_user(user_id)["name"]

# Tests must patch app.user_service.api_client.fetch_user.
```

Patching can couple tests to module layout, leak state if not restored, and break
when a refactor moves imports without changing behavior.

**Alternative:** pass the small dependency the operation actually needs.

```python
def get_user_name(user_id, client):
    return client.fetch_user(user_id)["name"]

class FakeUserClient:
    def fetch_user(self, user_id):
        return {"id": user_id, "name": "Ada"}

def test_returns_user_name():
    assert get_user_name(42, FakeUserClient()) == "Ada"
```

Constructor parameters, functions, adapters, or interfaces can all provide useful
seams. Choose the smallest one consistent with the project. A container or new
architecture is unnecessary for a single dependency.

Scoped patching is reasonable for some legacy code and unavoidable global APIs.
Patch where the dependency is actually looked up, restore it through the test
framework's fixture/context lifecycle, and avoid affecting concurrent tests.
Do not expand a narrow fix into an unrelated architecture rewrite just to avoid
patching. Conversely, do not repeatedly patch private internals when a small
explicit boundary would simplify both code and tests.

**Review questions:** Is there an existing seam? Can one argument make the
dependency explicit? Will this patch survive a behavior-preserving refactor?

## 5. Testing declarative infrastructure as raw text

**Weak test:** checking that a static configuration contains a resource type and
name, without determining whether it is valid or has the intended settings.

```typescript
test('defines orders queue', () => {
  const source = readFileSync('infra/queue.tf', 'utf8');
  expect(source).toContain('aws_sqs_queue');
  expect(source).toContain('orders_queue');
});
```

Comments or invalid declarations can satisfy this test. It duplicates part of the
configuration while giving little confidence in its meaning.

**Better validation:** use the tool's native checks and relevant policy checks.

```bash
terraform fmt -check
terraform validate
```

Run plans, builds, or integration checks only with the required environment and
authorization. Never imply syntax validation proves a deployment will work.

Tests are appropriate for code that generates configuration, selects settings at
runtime, maps environment variables, or wraps an infrastructure API. Assert parsed
results and meaningful defaults, overrides, invalid-input handling, and behavior.
For example, a generator test can verify that private mode disables public access.

Static configuration can also merit parsed regression checks for a security
contract, such as a required approval setting. Exact text assertions are valid
when text itself is the public output contract. Avoid redundant spelling checks,
not every test that reads a configuration file.

**Review questions:** What failure can this test detect that native validation
cannot? Is it testing a contract, generated behavior, or incidental spelling?

## 6. Unrealistic or incomplete mocks

**Weak fixture:** a hand-written response omits a required field that downstream
code consumes, or uses a shape the real API never returns.

```typescript
const response = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  // Required metadata.requestId is missing.
};
```

**Better fixture:** model the response contract used at this boundary.

```typescript
const response = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-test-123' },
} satisfies UserResponse;
```

Use the actual client type or schema where available. Types alone do not validate
runtime data, so add contract or integration checks where boundary compatibility
matters. Build representative fixtures from documentation or sanitized examples,
never from unredacted customer data or credentials.

Include required fields and relevant fields consumed downstream. There is no need
to reproduce every unrelated field in a large API response. An adapter returning
a deliberately smaller type should be tested against that adapter contract.
Exercise absent optional fields, empty collections, error responses, and malformed
input deliberately when the application must handle them; do not accidentally
omit required fields in a fixture intended to represent success.

**Review questions:** Is this a valid success response? Which boundary defines its
shape? Do the tests cover the variations the application actually handles?

## 7. Integration tests as an afterthought

Unit tests passing with fakes do not establish compatibility with a database,
filesystem, process, browser, or remote API. Add focused boundary tests when those
components interact in ways the unit tests cannot establish.

For example, a CLI argument test can confirm that a wrapper requests a read-only
mode. It cannot establish that the real tool enforces that mode. Distinguish
wrapper tests, native configuration parsing, and actual enforcement tests.

Use real local components and disposable fixtures where practical. External tests
require authorized non-production access. Do not send notifications, spend money,
or mutate shared data incidentally. If a required integration test cannot run,
state the limitation and remaining risk rather than claiming full verification.

Test-first development can guide interface design and catch regressions, but it
does not eliminate the need for realistic boundary tests. Verification belongs in
the definition of done, not an unspecified later phase.

**Review questions:** What remains untested when the fake passes? Is the required
integration actually exercised, or merely represented by a compatible method name?

## 8. Over-complex mocks and blind snapshots

Warning signs include mocking every collaborator, rebuilding an application in
test setup, and asserting long sequences of private calls. A setup longer than
the assertion is a reason to inspect the design, not an automatic reason to reject
the test; some realistic fixtures are necessarily substantial.

Prefer exercising real collaborators with a small number of boundary doubles.
Extract repeated fixture construction when it clarifies intent, but avoid shared
mutable fixtures that couple tests or make execution order significant.

Snapshots are useful for stable, reviewable output contracts. Large snapshots of
incidental output are easy to approve without understanding changes. Inspect every
snapshot update and add focused assertions for important behavior. Do not weaken
assertions, blindly regenerate expectations, hide failures, or add retries solely
to make the suite green. Control clocks, randomness, and async completion instead
of relying on arbitrary sleeps.

## Review checklist

- Name the behavior or contract each test protects.
- Confirm the test would fail for a plausible defect in that behavior.
- Keep real logic under test; isolate only the relevant boundaries.
- Use realistic fixtures and deliberate error/optional-field cases.
- Keep test cleanup in its proper owner and restore patched state.
- Prefer existing conventions and small seams over unrelated design changes.
- Use appropriate configuration validation and meaningful security checks.
- Run the relevant checks; broaden or repeat only when evidence warrants it.
- Report what ran, what passed, and what remains unverified.
