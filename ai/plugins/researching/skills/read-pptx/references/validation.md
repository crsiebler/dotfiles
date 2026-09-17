# Validation and limitations

Check source hash, selected slide numbers, record locations, unsupported entries,
and truncation before summarizing. Notes extraction reads only the speaker-note
body placeholder, not every shape/header/footer on a notes page. Master/layout
text is not duplicated onto slides. Group locations identify nesting, not a
transformation into visual reading coordinates. Tables retain stored grid positions;
merged continuation positions may have empty text.

Fixtures independently create notes, a table with a literal leading-zero value,
a grouped text shape, a supported category chart, a scatter chart and a picture.
Tests assert exact evidence/locations/caches, selected-slide exclusion, unsupported
notices, limit reporting, invalid selections/packages/paths, missing dependencies,
and byte-preserved source/isolated resources. No creation-skill import is used.

Chart extraction uses stored caches and supports only single-plot flat category
charts. Other chart structures are reported unsupported. No formula engine,
external connection, embedded object execution, notes creation, or save occurs.

No rendering is performed by the reader tests. Visual-only evidence, layout,
clipping, hidden relationships, custom note shapes, comments, animations and
hyperlinks require separate relevant inspection. Empty text and bounded output
are never proof of empty slides or complete content recovery.
