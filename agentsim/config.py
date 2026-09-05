"""Configuration management for AgentSim"""

import os
from pathlib import Path
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Load .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def _env(name: str, default=None):
    """``os.getenv`` where a blank value counts as unset.

    ``.env.example`` ships every key as ``NAME=`` so a user can fill in only what they
    need. ``os.getenv`` returns ``""`` for those, which is truthy enough to defeat the
    ``provider_available`` checks -- an unconfigured provider looks configured, the router
    stops skipping it, and a request goes out with an empty bearer token. It also makes
    ``int(os.getenv("OAI_TIMEOUT", "180"))`` raise at import when the line is left blank.
    Treating blank as absent is what a reader of ``.env.example`` expects.
    """
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value


class Config:
    """Global configuration from environment variables"""
    
    # ============================================
    # LLM Provider API Keys
    # ============================================
    OPENAI_API_KEY: Optional[str] = _env("OPENAI_API_KEY")
    OPENAI_ORG_ID: Optional[str] = _env("OPENAI_ORG_ID")
    
    ANTHROPIC_API_KEY: Optional[str] = _env("ANTHROPIC_API_KEY")
    
    GOOGLE_API_KEY: Optional[str] = _env("GOOGLE_API_KEY")
    GOOGLE_PROJECT_ID: Optional[str] = _env("GOOGLE_PROJECT_ID")
    
    MISTRAL_API_KEY: Optional[str] = _env("MISTRAL_API_KEY")
    COHERE_API_KEY: Optional[str] = _env("COHERE_API_KEY")
    TOGETHER_API_KEY: Optional[str] = _env("TOGETHER_API_KEY")
    
    # Custom endpoints
    CUSTOM_LLM_ENDPOINT: Optional[str] = _env("CUSTOM_LLM_ENDPOINT")
    CUSTOM_LLM_API_KEY: Optional[str] = _env("CUSTOM_LLM_API_KEY")

    # Generic OpenAI-compatible chat-completions endpoints (vLLM, TGI, LiteLLM, llama.cpp,
    # OpenRouter, a university gateway, ...). Address models as ``oai/<model>`` (served by
    # OAI_BASE_URL / OAI_API_KEY) or ``oai-<name>/<model>`` (served by OAI_<NAME>_BASE_URL /
    # OAI_<NAME>_API_KEY), so the teacher and the judge can live on different services.
    # The base URL must end in ``/v1``; the client appends ``/chat/completions``. The key
    # is optional (a local vLLM server needs none). Reasoning models that return their
    # chain-of-thought in ``reasoning_content`` are handled: only ``content`` is used.
    OAI_BASE_URL: Optional[str] = _env("OAI_BASE_URL")
    OAI_API_KEY: Optional[str] = _env("OAI_API_KEY")

    # EdenAI aggregator. NOTE: this is a *Responses*-style API, NOT OpenAI
    # chat-completions -- the request/response shapes are not interchangeable with the
    # OpenAI-compatible providers. The full endpoint URL is configured here (not a base),
    # because the API exposes the single /v3/responses route. Models are
    # addressed as ``edenai/<provider>/<model>`` (e.g. ``edenai/lilac/minimaxai/minimax-m3``,
    # where ``lilac`` is the upstream provider EdenAI routes to); the ``edenai/`` prefix is
    # stripped before the request. Commercial: every call bills real money and returns a
    # ``cost`` field.
    EDENAI_LLM_ENDPOINT: str = _env("EDENAI_LLM_ENDPOINT", "https://api.edenai.run/v3/responses")
    #: EdenAI also exposes an OpenAI-compatible chat-completions endpoint, which serves
    #: models the Responses API does not (and whose adapter is currently broken for some
    #: providers). Models listed here are sent there instead, in OpenAI request shape.
    EDENAI_CHAT_ENDPOINT: str = _env("EDENAI_CHAT_ENDPOINT", "https://api.edenai.run/v3/chat/completions")
    EDENAI_API_KEY: Optional[str] = _env("EDENAI_API_KEY")
    #: NVIDIA NIM ("NVIDIA Build") -- OpenAI-compatible, free development tier.
    NVIDIA_LLM_ENDPOINT: str = _env("NVIDIA_LLM_ENDPOINT", "https://integrate.api.nvidia.com/v1")
    NVIDIA_API_KEY: Optional[str] = _env("NVIDIA_API_KEY")

    # Local vLLM OpenAI-compatible server (student serving). Used instead of Ollama when a
    # small student needs high-throughput continuous batching on a big GPU: one server per
    # GPU serves many concurrent episodes. Address models as ``vllm/<served-model-name>``;
    # serve the model under its real HF id (``vllm/ibm-granite/granite-4.1-3b``) rather
    # than a placeholder, so traces record which student actually ran.
    # The endpoint has no /v1 suffix (the client appends /v1/chat/completions); each worker
    # process points at its own GPU's server via the VLLM_ENDPOINT env var, exactly as the
    # Ollama path uses OLLAMA_ENDPOINT.
    VLLM_ENDPOINT: str = _env("VLLM_ENDPOINT", "http://127.0.0.1:8300")

    # Ollama
    OLLAMA_ENDPOINT: str = _env("OLLAMA_ENDPOINT", "http://localhost:11434")
    OLLAMA_ENABLED: bool = _env("OLLAMA_ENABLED", "false").lower() == "true"
    # Hybrid "thinking" mode for Ollama models (Qwen3, etc.). Off by default because
    # this framework expects JSON-only outputs.
    OLLAMA_THINK: bool = _env("OLLAMA_THINK", "false").lower() == "true"
    
    # ============================================
    # Default Models
    # ============================================
    TEACHER_MODELS: List[str] = [m.strip() for m in _env("TEACHER_MODELS", "gpt-4o").split(",") if m.strip()]
    TEACHER_TEMPERATURE: float = float(_env("TEACHER_TEMPERATURE", "0.7"))
    
    CONSULTANT_MODELS: List[str] = [m.strip() for m in _env("CONSULTANT_MODELS", "").split(",") if m.strip()]
    CONSULTANT_TEMPERATURE: float = float(_env("CONSULTANT_TEMPERATURE", "0.7"))
    
    VERIFIER_MODEL: str = _env("VERIFIER_MODEL", "gpt-4o-mini")
    VERIFIER_TEMPERATURE: float = float(_env("VERIFIER_TEMPERATURE", "0.1"))
    
    # Embeddings
    LOCAL_EMBEDDING_MODEL: str = _env("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # ============================================
    # Retrieval
    # ============================================
    OPENSEARCH_HOST: str = _env("OPENSEARCH_HOST", "localhost")
    OPENSEARCH_PORT: int = int(_env("OPENSEARCH_PORT", "9200"))
    OPENSEARCH_INDEX: str = _env("OPENSEARCH_INDEX", "documents")
    OPENSEARCH_USER: Optional[str] = _env("OPENSEARCH_USER")
    OPENSEARCH_PASSWORD: Optional[str] = _env("OPENSEARCH_PASSWORD")
    OPENSEARCH_USE_SSL: bool = _env("OPENSEARCH_USE_SSL", "false").lower() == "true"
    
    VECTOR_SEARCH_ENABLED: bool = _env("VECTOR_SEARCH_ENABLED", "false").lower() == "true"
    VECTOR_SEARCH_ENDPOINT: Optional[str] = _env("VECTOR_SEARCH_ENDPOINT")
    
    # ChatNoir (primary retrieval)
    CHATNOIR_ENABLED: bool = _env("CHATNOIR_ENABLED", "true").lower() == "true"
    CHATNOIR_API_KEY: Optional[str] = _env("CHATNOIR_API_KEY")
    CHATNOIR_BASE_URL: str = _env("CHATNOIR_BASE_URL", "https://www.chatnoir.eu/api/v1")
    CHATNOIR_DEFAULT_CORPUS: str = _env("CHATNOIR_DEFAULT_CORPUS", "cw12")
    
    # ============================================
    # Simulation
    # ============================================
    MAX_ITERATIONS: int = int(_env("MAX_ITERATIONS", "5"))
    SIMILARITY_THRESHOLD: float = float(_env("SIMILARITY_THRESHOLD", "0.6"))
    SIMILARITY_METRIC: str = _env("SIMILARITY_METRIC", "embedding_cosine")
    
    OUTPUT_DIR: str = _env("OUTPUT_DIR", "./data/simulation_output")
    
    # ============================================
    # Advanced LLM Settings
    # ============================================
    LLM_TIMEOUT: int = int(_env("LLM_TIMEOUT", "60"))
    LLM_MAX_RETRIES: int = int(_env("LLM_MAX_RETRIES", "3"))
    # Hard wall-clock deadline (seconds) for a single OpenAI-compatible (``oai``) request.
    # httpx's timeout is inter-byte only, so a gateway that holds the connection open
    # trickling keepalive bytes never trips it and blocks forever. This asyncio.wait_for
    # cap guarantees a hung call raises so the router falls through to the next model.
    # Generous by default because a reasoning teacher's long generation is legitimate.
    OAI_TIMEOUT: int = int(_env("OAI_TIMEOUT", "180"))
    # Same wall-clock cap for a single custom/OpenRouter request (observed in
    # production: a momentary OpenRouter blip left workers frozen mid-call for 10+
    # minutes with the API healthy again). Generous default because a reasoning
    # teacher's long generation is legitimate.
    CUSTOM_TIMEOUT: int = int(_env("CUSTOM_TIMEOUT", "180"))
    # Same wall-clock cap for a single EdenAI request (a reasoning teacher such as
    # MiniMax-M3 can legitimately generate for a while), matching CUSTOM_TIMEOUT.
    EDENAI_TIMEOUT: int = int(_env("EDENAI_TIMEOUT", "180"))
    NVIDIA_TIMEOUT: int = int(_env("NVIDIA_TIMEOUT", "180"))
    LLM_MAX_TOKENS: int = int(_env("LLM_MAX_TOKENS", "4096"))
    
    @classmethod
    def get_provider_from_model_id(cls, model_id: str) -> str:
        """Detect provider from model ID"""
        model_lower = model_id.lower()
        
        # Explicit provider prefixes first
        if model_id.startswith("custom/"):
            return "custom"
        elif model_id.startswith("ollama/"):
            return "ollama"
        elif model_id.startswith("oai/") or model_id.startswith("oai-"):
            return "oai"
        elif model_id.startswith("mock/"):
            return "mock"
        elif model_id.startswith("edenai/"):
            return "edenai"
        elif model_id.startswith("nvidia/"):
            return "nvidia"
        elif model_id.startswith("edenchat/"):
            # Same provider and credentials, but EdenAI's OpenAI-compatible
            # chat-completions endpoint rather than the Responses API.
            return "edenai"
        elif model_id.startswith("vllm/"):
            return "vllm"
        elif any(x in model_lower for x in ["gpt", "openai", "o1", "davinci", "turbo"]):
            return "openai"
        elif any(x in model_lower for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_lower for x in ["gemini", "palm", "bison"]):
            return "google"
        elif "mistral" in model_lower:
            return "mistral"
        elif "cohere" in model_lower or "command" in model_lower:
            return "cohere"
        elif "together" in model_lower:
            return "together"
        else:
            # Default to openai for unknown models
            return "openai"
    
    @classmethod
    def oai_endpoint(cls, model_id: str):
        """Resolve ``(base_url, api_key, model_name)`` for an ``oai``-family model id.

        ``oai/<model>``        -> OAI_BASE_URL, OAI_API_KEY
        ``oai-<name>/<model>`` -> OAI_<NAME>_BASE_URL, OAI_<NAME>_API_KEY (NAME upper-cased,
                                  dashes turned into underscores)
        Environment variables are read at call time, and only at call time, so a process
        that sets *or clears* them after import gets what it asked for. A blank value
        counts as unset (see ``_env``).
        """
        if model_id.startswith("oai-"):
            name, _, model_name = model_id[len("oai-"):].partition("/")
            key = name.upper().replace("-", "_")
            return (_env(f"OAI_{key}_BASE_URL"), _env(f"OAI_{key}_API_KEY"), model_name)
        model_name = model_id[len("oai/"):] if model_id.startswith("oai/") else model_id
        # Read the environment only -- no fallback to the class attribute. That attribute is
        # a snapshot taken at import (``.env`` is loaded into the environment before it, so
        # it carries no value the environment lacks), and using it as a default means a
        # variable *removed* after import still resolves. The ``oai-<name>`` branch above
        # has always read the environment alone; these two now agree.
        return (_env("OAI_BASE_URL"), _env("OAI_API_KEY"), model_name)

    @classmethod
    def provider_available(cls, model_id: str) -> bool:
        """True if the provider backing this model has the credentials/endpoint it needs
        to be callable right now.

        Used by the router (``LLMClient.get_completion_with_fallback``) to *skip* an
        unconfigured provider instead of attempting a call that can only fail -- e.g. an
        ``oai/`` model when ``OAI_BASE_URL`` is unset. Checking here keeps the failure
        cheap (no wasted HTTP round-trip) and avoids a hard crash on providers that raise
        a non-HTTP ``ValueError`` for a missing key.
        """
        provider = cls.get_provider_from_model_id(model_id)
        if provider == "oai":
            return bool(cls.oai_endpoint(model_id)[0])
        if provider == "mock":
            return True
        if provider == "edenai":
            return bool(cls.EDENAI_LLM_ENDPOINT and cls.EDENAI_API_KEY)
        if provider == "nvidia":
            return bool(cls.NVIDIA_LLM_ENDPOINT and cls.NVIDIA_API_KEY)
        if provider == "custom":
            return bool(cls.CUSTOM_LLM_ENDPOINT and cls.CUSTOM_LLM_API_KEY)
        if provider == "vllm":
            return bool(cls.VLLM_ENDPOINT)
        if provider == "ollama":
            return bool(cls.OLLAMA_ENDPOINT)
        # Hosted providers (openai/anthropic/google/...): callable iff their key is set.
        return bool(cls.get_api_key_for_provider(provider))

    @classmethod
    def get_api_key_for_provider(cls, provider: str) -> Optional[str]:
        """Get API key for a specific provider"""
        provider_keys: Dict[str, Optional[str]] = {
            "openai": cls.OPENAI_API_KEY,
            "anthropic": cls.ANTHROPIC_API_KEY,
            "google": cls.GOOGLE_API_KEY,
            "mistral": cls.MISTRAL_API_KEY,
            "cohere": cls.COHERE_API_KEY,
            "together": cls.TOGETHER_API_KEY,
            "custom": cls.CUSTOM_LLM_API_KEY,
            "oai": cls.OAI_API_KEY,
            "edenai": cls.EDENAI_API_KEY,
            "nvidia": cls.NVIDIA_API_KEY,
            "vllm": None,  # local server, no API key
            "ollama": None,  # Ollama doesn't require API key by default
        }
        return provider_keys.get(provider.lower())
    
    @classmethod
    def get_model_api_key(cls, model_id: str) -> Optional[str]:
        """Get API key for a specific model ID"""
        provider = cls.get_provider_from_model_id(model_id)
        return cls.get_api_key_for_provider(provider)
    
    @classmethod
    def get_provider_config(cls, provider: str) -> Dict[str, any]:
        """Get additional provider-specific configuration"""
        configs = {
            "openai": {
                "api_key": cls.OPENAI_API_KEY,
                "organization": cls.OPENAI_ORG_ID,
            },
            "google": {
                "api_key": cls.GOOGLE_API_KEY,
                "project_id": cls.GOOGLE_PROJECT_ID,
            },
            "custom": {
                "api_key": cls.CUSTOM_LLM_API_KEY,
                "endpoint": cls.CUSTOM_LLM_ENDPOINT,
            },
            "oai": {
                "api_key": cls.OAI_API_KEY,
                "endpoint": cls.OAI_BASE_URL,
            },
            "edenai": {
                "api_key": cls.EDENAI_API_KEY,
                "endpoint": cls.EDENAI_LLM_ENDPOINT,
            },
            "vllm": {
                "endpoint": cls.VLLM_ENDPOINT,
            },
            "ollama": {
                "endpoint": cls.OLLAMA_ENDPOINT,
                "enabled": cls.OLLAMA_ENABLED,
            },
        }
        return configs.get(provider.lower(), {})


config = Config()

