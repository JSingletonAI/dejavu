from dejavu.configs.base import MemoryConfig, dejavu_dir


def test_default_dir_is_dejavu():
    assert dejavu_dir.endswith('.dejavu')


def test_default_db_is_memories_db():
    assert MemoryConfig().history_db_path.endswith('.dejavu\\memories.db') or MemoryConfig().history_db_path.endswith('.dejavu/memories.db')


def test_default_llm_provider_is_venice():
    assert MemoryConfig().llm.provider == 'venice'
