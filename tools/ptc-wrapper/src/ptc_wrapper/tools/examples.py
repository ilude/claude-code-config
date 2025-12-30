"""Auto-generate input examples for tools."""

from typing import Any

from ptc_wrapper.mcp.types import MCPTool


def generate_example_value(prop_name: str, prop_schema: dict[str, Any]) -> Any:
    """Generate an example value based on property schema.

    Args:
        prop_name: Property name (used for hints)
        prop_schema: JSON Schema for the property

    Returns:
        Example value appropriate for the schema
    """
    prop_type = prop_schema.get("type", "string")
    enum = prop_schema.get("enum")
    default = prop_schema.get("default")

    # Use default if provided
    if default is not None:
        return default

    # Use first enum value if available
    if enum:
        return enum[0]

    # Generate based on type and name hints
    if prop_type == "string":
        # Common patterns based on property name
        name_lower = prop_name.lower()
        if "url" in name_lower:
            return "https://example.com"
        elif "email" in name_lower:
            return "user@example.com"
        elif "path" in name_lower or "file" in name_lower:
            return "/path/to/file"
        elif "id" in name_lower:
            return "example-id-123"
        elif "query" in name_lower or "search" in name_lower:
            return "search query"
        elif "name" in name_lower:
            return "example-name"
        else:
            return "example"

    elif prop_type == "number" or prop_type == "integer":
        minimum = prop_schema.get("minimum", 1)
        maximum = prop_schema.get("maximum", 100)
        return min(max(minimum, 10), maximum)

    elif prop_type == "boolean":
        return True

    elif prop_type == "array":
        items = prop_schema.get("items", {})
        item_value = generate_example_value("item", items)
        return [item_value]

    elif prop_type == "object":
        return {}

    return "example"


def generate_input_examples(mcp_tool: MCPTool, max_examples: int = 2) -> list[dict[str, Any]]:
    """Auto-generate input examples based on tool schema.

    Args:
        mcp_tool: MCP tool definition
        max_examples: Maximum number of examples to generate

    Returns:
        List of input example dicts
    """
    examples = []
    schema = mcp_tool.inputSchema
    properties = schema.properties
    required = schema.required

    if not properties:
        return examples

    # Generate minimal example with required fields only
    if required:
        minimal = {}
        for prop_name in required:
            if prop_name in properties:
                minimal[prop_name] = generate_example_value(
                    prop_name, properties[prop_name]
                )
        if minimal:
            examples.append(minimal)

    # Generate full example with all fields (if different from minimal)
    if len(properties) > len(required) and len(examples) < max_examples:
        full = {}
        for prop_name, prop_schema in properties.items():
            full[prop_name] = generate_example_value(prop_name, prop_schema)
        if full != examples[0] if examples else True:
            examples.append(full)

    return examples
