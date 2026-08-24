from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Sequence

from .io import Grid, validate_grid


def grid_shape(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0])


def copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]


def rotate90(grid: Grid) -> Grid:
    height, width = grid_shape(grid)
    return [[grid[height - 1 - row][col] for row in range(height)] for col in range(width)]


def rotate180(grid: Grid) -> Grid:
    return rotate90(rotate90(grid))


def rotate270(grid: Grid) -> Grid:
    return rotate90(rotate180(grid))


def flip_horizontal(grid: Grid) -> Grid:
    return [list(reversed(row)) for row in grid]


def flip_vertical(grid: Grid) -> Grid:
    return [row[:] for row in reversed(grid)]


def transpose(grid: Grid) -> Grid:
    height, width = grid_shape(grid)
    return [[grid[row][col] for row in range(height)] for col in range(width)]


def anti_transpose(grid: Grid) -> Grid:
    return rotate180(transpose(grid))


D4: Mapping[str, Callable[[Grid], Grid]] = {
    "identity": copy_grid,
    "rot90": rotate90,
    "rot180": rotate180,
    "rot270": rotate270,
    "flip_h": flip_horizontal,
    "flip_v": flip_vertical,
    "transpose": transpose,
    "anti_transpose": anti_transpose,
}


def most_frequent_color(grid: Grid) -> int:
    counts = Counter(value for row in grid for value in row)
    return min(counts, key=lambda color: (-counts[color], color))


def background_color(grid: Grid, strategy: str) -> int:
    if strategy == "zero":
        return 0
    if strategy == "most_frequent":
        return most_frequent_color(grid)
    raise ValueError(f"unknown background strategy: {strategy}")


def crop_non_background(grid: Grid, strategy: str) -> Grid | None:
    bg = background_color(grid, strategy)
    cells = [
        (row, col)
        for row, values in enumerate(grid)
        for col, value in enumerate(values)
        if value != bg
    ]
    if not cells:
        return None
    rows = [row for row, _ in cells]
    cols = [col for _, col in cells]
    top, bottom = min(rows), max(rows)
    left, right = min(cols), max(cols)
    return [values[left : right + 1] for values in grid[top : bottom + 1]]


@dataclass(frozen=True)
class Component:
    cells: tuple[tuple[int, int], ...]
    background: int

    @property
    def size(self) -> int:
        return len(self.cells)

    @property
    def top(self) -> int:
        return min(row for row, _ in self.cells)

    @property
    def bottom(self) -> int:
        return max(row for row, _ in self.cells)

    @property
    def left(self) -> int:
        return min(col for _, col in self.cells)

    @property
    def right(self) -> int:
        return max(col for _, col in self.cells)


def connected_components(
    grid: Grid,
    *,
    background_strategy: str,
    connectivity: int,
    same_color: bool,
) -> list[Component]:
    bg = background_color(grid, background_strategy)
    height, width = grid_shape(grid)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if connectivity == 8:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    elif connectivity != 4:
        raise ValueError("connectivity must be 4 or 8")

    seen: set[tuple[int, int]] = set()
    result: list[Component] = []
    for row in range(height):
        for col in range(width):
            if (row, col) in seen or grid[row][col] == bg:
                continue
            seed_color = grid[row][col]
            stack = [(row, col)]
            seen.add((row, col))
            cells: list[tuple[int, int]] = []
            while stack:
                current_row, current_col = stack.pop()
                cells.append((current_row, current_col))
                for delta_row, delta_col in directions:
                    next_row = current_row + delta_row
                    next_col = current_col + delta_col
                    if not (0 <= next_row < height and 0 <= next_col < width):
                        continue
                    if (next_row, next_col) in seen:
                        continue
                    value = grid[next_row][next_col]
                    if value == bg:
                        continue
                    if same_color and value != seed_color:
                        continue
                    seen.add((next_row, next_col))
                    stack.append((next_row, next_col))
            result.append(Component(tuple(sorted(cells)), bg))
    return result


def component_grid(grid: Grid, component: Component) -> Grid:
    top, bottom = component.top, component.bottom
    left, right = component.left, component.right
    output = [
        [component.background for _ in range(right - left + 1)]
        for _ in range(bottom - top + 1)
    ]
    for row, col in component.cells:
        output[row - top][col - left] = grid[row][col]
    return output


