import logging
import typing
import xml.sax


def annotate(filename_or_stream):
    annotation_handler = _AnnotationHandler()
    xml.sax.parse(filename_or_stream, annotation_handler)
    return {"annotation": annotation_handler.annotation}


class PathElement(typing.NamedTuple):
    name: str
    attrs: dict


class _AnnotationHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.text_selector = AdocHtml5TextSelector()
        self.path = []
        self.annotation = []

    
    def startPrefixMapping(self, prefix, uri):
        assert False
        
    def endPrefixMapping(self, prefix):
        assert False

    def startElement(self, name, attrs):
        element = PathElement(name, dict(attrs))
        logging.debug("%s%s", len(self.path) * " ", element)
        self.path.append(element)

    def endElement(self, name):
        self.path = self.path[:-1]

    def startElementNS(self, name, qname, attrs):
        assert False

    def endElementNS(self, name, qname):
        assert False

    def characters(self, content):
        if content.strip():
            logging.debug("%s%s", len(self.path) * " ", content.strip())
        select = self.text_selector.is_selection(self.path)
        if select:
            self.annotation.append({"text": content})
            return
        self.annotation.append({"markup": content, "interpretAs": " "})

    def ignorableWhitespace(self, whitespace):
        assert False

    def processingInstruction(self, target, data):
        assert False

    def skippedEntity(self, name):
        assert False


class AdocHtml5TextSelector:
    def is_selection(self, path):
        if path[-1].name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return True
        if path[-1].name == "p":
            return True
        if path[-1].name == "a":
            return True
        if path[-1].name == "div" and path[-1].attrs.get("class") == "title":
            return True
        if path[-1].name == "em" and not has_pre_ancestor(path):
            return True
        return False


def has_pre_ancestor(path):
    for element in path:
        if element.name == "pre":
            return True
    return False
