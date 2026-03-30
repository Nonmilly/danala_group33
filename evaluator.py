from pathlib import Path


def is_whole_number(value: float) -> bool:
    return abs(value - round(value)) < 1e-10


def format_number(value: float) -> str:
    if is_whole_number(value):
        return str(int(round(value)))
    value = round(value, 4)
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text if text else "0"


def tokenize(expression: str):
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            dot_count = 0

            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    dot_count += 1
                i += 1

            literal = expression[start:i]

            if literal == "." or dot_count > 1:
                raise ValueError("Invalid number")

            tokens.append(("NUM", float(literal)))
            continue

        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", "("))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ")"))
            i += 1
            continue

        raise ValueError("Invalid character")

    tokens.append(("END", None))
    return tokens


def token_to_string(token):
    token_type, token_value = token

    if token_type == "NUM":
        return f"[NUM:{format_number(token_value)}]"
    if token_type == "OP":
        return f"[OP:{token_value}]"
    if token_type == "LPAREN":
        return "[LPAREN:(]"
    if token_type == "RPAREN":
        return "[RPAREN:)]"
    return "[END]"


def current_token(tokens, pos):
    return tokens[pos]


def parse_expression(tokens, pos):
    node, pos = parse_term(tokens, pos)

    while (
        current_token(tokens, pos)[0] == "OP"
        and current_token(tokens, pos)[1] in ("+", "-")
    ):
        op = current_token(tokens, pos)[1]
        pos += 1
        right, pos = parse_term(tokens, pos)
        node = ("bin", op, node, right)

    return node, pos


def parse_term(tokens, pos):
    node, pos = parse_unary(tokens, pos)

    while True:
        token_type, token_value = current_token(tokens, pos)

        if token_type == "OP" and token_value in ("*", "/"):
            op = token_value
            pos += 1
            right, pos = parse_unary(tokens, pos)
            node = ("bin", op, node, right)

        elif token_type in ("NUM", "LPAREN"):
            # implicit multiplication
            right, pos = parse_unary(tokens, pos)
            node = ("bin", "*", node, right)

        else:
            break

    return node, pos


def parse_unary(tokens, pos):
    token_type, token_value = current_token(tokens, pos)

    if token_type == "OP" and token_value == "-":
        pos += 1
        operand, pos = parse_unary(tokens, pos)
        return ("neg", operand), pos

    if token_type == "OP" and token_value == "+":
        raise ValueError("Unary plus is not supported")

    return parse_primary(tokens, pos)


def parse_primary(tokens, pos):
    token_type, token_value = current_token(tokens, pos)

    if token_type == "NUM":
        return ("num", token_value), pos + 1

    if token_type == "LPAREN":
        pos += 1
        node, pos = parse_expression(tokens, pos)

        if current_token(tokens, pos)[0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        pos += 1
        return node, pos

    raise ValueError("Expected number or (")


def parse(tokens):
    node, pos = parse_expression(tokens, 0)

    if current_token(tokens, pos)[0] != "END":
        raise ValueError("Unexpected token at end")

    return node


def tree_to_string(node):
    kind = node[0]

    if kind == "num":
        return format_number(node[1])

    if kind == "neg":
        return f"(neg {tree_to_string(node[1])})"

    if kind == "bin":
        op = node[1]
        left = tree_to_string(node[2])
        right = tree_to_string(node[3])
        return f"({op} {left} {right})"

    raise ValueError("Invalid tree")


def evaluate_tree(node):
    kind = node[0]

    if kind == "num":
        return node[1]

    if kind == "neg":
        return -evaluate_tree(node[1])

    if kind == "bin":
        op = node[1]
        left = evaluate_tree(node[2])
        right = evaluate_tree(node[3])

        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if abs(right) < 1e-12:
                raise ZeroDivisionError("Division by zero")
            return left / right

    raise ValueError("Invalid tree")


def process_expression(expression: str) -> dict:
    original = expression.rstrip("\n")

    try:
        tokens = tokenize(original)
        tree = parse(tokens)
        tree_str = tree_to_string(tree)
        tokens_str = " ".join(token_to_string(token) for token in tokens)
    except Exception:
        return {
            "input": original,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR",
        }

    try:
        result = float(evaluate_tree(tree))
    except Exception:
        result = "ERROR"

    return {
        "input": original,
        "tree": tree_str,
        "tokens": tokens_str,
        "result": result,
    }


def write_output(results, output_path: Path):
    blocks = []

    for item in results:
        if item["result"] == "ERROR":
            result_text = "ERROR"
        else:
            result_text = format_number(item["result"])

        block = (
            f"Input: {item['input']}\n"
            f"Tree: {item['tree']}\n"
            f"Tokens: {item['tokens']}\n"
            f"Result: {result_text}"
        )
        blocks.append(block)

    output_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def evaluate_file(input_path: str) -> list[dict]:
    path = Path(input_path)
    results = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            original_line = line.rstrip("\n")
            if original_line.strip() == "":
                continue
            results.append(process_expression(original_line))

    output_path = path.with_name("output.txt")
    write_output(results, output_path)
    return results


if __name__ == "__main__":
    evaluate_file("sample_input.txt")
    print("Done. Check output.txt")