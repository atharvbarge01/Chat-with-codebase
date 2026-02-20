from tree_sitter_language_pack import get_parser

def extract_code_summary(code_content: str, language: str) -> str:
    """
    Extracts class/function signatures and docstrings to create a compressed 
    but semantically rich version of the code block.
    """
    try:
        parser = get_parser(language)
        tree = parser.parse(bytes(code_content, "utf8"))
        root_node = tree.root_node

        summaries = []
        
        # Simple extraction logic: find function and class definitions
        # This is a simplified version; in a production system, we'd use 
        # tree-sitter queries for more precision.
        
        def traverse(node):
            if node.type in ["function_definition", "class_definition", "method_definition"]:
                # Get the first few lines (signature) and skip the body
                lines = code_content[node.start_byte:node.end_byte].splitlines()
                signature = lines[0]
                
                # Try to find a docstring (usually the first child after the signature)
                docstring = ""
                for child in node.children:
                    if child.type == "block":
                        for subchild in child.children:
                            if subchild.type == "string" or subchild.type == "expression_statement":
                                content = code_content[subchild.start_byte:subchild.end_byte].strip()
                                if content.startswith('"""') or content.startswith("'''"):
                                    docstring = f"\n    {content.splitlines()[0]} ... \"\"\""
                                    break
                        break
                
                summaries.append(f"{signature}{docstring}\n    # [Implementation Compressed]")
                return # Don't go deeper into compressed blocks
            
            for child in node.children:
                traverse(child)

        traverse(root_node)
        
        if not summaries:
            # Fallback for small snippets: return the first 5 lines
            return "\n".join(code_content.splitlines()[:5]) + "\n... [Rest Compressed]"
            
        return "\n".join(summaries)
        
    except Exception as e:
        # Resilient fallback
        return f"# [Compression Failed: {e}]\n" + "\n".join(code_content.splitlines()[:3]) + "\n..."
