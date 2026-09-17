# Validation

Validate names, rectangular rows, cell types, finite numbers, string limits,
formats and chart references before writing. Use explicit typed writers with all
implicit string conversions disabled. Writer return errors/warnings and close
failures stop publication. Build ZIP in memory and validate package limits/integrity;
independently reopen formula and cached-value views with openpyxl. Compare sheet
names, requested cell values/types/formulas/caches and named number formats before
exclusive publication. Inputs and existing outputs are preserved.

Tests independently inspect shared strings, cell types, formulas/caches, absence
of inferred hyperlinks, table/chart presence, freeze panes, filters and calculation
settings. They exercise leading zeros, formula-like strings, literal URLs, dates,
booleans, malformed rows, duplicate/invalid names, oversized strings, collisions,
missing packages, path/symlink boundaries, exact documentation recipe, isolated
resources and injected writer truncation/close failures.

Inspection is bounded and does not establish formula correctness or completeness
when truncated. It cannot infer whether an arbitrary cache was supplied, stale,
a writer placeholder, or calculated. Creation's cache provenance comes from its
request, not a calculation engine. Formulas must use Excel-supported English syntax;
unsupported syntax or library normalization may fail exact reopened verification.

No application rendering or formula recalculation is claimed. When required for
an artifact, use an available authorized application on a project-local copy,
inspect formatting/chart labels/column widths, and separately verify actual computed
results. Never use cache presence or fullCalcOnLoad as proof of recalculation.
No external data connection is refreshed. Chart caches can include formula placeholders;
review cache provenance before treating displayed bars as computed results.
