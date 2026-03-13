"""Document and Corpus loading utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from stilwerk.src.config.schema import ProjectConfig


@dataclass
class Document:
    """A single document in the corpus.

    Attributes:
        text: The full text content.
        label: Document label/identifier.
        author: Optional author attribution (inferred from directory name).
        path: Path to the source file.
        metadata: Additional metadata.
    """

    text: str
    label: str
    author: str | None = None
    path: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def paragraphs(self) -> list[str]:
        """Split text into paragraphs."""
        return [p.strip() for p in self.text.split("\n\n") if p.strip()]

    @property
    def word_count(self) -> int:
        """Count words in the document."""
        return len(self.text.split())

    @property
    def char_count(self) -> int:
        """Count characters in the document."""
        return len(self.text)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "label": self.label,
            "author": self.author,
            "path": str(self.path) if self.path else None,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "metadata": self.metadata,
        }

    @classmethod
    def from_file(
        cls,
        path: Path,
        label: str | None = None,
        author: str | None = None,
        encoding: str = "utf-8",
        **metadata: Any,
    ) -> "Document":
        """Load a document from a file.

        Args:
            path: Path to the text file.
            label: Optional label (defaults to filename).
            author: Optional author attribution (defaults to parent directory name).
            encoding: File encoding.
            **metadata: Additional metadata.

        Returns:
            Document instance.
        """
        path = Path(path)
        text = path.read_text(encoding=encoding)

        if label is None:
            label = path.stem

        if author is None:
            # Infer author from parent directory name
            author = path.parent.name

        return cls(
            text=text,
            label=label,
            author=author,
            path=path,
            metadata=metadata,
        )


@dataclass
class Corpus:
    """A collection of documents for analysis.

    Attributes:
        documents: List of Document instances.
        name: Corpus name.
        metadata: Additional metadata.
    """

    documents: list[Document] = field(default_factory=list)
    name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        """Return number of documents."""
        return len(self.documents)

    def __iter__(self) -> Iterator[Document]:
        """Iterate over documents."""
        return iter(self.documents)

    def __getitem__(self, index: int) -> Document:
        """Get document by index."""
        return self.documents[index]

    def add(self, document: Document) -> None:
        """Add a document to the corpus."""
        self.documents.append(document)

    def get_by_label(self, label: str) -> Document | None:
        """Find a document by label."""
        for doc in self.documents:
            if doc.label == label:
                return doc
        return None

    def get_by_author(self, author: str) -> list[Document]:
        """Find all documents by author."""
        return [doc for doc in self.documents if doc.author == author]

    @property
    def labels(self) -> list[str]:
        """Get all document labels."""
        return [doc.label for doc in self.documents]

    @property
    def authors(self) -> list[str | None]:
        """Get all unique authors."""
        return list(set(doc.author for doc in self.documents))

    @property
    def total_words(self) -> int:
        """Total word count across all documents."""
        return sum(doc.word_count for doc in self.documents)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "document_count": len(self.documents),
            "total_words": self.total_words,
            "documents": [doc.to_dict() for doc in self.documents],
            "metadata": self.metadata,
        }

    @classmethod
    def from_directory(
        cls,
        directory: Path | str,
        pattern: str = "*.txt",
        encoding: str = "utf-8",
        name: str | None = None,
        author: str | None = None,
    ) -> "Corpus":
        """Load all documents from a directory.

        Args:
            directory: Directory containing text files.
            pattern: Glob pattern for files.
            encoding: File encoding.
            name: Optional corpus name.
            author: Optional author override (defaults to directory name).

        Returns:
            Corpus instance.
        """
        directory = Path(directory)
        if name is None:
            name = directory.name

        corpus = cls(name=name)

        for path in sorted(directory.glob(pattern)):
            doc = Document.from_file(path, author=author, encoding=encoding)
            corpus.add(doc)

        return corpus

    @classmethod
    def from_directories(
        cls,
        directories: list[Path | str],
        pattern: str = "*.txt",
        encoding: str = "utf-8",
        name: str = "",
    ) -> "Corpus":
        """Load documents from multiple directories.

        Author is inferred from each directory name.

        Args:
            directories: List of directories containing text files.
            pattern: Glob pattern for files.
            encoding: File encoding.
            name: Optional corpus name.

        Returns:
            Corpus instance.
        """
        corpus = cls(name=name)

        for directory in directories:
            directory = Path(directory)
            author = directory.name  # Use directory name as author

            for path in sorted(directory.glob(pattern)):
                doc = Document.from_file(path, author=author, encoding=encoding)
                corpus.add(doc)

        return corpus

    @classmethod
    def from_config(cls, config: "ProjectConfig") -> "Corpus":
        """Load corpus from project configuration.

        Uses config.corpus.directories and config.corpus.files.
        Author is inferred from directory names.

        Args:
            config: Project configuration.

        Returns:
            Corpus instance.
        """
        corpus = cls(name=config.name)
        pattern = config.corpus.pattern

        # Load from directories
        for dir_path in config.corpus.directories:
            directory = Path(dir_path)
            author = directory.name

            for path in sorted(directory.glob(pattern)):
                doc = Document.from_file(path, author=author)
                corpus.add(doc)

        # Load individual files
        for file_path in config.corpus.files:
            path = Path(file_path)
            doc = Document.from_file(path)
            corpus.add(doc)

        return corpus

    @classmethod
    def from_texts(
        cls, texts: dict[str, str], name: str = ""
    ) -> "Corpus":
        """Create corpus from a dictionary of label -> text.

        Args:
            texts: Dictionary mapping labels to text content.
            name: Optional corpus name.

        Returns:
            Corpus instance.
        """
        corpus = cls(name=name)
        for label, text in texts.items():
            doc = Document(text=text, label=label)
            corpus.add(doc)
        return corpus
