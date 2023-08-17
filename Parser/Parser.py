import ast
import os, sys

import Parser.Base as Base
from Parser.Contents.ContentC import ContentC
import Parser.ParserClass as ParserClass
import Parser.ParserFunction as ParserFunction
import Parser.ParserBody as ParserBody


Redirection = {
    ast.ClassDef: ParserClass.ParserClass,
    ast.FunctionDef: ParserFunction.ParserFunction,
}

#convert to list
All_Parser =  []
for key in Redirection:
    All_Parser.append(Redirection[key])

Base.BaseParser.Redirection = Redirection

for parser in All_Parser:
    parser.Redirection = Redirection

def Parse(nodeAST):
    if not isinstance(nodeAST, ast.AST):
        Base.RaiseException(nodeAST, "The nodeAST must be an AST")
    if not isinstance(nodeAST, ast.Module):
        Base.RaiseException(nodeAST, "The nodeAST must be a Module")
    Content = ContentC()
    Content.filename = nodeAST.filename
    #parse code
    for parser in All_Parser:
        parser.Register = []
    for node in nodeAST.body:
        CC = Redirection.get(type(node))
        if CC is None:
            Base.RaiseException(node, "This line is not allowed")
        else:
            parser = CC(node)
            parser.Compile()
            if Base.DEBUG:
                parser.PrintVariables()
                print('#'*20)
            Content += parser.GetContent()
    return Content

def ParseFile(path):
    with open(path, "r") as f:
        content = f.read()
    try:
        nodeAST = ast.parse(content)
    except Exception as e:
        raise Exception("Error in the parsing of the file " + path + " |#| " + str(e))
    #add filename with name without extension
    nodeAST.filename = os.path.splitext(os.path.basename(path))[0]
    return nodeAST