def select_component(
    grid: Grid,
    *,
    selector: str,
    background_strategy: str,
    connectivity: int,
    same_color: bool,
) -> Grid | None:
    components = connected_components(
        grid,
        background_strategy=background_strategy,
        connectivity=connectivity,
        same_color=same_color,
    )
    if not components:
        return None

    if selector == "largest":
        values = [component.size for component in components]
        target = max(values)
    elif selector == "smallest":
        values = [component.size for component in components]
        target = min(values)
    elif selector == "topmost":
        values = [component.top for component in components]
        target = min(values)
    elif selector == "bottommost":
        values = [component.bottom for component in components]
        target = max(values)
    elif selector == "leftmost":
        values = [component.left for component in components]
        target = min(values)
    elif selector == "rightmost":
        values = [component.right for component in components]
        target = max(values)
    else:
        raise ValueError(f"unknown component selector: {selector}")

    winners = [index for index, value in enumerate(values) if value == target]
    if len(winners) != 1:
        return None
    return component_grid(grid, components[winners[0]])


def infer_color_map(sources: Sequence[Grid], targets: Sequence[Grid]) -> dict[int, int] | None:
    mapping: dict[int, int] = {}
    for source, target in zip(sources, targets):
        if grid_shape(source) != grid_shape(target):
            return None
        for source_row, target_row in zip(source, target):
            for source_value, target_value in zip(source_row, target_row):
                previous = mapping.get(source_value)
                if previous is not None and previous != target_value:
                    return None
                mapping[source_value] = target_value
    return mapping


def apply_color_map(grid: Grid, mapping: Mapping[int, int]) -> Grid:
    return [[mapping.get(value, value) for value in row] for row in grid]


def scale_cells(grid: Grid, row_factor: int, col_factor: int) -> Grid:
    output: Grid = []
    for row in grid:
        expanded: list[int] = []
        for value in row:
            expanded.extend([value] * col_factor)
        for _ in range(row_factor):
            output.append(expanded[:])
    return output


@dataclass(frozen=True)
class Hypothesis:
    family: str
    params: tuple[object, ...]
    color_map: tuple[tuple[int, int], ...]
    complexity: int

    @property
    def description(self) -> str:
        mapping = dict(self.color_map)
        return f"{self.family}{self.params} colors={mapping} complexity={self.complexity}"

    def apply(self, grid: Grid) -> Grid | None:
        mapping = dict(self.color_map)
        if self.family == "global":
            (transform,) = self.params
            candidate = D4[str(transform)](grid)
        elif self.family == "crop":
            strategy, transform = self.params
            cropped = crop_non_background(grid, str(strategy))
            if cropped is None:
                return None
            candidate = D4[str(transform)](cropped)
        elif self.family == "component":
            strategy, connectivity, same_color, selector, transform = self.params
            selected = select_component(
                grid,
                selector=str(selector),
                background_strategy=str(strategy),
                connectivity=int(connectivity),
                same_color=bool(same_color),
            )
            if selected is None:
                return None
            candidate = D4[str(transform)](selected)
        elif self.family == "scale":
            transform, row_factor, col_factor = self.params
            candidate = scale_cells(
                D4[str(transform)](grid),
                int(row_factor),
                int(col_factor),
            )
        elif self.family == "constant":
            frozen = self.params[0]
            candidate = [list(row) for row in frozen]  # type: ignore[arg-type]
        else:
            raise ValueError(f"unknown hypothesis family: {self.family}")
        return apply_color_map(candidate, mapping)


def _fit_color_verified(
    family: str,
    params: tuple[object, ...],
    sources: Sequence[Grid],
    targets: Sequence[Grid],
    complexity: int,
) -> Hypothesis | None:
    mapping = infer_color_map(sources, targets)
    if mapping is None:
        return None
    if not all(apply_color_map(source, mapping) == target for source, target in zip(sources, targets)):
        return None
    return Hypothesis(family, params, tuple(sorted(mapping.items())), complexity)


