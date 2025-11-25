try:
    import duckduckgo_search
    print(f"duckduckgo_search version: {duckduckgo_search.__version__}")
except ImportError:
    print("duckduckgo_search not installed")

try:
    from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
    print("DuckDuckGoSearchAPIWrapper imported successfully")
    wrapper = DuckDuckGoSearchAPIWrapper()
    print("Wrapper initialized")
except Exception as e:
    print(f"Error importing/initializing wrapper: {e}")
