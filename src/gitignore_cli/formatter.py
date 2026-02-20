import shutil


def format_list(technologies: list[str]) -> str:
    """Formata a lista de tecnologias em colunas ajustadas ao terminal."""
    if not technologies:
        return ''

    terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns
    col_width = max(len(t) for t in technologies) + 2
    num_cols = max(1, terminal_width // col_width)

    lines = []
    for i in range(0, len(technologies), num_cols):
        row = technologies[i : i + num_cols]
        lines.append(''.join(t.ljust(col_width) for t in row))

    return '\n'.join(lines)
