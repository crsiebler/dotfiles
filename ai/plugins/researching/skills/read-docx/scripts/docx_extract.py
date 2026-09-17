"""Original ordered DOCX extraction with explicit unsupported-content reporting."""
import io
from collections import Counter
import re
from docx import Document
from docx.table import Table

WORD='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
UNSUPPORTED={'ins':'tracked_insertions','del':'tracked_deletions','txbxContent':'text_boxes',
             'footnoteReference':'footnote_references','endnoteReference':'endnote_references',
             'commentReference':'comment_references','comment':'stored_comments',
             'sdt':'content_controls','drawing':'drawings','pict':'legacy_pictures',
             'object':'embedded_objects','altChunk':'external_content',
             'fldChar':'field_markers','instrText':'field_instructions','hyperlink':'hyperlink_targets'}


def unsupported_content(document):
    counts=Counter()
    for part in document.part.package.parts:
        element=getattr(part,'element',None)
        if element is None:
            continue
        for node in element.iter():
            if not isinstance(node.tag,str) or not node.tag.startswith('{'+WORD+'}'):
                continue
            tag=node.tag.split('}',1)[1]
            if tag in UNSUPPORTED:
                counts[UNSUPPORTED[tag]]+=1
            if tag=='tbl' and node.getparent().tag=='{'+WORD+'}tc':
                counts['nested_tables']+=1
    counts['unsupported_body_blocks']=sum(
        node.tag not in {'{'+WORD+'}'+name for name in ('p','tbl','sectPr')}
        for node in document.element.body)
    return {key:value for key,value in counts.items() if value}


def heading_level(paragraph):
    style=paragraph.style
    seen=set()
    while style is not None and style.style_id not in seen:
        seen.add(style.style_id)
        match=re.fullmatch(r'Heading ([1-9])',style.name)
        if match:
            return int(match[1])
        if style.name=='Title':
            return 0
        style=style.base_style
    return None


class Extractor:
    def __init__(self,max_records,max_chars,max_cells):
        self.max_records=max_records
        self.remaining=max_chars
        self.cells_remaining=max_cells
        self.records=[]
        self.truncated=False

    def excerpt(self,value):
        result=value[:self.remaining]
        self.remaining-=len(result)
        self.truncated |= len(result)<len(value)
        return result

    def blocks(self,container,location):
        for index,block in enumerate(container.iter_inner_content(),1):
            if len(self.records)>=self.max_records:
                self.truncated=True
                break
            where=f'{location}/block-{index}'
            if isinstance(block,Table):
                cells=[]
                for row_index,row in enumerate(block.rows,1):
                    for column_index,cell in enumerate(row.cells,1+row.grid_cols_before):
                        if not self.cells_remaining:
                            self.truncated=True
                            break
                        self.cells_remaining-=1
                        cells.append(dict(row=row_index,column=column_index,
                                          location=f'{where}/row-{row_index}/cell-{column_index}',
                                          text=self.excerpt(cell.text)))
                    if not self.cells_remaining:
                        if row_index<len(block.rows):
                            self.truncated=True
                        break
                self.records.append(dict(kind='table',location=where,cells=cells,
                                         rows=len(block.rows),columns=len(block.columns)))
            else:
                self.records.append(dict(kind='paragraph',location=where,
                                         text=self.excerpt(block.text),
                                         style=self.excerpt(block.style.name),
                                         heading_level=heading_level(block)))


def extract(content,max_records,max_chars,max_cells):
    document=Document(io.BytesIO(content))
    extractor=Extractor(max_records,max_chars,max_cells)
    unsupported=unsupported_content(document)
    extractor.blocks(document,'body')
    contexts=[]
    previous={}
    variants=('header','footer','first_page_header','first_page_footer','even_page_header','even_page_footer')
    for section_index,section in enumerate(document.sections[:100],1):
        for variant in variants:
            current=getattr(section,variant)
            linked=current.is_linked_to_previous
            if not linked:
                previous[variant]=(current,section_index)
            definition=previous.get(variant)
            enabled=(section.different_first_page_header_footer if variant.startswith('first_')
                     else document.settings.odd_and_even_pages_header_footer if variant.startswith('even_')
                     else True)
            location=f'section-{section_index}/{variant}'
            contexts.append(dict(location=location,section=section_index,variant=variant,
                                 enabled=enabled,linked_to_previous=linked,
                                 definition_section=definition[1] if definition else None))
            if definition:
                extractor.blocks(definition[0],location)
    extractor.truncated |= len(document.sections)>100
    return dict(records=extractor.records,contexts=contexts,unsupported=unsupported,
                truncated=extractor.truncated,limitations=[
                    'Locations are supported-block ordinals, not rendered pages.',
                    'Unsupported structures are reported, not rendered or reconstructed.',
                    'Tracked changes are not accepted; source is never saved.',
                    'Empty or truncated extraction does not establish empty source content.'])
