"""Tests for pydantic model lazy imports.

Ensures that the pydantic module uses lazy imports for provider dependencies,
allowing users to import the module without installing all optional provider packages.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest


class TestPydanticLazyImports:
    """Test lazy imports for pydantic models to prevent unnecessary dependencies."""

    def test_import_with_missing_dependencies(self):
        """Test that pydantic module imports successfully without optional provider packages."""
        mock_modules = {
            'cohere': None,
            'mistralai': None,
            'mistralai.sdk': None,
            'anthropic': None,
            'pydantic_ai.models.cohere': None,
            'pydantic_ai.models.mistral': None,
            'pydantic_ai.models.anthropic': None,
            'pydantic_ai.models.gemini': None,
            'pydantic_ai.models.openai': None,
            'pydantic_ai.providers.cohere': None,
            'pydantic_ai.providers.mistral': None,
            'pydantic_ai.providers.anthropic': None,
            'pydantic_ai.providers.openai': None,
        }
        
        with patch.dict('sys.modules', mock_modules, clear=False):
            try:
                for mod in ['blaxel.pydantic.model', 'blaxel.pydantic']:
                    sys.modules.pop(mod, None)
                
                import blaxel.pydantic.model
                
                assert blaxel.pydantic.model is not None
                assert hasattr(blaxel.pydantic.model, 'TokenRefreshingModel')
                assert hasattr(blaxel.pydantic.model, 'bl_model')
                
            except ImportError as e:
                pytest.fail(f"Module import failed without optional dependencies: {e}")
            finally:
                for mod in ['blaxel.pydantic.model', 'blaxel.pydantic']:
                    sys.modules.pop(mod, None)

    def test_bl_tools_import_without_provider_dependencies(self):
        """Test that bl_tools can be imported without provider-specific packages."""
        mock_modules = {
            'cohere': None,
            'mistralai': None,
            'mistralai.sdk': None,
            'anthropic': None,
        }
        
        with patch.dict('sys.modules', mock_modules, clear=False):
            try:
                for mod in ['blaxel.pydantic.model', 'blaxel.pydantic.tools', 'blaxel.pydantic']:
                    sys.modules.pop(mod, None)
                
                from blaxel.pydantic import bl_tools
                
                assert bl_tools is not None
                
            except ImportError as e:
                pytest.fail(f"Failed to import bl_tools without optional dependencies: {e}")
            finally:
                for mod in ['blaxel.pydantic.model', 'blaxel.pydantic.tools', 'blaxel.pydantic']:
                    sys.modules.pop(mod, None)

    def test_bl_model_import_without_all_providers(self):
        """Test that bl_model can be imported with only a subset of provider packages."""
        mock_modules = {
            'cohere': None,
            'mistralai': None,
            'mistralai.sdk': None,
        }
        
        with patch.dict('sys.modules', mock_modules, clear=False):
            try:
                for mod in ['blaxel.pydantic.model', 'blaxel.pydantic']:
                    sys.modules.pop(mod, None)
                
                from blaxel.pydantic import bl_model
                
                assert bl_model is not None
                assert callable(bl_model)
                
            except ImportError as e:
                pytest.fail(f"Failed to import bl_model without all providers: {e}")
            finally:
                for mod in ['blaxel.pydantic.model', 'blaxel.pydantic']:
                    sys.modules.pop(mod, None)

    def test_wrapper_creation_does_not_trigger_imports(self):
        """Test that creating TokenRefreshingModel wrapper doesn't import provider dependencies."""
        from blaxel.pydantic.model import TokenRefreshingModel
        
        provider_types = ["openai", "xai", "deepseek", "cerebras", "cohere", "mistral", "anthropic", "gemini"]
        
        for provider_type in provider_types:
            model_config = {
                "type": provider_type,
                "model": f"{provider_type}-test-model",
                "url": f"https://api.{provider_type}.com",
                "kwargs": {}
            }
            
            wrapper = TokenRefreshingModel(model_config)
            
            assert wrapper.model_config == model_config
            assert wrapper._cached_model is None

    def test_no_provider_imports_at_module_level(self):
        """Test that provider-specific imports are not at module level."""
        import inspect
        import re
        from blaxel.pydantic import model
        
        source = inspect.getsource(model)
        lines = source.split('\n')
        
        class_start = next((i for i, line in enumerate(lines) if 'class TokenRefreshingModel' in line), None)
        assert class_start is not None, "TokenRefreshingModel class not found"
        
        top_level_code = '\n'.join(lines[:class_start])
        
        # Check for provider model imports (e.g., from pydantic_ai.models.openai import ...)
        # Allow only the base Model class, not specific provider models
        provider_model_pattern = r'from pydantic_ai\.models\.(?!__)\w+'
        provider_model_matches = re.findall(provider_model_pattern, top_level_code)
        assert not provider_model_matches, \
            f"Found provider model imports at module level: {provider_model_matches}"
        
        # Check for provider imports (e.g., from pydantic_ai.providers.openai import ...)
        provider_pattern = r'from pydantic_ai\.providers\.\w+'
        provider_matches = re.findall(provider_pattern, top_level_code)
        assert not provider_matches, \
            f"Found provider imports at module level: {provider_matches}"
        
        # Check for specific provider client imports
        client_patterns = [
            (r'from cohere import', 'cohere'),
            (r'from mistralai', 'mistralai'),
            (r'from anthropic import', 'anthropic'),
        ]
        
        for pattern, provider_name in client_patterns:
            if re.search(pattern, top_level_code):
                pytest.fail(f"Found {provider_name} client import at module level")

    def test_basic_import_succeeds(self):
        """Test that basic pydantic imports work without errors."""
        from blaxel.pydantic import bl_model, bl_tools
        
        assert bl_model is not None
        assert bl_tools is not None
        assert callable(bl_model)

