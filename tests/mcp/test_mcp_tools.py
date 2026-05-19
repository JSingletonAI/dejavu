from dejavu.mcp.server import TOOLS


def test_mcp_tools():
    assert [tool['name'] for tool in TOOLS] == ['memory_search', 'memory_add', 'memory_list']
