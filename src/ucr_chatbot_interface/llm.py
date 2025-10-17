from dataclasses import dataclass


@dataclass
class ContentDict:
    """The input"""

    ...  # Define this as needed


@dataclass
class ModelResponse:
    """A language model's response"""

    content: ContentDict
    ...  # Define this as needed


class LanguageModelClient:
    """An abstract base class for language model clients."""

    def get_response(
        self, contents: list[ContentDict], max_tokens: int = 3000, stream: bool = False
    ) -> ModelResponse:
        """Gets a single, complete response from the language model.

        :param prompt: The prompt to feed into the language model.
        :param max_tokens: The maximal number of tokens to generate.
        :param stream: Wether to use a streamed response with the language model or not.
        :return: The completion from the language model.
        """
        ...  # This is an example. Define the interface as needed
