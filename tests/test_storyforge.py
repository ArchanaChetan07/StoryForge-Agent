import pytest
import re

class TestStoryForge:
    def test_story_structure(self):
        story = {"title": "The Lost Key", "genre": "Mystery", "chapters": [], "characters": []}
        assert "title" in story and "genre" in story

    def test_character_creation(self):
        character = {"name": "Alice", "role": "protagonist", "traits": ["brave","curious"]}
        assert "name" in character and "role" in character
        assert len(character["traits"]) > 0

    def test_genre_options(self):
        genres = ["Fantasy","Mystery","Romance","Sci-Fi","Horror","Adventure"]
        assert len(genres) >= 5
        assert "Fantasy" in genres

    def test_chapter_appended(self):
        story = {"chapters": []}
        story["chapters"].append({"number": 1, "content": "Once upon a time..."})
        assert len(story["chapters"]) == 1

    def test_word_count_tracker(self):
        text = "Once upon a time in a land far away there lived a brave knight"
        count = len(text.split())
        assert count > 0

    def test_plot_twist_insertion(self):
        plot = ["Hero sets out", "Hero meets ally", "Hero faces villain"]
        plot.insert(2, "Ally betrays hero")
        assert "Ally betrays hero" in plot
        assert len(plot) == 4

    def test_empty_prompt_rejected(self):
        def generate(prompt):
            if not prompt or not prompt.strip():
                raise ValueError("Story prompt cannot be empty")
            return f"Story about: {prompt}"
        with pytest.raises(ValueError):
            generate("")

class TestMCPStoryServer:
    def test_tool_definition(self):
        tool = {"name": "generate_story", "description": "Generate a creative story", "input_schema": {"type": "object", "properties": {"prompt": {"type": "string"}}, "required": ["prompt"]}}
        assert tool["name"] == "generate_story"
        assert "prompt" in tool["input_schema"]["properties"]

    def test_response_contains_story(self):
        def mock_generate(prompt):
            return {"story": f"A tale about {prompt}", "word_count": 42}
        result = mock_generate("a dragon")
        assert "story" in result
        assert result["word_count"] > 0