def fit_hypotheses(task: Mapping[str, object]) -> list[Hypothesis]:
    train = task.get("train")
    if not isinstance(train, list) or not train:
        raise ValueError("task must contain non-empty train pairs")

    inputs = [pair["input"] for pair in train]  # type: ignore[index]
    targets = [pair["output"] for pair in train]  # type: ignore[index]
    for grid in [*inputs, *targets]:
        validate_grid(grid)

    hypotheses: list[Hypothesis] = []

    if all(target == targets[0] for target in targets[1:]):
        frozen = tuple(tuple(row) for row in targets[0])
        hypotheses.append(Hypothesis("constant", (frozen,), (), 10))

    for transform_index, transform in enumerate(D4):
        transformed = [D4[transform](grid) for grid in inputs]
        hypothesis = _fit_color_verified(
            "global",
            (transform,),
            transformed,
            targets,
            transform_index,
        )
        if hypothesis is not None:
            hypotheses.append(hypothesis)

    for strategy_index, strategy in enumerate(("zero", "most_frequent")):
        for transform_index, transform in enumerate(D4):
            transformed: list[Grid] = []
            valid = True
            for grid in inputs:
                cropped = crop_non_background(grid, strategy)
                if cropped is None:
                    valid = False
                    break
                transformed.append(D4[transform](cropped))
            if not valid:
                continue
            hypothesis = _fit_color_verified(
                "crop",
                (strategy, transform),
                transformed,
                targets,
                12 + strategy_index + transform_index,
            )
            if hypothesis is not None:
                hypotheses.append(hypothesis)

    selectors = ("largest", "smallest", "topmost", "bottommost", "leftmost", "rightmost")
    for strategy_index, strategy in enumerate(("zero", "most_frequent")):
        for connectivity in (4, 8):
            for same_color in (True, False):
                for selector_index, selector in enumerate(selectors):
                    for transform_index, transform in enumerate(D4):
                        transformed = []
                        valid = True
                        for grid in inputs:
                            selected = select_component(
                                grid,
                                selector=selector,
                                background_strategy=strategy,
                                connectivity=connectivity,
                                same_color=same_color,
                            )
                            if selected is None:
                                valid = False
                                break
                            transformed.append(D4[transform](selected))
                        if not valid:
                            continue
                        hypothesis = _fit_color_verified(
                            "component",
                            (strategy, connectivity, same_color, selector, transform),
                            transformed,
                            targets,
                            24
                            + strategy_index
                            + (connectivity == 8)
                            + (not same_color)
                            + selector_index
                            + transform_index,
                        )
                        if hypothesis is not None:
                            hypotheses.append(hypothesis)

    for transform_index, transform in enumerate(D4):
        transformed = [D4[transform](grid) for grid in inputs]
        factors: list[tuple[int, int]] = []
        valid = True
        for source, target in zip(transformed, targets):
            source_height, source_width = grid_shape(source)
            target_height, target_width = grid_shape(target)
            if target_height % source_height or target_width % source_width:
                valid = False
                break
            row_factor = target_height // source_height
            col_factor = target_width // source_width
            if not (1 <= row_factor <= 5 and 1 <= col_factor <= 5):
                valid = False
                break
            factors.append((row_factor, col_factor))
        if not valid or len(set(factors)) != 1:
            continue
        row_factor, col_factor = factors[0]
        scaled = [scale_cells(grid, row_factor, col_factor) for grid in transformed]
        hypothesis = _fit_color_verified(
            "scale",
            (transform, row_factor, col_factor),
            scaled,
            targets,
            18 + transform_index + row_factor + col_factor,
        )
        if hypothesis is not None:
            hypotheses.append(hypothesis)

    unique: dict[tuple[object, ...], Hypothesis] = {}
    for hypothesis in hypotheses:
        key = (hypothesis.family, hypothesis.params, hypothesis.color_map)
        unique[key] = hypothesis
    return sorted(
        unique.values(),
        key=lambda hypothesis: (
            hypothesis.complexity,
            hypothesis.family,
            repr(hypothesis.params),
            hypothesis.color_map,
        ),
    )


def _valid_prediction(grid: Grid | None) -> bool:
    if grid is None:
        return False
    try:
        validate_grid(grid)
    except ValueError:
        return False
    return True


def solve_task(task: Mapping[str, object]) -> tuple[list[dict[str, Grid]], list[Hypothesis]]:
    hypotheses = fit_hypotheses(task)
    test_pairs = task.get("test")
    if not isinstance(test_pairs, list) or not test_pairs:
        raise ValueError("task must contain non-empty test pairs")

    predictions: list[dict[str, Grid]] = []
    for pair in test_pairs:
        input_grid = pair["input"]  # type: ignore[index]
        validate_grid(input_grid)
        candidates: list[Grid] = []
        for hypothesis in hypotheses:
            candidate = hypothesis.apply(input_grid)
            if _valid_prediction(candidate) and candidate not in candidates:
                candidates.append(candidate)  # type: ignore[arg-type]
            if len(candidates) == 2:
                break

        if not candidates:
            candidates.append(copy_grid(input_grid))
        if len(candidates) == 1:
            fallback = crop_non_background(input_grid, "most_frequent")
            if _valid_prediction(fallback) and fallback != candidates[0]:
                candidates.append(fallback)  # type: ignore[arg-type]
            else:
                candidates.append(copy_grid(input_grid))

        predictions.append({"attempt_1": candidates[0], "attempt_2": candidates[1]})
    return predictions, hypotheses


def make_symbolic_submission(challenges: Mapping[str, Mapping[str, object]]) -> dict[str, list[dict[str, Grid]]]:
    submission: dict[str, list[dict[str, Grid]]] = {}
    for task_id, task in challenges.items():
        predictions, _ = solve_task(task)
        submission[task_id] = predictions
    return submission